"""
Transformers for turning Kobo data into iNaturalist data
"""

from functools import partial

OBSERVATION_FIELD_IDS = {
    "EwA - Arthropod Developmental Stage": 15639,
    "EwA - Behavior Observed": 12551,
    "EwA - Host Documentation": 12550,
    "EwA - Length": 15607,
    "EwA - Observation Effort-time": 12553,
    "EwA - Plant Phenology": 14016,
    "EwA - Quantity": 12629,
    "EwA - Survey Method": 12552,
    "EwA - Wet Host": 16032,
}

# pylint: disable=unused-argument
def mapping_transform(
    entry_key: str, output_key: str, mapping: dict,
    default, entry: dict, **kwargs
) -> tuple:
    """
    Maps one value from kobo into a value for iNaturalist
    """
    return output_key, mapping.get(entry.get(entry_key), default)

# pylint: disable=unused-argument,redefined-builtin
def convert_key_transform(
    entry_key: str, output_key: str, type,
    default, entry: dict, **kwargs
) -> tuple:
    """
    Just updates the key that will be seen by iNaturalist
    """
    return output_key, type(entry.get(entry_key, default))

survey_transform = partial(
    mapping_transform,
    "session_info/survey_method",
    OBSERVATION_FIELD_IDS["EwA - Survey Method"],
    {
        "incidental": "Opportunistic encounter",
        "walking": "Semi-structured survey",
        "transect_survey": "Transect survey",
        "area": "Area search",
        "other": "Other"
    },
    "Other"
)

development_transform = partial(
    mapping_transform,
    "arthropod_documentation/developmental_stage",
    OBSERVATION_FIELD_IDS["EwA - Arthropod Developmental Stage"],
    {
        "adult": "Adult",
        "egg": "Egg or eggsac",
        "larva": "Larva or caterpillar",
        "pupa": "Pupa",
        "nymph": "Nymph",
        "other": "Other"
    },
    "null"
)

activity_transform = partial(
    mapping_transform,
    "arthropod_documentation/activity",
    OBSERVATION_FIELD_IDS["EwA - Behavior Observed"],
    {
        "mating": "Mating",
        "moving": "Moving",
        "foraging": "Foraging",
        "feeding": "Feeding",
        "resting": "Resting",
        "predator": "Preying",
        "prey": "Preyed upon",
        "guarding": "Guarding eggs or younglings",
        "tending": "Tending",
        "other": "Other",
        "cleaning": "Cleaning",
        "vigilant": "Vigilant"
    },
    "null"
)

host_phenology_transform = partial(
    mapping_transform,
    "host_documentation/host_phenology",
    OBSERVATION_FIELD_IDS["EwA - Plant Phenology"],
    {
        "initial": "Initial growth",
        "breaking": "Breaking leaf buds",
        "increasing": "Increasing leaf size",
        "flowers": "Flowers",
        "fruiting": "Fruits",
        "mature": "Leaves",
        "other": "Other"
    },
    "null"
)

effort_transform = partial(
    convert_key_transform,
    "session_info/Survey_duration",
    OBSERVATION_FIELD_IDS["EwA - Observation Effort-time"],
    float,
    None
)

quantity_transform = partial(
    convert_key_transform,
    "arthropod_documentation/quantity",
    OBSERVATION_FIELD_IDS["EwA - Quantity"],
    float,
    None
)

length_transform = partial(
    convert_key_transform,
    "arthropod_documentation/length",
    OBSERVATION_FIELD_IDS["EwA - Length"],
    float,
    None
)

wetness_transform = partial(
    convert_key_transform,
    "host_documentation/wet_support",
    OBSERVATION_FIELD_IDS["EwA - Wet Host"],
    str,
    None
)

INAT_ARTHROPOD_TAXA_IDS = {
    "aphidomorpha": 901813,
    "araneae": 47118,
    "blattodea": 81769,
    "cicadomorpha": 372849,
    "coleoptera": 47208,
    "diptera": 47822,
    "hemiptera": 47744,
    "hymenoptera_1": 47201,
    "hymenoptera_2": 47336,
    "lepidoptera": 47157,
    "opiliones": 47367,
    "trichoptera": 62164,
    "odonata": 47792,
    "orthoptera": 47651,
    "other": 47120,
    "unidentified": 47120,
}
arthropod_taxa_transform = partial(
    mapping_transform,
    "arthropod_documentation/arthropod_group",
    "taxa",
    INAT_ARTHROPOD_TAXA_IDS,
    None
)

