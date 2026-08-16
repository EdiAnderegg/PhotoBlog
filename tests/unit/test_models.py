import pytest

from portfolio.models import Collection, Photo

pytestmark = pytest.mark.django_db


def make_collection(**kwargs):
    defaults = {
        "title": "St. Petersburg After Rain",
        "slug": "st-petersburg-after-rain",
        "cover_image": "collections/cover.jpg",
    }
    defaults.update(kwargs)
    return Collection.objects.create(**defaults)


def make_photo(collection, **kwargs):
    defaults = {
        "collection": collection,
        "image": "photos/photo.jpg",
    }
    defaults.update(kwargs)
    return Photo.objects.create(**defaults)


def test_collection_defaults_to_unpublished():
    collection = make_collection()

    assert collection.is_published is False


def test_photo_defaults_to_unpublished():
    photo = make_photo(make_collection())

    assert photo.is_published is False


def test_collection_str_returns_title():
    collection = make_collection(title="Quiet Places")

    assert str(collection) == "Quiet Places"


def test_photo_str_returns_title_when_present():
    photo = make_photo(make_collection(), title="Canal at Dusk")

    assert str(photo) == "Canal at Dusk"


def test_photo_str_falls_back_to_id_when_title_blank():
    photo = make_photo(make_collection(), title="")

    assert str(photo) == f"Photo {photo.pk}"


def test_collections_are_ordered_by_display_order_then_title():
    second = make_collection(slug="second", title="Second", display_order=2)
    first = make_collection(slug="first", title="First", display_order=1)
    tied_a = make_collection(slug="tied-a", title="A Tied", display_order=1)

    ordered = list(Collection.objects.all())

    assert ordered == [tied_a, first, second]


def test_photos_are_ordered_by_display_order_then_id():
    collection = make_collection()
    second = make_photo(collection, display_order=2)
    first = make_photo(collection, display_order=1)

    ordered = list(Photo.objects.filter(collection=collection))

    assert ordered == [first, second]
