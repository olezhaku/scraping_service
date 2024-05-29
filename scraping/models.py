from django.db import models
from scraping.utils import from_cyrillic_to_eng


def default_urls():
    return {"rabota": "", "superjob": "", "remotejob": "", "careerjet": ""}


class City(models.Model):
    name = models.CharField(max_length=50, verbose_name="Город", unique=True)
    slug = models.CharField(max_length=50, blank=True, unique=True)

    class Meta:
        verbose_name = "Город"
        verbose_name_plural = "Городa"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = from_cyrillic_to_eng(self.name)
        super().save(*args, **kwargs)


class Language(models.Model):
    name = models.CharField(
        max_length=50, verbose_name="Язык программирования", unique=True
    )
    slug = models.CharField(max_length=50, blank=True, unique=True)

    class Meta:
        verbose_name = "Язык программирования"
        verbose_name_plural = "Языки программирования"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = from_cyrillic_to_eng(self.name)
        super().save(*args, **kwargs)


class Vacancy(models.Model):
    url = models.URLField(unique=True)
    title = models.CharField(max_length=250, verbose_name="Заголовок")
    company = models.CharField(max_length=250, verbose_name="Компания")
    description = models.TextField(verbose_name="Описание")
    city = models.ForeignKey("City", on_delete=models.CASCADE, verbose_name="Город")
    language = models.ForeignKey(
        "Language", on_delete=models.CASCADE, verbose_name="Язык программирования"
    )
    timestamp = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = "Вакансия"
        verbose_name_plural = "Вакансии"
        ordering = ["-timestamp"]

    def __str__(self):
        return self.title


class Error(models.Model):
    timestamp = models.DateField(auto_now_add=True)
    data = models.JSONField()


class Url(models.Model):
    city = models.ForeignKey("City", on_delete=models.CASCADE, verbose_name="Город")
    language = models.ForeignKey(
        "Language", on_delete=models.CASCADE, verbose_name="Язык программирования"
    )
    url_data = models.JSONField(default=default_urls)

    class Meta:
        unique_together = ("city", "language")
