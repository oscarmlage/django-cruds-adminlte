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
    # The trick is that if this appears in the rendered content,
    # everything went as planned.   
    assert "fa-address-book-o" in base_content
