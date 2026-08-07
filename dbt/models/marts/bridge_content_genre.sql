{{ config(materialized='table') }}

with content_genre as (
    select distinct
        c.content_key,
        g.genre_key
    from {{ ref('int_title_genres') }} tg
    inner join {{ ref('dim_content') }} c
        on lower(tg.title) = lower(c.title)
    inner join {{ ref('dim_genre') }} g
        on tg.genre = g.genre
)

select
    content_key,
    genre_key
from content_genre
