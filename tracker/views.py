from django.shortcuts import render ,redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import WatchedURL
import json
from .models import WatchedURL
from .forms import WatchedURLForm
from django.contrib.auth.decorators import login_required
from tracker.feach_price import fetch_product_details
@login_required
def watched_urls_view(request):
    user = request.user
    if request.method == 'POST':
        form = WatchedURLForm(request.POST)
        if form.is_valid():
            watched_url = form.save(commit=False)
            watched_url.user = user
            product_name , product_price  = fetch_product_details(watched_url.url)
            if product_name:
                watched_url.product_name = product_name
                
            
            watched_url.save()
            return redirect('watched_urls')  # نام مسیر را مطابق urls.py تنظیم کن
    else:
        form = WatchedURLForm()

    urls = WatchedURL.objects.filter(user=user).order_by('-created_at') 
    for watched_url in urls:
     print(watched_url.product_name)

    return render(request, 'tracker/watched_urls.html', {'form': form, 'urls': urls})









@csrf_exempt
def check_price(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        url = data.get('url')
        new_price = data.get('price')  # فرضاً فرانت اینو می‌فرسته

        try:
            watched = WatchedURL.objects.get(url=url)
            if watched.last_price != new_price:
                watched.last_price = new_price
                watched.save()
                return JsonResponse({'changed': True})
            return JsonResponse({'changed': False})
        except WatchedURL.DoesNotExist:
            return JsonResponse({'error': 'URL not found'}, status=404)

    return JsonResponse({'error': 'Invalid method'}, status=405)
