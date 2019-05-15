from django.db import models

# Create your models here.
class BaseModel(models.Model):
    create_time=models.DateTimeField(auto_now_add=True)
    update_time=models.DateTimeField(auto_now_add=True)
    class Meta:
        abstract = True
        


# 广告列表👍
class News(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)   
    type = models.IntegerField(default=0)
    pic = models.CharField(max_length=255)
    startTime = models.DateTimeField(auto_now_add=True)
    endTime = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(default=0)
    content = models.TextField(max_length=5000)
    sort = models.IntegerField(default=0)

    class Meta:
        db_table = 'news'


#品牌表
class Brand_copy(BaseModel,models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    first = models.CharField(max_length=100)
    logo = models.CharField(max_length=255)
    b_logo = models.CharField(max_length=255)
    story = models.CharField(max_length=255)
    sort = models.IntegerField()
    is_show = models.IntegerField(default=0)
    is_company = models.IntegerField(default=1)
    is_recommend = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=3,decimal_places=1)
    class Meta:
        db_table = "brand_copy"


#秒杀日期表
class Seckill_date(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)   #名称
    starting = models.DateField()    #开始时间
    ending = models.DateField()     #结束时间
    status = models.IntegerField(default=1)    #状态（1是0否）

    class Meta:
        db_table = 'seckill_date'


#秒杀时间段表（对一天24小时的）
class Seckill_time(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)   #名称
    starting = models.TimeField()    #开始时间
    ending = models.TimeField()     #结束时间
    status = models.IntegerField(default=1)    # 状态（1启用0不启用）
    class Meta:
        db_table = 'seckill_time'
    # def to_dict(self):
    #     dict = {'id':self.id, 'starting':self.starting, 'ending':self.ending}
    #     return dict
#秒杀商品表
class Seckill_product(models.Model):
    id = models.AutoField(primary_key=True) #货号
    name = models.CharField(max_length=100)   #商品名称
    code = models.CharField(max_length=50)  # 商品编号
    explain = models.CharField(max_length=100) # 商品注解
    pic = models.CharField(max_length=255)
    stock =  models.IntegerField() #库存
    price = models.DecimalField(max_digits=8,decimal_places=2) #原价
    class Meta:
        db_table = 'seckill_product'

    # def to_dict(self):
    #     dict = {'id':self.id, 'name':self.name, 'explain':self.explain, 'pic':self.pic}
    #     return dict
# 秒杀关系表
class Seckill_relation(models.Model):
    id = models.AutoField(primary_key=True)
    d_id = models.IntegerField()
    t_id = models.IntegerField()
    p_id = models.IntegerField()
    sprice = models.DecimalField(max_digits=8,decimal_places=2)  # 秒杀价格
    number = models.IntegerField()     #秒杀数量
    minimum = models.IntegerField()   #限购数量
    sort = models.IntegerField(default=1)    #排序
    class Meta:
        db_table = 'seckill_relation'



