import re

from django import forms
from django.contrib.auth import forms as auth_form, password_validation
from django.contrib.auth.forms import UsernameField, AuthenticationForm, PasswordChangeForm
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from common.forms.utils import PrettyErrotList
from identity.custom_validators.user import MobileValidator, TechnologyValidator
from identity.models import User


class RegisterForm(auth_form.UserCreationForm):
    department = forms.CharField(
        label=_("Department"),
        strip=False,
        widget=forms.TextInput(attrs={'class': "form-control",
                                      'placeholder': _('所在部门'), }),
    )
    first_name = forms.CharField(
        label=_("first_name"),
        strip=False,
        max_length=2,
        widget=forms.TextInput(attrs={'class': "form-control",
                                      'placeholder': _('姓氏'), }),
    )
    last_name = forms.CharField(
        label=_("last_name"),
        strip=False,
        min_length=1,
        max_length=2,
        widget=forms.TextInput(attrs={'class': "form-control",
                                      'placeholder': _('名字'), }),
    )
    email = forms.EmailField(
        label=_("email"),
        widget=forms.EmailInput(attrs={'class': "form-control",
                                       'placeholder': _('电子邮箱'), }),
    )
    technology = forms.CharField(
        label=_("Technology"),
        strip=False,
        widget=forms.TextInput(attrs={'class': "form-control",
                                      'placeholder': _('员工编号'), }),
    )
    mobile = forms.CharField(
        label=_("Mobile"),
        strip=False,
        widget=forms.TextInput(attrs={'class': "form-control",
                                      'placeholder': _('手机号'), }),
    )
    jobs = forms.CharField(
        label=_("Jobs"),
        strip=False,
        min_length=2,
        widget=forms.TextInput(attrs={'class': "form-control",
                                      'placeholder': _('岗位'), }),
    )
    """
    在父类UserCreationForm中,username字段是爷类ModelForm默认定义的字段,要吧直接使用widgets的attrs来定义html元素的属性及值;
    但在这里我们使用的UserCreationForm中password1和password2字段是在UserCreationForm层面定义的widgets的attrs属性不适用于两字段,
    所以使用以下方法对其进行定义html元素属性.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # 序列化父类(super()跳转到调用者)的所有方法和属性
        self.fields['password1'].widget.attrs.update({'class': "form-control", 'placeholder': _('Password'), })
        self.fields['password2'].widget.attrs.update(
            {'class': "form-control", 'placeholder': _('Password confirmation'), })

    class Meta:
        model = User
        fields = ("username",)
        field_classes = {'username': UsernameField}
        widgets = {
            'username': forms.TextInput(attrs={
                'class': "form-control",
                'placeholder': _('username'),
            })}

    def clean_department(self):
        department = self.cleaned_data.get("department")
        if len(department) < 4 | (not re.search(r'[科|室|车间]', department)):
            raise ValidationError(
                '部门名称少于4个字符或名称不规范.',
                code='部门无效',
            )
        return department

    def clean_technology(self):
        technology = self.cleaned_data.get("technology")
        if len(technology) < 8 | (not re.search(r'^0\d{7}', technology)):
            raise ValidationError(
                '员工号必须以0开头的8位数字.',
                code='员工号无效',
            )
        if User.objects.filter(technology=technology):
            raise ValidationError(
                '该员工号已注册过账户.',
                code='员工号无效',
            )
        return technology



    def clean_mobile(self):
        mobile = self.cleaned_data.get("mobile")
        if not re.search(
                r'^[1](([3][0-9])|([4][5-9])|([5][0-3,5-9])|([6][5,6])|([7][0-8])|([8][0-9])|([9][1,8,9]))[0-9]{8}$',
                mobile):
            raise ValidationError(
                '手机号输入不正确.',
                code='手机号无效',
            )
        if User.objects.filter(mobile=mobile):
            raise ValidationError(
                '该手机号已注册过账户.',
                code='员工号无效',
            )
        return mobile

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.department = self.cleaned_data['department']
        user.technology = self.cleaned_data['technology']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.mobile = self.cleaned_data['mobile']
        user.jobs = self.cleaned_data['jobs']
        if commit:
            user.save()
        return user



class CustomLoginForm(AuthenticationForm):

    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True,
                                                           'class': "form-control",
                                                           'placeholder': _('Username'),}))
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password',
                                          'class': "form-control",
                                          'placeholder': _('Password'),}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix=''


class CustomPasswordChangeForm(PasswordChangeForm):

    old_password = forms.CharField(
        label=_("Old password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'autofocus': True,
                                          'class': "form-control",
                                          'placeholder': _('Old password'),
                                          }),
    )
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password',
                                          'class': "form-control",
                                          'placeholder': _('New password'),
                                          }),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password',
                                          'class': "form-control",
                                          'placeholder': _('New password confirmation'),
                                          }),
    )

    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)
        self.label_suffix=''