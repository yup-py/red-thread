{{ config(materialized='table') }}

-- Bridge (junction) table resolving the many-to-many relationship between
-- content and genre. A title can carry several genres, but fact tables must
-- stay at the content grain -- filtering by genre in Power BI should go
-- fct_* -> dim_content -> bridge_content_genre -> dim_genre, which never
-- fans out fct_box_office / fct_streaming_catalog measures, since those
-- still join to dim_content 1:1 on content_key.

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
