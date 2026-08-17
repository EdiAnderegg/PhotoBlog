from django.views.generic import DetailView, ListView, TemplateView

from .models import Collection, Photo


class HomeView(TemplateView):
    template_name = "portfolio/home.html"


class CollectionListView(ListView):
    queryset = Collection.objects.filter(is_published=True)
    template_name = "portfolio/collection_list.html"
    context_object_name = "collections"


class CollectionDetailView(DetailView):
    queryset = Collection.objects.filter(is_published=True)
    template_name = "portfolio/collection_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["photos"] = self.object.photos.filter(is_published=True)
        return context


class PhotoDetailView(DetailView):
    template_name = "portfolio/photo_detail.html"

    def get_queryset(self):
        return Photo.objects.filter(
            is_published=True,
            collection__slug=self.kwargs["collection_slug"],
            collection__is_published=True,
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["next_photo"] = self.object.get_next_published()
        context["previous_photo"] = self.object.get_previous_published()
        return context


class AboutView(TemplateView):
    template_name = "portfolio/about.html"
