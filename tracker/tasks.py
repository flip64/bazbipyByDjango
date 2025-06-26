from celery import shared_task
from tracker.utils.feach_price import check_price_changes

@shared_task
def periodic_price_check():
    
    """تسک دوره‌ای برای بررسی قیمت‌ها"""
    print("ok")
    return check_price_changes()