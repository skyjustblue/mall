from rest_framework.views import APIView
from rest_framework.response import Response
from api.models import *
from api.serializers import *
from django.db import connection
import json
import time
#导入时间模块
from datetime import datetime
# 内置的哈希算法加密,比对密码
from django.contrib.auth.hashers import make_password,check_password
import os
# 配置文件
from mallback import settings


# 下载图片
def upload_all_image(img):
    f = open(os.path.join(settings.UPLOAD_ROOT,'',img.name),'wb')
    #写文件 遍历图片文件流
    for chunk in img.chunks():
        f.write(chunk)
    #关闭文件流
    f.close()


# 返回图片url
class UploadImage(APIView):
    def post(self, request):
        imgfile = request.FILES.get('img')
        upload_all_image(imgfile)
        imgurl = "http://127.0.0.1:8000/upload/" + imgfile.name
        mes = {}
        mes['image'] = imgurl
        return Response(mes)



class FetchNewsPic(APIView):
    """
    首页 轮播图
    """
    def get(self, request):
        res = News.objects.filter()
        ret = NewsModelSerializer(res, many=True).data
        mes = {}
        mes['code'] = 200
        mes['list'] = ret
        return Response(mes)



class FetchNews(APIView):
    """首页 新闻-详情"""
    def get(self, request):
        res = News.objects.filter()
        ret = News2ModelSerializer(res, many=True).data
        mes = {}
        mes['code'] = 200
        mes['list'] = ret
        return Response(mes)


# 品牌制造商
class FetchBrand(APIView):
    """
    首页 品牌制造商直供
    """
    def get(self, request):
        res = Brand_copy.objects.filter()[:5]
        ret = Brand_copyModelSerializer(res, many=True).data
        mes = {}
        mes['code'] = 200
        mes['list'] = ret
        return Response(mes)


class FlashProduct(APIView):
    """
    首页 秒杀专区
    秒杀日期判断🍄
    日期、时间数据丢失🍄
    """
    def get(self, request):
        mes = {}
        todaydate = datetime.now().strftime("%Y-%m-%d")
        # 秒杀日期判断🍄
        flashdate = Seckill_date.objects.filter(starting=todaydate).all()
        flashdateidlist = [ i.id for i in flashdate]
        flashtime = Seckill_time.objects.all()
        flashtimeidlist = [ i.id for i in flashtime]
        flashproduct = Seckill_relation.objects.filter(
            d_id__in = flashdateidlist,t_id__in = flashtimeidlist).all()
        flashproduct_serializer = FlashProductModelSerializer(
        flashproduct, many=True)
        mes['code'] = 200
        mes['list'] = flashproduct_serializer.data

        # print(todaydate)
        # print(flashdate)
        # print(flashtime)
        # print(flashdateidlist)
        # print(flashtimeidlist)
        # print(flashproduct)
        # print(mes['list'])
        return Response(mes)


class FetchSeckillProduct(APIView):
    """
    首页 新鲜好物
    """
    def get(self, request):
        res = Product.objects.filter()[:5]
        ret = ProductModelSerializer(res, many=True).data
        mes = {}
        mes['code'] = 200
        mes['list'] = ret
        return Response(mes)


class FetchLoveProduct(APIView):
    """
    首页 人气推荐
    """
    def get(self, request):
        res = Product.objects.filter().order_by('-lovenum')[:5]
        ret = ProductModelSerializer(res, many=True).data
        mes = {}
        mes['code'] = 200
        mes['list'] = ret
        return Response(mes)


class FetchSpecialOne(APIView):
    """
    首页 专题精选
    """
    def get(self, request):
        res = Special_detail.objects.filter(recommend=1).order_by('-sort')[:1]
        A_name = Special_cate.objects.get(id = res[0].s_cid_id).name # 通过子表来查询主表分类名称
        pic = Special_detail.objects.get(id = res[0].id).special_s_did.all() # 通过主表来查询子表
        res_serial = Special_detailModelSerializer(res, many=True).data
        pic_serial = Special_picModelSerializer(pic, many=True).data
        res_serial[0]['pic'] = [ x['pic'] for x in pic_serial] #值取第一个图片
        res_serial[0]['cate_name'] = A_name
        mes = {}
        mes['code'] = 200
        mes['list'] = res_serial
        return Response(mes)


