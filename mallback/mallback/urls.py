"""mallback URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path,include
#导入文件路由库
from django.views.static import serve
#导入配置文件的路径
from mallback.settings import UPLOAD_ROOT
from rest_framework.documentation import include_docs_urls

urlpatterns = [
    # 显示图片
    re_path(r'^docs/', include_docs_urls(title='API接口文档')),
    path('',include('api.urls')),
    re_path("^upload/(?P<path>.*)$",serve,{'document_root':UPLOAD_ROOT}),
    # path('admin/', admin.site.urls),
    # path('myadmin/',include('myadmin.urls')),
]