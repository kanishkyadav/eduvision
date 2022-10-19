from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from ckeditor.fields import RichTextField


class Category(models.Model):
    tutorial_name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, blank=True)
    discription = models.TextField()

    def __str__(self):
        return self.tutorial_name


def save(self, *args, **kwargs):
    self.slug = slugify(self.tutorial_name)
    super().save(*args, **kwargs)


def get_absolute_url(self):
    return reverse('cat-page', kwargs={'slug': self.slug})


class Post(models.Model):
    title = models.CharField(max_length=70)
    slug = models.SlugField(unique=True, blank=True)
    # content = HTMLField('Content')
    content = RichTextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts')
    # image = models.ImageField(upload_to= "blog/post",blank = True)
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('detail-post', kwargs={'slug': self.slug})


class ContactUs(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    comment = models.TextField()

    def __str__(self):
        return self.name