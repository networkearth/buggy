"""
Tests for mapping transforms fields
"""

def mapping_transform_test(survey, choices, page, question, expected_options):
    """
    Generic test for fields involved in mapping transforms
    """
    page = next(component for component in survey if component['name'] == page)
    assert page['type'] == 'begin_group'
    question = next(component for component in page['survey'] if component['name'] == question)
    _type, choices_key = question['type'].strip().split(' ')
    assert _type == 'select_one'
    options = set(choices[choices_key].keys())
    assert options == set(expected_options)

def test_survey(survey, choices):
    """
    Test for survey method transformer
    """
    mapping_transform_test(
        survey, choices, 'session_info', 'survey_method',
        [
            'incidental',
            'walking',
            'transect_survey',
            'area',
            'other'
        ]
    )

def test_development(survey, choices):
    """
    Test for development transformer
    """
    mapping_transform_test(
        survey, choices, 'arthropod_documentation',
        'developmental_stage',
        [
            'adult',
            'egg',
            'larva',
            'pupa',
            'nymph',
            'other'
        ]
    )

def test_activity(survey, choices):
    """
    Test for activity transformer
    """
    mapping_transform_test(
        survey, choices, 'arthropod_documentation',
        'activity',
        [
            'mating',
            'moving',
            'foraging',
            'feeding',
            'resting',
            'predator',
            'prey',
            'guarding',
            'tending',
            'other',
            'cleaning',
            'vigilant'
        ]
    )

def test_host_phenology(survey, choices):
    """
    Test for phenology transformer
    """
    mapping_transform_test(
        survey, choices, 'host_documentation',
        'host_phenology',
        [
            'initial',
            'breaking',
            'increasing',
            'flowers',
            'fruiting',
            'mature',
            'other'
        ]
    )

def test_arthropod_taxa(survey, choices):
    """
    Test for arthropod taxa transformer
    """
    mapping_transform_test(
        survey, choices, 'arthropod_documentation',
        'arthropod_group',
        [
            'aphidomorpha',
            'araneae',
            'blattodea',
            'cicadomorpha',
            'coleoptera',
            'diptera',
            'hemiptera',
            'hymenoptera_1',
            'hymenoptera_2',
            'lepidoptera',
            'opiliones',
            'trichoptera',
            'odonata',
            'orthoptera',
            'other',
            'unidentified'
        ]
    )

def test_host_taxa(survey, choices):
    """
    Test for host taxa transformer
    """
    mapping_transform_test(
        survey, choices, 'host_documentation',
        'host_group',
        [
            'angiospermae',
            'bryophyta',
            'fungi',
            'pinopsida',
            'poales',
            'polypodiopsida',
            'unidentified',
            'other'
        ]
    )
