import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckan.lib.plugins import DefaultTranslation, DefaultGroupForm

from ckanext.dataguide import helpers


class DataguidePlugin(plugins.SingletonPlugin, DefaultGroupForm, DefaultTranslation):
    plugins.implements(plugins.ITranslation)
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IRoutes, inherit=True)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IGroupForm, inherit=True)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'dataguide')

    def update_config_schema(self, schema):
        ignore_missing = toolkit.get_validator('ignore_missing')

        schema.update({
            'data_guide_items': [ignore_missing, unicode]
        })

        return schema

    # IRoutes

    def before_map(self, map):
        ctrl = 'ckanext.dataguide.controllers.dataguide:DataguideController'

        map.connect('eds_data_guide', '/data-guide',
                    action='data_guide', ckan_icon='folder-open', controller=ctrl)
        return map

    # ITemplateHelpers

    def get_helpers(self):
        return {
            'get_data_guide_items': helpers.get_data_guide_items,
            'dataguide_available_locales': helpers.dataguide_available_locales
        }

    ## IGroupForm

    def is_fallback(self):
        return False

    def group_types(self):
        return ['group']

    def form_to_db_schema(self):
        _convert_to_extras = plugins.toolkit.get_converter('convert_to_extras')
        _ignore_missing = plugins.toolkit.get_validator('ignore_missing')
        default_validators = [_ignore_missing, _convert_to_extras, unicode]
        schema = super(DataguidePlugin, self).form_to_db_schema()

        # Default group schema is missing num_followers and package_count
        schema.update({'num_followers': [plugins.toolkit.get_validator('ignore_missing')]})
        schema.update({'package_count': [plugins.toolkit.get_validator('ignore_missing')]})

        for locale in helpers.dataguide_available_locales():
            schema.update({
                'title_{0}'.format(locale): default_validators
            })
        return schema

    def db_to_form_schema(self):
        _convert_from_extras = plugins.toolkit.get_converter('convert_from_extras')
        _ignore_missing = plugins.toolkit.get_validator('ignore_missing')
        default_validators = [_convert_from_extras, _ignore_missing]
        schema = super(DataguidePlugin, self).form_to_db_schema()

        # Default group schema is missing num_followers and package_count
        schema.update({'num_followers': [plugins.toolkit.get_validator('not_empty')]})
        schema.update({'package_count': [plugins.toolkit.get_validator('not_empty')]})
        for locale in helpers.dataguide_available_locales():
            schema.update({
                'title_{0}'.format(locale): default_validators
            })
        return schema
