# pull in the default wazimap settings
from wazimap.settings import *  # noqa

# DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://wazimap:postgres@localhost/wazimap')
DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://postgres:@localhost/wazimap')
DJANGO_SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'this is some not so secret key but..')
DEBUG = os.environ.get('DJANGO_DEBUG', True)
DJANGO_SETTINGS_MODULE = os.environ.get('DJANGO_SETTINGS_MODULE', 'wazimap_ug.settings')

DATABASES = {
    'default': dj_database_url.parse(DATABASE_URL),
}
DATABASES['default']['ATOMIC_REQUESTS'] = True

# install this app before Wazimap
INSTALLED_APPS = ['wazimap_ug'] + INSTALLED_APPS

# Localise this instance of Wazimap
WAZIMAP['name'] = 'Wazimap Uganda'
WAZIMAP['url'] = 'http://uganda.wazimap.org'
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
        'children': ['subcounty'],
        },
    'subcounty': {
        'plural': 'subcounties',
        'children': []
    }
}

WAZIMAP['geometry_data'] = {
    'country': 'geo/country.topojson',
    'region': 'geo/region.topojson',
    'district': 'geo/district.topojson',
    'subcounty': 'geo/subcounty.topojson',
    }

WAZIMAP['twitter'] = '@Code4Africa'