{{ config(materialized='table') }}

with streaming as (
    select distinct
        title,
        content_type,
        release_year,
        age_rating,
        description
    from {{ ref('int_streaming_titles') }}
),

box_office as (
    select distinct
        title,
        'Movie' as content_type,
        release_year,
        null as age_rating,
        null as description
    from {{ ref('int_box_office') }}
),

unified as (
    select * from streaming
    union
    select * from box_office
),

deduped as (
    select
        title,
        content_type,
        release_year,
        age_rating,
        description
    from unified
    qualify row_number() over (
        partition by lower(title), content_type 
        order by release_year desc nulls last, age_rating nulls last, description nulls last
    ) = 1
)

select
    row_number() over (order by lower(title), content_type) as content_key,
    title,
    content_type,
    release_year,
    age_rating,
    description
from deduped