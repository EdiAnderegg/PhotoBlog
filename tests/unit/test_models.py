import pytest

from portfolio.models import Collection, Photo, Photographer

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


def test_photographer_save_always_uses_pk_one():
    first = Photographer.objects.create(name="Jane Doe")
    second = Photographer(name="Someone Else")
    second.save()

    assert first.pk == 1
    assert second.pk == 1
    assert Photographer.objects.count() == 1
    assert Photographer.objects.get().name == "Someone Else"


def test_get_next_published_returns_next_by_display_order():
    collection = make_collection()
    first = make_photo(collection, display_order=1, is_published=True)
    second = make_photo(collection, display_order=2, is_published=True)

    assert first.get_next_published() == second


def test_get_next_published_returns_none_at_the_end():
    collection = make_collection()
    only = make_photo(collection, display_order=1, is_published=True)

    assert only.get_next_published() is None


def test_get_next_published_skips_unpublished_photos():
    collection = make_collection()
    first = make_photo(collection, display_order=1, is_published=True)
    make_photo(collection, display_order=2, is_published=False)
    third = make_photo(collection, display_order=3, is_published=True)

    assert first.get_next_published() == third


def test_get_next_published_ignores_other_collections():
    collection = make_collection()
    other_collection = make_collection(slug="other", title="Other")
    only = make_photo(collection, display_order=1, is_published=True)
    make_photo(other_collection, display_order=2, is_published=True)

    assert only.get_next_published() is None


def test_get_previous_published_returns_previous_by_display_order():
    collection = make_collection()
    first = make_photo(collection, display_order=1, is_published=True)
    second = make_photo(collection, display_order=2, is_published=True)

    assert second.get_previous_published() == first


def test_get_previous_published_returns_none_at_the_start():
    collection = make_collection()
    only = make_photo(collection, display_order=1, is_published=True)

    assert only.get_previous_published() is None
