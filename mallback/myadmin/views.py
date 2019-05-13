# 视图方法模板
from django.shortcuts import render,redirect
# 处理请求类
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
# 类视图
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response
# django2.0.4版的反向解析方法
from django.urls import reverse
# 数据模型表类
from myadmin.models import *
from myadmin.serializers import *
# 源生mysql连接
from django.db import connection
import json
import time
#导入时间模块
from datetime import datetime
# 内置的哈希算法加密,比对密码
from django.contrib.auth.hashers import make_password,check_password
# 闪现
from django.contrib import messages
# 分页器类
from django.core.paginator import Paginator
import os
# 配置文件
from mallback import settings

# 测试GitHub
# 登录
class Login(APIView):
    def get(self,request):
        return Response({'code':200})


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


"""一、商品模块"""
'''1、商品列表页面'''


'''2、添加商品页面'''
#查询会员
class MemberLevelList(APIView):
    def get(self, request):
        mes = {}
        a = Member_grade.objects.filter().all()
        adver = Member_gradeModelSerializer(a, many=True).data
        mes['code'] = 200
        mes['list'] = adver
        mes['length'] = len(a)
        return Response(mes)


#查询类型
class FetchProductAttrCateList(APIView):
    def get(self, request):
        g = Goods_type.objects.filter()
        good = Goods_typeModelSerializer(g, many=True).data
        mes = {}
        mes['code'] = 200
        mes['list'] = good
        print(mes)
        return Response(mes)


'''3、商品分类页面'''
class ProductCategoryList(APIView): # 商品分类列表
    def get(self, request):
        parent_id = request.GET.get('parent_id')
        if parent_id:
            res = Category.objects.filter(parent_id=parent_id).all()    #parent_id上级分类
            b = CategoryModelSerializer(res, many=True)
        else:
            res = Category.objects.filter(level=0).all()    #level分类等级
            b = CategoryModelSerializer(res, many=True)
        list1 = []
        for i in res:
            to_dict = {}
            to_dict['id'] = i.id
            to_dict['name'] = i.name
            cate = Category.objects.filter(parent_id=i.id).all()
            list2 = []
            for a in cate:
                dict1 = {}
                dict1['id'] = a.id
                dict1['name'] = a.name
                list2.append(dict1)
            to_dict['children'] = list2
            list1.append(to_dict)
        mes = {}
        mes['code'] = 200
        mes['list'] = b.data
        mes['list1'] = list1 #2级分类
        return Response(mes)


# 分类导航栏开关 是否显示
class CateShow(APIView):
    def post(self, request):
        mes = {}
        id = request.POST.get('ids')
        is_nav_status = request.POST.get('is_nav_status')
        status = request.POST.get('status')
        if is_nav_status:
            Category.objects.filter(id=id).update(is_nav_status=is_nav_status)
        elif status:
            Category.objects.filter(id=id).update(status=status)
        mes['code'] = 200
        return Response(mes)


#删除分类列表
class DeleteProductCate(APIView):
    def post(self, request):
        mes = {}
        id = request.GET.get('id')
        Category.objects.filter(id=id).delete()
        # Category.objects.filter(id=id).count()
        mes['code'] = 200
        return Response(mes)


# 获取商品所有分类
class ProductCateNameList(APIView):
    def get(self,request):
        mes = {}
        res = Category.objects.raw("select id,name from category where level=0")
        serial = CategoryModelSerializer_2(res, many=True).data
        print(serial)
        mes['code'] = 200
        mes['list'] = serial
        return Response(mes)


# 商品分类详情页<添加-编辑>
class CreateProductCate(APIView):
    def get(self, request):
        mes = {}
        id = request.GET.get('id')
        # 此分类详情编辑前预留信息
        if id:
            data = Category.objects.filter(id=id)
            serial = CategoryModelSerializer(data, many=True).data
            print(serial)
            mes['list'] = serial
            mes['code'] = 200
        # 预处理--筛选属性2次循环封装json
        else:
            productAttrCate = []
            res = Goods_type.objects.filter().all()
            for i in res:
                d = i.to_dict()
                productAttributeList = Goods_type_attribute.objects.filter(type_id=i.id).all()
                productAttributeList = [ o.to_dict() for o in productAttributeList]
                d['productAttributeList'] = productAttributeList
                productAttrCate.append(d)
            mes['list'] = productAttrCate
            mes['code'] = 200
        return Response(mes)

    def post(self, request):
        mes = {}
        id = request.GET.get('id')
        data = request.data
        if id: # 修改商品分类表
            Category.objects.filter(id=id).update(
                name=data['name'],
                level=data['level'],
                parent_id=data['level'],
                is_nav_status=data['is_nav_status'],
                status= data['status'],
                sort= data['sort'],
                image= data['image'],
                keyword= data['keyword'],
                descrip= data['descrip'],
                count_danwei= data['count_danwei'])
            mes['code'] = 200
        else: # 添加商品分类表
            serial = CategorySerializer(data=data)
            if serial.is_valid():
                print('=====添加商品分类表====')
                serial.save()
                mes['code'] = 200
            else:
                print(serial.errors)
        return Response(mes)


