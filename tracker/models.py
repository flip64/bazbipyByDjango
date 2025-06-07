from django.db import models
from django.contrib.auth.models import User


class WatchedURL(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    url = models.URLField()
    last_checked = models.DateTimeField(null=True, blank=True)
    last_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.url



class PriceHistory(models.Model):
    watched_url = models.ForeignKey(WatchedURL, on_delete=models.CASCADE, related_name='history')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    checked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.price} at {self.checked_at}"