INAT_HOST_TAXA_IDS = {
    "angiospermae": 47125,
    "bryophyta": 311249,
    "fungi": 47170,
    "pinopsida": 136329,
    "poales": 47162,
    "polypodiopsida": 121943,
}
host_taxa_transform = partial(
    mapping_transform,
    "host_documentation/host_group",
    OBSERVATION_FIELD_IDS["EwA - Host Documentation"],
    INAT_HOST_TAXA_IDS,
    None
)

OBSERVATION_FIELD_TRANSFORMERS = [
    survey_transform,
    development_transform,
    activity_transform,
    host_phenology_transform,
    quantity_transform,
    length_transform,
    wetness_transform,
    host_taxa_transform
]

def observation_field_transformer(transformers: list, entry: dict, **kwargs) -> tuple:
    """
    Builds the observation field list
    """
    observation_fields = {}
    for transformer in transformers:
        key, value = transformer(entry, **kwargs)
        observation_fields[key] = value
    return "observation_fields", observation_fields

def extract_kobo_image_root(file_name: str) -> str:
    """
    Gets the root file and replaces whitespace with underscores
    """
    root = file_name.split("/")[-1]
    return '_'.join([e for e in root.split(' ') if e])

# pylint: disable=unused-argument
def image_transformer(image_fields, entry: dict, **kwargs) -> tuple:
    """
    Builds the image list
    """
    attachments = {
        extract_kobo_image_root(info["filename"]): info
        for info in entry["_attachments"]
    }
    order = [
        extract_kobo_image_root(entry[field])
        for field in image_fields
        if entry.get(field)
    ]
    image_info = [
        attachments[filename]["id"]
        for filename in order
    ]
    return "images", image_info

# pylint: disable=unused-argument
def longitude_transform(entry: dict, **kwargs) -> tuple:
    """
    Gets longitude
    """
    return 'longitude', entry['_geolocation'][1]

# pylint: disable=unused-argument
def latitude_transform(entry: dict, **kwargs) -> tuple:
    """
    Gets latitude
    """
    return 'latitude', entry['_geolocation'][0]

# pylint: disable=unused-argument
def accuracy_transform(entry: dict, **kwargs) -> tuple:
    """
    Gets positional accuracy
    """
    return 'positional_accuracy', float(entry['session_info/location'].strip().split(' ')[-1])

# pylint: disable=unused-argument
def notes_transform(sections: dict, order: list, entry: dict, **kwargs) -> tuple:
    """
    Gets the notes from the various free form
    text inputs
    """

    assert set(sections) == set(order)

    notes = ""
    for field in order:
        header = sections[field]
        if field in entry:
            notes += "\n".join([
                header,
                entry[field],
                "", ""
            ])
    return "notes", notes.strip()

# pylint: disable=unused-argument
def is_valid_transform(entry: dict, **kwargs) -> tuple:
    """
    Determines whether this record has been
    marked as valid in kobo
    """
    return (
        "is_valid",
        entry.get("_validation_status", {}).get("uid")
        == "validation_status_approved"
    )

BUGGY_TRANSFORMERS = [
    partial(observation_field_transformer, OBSERVATION_FIELD_TRANSFORMERS),
    partial(
        image_transformer,
        [
            "arthropod_documentation/arthropod_photo_1",
            "arthropod_documentation/arthropod_photo_2",
            "arthropod_documentation/arthropod_photo_3",
            "host_documentation/host_photo"
        ]
    ),
    longitude_transform,
    latitude_transform,
    accuracy_transform,
    partial(
        convert_key_transform,
        "session_info/survey_ts",
        "ts",
        str,
        None
    ),
    partial(
        convert_key_transform,
        "session_info/input_email",
        "email",
        str,
        None
    ),
    partial(
        notes_transform,
        {
            "session_info/survey_method_other": "Survey Method:",
            "arthropod_documentation/arthropod_group_other": "Arthropod Identification:",
            "arthropod_documentation/developmental_stage_other": "Development Stage:",
            "arthropod_documentation/activity_other": "Behavior:",
            "arthropod_documentation/arthropod_more": "Arthropod Notes:",
            "host_documentation/host_group_other": "Host Identification",
            "host_documentation/host_phenology_other": "Host Phenology",
            "host_documentation/host_more": "Host Notes"
        },
        [
            "session_info/survey_method_other",
            "arthropod_documentation/arthropod_group_other",
            "arthropod_documentation/developmental_stage_other",
            "arthropod_documentation/activity_other",
            "arthropod_documentation/arthropod_more",
            "host_documentation/host_group_other",
            "host_documentation/host_phenology_other",
            "host_documentation/host_more"
        ]
    ),
    arthropod_taxa_transform,
    partial(
        convert_key_transform,
        "_id", "instance", int, None
    ),
    is_valid_transform
]
