with source as (
    select * from {{ source('raw', 'RAW_BOLLYWOOD') }}
),

renamed as (
    select
        trim(movie_name) as title,
        cast(year as integer) as release_year,
        trim(genre) as genre,
        trim(director) as director,
        trim(lead_star) as lead_star,
        try_cast(imdb_rating as float) as imdb_rating
    from source
)

select * from renamed