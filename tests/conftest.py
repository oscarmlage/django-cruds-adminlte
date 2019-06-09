import shutil

import pytest
from django.test import RequestFactory


@pytest.fixture(autouse=True, scope="session")
def faker_default_locale():
    """ Force the locale for faker library. """
    import factory
    factory.Faker.override_default_locale('es_ES')
    factory.Faker._DEFAULT_LOCALE = 'es_ES'


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    """ Set the media root to a temporary folder. """
    settings.MEDIA_ROOT = tmpdir.strpath
    yield
    shutil.rmtree(tmpdir)


@pytest.fixture
def request_factory() -> RequestFactory:
    return RequestFactory()


""" SELENIUM """
@pytest.fixture
def chrome_options(chrome_options):
    """ Set options for the selenium chrome driver. """
    chrome_options.add_argument('headless')
    chrome_options.add_argument("--window-size=1280x800")
    return chrome_options


@pytest.fixture
def selenium(selenium):
    """ override selenium fixture to maximize. """
    selenium.maximize_window()
    return selenium


@pytest.fixture()
def admin_browser(selenium, admin_client, live_server):
    """Return a browser instance with logged-in user session.

    For an unauthenticated browser you'd only need selenium+live_server.
    """
    cookie = admin_client.cookies['sessionid']

    selenium.get(live_server.url)
    selenium.add_cookie({'name': 'sessionid', 'value': cookie.value, 'secure': False, 'path': '/'})
    selenium.implicitly_wait(3)
    selenium.refresh()

    return selenium

