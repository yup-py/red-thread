with source as (
    select * from {{ source('raw', 'RAW_HOTSTAR') }}
),

renamed as (
    select
        trim(title) as title,
        trim(type) as content_type,
        cast(year as integer) as release_year,
        trim(genre) as genre,
        trim(age_rating) as age_rating,
        trim(seasons) as seasons,
        trim(description) as description
    from source
)

select * from renamed