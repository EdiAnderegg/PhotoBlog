from django.urls import reverse


def test_admin_login_page_is_reachable(client):
    response = client.get(reverse("admin:login"))

    assert response.status_code == 200
