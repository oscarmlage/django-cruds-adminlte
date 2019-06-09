""" Test the urls of a basic crud app.

Note that we use live_server and admin_browser when it looks like it
would not be needed. We do so to capture screenshots of those pages.
"""
from datetime import date
from urllib.parse import urlencode

from django.templatetags.l10n import localize
from django.urls import reverse

from cruds_adminlte.utils import crud_url_name, ACTION_CREATE, ACTION_DETAIL, ACTION_UPDATE, ACTION_LIST, ACTION_DELETE
from testapp.factories import AuthorFactory
from testapp.models import Author


def test_login_required(admin_client, client):
    model = Author
    app_label = model._meta.app_label
    model_lower = model.__name__.lower()

    actions = [ACTION_CREATE, ACTION_LIST]
    for a in actions:
        urlname = crud_url_name(model, a)
        url = reverse(urlname)
        r = client.get(url)
        assert r.status_code == 302
        r = admin_client.get(url)
        assert r.status_code == 200

    author = AuthorFactory.create()
    actions = [ACTION_DELETE, ACTION_DETAIL, ACTION_UPDATE]
    for a in actions:
        urlname = crud_url_name(model, a)
        url = reverse(urlname, args=[author.pk, ])
        r = client.get(url)
        assert r.status_code == 302
        r = client.post(url)
        assert r.status_code == 302
        r = admin_client.get(url)
        assert r.status_code == 200
        # we don't try authenticated POST as this is tested later.


def test_create(admin_client, live_server, admin_browser):
    url = reverse('testapp_author_create')
    r = admin_client.get(url)
    assert r.status_code == 200

    author = AuthorFactory.build()
    r = admin_client.post(url, {
        'name': author.name,
        'birthday': author.birthday.strftime('%Y-%m-%d')
    })
    assert r.status_code == 302
    assert r.url == reverse('testapp_author_list')
    au = Author.objects.all()[0]
    assert au.name == author.name and au.birthday == author.birthday
    admin_browser.get(live_server.url + url)


def test_detail(admin_client, live_server, admin_browser):
    author = AuthorFactory.create()
    url = reverse('testapp_author_detail', args=[author.pk, ])
    r = admin_client.get(url)
    assert r.status_code == 200
    content = r.content.decode()
    birthdate_txt = localize(author.birthday)
    assert author.name in content
    assert birthdate_txt in content
    admin_browser.get(live_server.url + url)


def test_update(admin_client, live_server, admin_browser):
    author = AuthorFactory.create()
    url = reverse('testapp_author_update', args=[author.pk, ])
    r = admin_client.get(url)
    assert r.status_code == 200
    content = r.content.decode()
    assert author.name in content
    assert author.birthday.strftime('%Y-%m-%d') in content

    r = admin_client.post(url, {
        'name': 'MADE UP NAME',
        'birthday': '1983-08-04'
    })
    assert r.status_code == 302
    assert r.url == reverse('testapp_author_list')
    au = Author.objects.all()[0]
    assert au.name == 'MADE UP NAME'
    assert au.birthday == date(1983, 8, 4)
    admin_browser.get(live_server.url + url)


def test_delete(admin_client, live_server, admin_browser):
    author = AuthorFactory.create()
    url = reverse('testapp_author_delete', args=[author.pk, ])
    r = admin_client.get(url)
    admin_browser.get(live_server.url + url)
    assert r.status_code == 200
    content = r.content.decode()
    assert author.name in content
    assert 'Remove %s' % author.name in content

    r = admin_client.post(url)
    assert r.status_code == 302
    assert r.url == reverse('testapp_author_list')

    assert Author.objects.all().count() == 0
    admin_browser.get(live_server.url + url)


def test_list(admin_client, live_server, admin_browser):
    AuthorFactory.create_batch(50)
    url = reverse('testapp_author_list')

    r = admin_client.get(url)
    assert r.status_code == 200
    content = r.content.decode()
    assert 'Page 1 of' in content

    author = Author.objects.all()[0]
    r = admin_client.get(url + "?" + urlencode({'q': author.name}))
    assert r.status_code == 200
    content = r.content.decode()
    assert author.name in content

    admin_browser.get(live_server.url + url)
    admin_browser.get(live_server.url + url + "?" + urlencode({'q': author.name}))


# TODO: Check pagination
# TODO: Check CRUD Navigation (link on the list)
