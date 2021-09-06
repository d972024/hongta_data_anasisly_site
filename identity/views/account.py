from django.contrib.auth.views import LoginView, PasswordChangeView
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.utils.translation import gettext as _
from common.forms.utils import PrettyErrotList
from identity.forms.account import RegisterForm, CustomLoginForm, CustomPasswordChangeForm
from identity.models import User


class Register(CreateView):
    model=User
    form_class=RegisterForm
    template_name = 'account/register.html'
    success_url='/identity/login/'
    def get_form_kwargs(self):
        kwargs=super().get_form_kwargs()
        kwargs['error_class']=PrettyErrotList
        return kwargs

class CustomLoginView(LoginView):
    template_name = 'account/login.html'
    form_class=CustomLoginForm
    redirect_authenticated_user=True    # 用户在登陆状态时重定向
    success_url='/'
    def get_form_kwargs(self):
        kwargs=super().get_form_kwargs()
        kwargs['error_class']=PrettyErrotList
        return kwargs


class CustomPasswordChangeView(PasswordChangeView):
    form_class = CustomPasswordChangeForm
    success_url = reverse_lazy('identity:login')
    template_name = 'account/passwordchange.html'
    title = _('Password change')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['error_class'] = PrettyErrotList
        return kwargs