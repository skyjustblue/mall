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
    轮播图
    """
    def get(self, request):
        res = News.objects.filter()
        ret = NewsModelSerializer(res, many=True).data
        mes = {}
        mes['code'] = 200
        mes['list'] = ret
        return Response(mes)



class FetchNews(APIView):
    """新闻-详情"""
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
    品牌制造商直供
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
    秒杀专区
     秒杀日期判断🍄
    日期、时间数据丢失🍄
    """
    def get(self, request):
        mes = {}
        todaydate = datetime.now().strftime("%Y-%m-%d")
        # 秒杀日期判断🍄
        flashdate = Seckill_date.objects.filter(
        starting=todaydate).all()
        flashdateidlist = [ i.id for i in flashdate]
        flashtime = Seckill_time.objects.all()
        flashtimeidlist = [ i.id for i in flashtime]
        flashproduct = Seckill_relation.objects.filter(
        d_id__in = flashdateidlist,
        t_id__in = flashtimeidlist).all()
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
    新鲜好物
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
    人气推荐
    """
    def get(self, request):
        res = Product.objects.filter().order_by('-lovenum')[:5]
        ret = ProductModelSerializer(res, many=True).data
        mes = {}
        mes['code'] = 200
        mes['list'] = ret
        return Response(mes)


class FetchSpecialList(APIView):
    """
    专题精选
    """
    def get(self, request):
        res = Speciallist.objects.filter().order_by('-lovenum')[:5]
        ret = SpeciallistModelSerializer(res, many=True).data
        mes = {}
        mes['code'] = 200
        mes['list'] = ret
        return Response(mes)


class FetchLove(APIView):
    """
    猜你喜欢
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