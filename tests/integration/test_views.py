import pytest
from django.urls import reverse

from portfolio.models import Collection, Photo, Photographer

pytestmark = pytest.mark.django_db


def make_collection(**kwargs):
    defaults = {
        "title": "Quiet Places",
        "slug": "quiet-places",
        "cover_image": "collections/cover.jpg",
        "is_published": True,
    }
    defaults.update(kwargs)
    return Collection.objects.create(**defaults)


def make_photo(collection, **kwargs):
    defaults = {
        "collection": collection,
        "image": "photos/photo.jpg",
        "is_published": True,
    }
    defaults.update(kwargs)
    return Photo.objects.create(**defaults)


def test_home_lists_only_published_collections(client):
    published = make_collection()
    make_collection(slug="draft", title="Draft", is_published=False)

    response = client.get(reverse("home"))

    assert response.status_code == 200
    collections = list(response.context["collections"])
    assert collections == [published]


def test_collection_detail_shows_only_published_photos_in_order(client):
    collection = make_collection()
    second = make_photo(collection, display_order=2)
    first = make_photo(collection, display_order=1)
    make_photo(collection, display_order=3, is_published=False)

    response = client.get(
        reverse("collection-detail", kwargs={"slug": collection.slug})
    )

    assert response.status_code == 200
    assert list(response.context["photos"]) == [first, second]


def test_collection_detail_404s_when_unpublished(client):
    collection = make_collection(is_published=False)

    response = client.get(
        reverse("collection-detail", kwargs={"slug": collection.slug})
    )

    assert response.status_code == 404


def test_photo_detail_404s_when_unpublished(client):
    collection = make_collection()
    photo = make_photo(collection, is_published=False)

    response = client.get(
        reverse(
            "photo-detail",
            kwargs={"collection_slug": collection.slug, "pk": photo.pk},
        )
    )

    assert response.status_code == 404


def test_photo_detail_exposes_next_and_previous(client):
    collection = make_collection()
    first = make_photo(collection, display_order=1)
    second = make_photo(collection, display_order=2)
    third = make_photo(collection, display_order=3)

    response = client.get(
        reverse(
            "photo-detail",
            kwargs={"collection_slug": collection.slug, "pk": second.pk},
        )
    )

    assert response.status_code == 200
    assert response.context["previous_photo"] == first
    assert response.context["next_photo"] == third


def test_about_page_renders_photographer_info(client):
    Photographer.objects.create(
        name="Jane Doe",
        bio="Chasing quiet light.",
        instagram_url="https://instagram.com/example",
        email="hello@example.com",
    )

    response = client.get(reverse("about"))

    assert response.status_code == 200
    assert "Jane Doe" in response.content.decode()


def test_about_page_renders_without_a_photographer(client):
    response = client.get(reverse("about"))

    assert response.status_code == 200
