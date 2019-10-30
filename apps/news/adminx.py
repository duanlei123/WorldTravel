import xadmin
from xadmin import views
from .models import *



class NewsAdmin:
    """
    新闻后台管理
    """
    list_display = ['title', 'checknum', 'classification', 'add_times']
    list_filter = ['checknum', 'classification', 'add_times']
    search_fields = ['title', 'checknum', 'classification', 'add_times']
    fields = ['title', 'content', 'image', 'checknum', 'classification', 'add_times']
    readonly_fields = ['checknum']
    style_fields = {'content': 'ueditor'}


class GlobalSettings:
    site_title = '小熊后台管理系统'      # 标题
    site_footer = 'xiaoxiong Travel'     # 页脚
    menu_style = 'accordion'         # 菜单栏样式 折叠


class BaseSetting:
    enable_themes = True             # 开启主题选项
    use_bootswatch = True


xadmin.site.register(News, NewsAdmin)
xadmin.site.register(views.CommAdminView, GlobalSettings)
xadmin.site.register(views.BaseAdminView, BaseSetting)
