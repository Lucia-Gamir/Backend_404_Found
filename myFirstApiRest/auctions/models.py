from django.db import models
from users.models import CustomUser 
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
from django.db.models import Avg
from django.core.validators import MinValueValidator, MaxValueValidator

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
    stock = models.IntegerField()
    brand = models.CharField(max_length=100)
    category = models.ForeignKey(Category, related_name='auctions', on_delete=models.CASCADE)
    image = models.ImageField(upload_to="images", default='images/default.webp')
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

        now = self.creation_date or timezone.now()
        if self.closing_date <= now:
            errors['closing_date'] = "La fecha de cierre debe ser posterior a la fecha de creación."
        elif self.closing_date < now + timedelta(days=15):
            errors['closing_date'] = "La subasta debe durar al menos 15 días desde su creación."

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        creating = self.pk is None
        self.full_clean()
        super().save(*args, **kwargs)
        from ratings.models import Rating
        if creating:
            Rating.objects.create(
                auction=self,
                user=self.auctioneer,
                value=1
            )

    @property
    def rating(self):
        if self.pk:
            return self.ratings.aggregate(avg=Avg('value'))['avg'] or 0


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
    

class Comment(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    auction = models.ForeignKey('Auction', on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return f"{self.title} - {self.user.username}"
    

class Rating(models.Model):
    value = models.IntegerField(
        default=1,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )
    user = models.ForeignKey(CustomUser, related_name='ratings', on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, related_name='ratings', on_delete=models.CASCADE)
        
    class Meta:
        ordering=('id',)
    
    def __str__(self):
        return self.value