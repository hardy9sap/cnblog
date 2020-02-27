import re
from django import forms
from django.core.exceptions import ValidationError
from .models import UserInfo
from .models import Blog


class UserForm(forms.Form):
    # 一层校验
    email = forms.CharField(label='邮&nbsp;箱')
    tel = forms.CharField(min_length=11, max_length=11, label='手机号码')
    loginname = forms.CharField(min_length=4, label='登录名称')
    nickname = forms.CharField(min_length=2, label='显示名称')
    pwd = forms.CharField(min_length=8, label='密&nbsp;码')
    confirmpwd = forms.CharField(min_length=8, label='确认密码')

    @staticmethod
    def check_char(char_string):
        # 1. 判断是否含有特殊字符
        if not char_string.isalnum():  # not False --> 表示含有
            print('有特殊字符')
            # 2. 判断是否含有字母
            char_string = char_string.lower()
            if char_string.islower():  # True --> 表示含有
                print('有字母')
                ret = re.search(pattern=r'\d{1,}', string=char_string)
                if ret:  # 说明有数字
                    print('有数字')
                    return True
        return False

    def clean_email(self):
        email = self.cleaned_data.get('email')
        res = re.fullmatch(pattern=r'\w[-\w.+]*@([A-Za-z0-9][-A-Za-z0-9]+\.)+[A-Za-z]{2,14}', string=email)
        if res:
            status = UserInfo.objects.all().filter(email=email).exists()
            if not status:
                return email
            else:
                raise ValidationError(message='邮箱已存在')
        else:
            raise ValidationError(message='邮箱格式错误')

    def clean_tel(self):
        tel = self.cleaned_data.get('tel')
        if tel.isdigit():
            status = UserInfo.objects.all().filter(telephone=tel).exists()
            if not status:
                return tel
            else:
                raise ValidationError(message='号码已存在')
        else:
            raise ValidationError(message='手机号码必须为纯数字')

    def clean_pwd(self):
        pwd = self.cleaned_data.get('pwd')
        status = self.check_char(char_string=pwd)
        if status:
            return pwd
        else:
            raise ValidationError(message='密码必须包含字母、数字、特殊字符')

    def clean_confirmpwd(self):
        confirmpwd = self.cleaned_data.get('confirmpwd')
        status = self.check_char(char_string=confirmpwd)
        if status:
            return confirmpwd
        else:
            raise ValidationError(message='密码必须包含字母、数字、特殊字符')

    def clean_loginname(self):
        """
        局部钩子，验证登录用户名是否存在
        :return:
        """
        loginname = self.cleaned_data.get('loginname')
        status = UserInfo.objects.all().filter(username=loginname).exists()
        if not status:
            return loginname
        else:
            raise ValidationError('该用户已存在')

    def clean_nickname(self):
        """
        局部钩子，验证显示名称是否存在
        :return:
        """
        nickname = self.cleaned_data.get('nickname')
        status = Blog.objects.all().filter(title=nickname).exists()
        if not status:
            return nickname
        else:
            raise ValidationError('该名称已存在')

    def clean(self):
        """
        全局钩子，验证pwd和confirmpwd是否一致
        :return:
        """
        pwd = self.cleaned_data.get('pwd')
        confirmpwd = self.cleaned_data.get('confirmpwd')
        if pwd and confirmpwd:
            if pwd == confirmpwd:
                return self.cleaned_data
            else:
                raise ValidationError('两次密码不一致')
        else:
            return self.cleaned_data


