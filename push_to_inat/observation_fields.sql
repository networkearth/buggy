delete from observation_fields where id in (
    15639,
    12551,
    12550,
    15607,
    12553,
    14016,
    12629,
    12552,
    16032
);
insert into observation_fields (
	id,
	name,
	datatype,
	user_id
)
values 
(
	15639,
	'EwA - Arthropod Developmental Stage',
	'text',
	1
),
(
    12551,
    'EwA - Behavior Observed',
    'text',
    1
),
(
    12550,
    'EwA - Host Documentation',
    'taxon',
    1
),
(
    15607,
    'EwA - Length',
    'numeric',
    1
),
(
    12553,
    'EwA - Observation Effort-time',
    'numeric',
    1
),
(
    14016,
    'EwA - Plant Phenology',
    'text',
    1
),
(
    12629,
    'EwA - Quantity',
    'numeric',
    1
),
(
    12552,
    'EwA - Survey Method',
    'text',
    1
),
(
    16032,
    'EwA - Wet Host',
    'text',
    1
)