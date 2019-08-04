from django.db import models
from django.conf import settings

CATEGORY_CHOICES = (
    ('music', '음악'),
    ('clothing', '의류'),
    ('media', '영상')
)

# Create your models here.
interestChoice = (
    ('FAHION', '패션'),
    ('MEDIA', '미디어'),
    ('FOOD', '음식'),
    ('ETC', '기타'),
)


class Service(models.Model):
    company = models.CharField(max_length=50)
    service_name = models.CharField(max_length=50)
    price = models.IntegerField()
    link = models.CharField(max_length=500)
    description = models.TextField(null=True, blank=True)

    full_name = models.OneToOneField(
      'self', on_delete=models.CASCADE, null=True, blank=True)
   # category = models.CharField(choices=CATEGORY_CHOICES, max_length=50)
   # logo_image = models.FileField()

    def get_price(self):
        return format(self.price, ',')

    def __str__(self):
        return f"{self.company} {self.service_name} (+{self.price}원)"


class GuDogService(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    
    zzim_service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name="zzim_service",
        null=True,
        blank=True,
    )
    register_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        if self.service:
            return f"{self.user} {self.service.service_name}"
        else:
            return f"{self.user} 찜 {self.zzim_service.service_name}"
        


class GuDog(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    services = models.ManyToManyField(GuDogService)
    def __str__(self):
        return self.user.username
