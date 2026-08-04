{{ config(materialized='table') }}

-- Same logic as fct_box_office: int_imdb can have multiple titles sharing
-- the same (title, release_year) for homonyms/remakes. Dedup to the
-- highest-vote match before joining so this fact is never fanned out.
with imdb_deduped as (
    select *
    from {{ ref('int_imdb') }}
    qualify row_number() over (
        partition by lower(title), release_year
        order by num_votes desc nulls last
    ) = 1
)

select
    c.content_key,
    s.platform,
    s.platform_id,
    s.title,
    s.content_type,
    s.director,
    s.country,
    s.date_added,
    s.release_year,
    s.age_rating,
    s.duration,
    s.description,
    i.imdb_score
from {{ ref('int_streaming_titles') }} s
left join {{ ref('dim_content') }} c
    on lower(s.title) = lower(c.title)
   and s.content_type = c.content_type
left join imdb_deduped i
    on lower(s.title) = lower(i.title)
   and s.release_year = i.release_year