#商品表
class Product(BaseModel,models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    recommend = models.IntegerField(default=1)
    pic = models.CharField(max_length=255)
    lovenum = models.IntegerField(default=0)
    special_detail_id = models.IntegerField() # 专题外键
    class Meta:
        db_table = "product"


#专题栏分类表
class Special_cate(BaseModel,models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    img = models.CharField(max_length=255)
    recommend = models.IntegerField(default=0)

    class Meta:
        db_table = "special_cate"
    # @property
    # def info(self):
    #     return '%s' % (self.name)

# 专题详情
class Special_detail(BaseModel,models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    catename = models.CharField(max_length=100)
    content = models.CharField(max_length=6000)
    price = models.IntegerField(default=0)  # 商品起价
    recommend = models.IntegerField(default=1) #是否推荐
    sort = models.IntegerField(default=1)   #排序权重
    lovenum = models.IntegerField(default=0) # 收藏量
    browser = models.IntegerField(default=0)    #浏览量
    comment_num = models.IntegerField(default=0) # 评论量
    share_num = models.IntegerField(default=0) # 转发量
    s_cid = models.ForeignKey(Special_cate, to_field='id', on_delete='CASCADE', related_name='special_s_cid')
    class Meta:
        db_table = "special_detail"


# 专题图片
class Special_pic(BaseModel,models.Model):
    id = models.AutoField(primary_key=True)
    pic = models.CharField(max_length=255)
    s_did = models.ForeignKey(Special_detail, verbose_name='A类', to_field='id', on_delete='CASCADE', related_name='special_s_did')
    class Meta:
        db_table = "special_pic"
    # def to_dict(self):
    #     dict = {'pic': self.pic}
    #     return dict



# #后台用户表
# class Sadmins(BaseModel,models.Model):   
#     id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=30)
#     password = models.CharField(max_length=255)
#     image = models.CharField(max_length=100)
#     email = models.CharField(max_length=100)
#     nick_name = models.CharField(max_length=100)
#     status = models.IntegerField(default=1)
#     login_time=models.DateTimeField()
    
#     class Meta():
#         db_table = 'sadmins'

# #后台角色表
# class Roles(BaseModel,models.Model):   
#     id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=30)
#     status = models.IntegerField(default=1)

#     class Meta():
#         db_table = 'roles'

# #用户角色关联表
# class Admin_Roles(BaseModel,models.Model):   
#     id = models.AutoField(primary_key=True)
#     role_id = models.ForeignKey(Roles, to_field='id', on_delete='CASCADE', related_name='role_res')
#     admin_id = models.ForeignKey(Sadmins, to_field='id', on_delete='CASCADE', related_name='admin_role')

#     class Meta():
#         db_table = 'admin_roles'

# #权限表
# class Permission(BaseModel,models.Model):   
#     id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=100)
#     image = models.CharField(max_length=255)
#     url = models.CharField(max_length=100)
#     status = models.IntegerField(default=1)

#     class Meta():
#         db_table = 'permission'

# #角色权限表
# class Role_Permission(BaseModel,models.Model):   
#     id = models.AutoField(primary_key=True)
#     role_id = models.ForeignKey(Roles, to_field='id', on_delete='CASCADE', related_name='role_id')
#     permission_id = models.ForeignKey(Permission, to_field='id', on_delete='CASCADE', related_name='permission_id')

#     class Meta():
#         db_table = 'role_permission'

# #分类表
# class Category(BaseModel,models.Model):   
#     id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=100)
#     level = models.IntegerField(default=0)
#     parent_id = models.IntegerField(default=0)
#     is_nav_status = models.IntegerField(default=1)
#     status = models.IntegerField(default=1)
#     sort = models.IntegerField(default=0)
#     image = models.CharField(max_length=100)
#     keyword = models.CharField(max_length=100)
#     descrip = models.CharField(max_length=255)
#     count_danwei = models.CharField(max_length=255)

#     class Meta():
#         db_table = 'category'

# #商品类型表
# class Goods_type(BaseModel,models.Model):   
#     id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=100)
#     attribute_count = models.IntegerField(default=0)
#     param_count = models.IntegerField(default=0)
    
#     class Meta():
#         db_table = 'goods_type'

#     def to_dict(self):
#         dict = {'id': self.id, 'name': self.name}
#         return dict


# #商品类型属性表
# class Goods_type_attribute(BaseModel,models.Model):   
#     id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=100)
#     # 商品类型
#     type_id = models.ForeignKey(Goods_type, to_field='id', on_delete='CASCADE', related_name='type_id')
#     # 分类筛选样式
#     filter_type = models.IntegerField(default=1)
#     # 能否进行检索
#     is_select = models.IntegerField(default=0)
#     # 商品属性关联
#     related_status = models.IntegerField(default=0)
#     # 属性是否可选
#     select_type = models.IntegerField()
#     # 属性值的录入方式
#     input_type = models.IntegerField(default=0)
#     # 属性值可选值列表
#     input_list = models.CharField(max_length=255,default='')
#     # 是否支持手动新增
#     hand_add_status = models.IntegerField(default=0)
#     sort = models.IntegerField()
#     # 属性或是参数
#     type = models.IntegerField()
    
#     class Meta():
#         db_table = 'goods_type_attribute'

#     def to_dict(self):
#         dict = {'id': self.id, 'name': self.name}
#         return dict


# #分类属性关联表
# class Cate_attribute(BaseModel,models.Model):   
#     id = models.AutoField(primary_key=True)
#     cate_id = models.ForeignKey(Category, to_field='id', on_delete='CASCADE', related_name='cate_id')
#     goods_type_attribute_id = models.ForeignKey(Goods_type_attribute, to_field='id', on_delete='CASCADE', related_name='goods_type_attribute_id')

#     class Meta():
#         db_table = 'cate_attribute'


# #前台用户表
# class User(BaseModel,models.Model):
#     id = models.AutoField(primary_key=True)
#     mobile = models.CharField(max_length=50)
#     password = models.CharField(max_length=255)
#     login_count = models.IntegerField(default=0)

#     class Meta:
#         db_table = "user"

# #用户信息表
# class User_detail(BaseModel,models.Model):
#     id = models.AutoField(primary_key=True)
#     nickname = models.CharField(max_length=50)
#     sex = models.IntegerField(default=0)
#     user_id = models.IntegerField(default=0)
#     birthday = models.DateTimeField()
#     city = models.CharField(max_length=50)
#     occupation = models.CharField(max_length=50)
#     personalized = models.CharField(max_length=255)
#     image = models.CharField(max_length=255)
#     score = models.IntegerField(default=0)
#     growth = models.IntegerField(default=0)

#     class Meta:
#         db_table = "user_detail"

# #用户成长值表
# class Growth(BaseModel,models.Model):
#     id = models.AutoField(primary_key=True)
#     descrip = models.CharField(max_length=255)
#     score = models.IntegerField(default=0)
#     user_id = models.IntegerField(default=0)

#     class Meta:
#         db_table = "growth"

# #用户积分表
# class Score(BaseModel,models.Model):
#     id = models.AutoField(primary_key=True)
#     descrip = models.CharField(max_length=255)
#     score = models.IntegerField(default=0)
#     user_id = models.IntegerField(default=0)
#     action = models.IntegerField(default=0)

#     class Meta:
#         db_table = "score"

# #标签表
# class Label(BaseModel,models.Model):
#     id = models.AutoField(primary_key=True)
#     labelname = models.CharField(max_length=255)

#     class Meta:
#         db_table = "label"

# #话题分类表
# class Discourse_category(BaseModel,models.Model):
#     id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=255)

#     class Meta:
#         db_table = "discourse_category"

# #话题详情表
# class Discourse_detail(BaseModel,models.Model):
#     id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=255)
#     img = models.CharField(max_length=255)
#     user_id = models.IntegerField(default=0)
#     is_hort = models.IntegerField(default=0)
#     content = models.CharField(max_length=255)
#     collect_sum = models.IntegerField(default=0)
#     read_sum = models.IntegerField(default=0)
#     evaluate_sum = models.IntegerField(default=0)
#     is_show = models.IntegerField(default=0)
#     dc_id = models.IntegerField(default=0) #所属分类id

#     class Meta:
#         db_table = "discourse_detail"

# #话题标签表
# class Discourse_label(BaseModel,models.Model):   
#     id = models.AutoField(primary_key=True)
#     label_id = models.ForeignKey(Label, to_field='id', on_delete='CASCADE', related_name='label_id')
#     discourse_detail_id = models.ForeignKey(Discourse_detail, to_field='id', on_delete='CASCADE', related_name='discourse_detail_id')

#     class Meta():
#         db_table = 'discourse_label'

# #用户话题收藏表
# class Discourse_collect(BaseModel,models.Model):
#     id = models.AutoField(primary_key=True)
#     user_id = models.ForeignKey(User, to_field='id', on_delete='CASCADE', related_name='user_id')
#     discourse_id = models.ForeignKey(Discourse_detail, to_field='id', on_delete='CASCADE', related_name='discourse_id')
#     Type = models.IntegerField(default=0) #1话题  2专题  3商品 4 品牌

#     class Meta():
#         db_table = 'discourse_collect'

# #话题评论表
# class Discourse_comment(BaseModel,models.Model):
#     id = models.AutoField(primary_key=True)
#     user_id = models.IntegerField()
#     username = models.CharField(max_length=255)
#     pic = models.CharField(max_length=255)
#     discourse_id = models.IntegerField()
#     content = models.CharField(max_length=255)
#     pid = models.IntegerField(default=0)
#     total_zan = models.IntegerField(default=0)

#     class Meta:
#         db_table = "discourse_comment"

# #话题评论图片表
# class Discourse_comment_img(BaseModel,models.Model):
#     id = models.AutoField(primary_key=True)
#     discourse_comment_id = models.IntegerField()
#     pic = models.CharField(max_length=255)

#     class Meta:
#         db_table = "discourse_comment_img"

# #评论点赞表
# class Comment_zan(BaseModel,models.Model):   
#     id = models.AutoField(primary_key=True)
#     user_id = models.ForeignKey(User, to_field='id', on_delete='CASCADE', related_name='u_id')
#     discourse_comment_id = models.ForeignKey(Discourse_comment, to_field='id', on_delete='CASCADE', related_name='dc_id')

#     class Meta():
#         db_table = 'comment_zan'

# #话题评论表
# class Discourse_award(BaseModel,models.Model):
#     id = models.AutoField(primary_key=True)
#     user_id = models.IntegerField()
#     discourse_id = models.IntegerField()
#     discrip = models.CharField(max_length=255)
#     number = models.IntegerField(default=0)
#     Type = models.IntegerField(default=0)
#     score = models.IntegerField(default=0)
#     label_id = models.CharField(max_length=255) #优惠卷编码

#     class Meta:
#         db_table = "discourse_award"

# #优惠卷表
# class Coupon(models.Model):
#     id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=30)   #名称
#     type=models.IntegerField()     #0全场  1会员   2购物    3注册
#     pingtai=models.IntegerField()          #0全平台  1移动    2PC
#     faxing=models.IntegerField()        #总发行量
#     miane=models.DecimalField(max_digits=8,decimal_places=2)  # 优惠价格
#     limit = models.IntegerField()       #每人限领
#     doorsill = models.DecimalField(max_digits=8,decimal_places=2)    #使用门槛
#     start_time=models.DateField()    #开始时间
#     end_time=models.DateField()     #结束时间
#     goods_use=models.IntegerField()       #0全场通用   1指定分类     2指定商品
#     describe=models.CharField(max_length=255)  #描述
#     state=models.IntegerField()        #0未过期  1过期
#     neck_number=models.IntegerField(default=0)        #已领数量
#     stay_number=models.IntegerField(default=0)       #待领取数量
#     unused_number=models.IntegerField(default=0)     #未使用数量
#     use_number= models.IntegerField(default=0)       #待领取数量


#     class Meta:
#         db_table = 'coupon'

# #用户优惠卷表
# class User_label(BaseModel,models.Model):
#     id = models.AutoField(primary_key=True)
#     coupon_id = models.IntegerField()
#     user_id = models.IntegerField()
#     starttime = models.DateTimeField()
#     stoptime = models.DateTimeField()
#     coupon_code = models.CharField(max_length=255)
#     status = models.IntegerField(default=0)
    
#     class Meta:
#         db_table = "user_label"

# #喜欢的分类表
# class Like_category(BaseModel,models.Model):
#     id = models.AutoField(primary_key=True)
#     user_id = models.ForeignKey(User, to_field='id', on_delete='CASCADE', related_name='yonghu_id')
#     category_id = models.ForeignKey(Category, to_field='id', on_delete='CASCADE', related_name='c_id')

    
#     class Meta:
#         db_table = "like_category"

# #用户关注的品牌
# class User_concern_brand(BaseModel,models.Model):
#     id = models.AutoField(primary_key=True)
#     user_id = models.ForeignKey(User, to_field='id', on_delete='CASCADE', related_name='user_brand_id')
#     brand_id = models.ForeignKey(Brand, to_field='id', on_delete='CASCADE', related_name='brand_id')

    
#     class Meta:
#         db_table = "user_concern_brand"



# #商品促销价格表
# class Goods_sales_price(BaseModel,models.Model):
#     id = models.AutoField(primary_key=True)
#     goods_id = models.IntegerField()
#     promote_price = models.DecimalField(max_digits=8, decimal_places=2)
#     starttime = models.DateTimeField()
#     stoptime = models.DateTimeField()

#     class Meta:
#         db_table = "goods_sales_price"

# #商品会员价格表
# class Goods_member_price(BaseModel,models.Model):
#     id = models.AutoField(primary_key=True)
#     product_id = models.IntegerField()
#     member_level_id = models.IntegerField()
#     price = models.DecimalField(max_digits=8, decimal_places=2)
#     member_level_name = models.CharField(max_length=50)

#     class Meta:
#         db_table = "goods_member_price"

# #商品阶梯价格表
# class Goods_fight(BaseModel,models.Model):
#     id = models.AutoField(primary_key=True)
#     product_id = models.IntegerField()
#     pro_count = models.IntegerField()
#     discount = models.DecimalField(max_digits=8, decimal_places=2)
#     price = models.DecimalField(max_digits=8, decimal_places=2)

#     class Meta:
#         db_table = "goods_fight"

# #商品满减表
# class Goods_full_price(BaseModel,models.Model):
#     id = models.AutoField(primary_key=True)
#     product_id = models.IntegerField()
#     full_price = models.DecimalField(max_digits=8, decimal_places=2)
#     reduce_price = models.DecimalField(max_digits=8, decimal_places=2)

#     class Meta:
#         db_table = "goods_full_price"

# #商品属性表
# class Goods_attribute_value(BaseModel,models.Model):
#     id = models.AutoField(primary_key=True)
#     goods_id = models.ForeignKey(Goods, to_field='id', on_delete='CASCADE', related_name='g_id')
#     attribute_id = models.ForeignKey(Goods_type_attribute, to_field='id', on_delete='CASCADE', related_name='attribute_id')

#     class Meta:
#         db_table = "goods_attribute_value"

# #商品属性库存表
# class Goods_attribute_stock(BaseModel,models.Model):
#     id = models.AutoField(primary_key=True)
#     goods_id = models.IntegerField()
#     sku_code = models.CharField(max_length=255)
#     price = models.DecimalField(max_digits=8, decimal_places=2)
#     stock = models.IntegerField(default=0)
#     low_stock = models.IntegerField(default=0)
#     sp1 = models.CharField(max_length=255)
#     sp2 = models.CharField(max_length=255)
#     sp3 = models.CharField(max_length=255)
#     sale = models.IntegerField(default=0)
#     lock_stocp = models.IntegerField(default=0)

#     class Meta:
#         db_table = "goods_attribute_stock"

# #商品相册表
# class Goods_pics(BaseModel,models.Model):
#     id = models.AutoField(primary_key=True)
#     goods_id = models.IntegerField()
#     pic = models.CharField(max_length=255)

#     class Meta:
#         db_table = "goods_pics"

# #指定商品优惠表
# class Goods_coupon(BaseModel,models.Model):
#     id = models.AutoField(primary_key=True)
#     coupon_id = models.ForeignKey(Coupon, to_field='id', on_delete='CASCADE', related_name='cou_id')
#     goods_id = models.ForeignKey(Goods, to_field='id', on_delete='CASCADE', related_name='goods_id')

#     class Meta:
#         db_table = "goods_coupon"

# #优惠卷分类表
# class Coupon_cate(BaseModel,models.Model):   
#     id = models.AutoField(primary_key=True)
#     coupon_id = models.ForeignKey(Coupon, to_field='id', on_delete='CASCADE', related_name='coup_id')
#     cate_id = models.ForeignKey(Category, to_field='id', on_delete='CASCADE', related_name='category_id')

#     class Meta():
#         db_table = 'coupon_cate'

# #省市区表
# class Area(BaseModel,models.Model):
#     id = models.AutoField(primary_key=True)
#     pid = models.IntegerField(default=0)
#     name = models.CharField(max_length=255)

#     class Meta:
#         db_table = "area"

# #用户收获地址表
# class Address(BaseModel,models.Model):
#     id = models.AutoField(primary_key=True)
#     user_id = models.IntegerField()
#     name = models.CharField(max_length=255)
#     country = models.IntegerField(default=0)
#     city = models.IntegerField(default=0)
#     area = models.IntegerField(default=0)
#     address = models.CharField(max_length=255)
#     telphone = models.CharField(max_length=255)
#     is_default = models.IntegerField(default=0)

#     class Meta:
#         db_table = "address"

# #购物车表
# class Cart(BaseModel,models.Model):
#     id = models.AutoField(primary_key=True)
#     user_id = models.IntegerField()
#     goods_id = models.IntegerField()
#     goods_name = models.CharField(max_length=255)
#     sp1 = models.CharField(max_length=255)
#     price = models.DecimalField(max_digits=8, decimal_places=2)
#     count = models.IntegerField(default=0)
#     status = models.IntegerField(default=0)
#     img = models.CharField(max_length=255)

#     class Meta:
#         db_table = "cart"

# #用户订单表
# class User_orders(BaseModel,models.Model):
#     id = models.AutoField(primary_key=True)
#     order_sn = models.CharField(max_length=255)
#     user_id = models.IntegerField()
#     username = models.CharField(max_length=255)
#     total_money = models.DecimalField(max_digits=8, decimal_places=2)
#     coupon_money = models.DecimalField(max_digits=8, decimal_places=2)
#     actual_money = models.DecimalField(max_digits=8, decimal_places=2)
#     pay_type = models.IntegerField(default=0)
#     source = models.IntegerField(default=0)
#     status = models.IntegerField(default=0)
#     pay_code = models.CharField(max_length=255)

#     class Meta:
#         db_table = "user_orders"


# #优选表
# class Super(BaseModel,models.Model):
#     id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=255)
#     title = models.CharField(max_length=255)
#     img = models.CharField(max_length=255)

#     class Meta:
#         db_table = "super"

# #帮助/管理表
# class Manage(BaseModel,models.Model):
#     id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=255)
#     content = models.CharField(max_length=255)

#     class Meta:
#         db_table = "manage"







# #订单设置👍
# class Dingdan_setting(models.Model):
#     id = models.AutoField(primary_key=True)
#     flashOrderOvertime = models.IntegerField(default=0)
#     normalOrderOvertime = models.IntegerField(default=0)
#     confirmOvertime = models.IntegerField(default=0)
#     finishOvertime = models.IntegerField(default=0)
#     commentOvertime = models.IntegerField(default=0)

#     class Meta:
#         db_table = 'dingdan_setting'


# #会员等级表👍
# class Member_grade(models.Model):
#     id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=255)   

#     class Meta:
#         db_table = 'member_grade'