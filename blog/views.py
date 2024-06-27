from django.utils import timezone
from django.views.generic import DetailView, ListView
from .models import Blog

class BlogListView(ListView):
    model = Blog
    template_name = 'blog/blog_list.html'
    context_object_name = 'blogs'
    paginate_by = 4

    def get_queryset(self):
        return Blog.objects.all().order_by('-date_added')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        for blog in context['blogs']:
            blog.time_since = self.time_since(blog.date_added)
        return context

    @staticmethod
    def time_since(value):
        now = timezone.now()
        diff = now - value

        if diff.days == 0:
            if diff.seconds < 60:
                return 'только что'
            elif diff.seconds < 3600:
                minutes = diff.seconds // 60
                return f'{minutes} мин. назад'
            else:
                hours = diff.seconds // 3600
                return f'{hours} ч. назад'
        elif diff.days < 7:
            return f'{diff.days} д. назад'
        elif diff.days < 30:
            weeks = diff.days // 7
            return f'{weeks} нед. назад'
        else:
            months = diff.days // 30
            return f'{months} мес. назад'

        return value

class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blog/blog_detail.html'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views += 1
        self.object.save()
        return self.object