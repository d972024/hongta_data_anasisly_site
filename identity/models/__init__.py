"""
在一个包中管理模型¶
manage.py startapp 命令创建了一个应用结构，包含一个 models.py 文件。若你有很多 models.py 文件，用独立的文件管理它们会很实用。
为了达到此目的，创建一个 models 包。删除 models.py，创建一个 myapp/models 目录，包含一个 __init__.py 文件和存储模型的文件。
你必须在 __init__.py 文件中导入这些模块。
比如，若你在 models 目录下有 organic.py 和 synthetic.py：
myapp/models/__init__.py¶
from .organic import Person
from .synthetic import Robot
显式导入每个模块，而不是使用 from .models import * 有助于不打乱命名空间，使代码更具可读性，让代码分析工具更有用。
参见
这里使用*来代表对应model中使用__all__定义的变量
"""

from .account import *
