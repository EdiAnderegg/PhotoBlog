import pytest
from django.db import IntegrityError

from portfolio.models import Collection, Photo

pytestmark = pytest.mark.django_db


def test_photo_requires_a_collection():
    with pytest.raises(IntegrityError):
        Photo.objects.create(image="photos/photo.jpg")


def test_collection_exposes_its_related_photos():
    collection = Collection.objects.create(
        title="Faces of Summer",
        slug="faces-of-summer",
        cover_image="collections/cover.jpg",
    )
    photo = Photo.objects.create(collection=collection, image="photos/photo.jpg")

    assert list(collection.photos.all()) == [photo]


def test_deleting_a_collection_deletes_its_photos():
    collection = Collection.objects.create(
        title="Faces of Summer",
        slug="faces-of-summer-2",
        cover_image="collections/cover.jpg",
    )
    Photo.objects.create(collection=collection, image="photos/photo.jpg")

    collection.delete()

    assert Photo.objects.count() == 0
