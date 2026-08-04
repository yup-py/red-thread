with source as (
    select * from {{ source('raw', 'RAW_HOTSTAR') }}
),

renamed as (
    select
        trim(title) as title,
        case
            when lower(trim(type)) = 'movie' then 'Movie'
            when lower(trim(type)) = 'tv' then 'TV Show'
            else initcap(trim(type))
        end as content_type,
        cast(year as integer) as release_year,
        trim(genre) as genre,
        trim(age_rating) as age_rating,
        cast(running_time as integer) as duration_minutes,
        trim(description) as description
    from source
)

select * from renamed