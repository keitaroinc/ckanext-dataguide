"""
Copyright (c) 2018 Keitaro AB

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import logging
import json
from operator import itemgetter

try:
    # CKAN 2.7 and later
    from ckan.common import config
except ImportError:
    # CKAN 2.6 and earlier
    from pylons import config

from ckan.controllers.admin import AdminController
import ckan.lib.base as base
import ckan.lib.helpers as h
import ckan.logic as logic
import ckan.model as model
from ckanext.dataguide import helpers

c = base.c
request = base.request
_ = base._

log = logging.getLogger(__name__)

class DataguideController(AdminController):
    ctrl = 'ckanext.dataguide.controllers.dataguide:DataguideController'

    def _get_ctx(self):
        return {
            'model': model, 'session': model.Session,
            'user': c.user,
            'auth_user_obj': c.userobj,
            'for_view': True
        }

    def data_guide(self):

        context = self._get_ctx()

        if request.method == 'POST':
            try:
                data_dict = dict(request.POST)
                data = logic.get_action('config_option_update')(
                    {'user': c.user}, data_dict)

            except logic.ValidationError, e:
                errors = e.error_dict
                error_summary = e.error_summary
                vars = {'data': data, 'errors': errors,
                        'error_summary': error_summary}
                return base.render('admin/data_guide.html', extra_vars=vars)

            h.redirect_to(controller=self.ctrl, action='data_guide')

        c.site_groups = logic.get_action('group_list')(context, {'all_fields': True})
        data = {}

        if config.get('data_guide_items'):

            data_guide_items = config.get('data_guide_items').split(',')

            data = helpers.get_data_guide_items()

            for item in data_guide_items:
                for site_group in c.site_groups:
                    if site_group['id']  == item:
                        c.site_groups.remove(site_group)


        vars = {'data': data, 'errors': {}}

        return base.render('admin/data_guide.html', extra_vars=vars)