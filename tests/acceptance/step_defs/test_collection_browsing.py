import pytest
from django.urls import reverse
from pytest_bdd import given, scenarios, then, when

from portfolio.models import Collection, Photo

pytestmark = pytest.mark.django_db

scenarios("../features/collection_browsing.feature")


@given(
    "a published collection contains published photographs",
    target_fixture="collection_context",
)
def published_collection_with_photographs():
    collection = Collection.objects.create(
        title="Quiet Places",
        slug="quiet-places",
        cover_image="collections/cover.jpg",
        is_published=True,
    )
    second = Photo.objects.create(
        collection=collection,
        image="photos/second.jpg",
        title="Second",
        is_published=True,
        display_order=2,
    )
    first = Photo.objects.create(
        collection=collection,
        image="photos/first.jpg",
        title="First",
        is_published=True,
        display_order=1,
    )
    hidden = Photo.objects.create(
        collection=collection,
        image="photos/hidden.jpg",
        title="Hidden",
        is_published=False,
        display_order=3,
    )
    return {
        "collection": collection,
        "expected_order": [first, second],
        "hidden": hidden,
    }


@when("a visitor opens the collection", target_fixture="response")
def visitor_opens_collection(client, collection_context):
    return client.get(
        reverse(
            "collection-detail", kwargs={"slug": collection_context["collection"].slug}
        )
    )


@then("the published photographs are displayed in their configured order")
def photographs_displayed_in_order(response, collection_context):
    assert response.status_code == 200
    displayed = list(response.context["photos"])
    assert displayed == collection_context["expected_order"]
    assert collection_context["hidden"] not in displayed
