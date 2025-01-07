import pathlib
from datetime import datetime
from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver


class Real(models.Model):

    @staticmethod
    def file_path(filename):
        file = pathlib.Path(filename)
        ext = file.suffix or ".pmg"
        path = datetime.strftime(datetime.now(), "real/%Y%m%d%H%M%S")
        return path + ext

    name = models.CharField(max_length=120, verbose_name="Название")
    is_active = models.BooleanField(default=False, verbose_name="Активная запись")
    is_vip = models.BooleanField(default=False, verbose_name="Лучшее предложение")
    photo = models.ImageField(upload_to=file_path, null=True, blank=True, verbose_name="Главное фото")
    VILLA = "V"
    APARTMENT = "A"
    SECTOR = "S"
    CHOOSES = [
        (VILLA, "Villa"), (APARTMENT, "Apartment"), (SECTOR, "Sector")]
    type = models.CharField(max_length=1, choices=CHOOSES, verbose_name="Тип объекта")
    location = models.CharField(max_length=50, null=True, blank=True, verbose_name="Координаты")
    address_ru = models.CharField(max_length=256, null=True, blank=True, verbose_name="Адрес_ру")
    address_en = models.CharField(max_length=256, null=True, blank=True, verbose_name="Адрес_en")
    mini_description_ru = models.CharField(max_length=256, null=True, blank=True, verbose_name="Краткое описание_ру")
    mini_description_en = models.CharField(max_length=256, null=True, blank=True, verbose_name="Краткое описание_en")
    description_ru = models.TextField(null=True, blank=True, verbose_name="Описание_ru")
    description_en = models.TextField(null=True, blank=True, verbose_name="Описание_en")
    price_ru = models.CharField(max_length=256, null=True, blank=True, verbose_name="Цена_ру")
    price_en = models.CharField(max_length=256, null=True, blank=True, verbose_name="Цена_en")
    area_ru = models.CharField(max_length=256, null=True, blank=True, verbose_name="Площадь_ру")
    area_en = models.CharField(max_length=256, null=True, blank=True, verbose_name="Площадь_en")
    date_ru = models.CharField(max_length=256, null=True, blank=True, verbose_name="Срок сдачи_ру")
    date_en = models.CharField(max_length=256, null=True, blank=True, verbose_name="Срок сдачи_en")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        storage, path = self.photo.storage, self.photo.path
        super(Real, self).delete(*args, **kwargs)
        storage.delete(path)

    class Meta:
        verbose_name_plural = "Объекты"


@receiver(pre_save, sender=Real)
def delete_previous_photo(sender, instance, **kwargs):
    if instance.pk:
        try:
            previous_instance = sender.get(pk=instance.pk)
            if previous_instance.photo != instance.photo:
                if previous_instance.photo:
                    previous_instance.photo.delete(save=False)
        except Real.DoesNotExist:
            pass


class RealPhoto(models.Model):

    @staticmethod
    def file_path(filename):
        file = pathlib.Path(filename)
        ext = file.suffix or ".pmg"
        path = datetime.strftime(datetime.now(), "real/%Y%m%d%H%M%S")
        return path + ext

    objects = models.ForeignKey(Real, on_delete=models.CASCADE, verbose_name="Объект")
    photo = models.ImageField(upload_to=file_path, verbose_name="дополнительное фото")

    def delete(self, *args, **kwargs):
        storage, path = self.photo.storage, self.photo.path
        super(RealPhoto, self).delete(*args, **kwargs)
        storage.delete(path)

    class Meta:
        verbose_name_plural = "Фото объектов"


@receiver(pre_save, sender=RealPhoto)
def delete_previous_photo(sender, instance, **kwargs):
    if instance.pk:
        try:
            previous_instance = sender.objects.get(pk=instance.pk)
            if previous_instance.photo != instance.photo:
                if previous_instance.photo:
                    previous_instance.photo.delete(save=False)
        except Real.DoesNotExist:
            pass


class Feedback(models.Model):

    name = models.CharField(max_length=128, null=True, blank=False, verbose_name="Имя")
    email = models.EmailField(null=True, blank=True, verbose_name="email")
    phoneNumberRegex = RegexValidator(radex=r"\+?1?\d{8,15}$")
    phone = models.CharField(validators=[phoneNumberRegex], max_length=20, null=True, blank=True, verbose_name="Телефон")
    objects = models.ForeignKey(Real, models.DO_NOTHING, null=True, blank=True, verbose_name="Объект")
    message = models.TextField(null=True, blank=False, verbose_name="Сообщение")
    NEW = "N"
    IN_PROGRESS = "W"
    PAUSE = "P"
    DONE = "D"
    CHOOSES = [(NEW, "New"), (IN_PROGRESS, "In Progress"), (PAUSE, "Pause"), (DONE, "Done")]
    status = models.CharField(max_length=1, choices=CHOOSES, default="N", verbose_name="Статус")
    staff = models.ForeignKey(User, models.DO_NOTHING, null=True, related_name="Ответственный")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Сообщение пользователя"


class InfoPost(models.Model):

    @staticmethod
    def file_path(filename):
        file = pathlib.Path(filename)
        ext = file.suffix or ".pmg"
        path = datetime.strftime(datetime.now(), "post/%Y%m%d%H%M%S")
        return path + ext

    title_en = models.CharField(max_length=128, null=True, blank=True, verbose_name="Тема Eng")
    post_en = models.TextField(null=True, blank=True, verbose_name="Описание Eng")
    title_ru = models.CharField(max_length=128, null=True, blank=True, verbose_name="Тема Ru")
    post_ru = models.TextField(null=True, blank=True, verbose_name="Описание Ru")
    title_pl = models.CharField(max_length=128, null=True, blank=True, verbose_name="Тема Pl")
    post_pl = models.TextField(null=True, blank=True, verbose_name="Описание Pl")
    is_active = models.BooleanField(default=False, verbose_name="Активная запись")
    photo = models.ImageField(upload_to=file_path, null=True, blank=True, verbose_name="Имя файла")

    def delete(self, *args, **kwargs):
        storage, path = self.photo.storage, self.photo.path
        super(InfoPost, self).delete(*args, **kwargs)
        storage.delete(path)

    class Meta:
        verbose_name_plural = "FAQ"


@receiver(pre_save, sender=InfoPost)
def delete_previous_photo(sender, instance, **kwargs):
    if instance.pk:
        try:
            previous_instance = sender.objects.get(pk=instance.pk)
            if previous_instance.photo != instance.photo:
                if previous_instance.photo:
                    previous_instance.photo.delete(save=False)
        except Real.DoesNotExist:
            pass

