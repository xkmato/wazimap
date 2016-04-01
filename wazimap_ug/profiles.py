from wazimap.data.tables import get_datatable

__author__ = 'kenneth'


def get_profile(geo_code, geo_level, profile_name=None):
    data = {'demographics': get_demographics_profile(geo_code, geo_level)}
    return data


def get_demographics_profile(geo_code, geo_level):
    all_dist_data, total_pop = get_datatable('population_data_2014').\
        get_stat_data(geo_level, geo_code)
    print all_dist_data['reg_voters']
    return {
        'all_dist_data': all_dist_data['reg_voters'],
        }