"""
Tests for misc transforms fields
"""

def get_question(survey, page, question):
    """
    Grabs a specific question from the survey info
    """
    page = next(component for component in survey if component['name'] == page)
    assert page['type'] == 'begin_group'
    return next(component for component in page['survey'] if component['name'] == question)

def test_accuracy(survey):
    """
    Test for accuracy transformer
    """
    question = get_question(
        survey, 'session_info', 'location'
    )
    assert question['type'] == 'geopoint'

def test_notes(survey):
    """
    Test for notes transformer
    """
    paths = [
        'session_info/survey_method_other',
        'arthropod_documentation/arthropod_group_other',
        'arthropod_documentation/developmental_stage_other',
        'arthropod_documentation/activity_other',
        'arthropod_documentation/arthropod_more',
        'host_documentation/host_group_other',
        'host_documentation/host_phenology_other',
        'host_documentation/host_more'
    ]
    for path in paths:
        page, question = path.split('/')
        question = get_question(survey, page, question)
        assert question['type'] == 'text'

def test_image(survey):
    """
    Test for image transformer
    """
    paths = [
        'arthropod_documentation/arthropod_photo_1',
        'arthropod_documentation/arthropod_photo_2',
        'arthropod_documentation/arthropod_photo_3',
        'host_documentation/host_photo'
    ]
    for path in paths:
        page, question = path.split('/')
        question = get_question(survey, page, question)
        assert question['type'] == 'image'
