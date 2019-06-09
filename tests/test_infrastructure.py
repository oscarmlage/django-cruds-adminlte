""" Basic test to check our stuff is in place. """
import re

import pytest
from django.urls import reverse


@pytest.mark.selenium
def test_browser_homepage(selenium, live_server):
    """ Check that we can open the test_project homepage. """
    test_page_url = reverse('hello_page')
    assert test_page_url == '/hello'
    selenium.get(live_server.url + test_page_url)
    assert 'Welcome to test_project' in selenium.page_source


@pytest.mark.selenium
def test_browser_homepage_loggedin(admin_browser, live_server):
    """ Check that we can open the test_project homepage. """
    test_page_url = reverse('hello_page')
    assert test_page_url == '/hello'
    admin_browser.get(live_server.url + test_page_url)
    assert re.match(r".*Welcome 'admin' to test_project.*", admin_browser.page_source)
