from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import AnonymousUser
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import TemplateView, DetailView, CreateView, UpdateView, DeleteView
import random
from blog.models import Blog
from .models import Client, Message, Mailing, Attempt
from .forms import ClientForm, MessageForm, MailingForm

User = get_user_model()


# General
class GeneralPageView(TemplateView):
    template_name = 'main/general_page.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        user = self.request.user
        context = super().get_context_data(**kwargs)

        if isinstance(user, AnonymousUser):
            context['blogs'] = random.sample(list(Blog.objects.all()), 3)
            context['info'] = {
                'active_mailings': 0,
                'all_mailings': 0,
                'all_clients': 0,
            }
        else:
            context['blogs'] = random.sample(list(Blog.objects.all()), 3)
            context['info'] = {
                'active_mailings': Mailing.objects.filter(status__in=[Mailing.CREATED, Mailing.SENT],
                                                          owner=user).count(),
                'all_mailings': Mailing.objects.filter(owner=user).count(),
                'all_clients': Client.objects.filter(owner=user).count(),
            }

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


# Creator (instead of many List Views, I replaced everything into one Template View)
class CreatorPageView(LoginRequiredMixin, TemplateView):
    template_name = 'main/creator_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        users = User.objects.all()
        user_is_manager = user.groups.filter(name='manager').exists()
        if user.is_superuser:
            user_is_manager = True

        # Фильтрация данных в зависимости от пользователя
        if user.is_superuser or user.is_staff or user_is_manager:
            clients = Client.objects.all()
            messages = Message.objects.all()
            mailings = Mailing.objects.all()
            attempts = Attempt.objects.all()
        else:
            clients = Client.objects.filter(owner=user)
            messages = Message.objects.filter(owner=user)
            mailings = Mailing.objects.filter(owner=user)
            attempts = Attempt.objects.filter(mailing__owner=user)

        # Сортировка данных
        context['clients'] = clients.order_by('pk')
        context['messages'] = messages.order_by('pk')
        context['mailings'] = mailings.order_by('-start_time')
        context['attempts'] = attempts.order_by('-attempt_time')
        context['users'] = users.order_by('pk')
        context['user_is_manager'] = user_is_manager

        return context


@permission_required('main.block_user')
def block_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if user.is_staff:
        return redirect('creator-page')
    else:
        user.is_active = False
        user.save()
        return redirect('creator-page')


@permission_required('main.unblock_user')
def unblock_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if user.is_staff:
        return redirect('creator-page')
    else:
        user.is_active = True
        user.save()
        return redirect('creator-page')


@permission_required('main.disable_mailing')
def disable_mailing(request, mailing_id):
    mailing = get_object_or_404(Mailing, id=mailing_id)
    mailing.status = mailing.FINISHED
    mailing.save()
    return redirect('creator-page')


@permission_required('main.allow_mailing')
def allow_mailing(request, mailing_id):
    mailing = get_object_or_404(Mailing, id=mailing_id)
    mailing.status = mailing.CREATED
    mailing.save()
    return redirect('creator-page')


# Client
class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client
    template_name = 'main/client_detail.html'


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'main/forms/client_form.html'
    title = 'Create Client'
    success_url = reverse_lazy('creator-page')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'main/forms/client_form.html'
    title = 'Create Client'
    success_url = reverse_lazy('creator-page')


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('creator-page')


# Message
class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message
    template_name = 'main/message_detail.html'


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'main/forms/message_form.html'
    title = 'Create Message'
    success_url = reverse_lazy('creator-page')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    template_name = 'main/forms/message_form.html'
    title = 'Create Message'
    success_url = reverse_lazy('creator-page')


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    template_name = 'main/message_confirm_delete.html'
    success_url = reverse_lazy('creator-page')


# Mailing
class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing
    template_name = 'main/mailing_detail.html'


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'main/forms/mailing_form.html'
    title = 'Create Mailing'
    success_url = reverse_lazy('creator-page')

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        form = super(MailingCreateView, self).get_form(form_class)
        form.fields['clients'].queryset = Client.objects.filter(owner=self.request.user)
        return form

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'main/forms/mailing_form.html'
    title = 'Create Mailing'
    success_url = reverse_lazy('creator-page')


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    template_name = 'main/mailing_confirm_delete.html'
    success_url = reverse_lazy('creator-page')
