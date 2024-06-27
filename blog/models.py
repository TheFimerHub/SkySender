from django.db import models

class Blog(models.Model):
    title = models.CharField(max_length=255, verbose_name='title')
    content = models.TextField(max_length=2000, verbose_name='content')
    image = models.ImageField(upload_to='blog/', verbose_name='image', blank=True, null=True)
    views = models.IntegerField(default=0, verbose_name='views')
    date_added = models.DateTimeField(auto_now_add=True, verbose_name='date_added')

    class Meta:
        verbose_name = 'Blog'
        verbose_name_plural = 'Blogs'
