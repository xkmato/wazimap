# pull in the default wazimap settings
from wazimap.settings import *  # noqa

# install this app before Wazimap
INSTALLED_APPS = ['wazimap_ug'] + INSTALLED_APPS

# Localise this instance of Wazimap
WAZIMAP['name'] = 'Wazimap Uganda'
WAZIMAP['url'] = 'http://wazimap.example.com'
WAZIMAP['country_code'] = 'UG'
WAZIMAP['profile_builder'] = 'wazimap_ug.profiles.get_profile'
WAZIMAP['levels'] = {
    'country': {
        'plural': 'countries',
        'children': ['region'],
        },
    'region': {
        'plural': 'regions',
        'children': ['district'],
        },
    'district': {
        'plural': 'districts',
        'children': [],
        }
}

WAZIMAP['geometry_data'] = {
    'country': 'geo/country.topojson',
    'region': 'geo/regions.topojson',
    'district': 'geo/districts.topojson',
    }