class FetchSpecialCate(APIView):
    """
    专题 get全部分类  post全部专题
    """
    def get(self, request):
        res = Special_cate.objects.all()
        res_serial = Special_cateModelSerializer(res, many=True).data
        mes = {}
        mes['code'] = 200
        mes['list'] = res_serial
        return Response(mes)

    def post(self, request):
        res = Special_detail.objects.filter(recommend=1).order_by('-sort')[:]
        print(res)
        res_serial = Special_detailModelSerializer(res, many=True).data
        print(res_serial)
        for x,i in enumerate(res):
            pic = Special_detail.objects.get(id = i.id).special_s_did.all()
            print(pic)
            pic_serial = Special_picModelSerializer(pic, many=True).data
            print(pic_serial)
            res_serial[x]['pic'] = [ x['pic'] for x in pic_serial]
            print(res_serial[x])
            A_name = Special_cate.objects.get(id = res[x].s_cid_id).name # 通过子表来查询主表分类名称
            res_serial[x]['cate_name'] = A_name
        mes = {}
        mes['code'] = 200
        mes['list'] = res_serial
        return Response(mes)


class FetchSpecialList(APIView):
        """
        专题  post专题列表
        😂给我专题的标识id 
        例子1：
        export function updateBrand(id,data) {
            return request({
                url:'/xxxxx?id='+id,
                method:'post',
                data:data
            })
        }
        例子2：
        export function updateBrand(data) {
            return request({
                url:'/xxxxx,
                method:'post',
                data:data  //这个data是json let data={'id':id}
            })
        }
        我的后端接收
        id = id = request.data.get('id',1)
        """
        def post(self, request):
            id = request.data.get('id',1)
            if id:
                A_name = Special_cate.objects.get(id=id).name
                res = Special_detail.objects.filter(recommend=1,s_cid=id).order_by('-sort')
                print(res)
                res_serial = Special_detailModelSerializer(res, many=True).data
                print(res_serial)
                for x,i in enumerate(res):
                    pic = Special_detail.objects.get(id = i.id).special_s_did.all()
                    print(pic)
                    pic_serial = Special_picModelSerializer(pic, many=True).data
                    print(pic_serial)
                    res_serial[x]['pic'] = [ x['pic'] for x in pic_serial]
                    print(res_serial[x])
                    res_serial[x]['cate_name'] = A_name
                mes = {}
                mes['code'] = 200
                mes['list'] = res_serial
                return Response(mes)


class FetchSpecialDetail(APIView):
    """
    专题 post专题详情页
    前端传id
    后端 id = request.data.get('id',1)
    """
    def post(self, request):
        id = request.data.get('id',1)
        if id:
            res = Special_detail.objects.filter(id=id,recommend=1)
            A_name = Special_cate.objects.get(id = res[0].s_cid_id).name # 通过子表来查询主表分类名称
            pic = Special_detail.objects.get(id = res[0].id).special_s_did.all() # 通过主表来查询子表
            res_serial = Special_detailModelSerializer_2(res, many=True).data
            pic_serial = Special_picModelSerializer(pic, many=True).data
            res_serial[0]['pic'] = [ x['pic'] for x in pic_serial]
            res_serial[0]['cate_name'] = A_name
            mes = {}
            mes['code'] = 200
            mes['list'] = res_serial
            return Response(mes)


class FetchLove(APIView):
    """
    首页 猜你喜欢
    """
    def get(self, request):
        res = Product.objects.filter().order_by('-lovenum')[:5]
        ret = ProductModelSerializer(res, many=True).data
        mes = {}
        mes['code'] = 200
        mes['list'] = ret
        return Response(mes)



# # 首页推荐专题表
# class SmsHomeRecommendSubject(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     subject_id = models.BigIntegerField(blank=True, null=True) # 专题id
#     subject_name = models.CharField(max_length=64, blank=True, null=True) # 专题名称
#     recommend_status = models.IntegerField(blank=True, null=True) # 推荐状态(是否推荐)
#     sort = models.IntegerField(blank=True, null=True) # 排序

#     class Meta:
#         managed = False
#         db_table = 'sms_home_recommend_subject'