'''4、商品类型页面'''
class AddEditGoodtype(APIView):
    #定义封装方法
    def func(self,res):
        mlist = []
        for i in res:
            d = i.to_dict()  # 序列化出商品类型表 | dict = {'id': self.id, 'name': self.name} 
            attr_n = Goods_type_attribute.objects.filter(type_id=i.id, type=0).count() # 属性数量
            param_n = Goods_type_attribute.objects.filter(type_id=i.id, type=1).count() # 参数数量
            d['attribute_count'] = attr_n
            d['param_count'] = param_n
            mlist.append(d)
        return mlist
    
    def get(self,request):
        try:
            mes = {}
            res = Goods_type.objects.filter().all()
            mes['list'] = self.func(res)    #调用封装方法
            mes['code'] = 200
        except Exception as e:
            print(str(e))
        return Response(mes)

    # 添加 | 编辑 --商品类型
    def post(self,request):
        try:
            mes = {}
            id = request.POST.get('id')
            if id:    # 编辑商品类型
                Goods_type.objects.filter(id=id).update(name=request.data['name'])
                mes['code'] = 200
            else:     # 添加商品类型
                serial = AddGoods_TypeSerializer(data=request.data)
                if serial.is_valid():
                    serial.save()
                    mes['code'] = 200
        except Exception as e:
            print(str(e))
        return Response(mes)


# 删除商品类型  😂通过父表删除子表的串联数据、没实现
class DelGoodtype(APIView):
    def post(self,request):
        try:
            mes = {}
            id = request.data['id']
            if id:
                Goods_type.objects.filter(id=id).delete()
                mes['code'] = 200
        except Exception as e:
            print(str(e))
        return Response(mes)


#  获取单个商品类型对应的 属性|参数列表
class ProductAttrParamList(APIView):
    def get(self, request):
        mes = {}
        try:
            id = request.GET.get('id')  # 所属商品类型id
            type = request.GET.get('type')
            print(id)
            print(type)
            if type:
                attr = Goods_type_attribute.objects.filter(type_id=id,type=type).all()
            else:
                attr = Goods_type_attribute.objects.filter(id=id).all()
            serial = Goods_type_attributeModelSerializer(attr,many=True).data
            mes['code'] = 200
            mes['list'] = serial
        except Exception as e:
            mes['code'] = str(e)
        return Response(mes)


# 商品属性|参数\列表 <单个删除、批量删除>
class DeleteProductAttr(APIView): 
    def post(self, request):
        mes = {}
        ids = request.data['ids'].split(',')
        if isinstance(ids,list):
            # ret = Goods_type_attribute.objects.filter(id__in=ids).count()
            Goods_type_attribute.objects.filter(id__in=ids).delete()
            mes['code'] = 200
        elif isinstance(ids,str):
            Goods_type_attribute.objects.filter(id=ids).delete()
            mes['code'] = 200
        return Response(mes)


'''
添加 ->取出商品类型名称-id-namelist -> 修改商品类型表-属性参数表
编辑 ->取出商品类型名称-name + 用商品的属性-id + 查出商品的属性详情
'productAttributeCategoryId':点击添加/编辑前的商品类型id        'type_id':点击提交后的商品类型id
'''
# 属性|参数\详情页 <添加>
class CreateProductAttr(APIView):
    def post(self, request):
        mes = {}
        data = request.data
        type_id_object = Goods_type.objects.filter(id=data['type_id'])[0]
        if data['input_list'] == '':  # 删除空的可选列表值的字段{}
            del data['input_list']
        serial = AddgoodstypeSerializer(data=data, context={"type_id_object": type_id_object})  # context反序列化指定外键
        if serial.is_valid():
            serial.save()
            if data['type'] == 0:   # 属性表
                go = Goods_type.objects.filter(id=data['type_id'])[0]
                go.attribute_count += 1
                go.save()
                mes['code'] = 200
            else:   # 参数表
                go = Goods_type.objects.filter(id=data['type_id'])[0]
                print(go.param_count)
                go.param_count += 1
                go.save()
                mes['code'] = 200
        else:
            print(serial.errors)
        return Response(mes)


