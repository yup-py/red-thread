{{ config(materialized='table') }}

with genres as (
    select distinct
        genre
    from {{ ref('int_title_genres') }}
)

select
    md5(genre) as genre_key,
    genre
from genres