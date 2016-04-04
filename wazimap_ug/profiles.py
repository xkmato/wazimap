from wazimap.data.tables import get_datatable

__author__ = 'kenneth'


def get_profile(geo_code, geo_level, profile_name=None):
    data = {'demographics': get_demographics_profile(geo_code, geo_level)}
    return data


def get_demographics_profile(geo_code, geo_level):
    return {
        'all_dist_data': {}, #Todo Retrun data info here
        }