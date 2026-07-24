with source as (
    select * from {{ source('raw', 'RAW_HOLLYWOOD') }}
),

renamed as (
    select
        trim(column_0) as title,
        cast(column_1 as integer) as release_year,
        trim(column_2) as genre,
        trim(column_3) as director,
        trim(column_4) as lead_star,
        try_cast(column_5 as float) as imdb_rating
    from source
)

select * from renamed