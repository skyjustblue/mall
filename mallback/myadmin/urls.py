from django.urls import path,include,re_path
from django.views.generic import TemplateView
from myadmin import views

app_name = 'myadmin'  #声明命名空间/子应用
urlpatterns = [
    path('do_login/',views.Login.as_view()),  # 登录接口
    

    # # path('', TemplateView.as_view(template_name = 'admin/login.html')), # 登录页面
    
    # path('index/', TemplateView.as_view(template_name = 'admin/index.html')),   # 后台首页
    # # 一、商品列表页面
    # # 二、添加商品页面
    # 会员
    path('memberLevelList',views.MemberLevelList.as_view()),
    path('fetchProductAttrCateList',views.FetchProductAttrCateList.as_view()),
    # # 三、商品分类页面
    path('productCategoryList',views.ProductCategoryList.as_view()),
    path('createProductCate',views.CreateProductCate.as_view()),   # 添加 | 编辑 --商品分类
    path('productCateList',views.ProductCateNameList.as_view()),  # 预先获取所有分类id,name
    path('cateShow',views.CateShow.as_view()),    # 分类导航栏开关 是否显示
    path('deleteProductCate',views.DeleteProductCate.as_view()),    # 删除分类列表


    # 四、商品类型页面
    path('addEditGoodtype',views.AddEditGoodtype.as_view()),   # 添加 | 编辑 --商品类型
    path('deleteGoodtype',views.DelGoodtype.as_view()),    # 删除商品类型
    path('productAttrList/',views.ProductAttrParamList.as_view()), # 属性/参数列表页
    path('deleteProductAttr/', views.DeleteProductAttr.as_view()),  # 删除-属性/参数列表页
    path('createProductAttr',views.CreateProductAttr.as_view()), # 添加-属性/参数
    path('updateProductAttr',views.UpdateProductAttr.as_view()), # 编辑-属性/参数
    
    # 五、品牌管理页面
    path('brands',views.Brands.as_view()),
    # 是否为品牌制造商 | 是否显示
    path('brand_show',views.Brand_show.as_view()),
    # #品牌管理详情页
    path('uploadimage/',views.UploadImage.as_view()),   #上传图片
    path('create_brand_detail',views.Brand_detail.as_view()),
    # #品牌删除
    path('del_brand', views.Del_brand.as_view()),


    # 广告列表
    path('advertiseList',views.AdvertiseList.as_view()),
    # 添加广告
    path('createAdvertise',views.CreateAdvertise.as_view()),
    # 修改单个广告上线下线
    path('advertise_Show',views.Advertise_Show.as_view()),
    # 批量 | 单删 广告
    path('delAdvertise',views.DelAdvertise.as_view()),

    # 专题推荐
    # subjectList
    # """二、订单模块"""
    # '''1、订单列表'''
    # '''2、订单设置'''
    # '''3、退货申请处理'''
    # '''4、退货原因设置'''


    # """三、营销模块"""
    # '''1、秒杀活动列表'''
    # '''2、优惠券列表'''
    # '''3、品牌推荐'''
    # 全部品牌
    path('recommendBrandList',views.RecommendBrandList.as_view()),
    # 选择品牌加入推荐
    path('createHomeBrand',views.CreateHomeBrand.as_view()),
    # 设置排序
    # path('updateHomeBrandSort/',views.UpdateHomeBrandSort.as_view()),
    # 单个|批量 选择品牌是否推荐
    path('updateRecommendStatus',views.UpdateRecommendStatus.as_view()),
    # 单个|批量 删除品牌
    path('deleteHomeBrand',views.DeleteHomeBrand.as_view()),


    # '''4、新品推荐'''
    # '''5、人气推荐'''
    # '''6、专题推荐'''
    # '''7、广告列表'''



    # #分类列表二级分类封装
    # path('type/',views.Type_list.as_view()),
    # path('add_type/',views.Add_type.as_view()),
    # path('add_property/', views.Add_property.as_view()),

    # path('delete_pro/', views.Delete_pro.as_view()),
    # path('jia_leixing/', views.Jia_leixing.as_view()),
    # path('shop_type/', views.Shop_type.as_view()),
    # path('delete_type_list/', views.Delete_type_list.as_view()),
    
    # path('shop_type_cate/', views.Shop_type_cate.as_view()),
    # #修改商品是否新品推荐
    # path('goods_xin_update/', views.Goods_xin_update.as_view()),
    # #删除新品推荐商品
    # path('goods_xinpin_delete/', views.Goods_xinpin_delete.as_view()),
    # #修改新品推荐商品
    # path('goods_xinpin_update/', views.Goods_xinpin_update.as_view()),
    # #修改新品推荐商品列表
    # path('goods_xinpinlist_update/', views.Goods_xinpinlist_update.as_view()),
    # #展示新品推荐商品列表
    # path('goods_xinpin/', views.Goods_xinpin.as_view()),
    # #修改新品推荐商品排序
    # path('goods_xinpin_sort/', views.Goods_xinpin_sort.as_view()),
    # #展示商品列表
    # path('goods_list/', views.Goods_list.as_view()),
    # #修改商品上架状态
    # path('goods_status_update/', views.Goods_status_update.as_view()),
    # #分类是否显示
    # path('cate_show/', views.Cate_show.as_view()),
    # #添加品牌
    # path('add_brand/', views.Add_brand.as_view()),
    # #类型加属性
    # path('type_shuxing/', views.Type_shuxing.as_view()),
    # #品牌管理
    # path('brand_lods', views.Shop_guan.as_view()),
    # #添加到品牌推荐
    # path('add_brand_show/',views.Add_brand_show.as_view()),
    # #品牌是否显示
    # path('brand_show',views.Brand_show.as_view()),
    # #品牌管理详情页
    # path('brand__detail',views.Brand_detail.as_view()),
    # #删除类型
    # path('del_brand', views.Del_brand.as_view()),
    # #删除品牌
    # path('del_pinpai', views.Del_pinpai.as_view()),
    # #品牌排序
    # path('pinpai_sort/', views.Pinpai_sort.as_view()),
    # #品牌推荐列表
    # path('pinpai_list/', views.Pinpai_list.as_view()),
    # #上传图片
    # path('image/', views.Image.as_view()),
    # #添加广告
    # path('add_guanggao/', views.Add_guanggao.as_view()),
    # #查询广告
    # path('guanggao_list/', views.Guanggao_list.as_view()),
    # #修改广告上线下线
    # path('guanggao_show/', views.Guanggao_show.as_view()),
    # #删除广告
    # path('guanggao_delete/', views.Guanggao_delete.as_view()),
    # #查询会员
    # path('huiyuan_list/', views.Huiyuan_list.as_view()),
    # #添加商品
    # path('add_shop/', views.Add_shop.as_view()),
    # #添加优惠卷
    # path('add_coupon/', views.Add_coupon.as_view()),
    # #添加活动
    # path('add_huodong/', views.Add_huodong.as_view()),
    # #活动列表
    # path('huodong_list/', views.Huodong_list.as_view()),
    # #删除活动
    # path('huodong_delete/', views.Huodong_delete.as_view()),
    # #修改活动状态
    # path('huodong_status_show/', views.Huodong_status_show.as_view()),
    # #添加秒杀活动
    # path('add_miaoshahuodong/', views.Add_miaoshahuodong.as_view()),
    # #秒杀活动列表
    # path('miaoshahuodong_list/', views.Miaoshahuodong_list.as_view()),
    # #修改秒杀活动
    # path('update_miaoshahuodong/', views.Update_miaoshahuodong.as_view()),
    # #删除秒杀活动
    # path('miaoshahuodong_delete/', views.Miaoshahuodong_delete.as_view()),
    # #订单设置
    # path('order_setting/', views.Order_setting.as_view()),
    # #订单设置列表
    # path('dingdan_setting_list/', views.Dingdan_setting_list.as_view()),
    # #优惠卷列表
    # path('coupon_list/', views.Coupon_list.as_view()),
    # #修改优惠卷
    # path('coupon_update/', views.Coupon_update.as_view()),

]
