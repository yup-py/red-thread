with source as (
    select * from {{ source('raw', 'RAW_HOLLYWOOD') }}
),

renamed as (
    select
        trim(column_0::varchar) as title,
        try_to_date(column_1::varchar, 'DD-MM-YYYY') as release_date,
        trim(column_2::varchar) as genre,
        trim(column_3::varchar) as original_language,
        cast(column_4 as float) as revenue_usd,
        cast(column_5 as float) as budget_usd,
        trim(column_6::varchar) as country,
        cast(column_7 as float) as imdb_score
    from source
)

select * from renamed