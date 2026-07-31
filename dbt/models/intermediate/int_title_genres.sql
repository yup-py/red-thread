with all_raw_genres as (
    select
        title,
        regexp_replace(raw_genres, $$[\[\]'"]$$, '') as cleaned_raw_genres,
        'Streaming' as source_type
    from {{ ref('int_streaming_titles') }}
    where raw_genres is not null

    union all

    select
        title,
        regexp_replace(raw_genres, $$[\[\]'"]$$, '') as cleaned_raw_genres,
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
),

cleaned_genres as (
    select
        title,
        source_type,
        case
            when lower(trim(raw_genre)) in ('comedies', 'comedy movies', 'tv comedies', 'comedy') then 'Comedy'
            when lower(trim(raw_genre)) in ('dramas', 'drama movies', 'tv dramas', 'drama') then 'Drama'
            when lower(trim(raw_genre)) in ('action & adventure', 'tv action & adventure', 'action') then 'Action & Adventure'
            when lower(trim(raw_genre)) in ('docuseries', 'documentaries', 'documentation', 'documentary') then 'Documentary'
            when lower(trim(raw_genre)) in ('horror movies', 'tv horror', 'horror') then 'Horror'
            when lower(trim(raw_genre)) in ('romantic movies', 'romantic tv shows', 'romance') then 'Romance'
            when lower(trim(raw_genre)) in ('thriller', 'thrillers') then 'Thriller'
            when lower(trim(raw_genre)) in ('family', 'family movies', 'kids') then 'Family & Kids'
            when lower(trim(raw_genre)) in ('unknown', '') then null
            else initcap(trim(raw_genre))
        end as genre
    from unpivoted_genres
)

select distinct
    title,
    source_type,
    genre
from cleaned_genres
where genre is not null and genre != ''