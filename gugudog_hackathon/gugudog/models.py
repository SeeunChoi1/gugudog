from django.db import models
from django.conf import settings

CATEGORY_CHOICES = (
    ('music', '음악'),
    ('clothing', '의류'),
    ('media', '영상')
)

# Create your models here.
class Service(models.Model):
    company = models.CharField(max_length=50)
    service_name = models.CharField(max_length=50)
    price = models.IntegerField()
    link = models.CharField(max_length=500)
    
    full_name = models.OneToOneField('self', on_delete=models.CASCADE, null=True, blank=True)
    # category = models.CharField(choices=CATEGORY_CHOICES, max_length=50)
    # logo_image = models.FileField()

    def get_price(self):
        return format(self.price, ',')
   
    def __str__(self): 
        return self.company + " " + self.service_name + " (+" + str(self.price)  + "원)"

class GuDogService(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)

    register_date = models.DateField(null=True, blank=True)


    def __str__(self):
        return str(self.user) + " " + str(self.service)

class GuDog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    services = models.ManyToManyField(GuDogService)