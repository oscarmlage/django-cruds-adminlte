# -*- coding: utf-8 -*-
from cruds_adminlte.template_loader import Loader
from django.template import loader
from django.template import engines


def test_get_loaders():
    tpl_index = loader.get_template('adminlte/index.html')
    assert "block nav_links_ul" not in tpl_index.template.source

    tpl_base = loader.get_template('adminlte/base.html')
    assert "tests/demo_project/demo/templates/adminlte/base.html" in tpl_base.origin.name    
    base_content = tpl_base.render()
    assert "fa-address-book-o" in base_content

    tpl_base2 = loader.get_template('cruds/base.html')
    assert "templates/cruds/base.html" in tpl_base2.origin.name    
    base_content = tpl_base2.render()
    assert "fa-address-book-o" in base_content

    # Now we ask for a template that is outside of the library,
    # but extends the library
    tpl = loader.get_template('homepage.html')
    assert "templates/homepage.html" in tpl.origin.name
    tpl_content = tpl.render()
    assert "Hello." in tpl_content
    assert "fa-address-book-o" in tpl_content
