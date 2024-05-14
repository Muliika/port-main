from django.db import models
from django.utils import timezone
from accounts.models import UserBase
from django.urls import reverse
# from mptt.models import MPTTModel, TreeForeignKey
from taggit.managers import TaggableManager
from ckeditor_uploader.fields import RichTextUploadingField



def user_directory_path(instance, filename):
    # Use strftime to format the date and include the filename
    return 'posts/{}/{}/{}/{}'.format(
        instance.publish.year,
        instance.publish.month,
        instance.publish.day,
        filename
    )


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Post(models.Model):

    class NewManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status='published')

    options = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    category = models.ForeignKey(Category, on_delete=models.PROTECT, default=1)
    title = models.CharField(max_length=250)
    excerpt = RichTextUploadingField(null=True)
    image = models.ImageField(upload_to=user_directory_path, default='posts/default.jpg')
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    publish = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(UserBase, on_delete=models.CASCADE, related_name='blog_posts')
    content = RichTextUploadingField()
    tags = TaggableManager(blank=True)
    status = models.CharField(max_length=10, choices=options, default='draft')
    objects = models.Manager()  # default manager
    newmanager = NewManager()  # custom manager

    def get_absolute_url(self):
        return reverse('portfolio:post_single', args=[self.slug])

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title


class Comment(models.Model):

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=50)
    email = models.EmailField()
    content = models.TextField()
    publish = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)

    class Meta:
        ordering = ('publish',)

    def __str__(self):
        return f'Comment by {self.name}'

