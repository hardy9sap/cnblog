"""cnblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf.urls import url, include
from django.views.static import serve
from django.urls import path, re_path
from blog import views
from cnblog import settings

urlpatterns = [
    path('admin/', admin.site.urls),  # 后台数据管理
    re_path('^$', views.get_index),  # index页面
    re_path('^test', views.test),  # 自定义测试页面
    re_path('^diggit', views.diggit),  # 赞、反对视图
    re_path('^media/(?P<path>.*)/$', serve, {'document_root': settings.MEDIA_ROOT}),  # media接口
    re_path('^register/(?P<protocol>protocol/)?$', views.register),  # 注册视图
    re_path('^login/', views.login),  # 登录视图
    re_path('^logout/', views.logout),  # 注销视图
    re_path('^comment/', views.comment),  # 评论视图
    re_path('^get-comment-tree/', views.get_comment_tree),  # 评论树
    re_path('^cnblog-backend/$', views.manage_backend),  # 后台管理
    re_path('^cnblog-backend/add-article/', views.add_article),  # 添加文章
    re_path('^upload/', views.upload),  # 文本编辑器上传
    url(regex=r'^pc-geetest/register', view=views.pcgetcaptcha, name='pcgetcaptcha'),  # 滑动验证码第一次校验
    re_path('^(?P<sitename>\w{4,})$', views.get_homesite),  # 个人站点视图
    re_path('^(?P<sitename>\w{4,})/(?P<condition>tag|category|archive|)/(?P<param>.+)', views.get_homesite),
    # 标签、分类、档案请求
    re_path('^(?P<sitename>\w{4,})/(?P<article>article)/(?P<article_id>\d+)', views.get_article_detail),  # 文章详情

    # markdown
    re_path('^markdown/', views.simplemde),

    re_path('^', views.get_404_page),  # 404

]
