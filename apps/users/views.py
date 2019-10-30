from datetime import datetime
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.base import View
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url
from django.contrib.auth.hashers import make_password
from users.models import Myuser, EmailVerifyRecord, AreaInfo, TheContact
from utils.send_email import send_register_email
from .forms import *
from django.contrib.auth import authenticate, login, logout
import json

class IndexView(View):
    """
    首页
    """

    def get(self, request):
        return render(request, 'index.html', {
            'now_type': 'index',
        })


class RegisterView(View):
    """
    注册
    """

    # 获取验证码, 返回注册页面
    def get(self, request):

        register_form = RegisterForm()
        hashkey = CaptchaStore.generate_key()
        image_url = captcha_image_url(hashkey)
        return render(request, 'users/register.html', {
            'register_form': register_form,
            'hashkey': hashkey,
            'image_url': image_url,
        })

    # 用户点击注册
    def post(self, request):
        # 获取邮箱和密码,并校验
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            # 获取邮箱
            user_name = request.POST.get('email', '')
            # 根据user_name查询数据库
            if Myuser.objects.filter(email=user_name):
                # 可以查询到用户
                return render(request, 'users/register.html', {
                    'register_form': register_form,
                    'msg': '用户已经存在'
                })
            # 完善用户信息
            password = request.POST.get('password', '')
            user_profile = Myuser()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.is_active = False
            user_profile.password = make_password(password)
            user_profile.save()

            # 发送邮件
            send_register_email(user_name)
            messages.add_message(request, messages.SUCCESS, '注册成功！请在邮箱中点击激活链接激活账号！')
            return render(request, 'users/register.html', {})
        else:
            hashkey = CaptchaStore.generate_key()
            image_url = captcha_image_url(hashkey)
            return render(request, 'users/register.html', {
                'register_form': register_form,
                'hashkey': hashkey,
                'image_url': image_url})


class ActiveView(View):
    """
    账号激活
    """

    def get(self, request, active_code):
        # 根据active_code获取邮箱信息
        all_records = EmailVerifyRecord.objects.filter(send_type='register', code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = Myuser.objects.get(email=email)
                user.is_active = True
                user.save()
        return render(request, 'users/register.html', {})


class LoginView(View):
    """
    登录
    """

    def get(self, request):
        return render(request, 'users/login.html', {})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            # 参数校验成功,获取用户名和密码
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            is_keep = request.POST.get('is_keep', '')
            user = authenticate(username=username, password=password)
            # 如果用户存在
            if user is not None and user.is_active:
                login(request, user)
                # 如果保持登陆状态
                if not is_keep:
                    # 关闭浏览器session实效
                    request.session.set_expiry(0)
                return HttpResponseRedirect(reverse('index'))
            else:
                return render(request, 'users/login.html', {'msg': '用户名或密码错误！'})
        else:
            return render(request, 'users/login.html', {'login_form': login_form})


class LogoutView(View):
    """
    退出登录
    """

    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('index'))


class ForgetPwdView(View):
    """
    忘记密码
    """

    def get(self, request):
        forget_form = ForgetForm()
        hashkey = CaptchaStore.generate_key()
        image_url = captcha_image_url(hashkey)
        return render(request, 'users/forget_pwd.html', {
            'forget_form': forget_form,
            'hashkey': hashkey,
            'image_url': image_url,
        })

    def post(self, request):
        forget_form = ForgetForm(request.POST)
        hashkey = CaptchaStore.generate_key()
        image_url = captcha_image_url(hashkey)
        if forget_form.is_valid():
            email = request.POST.get('email', '')
            send_register_email(email, 'find')
            messages.add_message(request, messages.SUCCESS, '邮件发送成功！请点击邮件中的链接找回密码')
            return render(request, 'users/forget_pwd.html', {
                'hashkey': hashkey,
                'image_url': image_url,
            })
        else:
            return render(request, 'users/forget_pwd.html', {
                'forget_form': forget_form,
                'hashkey': hashkey,
                'image_url': image_url,
            })


class ResetView(View):
    """
    找回密码
    """

    def get(self, request, find_code):
        all_records = EmailVerifyRecord.objects.filter(send_type='find', code=find_code)
        if all_records:
            for rcord in all_records:
                email = rcord.email
                return render(request, 'users/new_pwd.html', {
                    'email': email,
                })


