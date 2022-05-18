import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

class UserManager(BaseUserManager):
    def create_user(self, email, nickname, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Eメールアドレスが入力されていないよ')
        if not nickname:
            raise ValueError('ニックネームが入力されていないよ')
        user = self.model(
            email=self.normalize_email(email),
            nickname=nickname,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nickname, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            nickname=nickname,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    class Meta:
        db_table = 'user'
        ordering = ['created_at']
        verbose_name = verbose_name_plural = 'ユーザ'

    email = models.EmailField(
        verbose_name='Eメールアドレス',
        max_length=255,
        unique=True,
    )
    nickname = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)	# 日付、デフォルト現在日
    updated_at = models.DateTimeField(auto_now=True)	# 日付、デフォルト現在日

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


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