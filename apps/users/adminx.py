import xadmin
from .models import *
from xadmin import views


class UsersAdmin:
    """
    用户后台管理
    """
    list_display = ['username', 'email', 'portrait', 'integral', 'is_superuser', 'last_login']
    list_filter = ['username', 'email', 'is_superuser']
    search_fields = ['username', 'email', 'is_superuser']
    fields = ['username', 'email', 'portrait', 'integral', 'last_login']
    readonly_fields = ['portrait', 'last_login']
    style_fields = {'content': 'ueditor'}


# class GlobalSettings:
#     site_title = '小熊后台管理系统'      # 标题
#     site_footer = 'xiaoxiong Travel'     # 页脚
#     menu_style = 'accordion'         # 菜单栏样式 折叠
#
#
# class BaseSetting:
#     enable_themes = True             # 开启主题选项
#     use_bootswatch = True
#
#
xadmin.site.unregister(Myuser)
xadmin.site.register(Myuser, UsersAdmin)
# xadmin.site.register(views.CommAdminView, GlobalSettings)
# xadmin.site.register(views.BaseAdminView, BaseSetting)
