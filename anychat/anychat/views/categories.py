from vanilla.model_views import DetailView, ListView
from anychat.anychat.models import Category


class CategoryList(ListView):
    model = Category


class CategoryDetail(DetailView):
    model = Category
