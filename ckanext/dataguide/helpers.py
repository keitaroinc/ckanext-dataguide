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

try:
    # CKAN 2.7 and later
    from ckan.common import config
except ImportError:
    # CKAN 2.6 and earlier
    from pylons import config

from ckan.plugins import toolkit
from ckan import model, logic
from ckan.common import c

log = logging.getLogger(__name__)


def _get_context():
    return {
        'model': model,
        'session': model.Session,
        'user': c.user or c.author,
        'auth_user_obj': c.userobj
    }


def get_data_guide_items():
    context = _get_context()
    groups = []

    if config.get('data_guide_items'):
        data_guide_items = config.get('data_guide_items').split(',')

        for item in data_guide_items:
            try:
                group = logic.get_action('group_show')(context, {'id': item})
                groups.append(group)
            except:
                pass

    return groups


def dataguide_available_locales():
    return toolkit.aslist(
        config.get('ckanext.eds.available_locales',
                   'en da_DK')
    )
