with all_raw_genres as (

    select
        title,
        regexp_replace(regexp_replace(raw_genres, $$[\[\]'"]$$, ''), '/', ',') as cleaned_raw_genres,
        'Streaming' as source_type
    from {{ ref('int_streaming_titles') }}
    where raw_genres is not null

    union all

    select
        title,
        regexp_replace(regexp_replace(raw_genres, $$[\[\]'"]$$, ''), '/', ',') as cleaned_raw_genres,
        'Box Office' as source_type
    from {{ ref('int_box_office') }}
    where raw_genres is not null

),

unpivoted_genres as (

    select
        title,
        source_type,
        trim(f.value::string) as raw_genre
    from all_raw_genres,
         table(flatten(input => split(cleaned_raw_genres, ','))) f

)

select distinct
    title,
    source_type,
    initcap(trim(raw_genre)) as genre
from unpivoted_genres
where trim(raw_genre) <> ''