# 属性|参数\详情页 <编辑>
class UpdateProductAttr(APIView):
    def post(self, request):
        mes = {}
        id = request.GET.get('id')
        data = request.data
        Goods_type_attribute.objects.filter(id=id).update(
            name=data['name'],
            filter_type=data['filter_type'],
            is_select=data['is_select'],
            related_status=data['related_status'],
            select_type=data['select_type'],
            input_type=data['input_type'],
            input_list=data['input_list'],
            hand_add_status=data['hand_add_status'],
            sort=data['sort'],
            type=data['type'])
        mes['code'] = 200
        return Response(mes)


'''5、品牌管理页面'''
class Brands(APIView):
    def get(self,request):
        try:
            keyword = request.GET.get('keyword','').strip()
            res = Brand.objects.filter(name__icontains=keyword).order_by('-sort')
            res = BrandModelSerializer(res,many=True).data
            msg = {}
            msg['list'] = res
            msg['code'] = 200
        except Exception as e:
            print(str(e))
        return Response(msg)
    


#品牌详情 添加|编辑
class Brand_detail(APIView):
    # // 展示预编辑品牌原有信息
    def get(self, request):
        id = request.GET.get('id')
        res = Brand.objects.filter(id=id).all()
        b = BrandModelSerializer(res, many=True).data
        mes = {}
        mes['code'] = 200
        mes['list'] = b
        return Response(mes)
 
    def post(self, request):
        try:
            mes = {}
            name = request.data
            id = request.GET.get('id')
            if id: # 编辑
                Brand.objects.filter(id=id).update(name=name['name'],first=name['first'],logo=name['logo'],b_logo=name['b_logo'],story=name['story'],sort=name['sort'],is_show=name['is_show'],is_company=name['is_company'])
                mes['code'] = 200
            else:  # 添加
                data = {'name':name['name'],'first':name['first'],'logo':name['logo'],'b_logo':name['b_logo'],'story':name['story'],'sort':name['sort'],'is_show':name['is_show'],'is_company':name['is_company']}
                serial = AddbrandSerializer(data=data)
                if serial.is_valid():
                    serial.save()
                    mes['code'] = 200
        except Exception as e:
            print(str(e))
        return Response(mes)



#删除品牌
class Del_brand(APIView):
    def post(self,request):
        try:
            data = request.data
            print(data,type(data))
            id = data['id']
            mes = {}
            if id:
                Brand.objects.get(id=int(id)).delete()
                mes['code'] = 200
        except Exception as e:
            print(str(e))
        return Response(mes)


#品牌是否显示
class Brand_show(APIView):
    #  单个操作 是否为品牌制造商 | 是否显示
    def get(self, request):
        try:
            id = request.GET.get('id')
            is_company = request.GET.get('is_company')
            is_show = request.GET.get('is_show')
            # print('x '*20,id)
            # print('x '*20,is_company)
            # print('x '*20,is_show)
            mes = {}
            if is_company: # 是否为品牌制造商
                Brand.objects.filter(id=id).update(is_company=is_company)
                mes['code'] = 200
            if is_show:  # 是否显示
                Brand.objects.filter(id=int(id)).update(is_show=is_show)
                mes['code'] = 200
        except Exception as e:
            print(str(e))
        return Response(mes)

    #  批量操作 | 是否显示
    def post(self, request):
        try:
            data = request.data
            ids = data['ids'].split(',')
            is_show = request.POST.get('is_show')
            mes = {}
            Brand.objects.filter(id__in=ids).update(is_show=is_show)
            mes['code'] = 200
        except Exception as e:
            print(str(e))
        return Response(mes)



"""二、订单模块"""
'''1、订单列表'''
'''2、订单设置'''
'''3、退货申请处理'''
'''4、退货原因设置'''


"""三、营销模块"""
'''1、秒杀活动列表'''
'''2、优惠券列表'''
'''3、品牌推荐'''
#品牌推荐列表 | 渲染推荐状态中的品牌 | 筛选
class RecommendBrandList(APIView):
    def get(self, request):
        mes = {}
        name = request.GET.get('brandName','').strip()
        is_recommend = request.GET.get('recommendStatus')
        if name != '' and is_recommend:
            res = Brand.objects.filter(name__icontains=name).filter(is_recommend=is_recommend).order_by('-sort')
        elif name != '':
            res = Brand.objects.filter(name__icontains=name).order_by('-sort')
        elif is_recommend:
            res = Brand.objects.filter(is_recommend=is_recommend).order_by('-sort')
        else:
            res = Brand.objects.filter(is_recommend=1).all().order_by('-sort')
        seria = BrandModelSerializer(res, many=True).data
        mes['code'] = 200
        mes['list'] = seria
        return Response(mes)


