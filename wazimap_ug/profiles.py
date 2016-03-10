from wazimap.data.tables import get_datatable
from wazimap.data.utils import get_session, get_stat_data

__author__ = 'kenneth'


def get_profile(geo_code, geo_level, profile_name=None):
    data = {'demographics': get_demographics_profile(geo_code, geo_level)}
    return data


def get_demographics_profile(geo_code, geo_level):
    sex_dist_data, total_pop = get_datatable('population_data_2014').\
        get_stat_data(geo_level, geo_code)
    return {
        'sex_distribution': sex_dist_data,
        }