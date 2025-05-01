from django.db import models
from users.models import CustomUser 
from auctions.models import Auction
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
from django.db import models

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