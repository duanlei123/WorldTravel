from django.shortcuts import render

# Create your views here.

from django.shortcuts import render,render_to_response
from django.views.generic import View
from .models import *


class NewsView(View):
    """
    新闻列表
    """
    def get(self, request):
        # 以添加时间倒序获取所有新闻
        all_news = News.objects.all().order_by('-add_times')
        # 获取request新闻分类
        news_type = request.GET.get('classification', '')
        if news_type:
            # 如果classication存在, 根据分类过滤出新闻
            all_news = all_news.filter(classification=news_type)

        public_box = get_public_box()
        return render(request, 'news/news_list.html', {
            'all_news': all_news,
            'classification': news_type,
            'culture': public_box.get('culture'),
            'specialty': public_box.get('specialty'),
            'food': public_box.get('food'),
            'life': public_box.get('life'),
            'now_type': 'news',
        })


class NewsDetails(View):
    """
    新闻详情页
    """
    def get(self, request, news_id):
        public_box = get_public_box()
        # 根据新闻id获取新闻info
        news = News.objects.get(id=(int(news_id)))
        # 阅读数量+1, 并更新数据
        news.checknum += 1
        news.save()
        return render(request, 'news/article.html', {
            'news': news,
            'culture': public_box.get('culture'),
            'specialty': public_box.get('specialty'),
            'food': public_box.get('food'),
            'life': public_box.get('life'),
            'now_type': 'news',
        })


def get_public_box():
    all_news = News.objects.all().order_by('-add_times')
    culture = all_news.filter(classification='culture')[:3]
    specialty = all_news.filter(classification='specialty')[:3]
    food = all_news.filter(classification='food')[:3]
    life = all_news.filter(classification='life')[:3]

    public_box = {
        'culture': culture,
        'specialty': specialty,
        'food': food,
        'life': life,
    }

    return public_box