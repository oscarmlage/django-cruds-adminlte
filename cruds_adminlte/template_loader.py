"""The Template Loader.

Using the standard django template inheritance and extension mechanism,
it would happen that you would end up with lots of template overrides.

That is, you cannot, by default, override a block defined in an included
template (like the sidebar, or the headbar) thus, in order to define the
sidebar you would need to override that template. And if you want different
sidebars for different things... you get the point.

The Template Loader those a simple trick: it "compiles" a template by embedding
into its contents the contents of the included templates. So that at the eyes
of Django Template System when you extend from such compiled template, all is one
single template the block of which can be extended.

Note that we can only handle embedding of calls to include which do not have a 'with'.
Also, we do not currently support embedding a template that uses 'extends' itself.

THIS IS EXPERIMENTAL FEATURE.
Our solution is heavily based in the code by github's @uw-it-aca/django-template-preprocess
which is in turn based of django-compressor.
Also borrowing some code of django's builtin cached template loader.
"""
from importlib import import_module
from django.template import engines
from django.template import loader
from django.utils.encoding import smart_text
import hashlib

from django.template import TemplateDoesNotExist
from django.template.backends.django import copy_exception

from django.template.loaders.base import Loader as BaseLoader
from fnmatch import fnmatch
import codecs
import re
import os


class Loader(BaseLoader):
    # List of templates on which rendering we intervene.
    templates = ['adminlte/base.html', 
                 r'^adminlte/lib/.*',
                 r'^cruds/.*',
                 ]

    def __init__(self, engine, templates=None):
        if templates:
            self.templates = templates
        self.engine = engine
        #self.loaders = engine.get_template_loaders(loaders)
        self.loaders = self.get_loaders()
        super().__init__(engine)

    def check_intervene(self, template_name):
        for m in self.templates:
            if m == template_name or re.match(m, template_name):
                return True
        return False

    def get_template_sources(self, template_name):
        if self.check_intervene(template_name):
            for loader in self.loaders:
                yield from loader.get_template_sources(template_name)

    def get_contents(self, origin):
        content = origin.loader.get_contents(origin)
        content = process_template_content(content)
        return content

    def get_loaders(self):
        template_source_loaders = self.engine.loaders
        myname = self.__class__.__module__ + '.' + self.__class__.__qualname__
        template_source_loaders.remove(myname)
        template_source_loaders = self.engine.get_template_loaders(template_source_loaders)
        loaders = []
        # Unwrap the loaders inside the CachedTemplateLoader if applicable.
        for loader in template_source_loaders:
            if hasattr(loader, 'loaders'):
                loaders.extend(loader.loaders)
            else:
                loaders.append(loader)
        return loaders

    def get_template(self, template_name, skip=None):
        template = super().get_template(template_name, skip)
        return template


def handle_includes(content, seen_templates, template_processor):
    def insert_template(match):
        name = match.group(1)

        if name in seen_templates:
            raise Exception("Recursive template includes")

        seen_templates[name] = True

        content = template_processor(name, seen_templates)
        return content

    # FIXME: Make sure we do not process an include with 'with'
    content = re.sub(r"""{%\s*include\s*['"]([^"']+?)["']\s*%}""",
                     insert_template,
                     content, flags=re.UNICODE)

    return content


def process_sub_template(name, seen_templates):
    content = loader.get_template(name).template.source
    return process_template_content(content,
                                    seen_templates,
                                    subcall=True)


def process_template_content(content,
                             seen_templates=None,
                             subcall=False):
    if seen_templates is None:
        seen_templates = {}
    content = handle_includes(content,
                        seen_templates=seen_templates,
                        template_processor=process_sub_template,
                        )
    return content

