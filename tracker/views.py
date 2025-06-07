from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import WatchedURL
import json

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
