import uuid
from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    face_image = models.ImageField(upload_to='images/users/faces/', null=True, blank=True, verbose_name='アイコン画像')
    nickname = models.CharField(max_length=30, verbose_name='ユーザ名（和名）')

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname']

    def __str__(self):
        return f'{self.nickname}'


class Character(models.Model):
    class Meta:
        db_table = 'character'
        ordering = ['created_at']
        verbose_name = verbose_name_plural = 'キャラクター'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    users = models.ManyToManyField(get_user_model(), blank=True)
    slug = models.SlugField(max_length=20, unique=True, verbose_name='URLスラッグ')
    image = models.ImageField(upload_to='images/characters/', blank=True, null=True, verbose_name='キャラクター画像')
    name = models.CharField(max_length=50, verbose_name='キャラクター名')	# 文字列
    world = models.CharField(max_length=20, verbose_name='所属ワールド')	# 文字列
    how_to_get = models.CharField(max_length=20, default='premium', choices=[('happiness', 'ハピネスBOX'), ('premium', 'プレミアムBOX')], verbose_name='獲得方法')
    description = models.CharField(max_length=100, verbose_name='説明文')	# 文字列
    created_at = models.DateTimeField(auto_now_add=True)	# 日付、デフォルト現在日
    updated_at = models.DateTimeField(auto_now=True)	# 日付、デフォルト現在日

    def __str__(self):
        return f'{self.name}/{self.name}'