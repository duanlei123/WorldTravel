import json

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views import View

from news.views import get_public_box
from scenicspots.models import Spots, Active


class ScenicListView(View):
    """
    景区列表
    """
    def get(self, request):
        list_type = request.GET.get('list_type', '')
        public_box = get_public_box()
        if list_type == 'scenic':
            all_spots = Spots.objects.all().order_by('-add_times')
        elif list_type == 'active':
            all_spots = Active.objects.all().order_by('go_time')
        else:
            result = json.dumps({"status": "failed", "msg": "来源错误"}, ensure_ascii=False)
            return HttpResponse(result)
        return render(request, 'scenicspots/scenic_list.html', {
                    'all_spots': all_spots,
                    'culture': public_box.get('culture'),
                    'specialty': public_box.get('specialty'),
                    'food': public_box.get('food'),
                    'life': public_box.get('life'),
                    'now_type': 'scenic',
                    'list_type': list_type,
                })


class ScenicDetails(View):
    """
    旅游景区详情
    """
    def get(self, request, scenic_id):
        scenic = Spots.objects.get(id=int(scenic_id))
        gallerys = scenic.gallery_set.all()
        # products = Product.objects.all().order_by('-buyers')[:6]
        # comments = SpotsComments.objects.filter(spots=scenic)
        return render(request, 'scenicspots/scenic.html', {
            'scenic': scenic,
            'gallerys': gallerys,
            'now_type': 'scenic',
            # 'products': products,
            # 'comments': comments,
        })


class ActiveDetails(View):
    """
    旅游活动详情
    """
    def get(self, request, active_id):
        active = Active.objects.get(id=int(active_id))
        other_actives = Active.objects.all().order_by('-add_time')[:5]
        # comments = ActiveComments.objects.filter(active=active)
        return render(request, 'scenicspots/activities.html', {
            'now_type': 'scenic',
            'active': active,
            'other_actives': other_actives,
            # 'comments': comments,
        })