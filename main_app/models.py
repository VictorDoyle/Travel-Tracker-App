from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify
# Create your models here.
from account.models import Account
# modify the urls/ slugs
from django.template.defaultfilters import slugify
from django.urls import reverse


# posts = models.ManyToManyField(Post, blank=True)
# cities = models.ManyToManyField(City)
# class FileType(paperclip.models.FileType):
#     pass

# class Attachment(paperclip.models.Attachment):
#     pass
# need to have profile avatar in post class so i can load all posts on profile page


class City(models.Model):
    name = models.CharField(max_length=20, unique=True)
    description = models.CharField(max_length=100)
    flags = models.CharField(verbose_name='Image(Url):', max_length=200)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    """ posts = models.ManyToManyField(Post, blank=True)  """
    slug = models.SlugField(default='', editable=False,
                            max_length=20, null=True)

    def get_absolute_url(self):
        kwargs = {
            'city_id': self.id,
            'slug': self.slug
        }

        return reverse("city_detail", kwargs=kwargs)

    def save(self, *args, **kwargs):
        value = self.name
        self.slug = slugify(value)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        ordering = ['-created_at']


class Profile(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    username = models.CharField(max_length=30, unique=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    avatar = models.CharField(max_length=200)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=Account)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, username=instance.username)


@receiver(post_save, sender=Account)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
