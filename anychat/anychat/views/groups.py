from django.shortcuts import get_object_or_404
from vanilla.model_views import DetailView, CreateView
from anychat.anychat import models
from anychat.anychat.models import Group, User, Category


class GroupDetail(DetailView):
    model = Group

    def get(self, request, *args, **kwargs):
        return_value = super(GroupDetail, self).get(request)

        session_key = request.session.session_key
        user = User(group=self.object, session=session_key)

        user.save()  # save to DB
        self.object.save()
        return return_value


class GroupCreate(CreateView):
    model = Group
    fields = ['name', 'description']

    def form_valid(self, form):
        form.instance.category = get_object_or_404(Category, name=self.kwargs.get('category'))
        form.instance.slug = models.next_slug()
        form.instance.point = 'POINT(0.0 0.0)'
        return super(GroupCreate, self).form_valid(form)

    def get_success_url(self):
        category = self.object.category.name
        group = self.object.slug
        return '/chat/%s/%s' % (category, group)
