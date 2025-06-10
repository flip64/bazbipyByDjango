from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import WatchedURL, PriceHistory
from .forms import WatchedURLForm
from django.contrib.auth.decorators import login_required
from tracker.feach_price import fetch_product_details
from django.utils import timezone

import re
import json


@login_required
def watched_urls_view(request):
    user = request.user
    if request.method == 'POST':
        form = WatchedURLForm(request.POST, user=user)  # پاس دادن user به فرم
        if form.is_valid():
            watched_url = form.save(commit=False)
            watched_url.user = user

            product_name, product_price_text = fetch_product_details(watched_url.url)
            if product_name:
                watched_url.product_name = product_name

            cleaned_price = clean_price_text(product_price_text)
            if cleaned_price is not None:
                watched_url.last_price = cleaned_price
                watched_url.last_checked = timezone.now()  # این خط رو اضافه کن


            watched_url.save()

            # ذخیره در تاریخچه قیمت
            if cleaned_price is not None:
                PriceHistory.objects.create(
                    watched_url=watched_url,
                    price=cleaned_price
                )

            return redirect('watched_urls')
    else:
        form = WatchedURLForm(user=user)  # پاس دادن user به فرم

    urls = WatchedURL.objects.filter(user=user).order_by('-created_at')
    for watched_url in urls:
        print(watched_url.product_name)

    return render(request, 'tracker/watched_urls.html', {'form': form, 'urls': urls})


def clean_price_text(price_text):
    """
    تبدیل قیمت مثل "850,000 ریال" به 850000 (عدد صحیح بزرگ)
    """
    if not price_text:
        return None
    cleaned = re.sub(r'[^\d]', '', price_text)
    return int(cleaned) if cleaned.isdigit() else None


@csrf_exempt
def check_price(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        url = data.get('url')
        new_price = data.get('price')  # فرضاً فرانت اینو می‌فرسته

        try:
            # اگر می‌خوای بررسی کاربر هم باشه باید user رو از request بدست بیاری (اگر احراز هویت هست)
            watched = WatchedURL.objects.get(url=url)
            if watched.last_price != new_price:
                watched.last_price = new_price
                watched.save()
                return JsonResponse({'changed': True})
            return JsonResponse({'changed': False})
        except WatchedURL.DoesNotExist:
            return JsonResponse({'error': 'URL not found'}, status=404)

    return JsonResponse({'error': 'Invalid method'}, status=405)
