from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from services.base.models import TimeStampModel


class UserManager(BaseUserManager):
    """Custom user manager for User model with an email as a username"""

    use_in_migrations = True

    def _create_user(self, email: str, password: str, **extra_fields):
        if not email:
            raise ValueError("The given value must be set")
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email: str, password: str, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email: str, password: str, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser, TimeStampModel):
    """Model for users"""

    class Genders(models.TextChoices):
        FEMALE = "female", "Женский"
        MALE = "male", "Мужской"

    username = models.CharField(
        max_length=150, unique=True, verbose_name="Имя пользователя"
    )
    email = models.EmailField(
        max_length=254, verbose_name="Email", unique=True
    )
    first_name = models.CharField(
        max_length=30, verbose_name="Имя", blank=True, null=True
    )
    last_name = models.CharField(
        max_length=30, verbose_name="Фамилия", blank=True, null=True
    )
    gender = models.CharField(
        max_length=10, choices=Genders.choices, verbose_name="Пол", blank=True, null=True
    )
    profile_picture = models.ImageField(
        upload_to='profile_pics/', verbose_name="Фото профиля", blank=True, null=True
    )
    date_of_birth = models.DateField(verbose_name="Дата рождения", blank=True, null=True)
    country = models.ForeignKey('countries.Country', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Страна проживания")
    website = models.URLField(max_length=200, blank=True, null=True, verbose_name="Сайт")
    phone_number = models.CharField(max_length=15, blank=True, null=True, verbose_name="Телефонный номер")
    travel_preferences = models.TextField(blank=True, null=True, verbose_name="Предпочтения в путешествиях")
    languages_spoken = models.CharField(max_length=100, blank=True, null=True, verbose_name="Языки")
    followers_count = models.PositiveIntegerField(default=0, verbose_name="Количество подписчиков")
    notifications_enabled = models.BooleanField(default=True, verbose_name="Включены уведомления")
    bblocked_users = models.ManyToManyField(
        'self',
        symmetrical=False,
        blank=True,
        verbose_name="Заблокированные пользователи",
        related_name='blocked_by'
    )

    subscribed_users = models.ManyToManyField(
        'self',
        symmetrical=False,
        blank=True,
        verbose_name="Подписанные пользователи",
        related_name='subscribers'  # Для подписанных пользователей
    )

    subscribed_countries = models.ManyToManyField(
        'countries.Country',
        blank=True,
        verbose_name="Подписанные страны",
        related_name='subscribed_users'  # Уникальное имя для подписанных стран
    )

    subscribed_tags = models.ManyToManyField(
        'posts.Tag',  # Убедитесь, что вы правильно указали путь к модели Tag
        blank=True,
        verbose_name="Подписанные теги",
        related_name='subscribed_users'  # Уникальное имя для подписанных тегов
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = UserManager()

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"

    def __str__(self) -> str:
        return self.email
