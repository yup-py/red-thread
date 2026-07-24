with source as (
    select * from {{ source('raw', 'RAW_APPLE') }}
),

renamed as (
    select
        trim(id) as content_id,
        trim(title) as title,
        trim(type) as content_type,
        trim(genres) as genres,
        cast(release_year as integer) as release_year,
        trim(imdb_score) as imdb_score,
        trim(rating) as rating
    from source
)

select * from renamed