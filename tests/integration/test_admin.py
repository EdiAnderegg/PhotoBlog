import pytest
from django.contrib import admin

from portfolio.models import Collection, Photo


def test_collection_and_photo_are_registered_in_admin():
    assert Collection in admin.site._registry
    assert Photo in admin.site._registry


@pytest.mark.django_db
def test_collection_changelist_is_reachable(admin_client):
    response = admin_client.get("/admin/portfolio/collection/")

    assert response.status_code == 200


@pytest.mark.django_db
def test_photo_changelist_is_reachable(admin_client):
    response = admin_client.get("/admin/portfolio/photo/")

    assert response.status_code == 200
