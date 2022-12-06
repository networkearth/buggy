from project.transformers.transformers import BUGGY_TRANSFORMERS

EXAMPLE_RECORDS = [
    {
        'arthropod_documentation/quantity': 2,
        'arthropod_documentation/length': 3,
        '_attachments': [
            {'filename': 'dir/abugphoto.jpeg', 'id': 10},
            {'filename': 'dir/ahostphoto.jpeg', 'id': 14}
        ],
        'arthropod_documentation/arthropod_photo_1': 'abugphoto.jpeg',
        'host_documentation/host_photo': 'ahostphoto.jpeg',
        '_geolocation': [44, 45],
        'session_info/location': '44 45 0 12',
        '_id': 12345
    }
]

def test_inaturalist_field_present():
    for entry in EXAMPLE_RECORDS:
        transformed = {}
        for transformer in BUGGY_TRANSFORMERS:
            key, value = transformer(entry)
            transformed[key] = value
        assert not set([
            'images', 'instance'
        ]) - set(transformed.keys())
