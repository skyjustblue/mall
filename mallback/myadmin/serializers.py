from rest_framework import serializers
from myadmin.models import *
from werkzeug.security import generate_password_hash,check_password_hash

#获取品牌
class BrandModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = "__all__"

#获取商品分类
class CategoryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class CategoryModelSerializer_2(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')
    
#获取商品类型
class Goods_typeModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goods_type
        fields = "__all__"

#获取商品属性参数
class Goods_type_attributeModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goods_type_attribute
        fields = "__all__"


#获取广告
class AdvertisingModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertising
        fields = "__all__"


#获取会员
class Member_gradeModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member_grade
        fields = "__all__"

# #添加用户
# class AdduserSerializer(serializers.Serializer):
#     name = serializers.CharField(required=True, max_length=30)
#     password = serializers.CharField(required=True, max_length=255)
#     email = serializers.CharField(required=True, max_length=100)
#     Dep_id = serializers.IntegerField(required=True)
    
#     def create(self, validated_data):
#         validated_data['password'] = generate_password_hash(validated_data['password'])
#         return User.objects.create(**validated_data)

#添加品牌
class AddbrandSerializer(serializers.Serializer):
    name = serializers.CharField(required=True, max_length=50)
    first = serializers.CharField(required=True, max_length=1)
    logo = serializers.CharField(required=True, max_length=255)
    b_logo = serializers.CharField(required=True, max_length=255)
    story = serializers.CharField(required=True, max_length=255)
    sort = serializers.IntegerField(required=True)
    is_show = serializers.IntegerField(required=True)
    is_company = serializers.IntegerField(required=True)
    # is_recommend = serializers.IntegerField(default=0)

    def create(self, validated_data):
        return Brand.objects.create(**validated_data)


# 添加商品类型
class AddGoods_TypeSerializer(serializers.Serializer):
    name = serializers.CharField(required=True, max_length = 50) #类型名称
    def create(self, validated_data):
        return Goods_type.objects.create(**validated_data)



#添加类型属性
class AddgoodstypeSerializer(serializers.Serializer):
    name = serializers.CharField(required=True, max_length=50)
    filter_type = serializers.IntegerField(required=True)
    is_select = serializers.IntegerField(required=True)
    related_status = serializers.IntegerField(required=True)
    select_type = serializers.IntegerField(required=True)
    input_type = serializers.IntegerField(required=True)
    input_list = serializers.CharField(default='')
    hand_add_status = serializers.IntegerField(required=True)
    sort = serializers.IntegerField(required=True)
    type = serializers.IntegerField(required=True)
    
    #指定序列化外键 type_id 
    def create(self, validated_data):
        return Goods_type_attribute.objects.create(type_id=self.context["type_id_object"],**validated_data)



#添加商品分类
class CategorySerializer(serializers.Serializer):
    name = serializers.CharField(required=True, max_length=100)
    level = serializers.IntegerField(required=True)
    parent_id = serializers.IntegerField(required=True)
    is_nav_status = serializers.IntegerField(default=1) #required=True 要进行验证
    status = serializers.IntegerField(default=1)
    sort = serializers.IntegerField(required=True)
    image = serializers.CharField(required=True, max_length=100)
    keyword = serializers.CharField(required=True, max_length=100)
    descrip = serializers.CharField(required=True, max_length=255)
    count_danwei = serializers.CharField(required=True, max_length=255)
    
    def create(self, validated_data):
        return Category.objects.create(**validated_data)



#添加广告
class AdvertisingSerializer(serializers.Serializer):
    name = serializers.CharField(required=True, max_length=255)
    type = serializers.IntegerField(required=True)
    pic = serializers.CharField(required=True, max_length=255)
    startTime = serializers.CharField(required=True, max_length=255)
    endTime = serializers.CharField(required=True, max_length=255)
    url = serializers.CharField(required=True, max_length=255)
    status = serializers.IntegerField(required=True)
    note = serializers.CharField(required=True, max_length=255)
    sort = serializers.IntegerField(required=True)

    def create(self, validated_data):
        return Advertising.objects.create(**validated_data)

    def update(self, instance, validated_data):
        print(validated_data)
        """更新，instance为要更新的对象实例"""
        instance.name = validated_data.get('name', instance.name)
        instance.type = validated_data.get('type', instance.type)
        instance.pic = validated_data.get('pic', instance.pic)
        instance.startTime = validated_data.get('startTime', instance.startTime)
        instance.endTime = validated_data.get('endTime', instance.endTime)
        instance.url = validated_data.get('url', instance.url)
        instance.status = validated_data.get('status', instance.status)
        instance.note = validated_data.get('note', instance.note)
        instance.sort = validated_data.get('sort', instance.sort)
        instance.save()
        return instance