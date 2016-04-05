from wazimap.data.tables import get_datatable
from wazimap.data.utils import merge_dicts, get_session, get_stat_data, LocationNotFound
from wazimap.geo import geo_data

__author__ = 'kenneth'


def get_demographics_profile(geo_code, geo_level, session):
    try:
        sex_dist_data, total_pop = get_stat_data('sex', geo_level, geo_code, session, table_fields=['sex'])
        urban_dist_data, _ = get_stat_data('rural or urban', geo_level, geo_code, session, table_fields=['rural or urban'])
    except LocationNotFound:
        sex_dist_data, total_pop = {}, 1
        urban_dist_data = {'Urban': {}, 'Rural': {}}

    total_urbanised = 0
    for data, value in urban_dist_data['Urban'].iteritems():
        if data == 'numerators':
            total_urbanised += value['this']

    final_data = {
        'sex_ratio': sex_dist_data,
        'urban_distribution': urban_dist_data,
        'urbanised': {
            'name': 'In urban areas',
            'numerators': {'this': total_urbanised},
            'values': {'this': round(total_urbanised / total_pop * 100, 2)}
        },
        'total_population': {
            "name": "People",
            "values": {"this": total_pop}
        }}
    return final_data


def get_profile(geo_code, geo_level, profile_name=None):
    session = get_session()

    try:
        geo_summary_levels = geo_data.get_summary_geo_info(geo_code, geo_level)
        data = {'demographics': get_demographics_profile(geo_code, geo_level, session)}

        for level, code in geo_summary_levels:
            merge_dicts(data['demographics'], get_demographics_profile(code, level, session), level)
        return data

    finally:
        session.close()


