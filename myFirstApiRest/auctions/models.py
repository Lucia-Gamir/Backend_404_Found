from django.db import models
from users.models import CustomUser 
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta

# Create your models here.
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=50, blank=False, unique=True)
    
    class Meta:
        ordering=('id',)
    
    def __str__(self):
        return self.name


class Auction(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.DecimalField(max_digits=3, decimal_places=2)
    stock = models.IntegerField()
    brand = models.CharField(max_length=100)
    category = models.ForeignKey(Category, related_name='auctions', on_delete=models.CASCADE)
    thumbnail = models.URLField()
    creation_date = models.DateTimeField(auto_now_add=True)
    closing_date = models.DateTimeField()
    auctioneer = models.ForeignKey(CustomUser, related_name='auctions', on_delete=models.CASCADE) 
    
    class Meta:
        ordering=('id',)
    
    def __str__(self):
        return self.title

    def clean(self):
        errors = {}

        if self.price <= 0:
            errors['price'] = "El precio debe ser un número positivo."

        if self.stock <= 0:
            errors['stock'] = "El stock debe ser un número natural positivo."

        if not (1 <= self.rating <= 5):
            errors['rating'] = "La valoración debe estar entre 1 y 5."

        now = self.creation_date or timezone.now()
        if self.closing_date <= now:
            errors['closing_date'] = "La fecha de cierre debe ser posterior a la fecha de creación."
        elif self.closing_date < now + timedelta(days=15):
            errors['closing_date'] = "La subasta debe durar al menos 15 días desde su creación."

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class Bid(models.Model):
    auction = models.ForeignKey(Auction, related_name='bids', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    creation_date = models.DateTimeField(auto_now_add=True)
    bidder = models.ForeignKey(CustomUser, related_name='bids', on_delete=models.CASCADE)
    
    class Meta:
        ordering = ('id',)

    def get_bidder_username(self, obj):
        return obj.bidder.username
    
    def __str__(self):
        return f"Id: {self.id}, Auction: {self.auction.title}, Bidder: {self.bidder.username}"