from django.contrib import admin

class FormFilter(admin.ListFilter):
    template = "filter/forms.html"
    form = None
    form_instance = None
    remove_params = []
    map_parameters = None  # {}
    delimeter = "|"

    def _get_map_filter(self):
        if self.map_parameters is None:
            self.map_parameters = {}
        for param in self._get_parameter_name():
            if param not in self.map_parameters:
                self.map_parameters[param] = param
        return self.map_parameters

    def get_map_filter(self):
        """ Overwrite this function to provide new map params
            def get_map_filter(self):
                dev = super(MyClass, self).get_map_filter
                dev['myparam'] = 'query_set_param'
                return dev
        """
        return self._get_map_filter()

    def _get_parameter_name(self, request=None):
        if self.form_instance is None:
            if request is not None:
                self.form_instance = self.form(request.GET)
            else:
                self.form_instance = self.form()
        return self.form_instance.fields.keys()

    def __init__(self, request, params, model, model_admin):

        self.used_parameters = {}
        # super(FormFilter, self).__init__(
        #    request, params, model, model_admin)
        if self.form is None:
            raise ImproperlyConfigured(
                "The form filter '%s' does not specify "
                "a 'form'." % self.__class__.__name__)

        for parameter_name in self._get_parameter_name(request):
            if parameter_name in params:
                value = params.pop(parameter_name)
                self.used_parameters[parameter_name] = value

        for param in self.remove_params:
            if param in params:
                params.pop(param)

    def has_output(self):
        return True

    def value(self):
        """
        Returns the value (in string format) provided in the request's
        query string for this filter, if any. If the value wasn't provided then
        returns None.
        """
        return None  # revisar

    def expected_parameters(self):
        return self._get_parameter_name()

    def choices(self, cl):
        yield {'title': self.title,
               'form': self.form_instance
               }

    def get_real_value(self, value):
        if not value:
            return None
        if self.delimeter in value:
            values = [x for x in value.split(self.delimeter)
                      if x != self.delimeter and x != '']
            if len(values):
                return values
            else:
                return None
        return value

    def get_filters(self):
        query_filter = {}
        map_parameters = self.get_map_filter()
        for used_param in self.used_parameters:
            value = self.get_real_value(self.used_parameters[used_param])
            filter_name = map_parameters[used_param]
            if value is None:
                continue
            if isinstance(value, list):
                filter_name += '__in'
            query_filter[filter_name] = value
        return query_filter

    def queryset(self, request, queryset):
        query_filters = self.get_filters()
        return queryset.filter(**query_filters)
