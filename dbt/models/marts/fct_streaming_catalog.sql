{{ config(materialized='table') }}

select
    md5(concat(coalesce(s.title, ''), coalesce(s.content_type, ''))) as content_key,
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