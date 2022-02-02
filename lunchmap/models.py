from django.db import models
from django.contrib.auth.models import User
from myapp import settings
from django.urls import reverse


SCORE_CHOICES = [
    (1, '★'),
    (2, '★★'),
    (3, '★★★'),
    (4, '★★★★'),
    (5, '★★★★★'),
]

SPEED = [
    (1, '★'),
    (2, '★★'),
    (3, '★★★'),
    (4, '★★★★'),
    (5, '★★★★★'),
]
LENGTH = [
    (3, '3'),
    (4, '4'),
    (5, '5'),
    (6, '6'),
    (7, '7'),
    (8, '8'),
    (9, '9'),
    (10, '10'),
    (15, '15'),
    (20, '20以上'),
]

YESNO = [
    ('あり', 'あり'),
    ('渋い', '渋い'),
    ('なし', 'なし'),
]

class Category(models.Model):
  name = models.CharField(verbose_name='カテゴリー', max_length=255)
  author = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
  )
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.name

class Shop(models.Model):
    name = models.CharField(verbose_name='店名', max_length=255)
    address = models.CharField(verbose_name='住所', max_length=255)
    favorite_menu = models.CharField(verbose_name='おすすめメニュー', max_length=255)
    in_camp = models.CharField(verbose_name='合宿のお昼におすすめか', max_length=255,choices=YESNO)
    length = models.PositiveSmallIntegerField(verbose_name='ハコから何分',default='3',choices=LENGTH)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        verbose_name='カテゴリー',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('lunchmap:detail', kwargs={'pk': self.pk})

class Review(models.Model):
    shop = models.ForeignKey(
        Shop,
        on_delete=models.CASCADE,
        related_name='review')
    title = models.CharField(verbose_name='タイトル', max_length=100)
    review = models.TextField(verbose_name='レビュー', max_length=255)
    score = models.PositiveSmallIntegerField(verbose_name='レビュースコア', choices=SCORE_CHOICES, default='3')
    speed = models.PositiveSmallIntegerField(verbose_name='提供スピード', choices=SCORE_CHOICES, default='3')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)

    class Meta:
        unique_together = ('shop', 'user')
 
    def __str__(self):
        return self.review

    def get_percent(self):
        percent = round(self.score / 5 * 100)
        return percent
