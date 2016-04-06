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


def get_households_profile(geocode, geo_level, session):
    try:
        light_source, total_households = get_stat_data('household distribution by light source', geo_level, geocode,
                                                       session, table_fields=['household distribution by light source'])
        energy_source, _ = get_stat_data('household distribution by energy source', geo_level, geocode, session,
                                         table_fields=['household distribution by energy source'])
    except LocationNotFound:
        household_dist, total_households = {}, 1
        light_source = {}
        energy_source = {}

    total_electrified_lighting = 0
    for data, value in light_source.get('Electricity', {}).iteritems():
        if data == 'numerators':
            total_electrified_lighting += value['this']

    total_charcoal_energy = 0
    for data, value in energy_source.get('Charcoal', {}).iteritems():
        if data == 'numerators':
            total_charcoal_energy += value['this']

    final_data = {
        'light_source_distribution': light_source,
        'electrified_lighting': {
            'name': 'Lighting with Electricity',
            'numerators': {'this': total_electrified_lighting},
            'values': {'this': round(total_electrified_lighting / total_households * 100, 2)}
        },
        'energy_source_distribution': energy_source,
        'charcoal_energy': {
            'name': 'Cooking with Charcoal',
            'numerators': {'this': total_charcoal_energy},
            'values': {'this': round(total_charcoal_energy / total_households * 100, 2)}
        },
        'total_households': {
            "name": "Households",
            "values": {"this": total_households}
        }
    }
    return final_data


PROFILE_SECTIONS = ['demographics', 'households']


def get_profile(geo_code, geo_level, profile_name=None):
    session = get_session()

    try:
        geo_summary_levels = geo_data.get_summary_geo_info(geo_code, geo_level)
        data = {}

        for section in PROFILE_SECTIONS:
            function_name = 'get_%s_profile' % section
            if function_name in globals():
                func = globals()[function_name]
                data[section] = func(geo_code, geo_level, session)

                for level, code in geo_summary_levels:
                    merge_dicts(data[section], func(code, level, session), level)
        return data

    finally:
        session.close()


