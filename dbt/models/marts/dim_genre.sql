{{ config(materialized='table') }}

with distinct_genres as (
    select distinct
        genre
    from {{ ref('int_title_genres') }}
)

select
    dense_rank() over (order by genre) as genre_key,
    genre
from distinct_genres