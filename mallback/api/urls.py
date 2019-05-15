from django.urls import path,include,re_path
from django.views.generic import TemplateView
from api import views

app_name = 'myadmin'  #声明命名空间/子应用
urlpatterns = [
    # 轮播图
    path('fetchNewsPic',views.FetchNewsPic.as_view()),
    # 新闻-详情
    path('fetchNews',views.FetchNews.as_view()),
    # 品牌制造商
    path('fetchBrand',views.FetchBrand.as_view()),
    # 秒杀商品 IndexFlashProduct
    path('FlashProduct',views.FlashProduct.as_view()),
    # 新鲜好物
    path('fetchSeckillProduct',views.FetchSeckillProduct.as_view()),
    # 人气推荐 
    path('fetchLoveProduct',views.FetchLoveProduct.as_view()),
    # 专题推荐
    path('fetchSpecialOne',views.FetchSpecialOne.as_view()),
    # 更多推荐
    path('fetchSpecialList',views.FetchSpecialList.as_view()),
    path('fetchSpecialCate',views.FetchSpecialCate.as_view()),
    path('fetchSpecialDetail',views.FetchSpecialDetail.as_view()),
    # 猜你喜欢
    path('fetchLoveProduct',views.FetchLove.as_view()),
]