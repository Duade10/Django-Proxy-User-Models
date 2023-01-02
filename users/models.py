from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    class Types(models.TextChoices):
        SPY = "SPY", "Spy"
        DRIVER = "DRIVER", "Driver"

    type = models.CharField(_("Type"), max_length=50, choices=Types.choices, default=Types.SPY)
    name = models.CharField(_("Name of User"), max_length=100, blank=True, null=True)

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"pk": self.pk})


class SpyManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs).filter(type=User.Types.SPY)
        return queryset


class Spy(User):
    objects = SpyManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = User.Types.SPY
        return super().save(*args, **kwargs)


class DriverManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs).filter(type=User.Types.DRIVER)
        return queryset


class DriverMore(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    model = models.CharField(max_length=255)
    make = models.CharField(max_length=255)
    year = models.IntegerField()


class Driver(User):
    objects = DriverManager()

    @property
    def more(self):
        return self.drivermore

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = User.Types.DRIVER
        return super().save(*args, **kwargs)