class NewPwdView(View):
    """
    修改密码
    """

    def post(self, request):
        newpwd_form = NewPwdForm(request.POST)
        if newpwd_form.is_valid():
            pwd1 = request.POST.get('pwd1', '')
            pwd2 = request.POST.get('pwd2', '')
            email = request.POST.get('email', '')
            if pwd1 != pwd2:
                return render(request, 'users/new_pwd.html', {
                    'email': email,
                    'msg': '两次输入的密码不一致',
                })
            user = Myuser.objects.get(email=email)
            user.password = make_password(pwd2)
            user.save()
            return HttpResponseRedirect(reverse('login'))
        else:
            email = request.POST.get('email', '')
            return render(request, 'users/new_pwd.html', {
                'email': email,
                'newpwd_form': newpwd_form,
            })


class CheckView(View):
    """
    签到
    """
    def post(self, request):
        # 获取用户
        username = request.POST.get('user', '')
        # 查询用户详情
        user = Myuser.objects.filter(username=username)
        now = datetime.now().strftime('%Y-%m-%d')
        for now_user in user:
            # 判断用户签到时间与当前时间不相同(一天只能签到一次)
            if str(now_user.check_time) != now:
                # 修改当前积分加20
                now_user.integral += 20
                # 修改签到时间
                now_user.check_time = now
                now_user.save()
                result = json.dumps({"status": "success", "msg": "签到成功"}, ensure_ascii=False)
            else:
                result = json.dumps({"status": "fail", "msg": "签到失败，今天已经签过了"}, ensure_ascii=False)
            return HttpResponse(result)


class ProvinceView(View):
    """
    获取省
    """
    def get(self, request):
        pros = AreaInfo.objects.filter(Parent=0)
        pro_list = []
        for pro in pros:
            pro_list.append([pro.id, pro.title])
        return JsonResponse({'prov': pro_list})


class CityView(View):
    """
    获取市
    """
    def get(self, request, pid):
        print(pid)
        citys = AreaInfo.objects.filter(Parent=pid)
        city_list = []
        for city in citys:
            city_list.append([city.id, city.title])
        return JsonResponse({'city': city_list})

class CountyView(View):
    """
    获取县
    """
    def get(self, requset, pid):
        countys = AreaInfo.objects.filter(Parent=pid)
        county_list = []
        for county in countys:
            county_list.append([county.id, county.title])
        return JsonResponse({'coun': county_list})


class UserInfoView(View):
    """
    我的设置 - 个人信息页面
    """
    def get(self, request, info_type):
        if info_type == 'info':
            city_id = request.user.city_addr
            coun = AreaInfo.objects.filter(id=int(city_id))
            user_coun = coun.values('title', 'Parent')[0]
            city = AreaInfo.objects.filter(id=user_coun['Parent'])
            user_city = city.values('title', 'Parent')[0]
            prov = AreaInfo.objects.filter(id=user_city['Parent'])
            user_prov = prov.values('title')[0]

            return render(request, 'users/my_info.html', {
                'user_prov': user_prov['title'],
                'user_city': user_city['title'],
                'user_coun': user_coun['title'],

                'info_type': 'info',
            })

        elif info_type == 'head':
            return render(request, 'users/my_head.html', {
                'info_type': 'head',
            })

        elif info_type == 'contact':
            user_all_contact = TheContact.objects.filter(user=request.user).order_by('-is_default', '-id')
            alreadycount = user_all_contact.count()
            remainingcount = 10 - user_all_contact.count()
            all_contacts = []
            for contact in user_all_contact:
                cont = {}
                cont['id'] = contact.id
                cont['name'] = contact.name

                city_id = contact.city_addr
                coun = AreaInfo.objects.filter(id=int(city_id))
                coutact_coun = coun.values('title', 'Parent')[0]
                city = AreaInfo.objects.filter(id=coutact_coun['Parent'])
                coutact_city = city.values('title', 'Parent')[0]
                prov = AreaInfo.objects.filter(id=coutact_city['Parent'])
                coutact_prov = prov.values('title')[0]

                cont['city'] = coutact_prov['title'] + ' ' + coutact_city['title'] + ' ' + coutact_coun['title']
                cont['address'] = contact.address
                cont['zip_code'] = contact.zip_code
                cont['mobile'] = contact.mobile
                cont['is_default'] = contact.is_default
                all_contacts.append(cont)

            return render(request, 'users/my_contact.html', {
                'all_contacts': all_contacts,
                'alreadycount': alreadycount,
                'remainingcount': remainingcount,
                'info_type': 'contact',
            })
        else:
            return render(request, 'users/security.html', {
                'info_type': 'security',
            })


class SettingInfoView(View):
    """
    修改个人信息
    """
