with all_raw_genres as (
    select
        title,
        raw_genres,
        'Streaming' as source_type
    from {{ ref('int_streaming_titles') }}
    where raw_genres is not null

    union all

    select
        title,
        raw_genres,
        'Box Office' as source_type
    from {{ ref('int_box_office') }}
    where raw_genres is not null
),

unpivoted_genres as (
    select
        title,
        source_type,
        trim(f.value::string) as genre
    from all_raw_genres,
    table(flatten(input => split(raw_genres, ','))) f
)

select distinct
    title,
    source_type,
    genre
from unpivoted_genres
where genre is not null and genre != ''