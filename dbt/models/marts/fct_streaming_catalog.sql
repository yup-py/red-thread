{{ config(materialized='table') }}

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
    s.description
from {{ ref('int_streaming_titles') }} s
left join {{ ref('dim_content') }} c
    on lower(s.title) = lower(c.title)
   and s.content_type = c.content_type