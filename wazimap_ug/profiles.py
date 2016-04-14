from wazimap.data.tables import get_datatable
from wazimap.data.utils import merge_dicts, get_session, get_stat_data, LocationNotFound
from wazimap.geo import geo_data

__author__ = 'kenneth'

LOCATIONNOTFOUND = {'name': 'No Data Found', 'numerators': {'this': 0}, 'values': {'this': 0}}


def get_demographics_profile(geo_code, geo_level, session):
    try:
        sex_dist_data, total_pop = get_stat_data('sex', geo_level, geo_code, session, table_fields=['sex'])
        urban_dist_data, _ = get_stat_data('rural or urban', geo_level, geo_code, session,
                                           table_fields=['rural or urban'])
    except LocationNotFound:
        sex_dist_data, total_pop = LOCATIONNOTFOUND, -1
        urban_dist_data = LOCATIONNOTFOUND

    total_urbanised = 0
    for data, value in urban_dist_data.get('Urban', {}).iteritems():
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
        household_dist, total_households = LOCATIONNOTFOUND, -1
        light_source = LOCATIONNOTFOUND
        energy_source = LOCATIONNOTFOUND

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


def get_elections2016_profile(geocode, geo_level, session):
    try:
        candidate, total_votes = get_stat_data('presidential candidate', geo_level, geocode, session,
                                               table_fields=['presidential candidate'])
    except LocationNotFound:
        candidate, total_votes = LOCATIONNOTFOUND, -1

    total_besigye = 0
    for data, value in candidate.get('Kizza besigye', {}).iteritems():
        if data == 'numerators':
            total_besigye += value['this']

    final_data = {
        'candidate_distribution': candidate,
        'besigye_votes': {
            'name': 'Besigye Votes',
            'numerators': {'this': total_besigye},
            'values': {'this': round(total_besigye / total_votes * 100, 2)}
        },

        'total_votes': {
            "name": "Votes",
            "values": {"this": total_votes}
        }
    }
    return final_data


def get_disabilities_profile(geocode, geo_level, session):
    try:
        disabled_or_not, total_ = get_stat_data('disabled or not', geo_level, geocode, session,
                                                table_fields=['disabled or not'])
        disability, _ = get_stat_data('disability', geo_level, geocode, session, table_fields=['disability'])
    except LocationNotFound:
        disabled_or_not, total_ = LOCATIONNOTFOUND, -1
        disability = LOCATIONNOTFOUND

    total_disabled = 0
    for data, value in disabled_or_not.get('With disability', {}).iteritems():
        if data == 'numerators':
            total_disabled += value['this']

    final_data = {
        'disabled_or_not_distribution': disabled_or_not,
        'disability': disability,
        'total_disabled': {
            'name': 'Disabled',
            'numerators': {'this': total_disabled},
            'values': {'this': round(total_disabled / total_ * 100, 2)}
        },

        'total_': {
            "name": "Population",
            "values": {"this": total_}
        }
    }
    return final_data


PROFILE_SECTIONS = ['demographics', 'households', 'elections2016', 'disabilities']


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


