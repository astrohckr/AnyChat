from anychat.anychat.models import Group, Category, Point
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView
from vanilla.model_views import CreateView


class GroupChat(TemplateView):
    template_name = 'anychat/group_chat.html'

    def get_context_data(self, **kwargs):
        if 'view' not in kwargs:
            kwargs['view'] = self

        category = kwargs['category']
        group = kwargs['group']
        kwargs['group'] = Group.objects.filter(category__slug=category, slug=group).get()

        return kwargs


class GroupCreate(CreateView):
    model = Group
    fields = ['name', 'description']

    def form_valid(self, form):
        point = Point()
        point.longitude = self.request.session['point']['longitude']
        point.latitude = self.request.session['point']['latitude']
        point.save()

        form.instance.category = get_object_or_404(Category, name=self.kwargs.get('category'))
        form.instance.point = point

        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        group = self.object.slug
        return reverse('anychat:group_chat', kwargs={'category': group.category.slug, 'group': group.slug})
