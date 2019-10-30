"""WorldTravel URL Configuration

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
from django.conf.urls import url
from DjangoUeditor import urls as DjangoUeditor_urls
from django.urls import path, re_path, include
from django.views.static import serve
import xadmin
from WorldTravel import settings
# from WorldTravel.settings import MEDIA_ROOT, STATIC_ROOT
from users.views import RegisterView, LoginView, ActiveView, IndexView, LogoutView, ForgetPwdView, ResetView, \
    NewPwdView, CheckView, UserInfoView, ProvinceView, CityView, CountyView, SettingInfoView

urlpatterns = [

    # path('admin/', admin.site.urls),
    path('xadmin/', xadmin.site.urls),
    # 用户上传文件路径
    # re_path(r'media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
    # static文件路径
    # re_path(r'static/(?P<path>.*)$',serve,{"document_root": STATIC_ROOT}),
    # 富文本编辑器
    path('ueditor/', include('DjangoUeditor.urls')),
    #验证码
    re_path(r'^captcha/', include('captcha.urls')),


    # 用户相关
    # 用户注册
    path('register/', RegisterView.as_view(), name='register'),
    # 登陆
    path('login/', LoginView.as_view(), name='login'),
    # 账号激活
    path('active/<slug:active_code>', ActiveView.as_view(), name='active'),
    # 退出登录
    path('logout/', LogoutView.as_view(), name='logout'),
    # 忘记密码
    path('forget_pwd', ForgetPwdView.as_view(), name='forget_pwd'),
    # 找回密码
    path('find/<slug:find_code>', ResetView.as_view(), name='find'),
    # 修改密码
    path('new_pwd/', NewPwdView.as_view(), name='new_pwd'),
    # 签到页面
    path('check/', CheckView.as_view(), name='check'),
    # 设置页面
    path('userinfo/<slug:info_type>', UserInfoView.as_view(), name='userinfo'),
    # 获取省市区信息
    path('province/', ProvinceView.as_view(), name='province'),
    path('city_<int:pid>/', CityView.as_view(), name='city'),
    path('county_<int:pid>/', CountyView.as_view(), name='county'),
    # 修改个人信息
    path('setting/<slug:setting_type>', SettingInfoView.as_view(), name='setting'),

    # 网站相关
    # 主页
    path('', IndexView.as_view(), name='index'),
    # 新闻
    path('news/', include(('news.urls', 'news'))),
    # 旅游页面
    path('scenicspots/', include(('scenicspots.urls', 'scenicspots')), name='scenicspots'),

]

if settings.DEBUG:
   from django.conf.urls.static import static
   urlpatterns += static(
       settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
   )