# 选择品牌加入推荐
class CreateHomeBrand(APIView):
    def post(self, request):
        mes = {}
        data = request.data
        try:
            for i in data:
                Brand.objects.filter(id=i['brandId']).update(is_recommend=1)
            mes['code'] = 200
        except:
            mes['code'] = 10010
        return Response(mes)


# 复选框删除
class DeleteHomeBrand(APIView):
    def post(self, request):
        mes = {}
        ids = request.data.get('ids').split(',')
        try:
            Brand.objects.filter(id__in=ids).delete()
            mes['code'] = 200
        except:
            mes['code'] = 10010
        return Response(mes)


# 复选框修改是否推荐
class UpdateRecommendStatus(APIView):
    def post(self, request):
        mes = {}
        ids = request.data.get('ids').split(',')
        is_recommend = request.data.get('is_recommend')
        try:
            Brand.objects.filter(id__in=ids).update(is_recommend=is_recommend)
            mes['code'] = 200
        except:
            mes['code'] = 10010
        return Response(mes)


# 设置排序
class UpdateHomeBrandSort(APIView):
    def post(self, request):
        mes = {}
        id = request.data.get('id')
        sort = request.data.get('sort')
        print(id)
        print(sort)
        try:
            Brand.objects.filter(id=id).update(sort=sort)
            mes['code'] = 200
        except:
            mes['code'] = 10010
        return Response(mes)


'''4、新品推荐'''
'''5、人气推荐'''
'''6、专题推荐'''
'''7、广告列表'''
class AdvertiseList(APIView):
    def get(self, request):
        mes = {}
        # 筛选搜索
        name = request.GET.get('name','').strip()
        type = request.GET.get('type')
        endTime = request.GET.get('endTime')
        if all([name,type,endTime]):
            res = Advertising.objects.filter(name__icontains=name, type=type, endTime__contains=endTime)
        elif name:
            res = Advertising.objects.filter(name__icontains=name)
        elif type:
            res = Advertising.objects.filter(type=type)
        elif endTime:
            res = Advertising.objects.filter(endTime__contains=endTime)
        elif name and type:
            res = Advertising.objects.filter(name__icontains=name, type=type)
        elif type and endTime:
            res = Advertising.objects.filter(endTime__contains=endTime, type=type)
        elif name and endTime:
            res = Advertising.objects.filter(name__icontains=name, endTime__contains=endTime)
        else:
            res = Advertising.objects.all()
        adver = AdvertisingModelSerializer(res, many=True).data
        mes['list'] = adver
        mes['code'] = 200
            
        return Response(mes)


#添加/编辑 广告
class CreateAdvertise(APIView):
    # 编辑前预览
    def get(self, request):
        mes = {}
        id = request.GET.get('id')
        a = Advertising.objects.filter(id=id).all()
        adver = AdvertisingModelSerializer(a, many=True).data
        mes['list'] = adver
        mes['code'] = 200
        return Response(mes)
    
    def post(self, request):
        mes = {}
        id = request.GET.get('id')
        if not id:  # 添加
            gg = AdvertisingSerializer(data=request.data)
            if gg.is_valid():
                gg.save()
                mes['code'] = 200
            else:
                print(gg.errors)
                mes['code'] = 10010
                mes['erro'] = '添加失败'
        else:
            print(request.data)
            d = request.data
            # lenth = len(d['startTime'].split('.')[0])
            Advertising.objects.filter(id=id).update(name=d['name'], type=d['type'], pic=d['pic'], startTime=d['startTime'],
            endTime=d['endTime'], status=d['status'], url=['url'], note=d['note'], sort=d['sort'])
            mes['code'] = 200
        return Response(mes)



# 修改单个广告上线下线
class Advertise_Show(APIView):
    def post(self, request):
        mes = {}
        id = request.GET.get('id')
        data = request.data
        try:
            Advertising.objects.filter(id=id).update(status=data['status'])
            mes['code'] = 200
        except:
            mes['code'] = 10010
            mes['erro'] = '修改失败'
        return Response(mes)


#批量 | 单删 广告
class DelAdvertise(APIView):
    def post(self, request):
        mes = {}
        id = request.GET.get('id')
        try:
            if id:
                Advertising.objects.filter(id=int(id)).delete()
            else:
                ids = request.data['ids'].split(',')
                Advertising.objects.filter(id__in=ids).delete()
                mes['code'] = 200
        except Exception as e:
            print(str(e))
        return Response(mes)