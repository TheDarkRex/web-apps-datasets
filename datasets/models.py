from django.db import models
from django.contrib.auth.models import User


class Dataset(models.Model):
    class SizeClass(models.TextChoices):
        SMALL = 'S', 'Mała'
        MEDIUM = 'M', 'Średnia'
        LARGE = 'L', 'Duża'
        VERY_LARGE = 'XL', 'Bardzo duża'

    name = models.CharField(max_length=255, verbose_name="Nazwa")
    author = models.CharField(max_length=255, verbose_name="Autorzy (osoba/instytucja)")
    topic = models.CharField(max_length=255, verbose_name="Tematyka")

    size_class = models.CharField(
        max_length=2,
        choices=SizeClass.choices,
        default=SizeClass.MEDIUM,
        verbose_name="Klasa wielkości"
    )

    link = models.URLField(verbose_name="Link do danych")

    description = models.TextField(max_length=2000, verbose_name="Opis")

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='datasets',
        verbose_name="Właściciel"
    )

    table_count = models.PositiveIntegerField(
        verbose_name="Skomplikowanie (liczba tabel)",
        default=1
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.get_size_class_display()})"

class DatasetSchema(models.Model):
    dataset = models.OneToOneField(
        Dataset,
        on_delete=models.CASCADE,
        related_name='schema',
        verbose_name="Baza danych"
    )

    image = models.ImageField(
        upload_to='schemas/images/',
        blank=True,
        null=True,
        verbose_name="Obraz schematu"
    )

    ddl_file = models.FileField(
        upload_to='schemas/ddl_files/',
        blank=True,
        null=True,
        verbose_name="Plik DDL"
    )

    def __str__(self):
        return f"Schemat dla: {self.dataset.name}"

class Query(models.Model):
    dataset = models.ForeignKey(
        Dataset,
        on_delete=models.CASCADE,
        related_name='queries',
        verbose_name="Baza danych"
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='queries',
        verbose_name="Autor zapytania"
    )
    content = models.TextField(verbose_name="Treść zapytania")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data dodania")

    def __str__(self):
        return f"Zapytanie od {self.author.username} do {self.dataset.name}"

class Answer(models.Model):
    query = models.ForeignKey(
        Query,
        on_delete=models.CASCADE,
        related_name='answers',
        verbose_name="Zapytanie"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='answers',
        verbose_name="Autor odpowiedzi"
    )
    content = models.TextField(verbose_name="Treść odpowiedzi")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data dodania")

    def __str__(self):
        return f"Odpowiedź od {self.author.username} (ID Zapytania: {self.query.id})"