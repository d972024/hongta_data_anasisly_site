from django.core import validators
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class TechnologyValidator(validators.RegexValidator):
    regex = r'^[0-9]{8}'
    message = _(
        '员工编号必须由8位数字字符组成！'
    )
    flags = 0

@deconstructible
class MobileValidator(validators.RegexValidator):
    regex = r'^(13[0-9]|14[01456879]|15[0-35-9]|16[2567]|17[0-8]|18[0-9]|19[0-35-9])\d{8}$'
    message = _(
        '手机号应由[13 14 15 16 17 18 19]开头组成的11位数字字符组成！'
    )
    flags = 0
