"""
Tests for convert key transforms fields
"""

def convert_key_transform_test(survey, page, question, allowed_types):
    """
    Generic test for fields involved in convert key transforms
    """
    page = next(component for component in survey if component['name'] == page)
    assert page['type'] == 'begin_group'
    question = next(component for component in page['survey'] if component['name'] == question)
    assert question['type'] in allowed_types

def test_effort(survey):
    """
    Test for effort transformer
    """
    convert_key_transform_test(
        survey, 'session_info', 'Survey_duration',
        allowed_types=('integer',)
    )
    assert False

def test_quantity(survey):
    """
    Test for quantity transformer
    """
    convert_key_transform_test(
        survey, 'arthropod_documentation', 'quantity',
        allowed_types=('integer',)
    )

def test_length(survey):
    """
    Test for length transformer
    """
    convert_key_transform_test(
        survey, 'arthropod_documentation', 'length',
        allowed_types=('integer',)
    )

def test_wet_support(survey, choices):
    """
    Test for wet support transformer
    """
    convert_key_transform_test(
        survey, 'host_documentation', 'wet_support',
        allowed_types=('select_one yes_no',)
    )
    assert 'yes_no' in choices
    assert set(['yes', 'no']) == set(choices['yes_no'].keys())

def test_time(survey):
    """
    Test for time transformer
    """
    convert_key_transform_test(
        survey, 'session_info', 'survey_ts',
        allowed_types=('datetime',)
    )

def test_email(survey):
    """
    Test for email transformer
    """
    convert_key_transform_test(
        survey, 'session_info', 'input_email',
        allowed_types=('text',)
    )
