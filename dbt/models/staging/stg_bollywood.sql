with source as (
    select * from {{ source('raw', 'RAW_BOLLYWOOD') }}
),

renamed as (
    select
        trim(title::varchar) as title,
        coalesce(
            try_to_date(date::varchar, 'DD-MM-YYYY'),
            try_to_date(date::varchar, 'YYYY-MM-DD')
        ) as release_date,
        trim(genre::varchar) as genre,
        trim(orig_lang::varchar) as original_language,
        cast("REVENUE($)" as float) as revenue_usd,
        cast("BUDGET($)" as float) as budget_usd,
        trim(country::varchar) as country,
        cast(score as float) as imdb_score
    from source
)

select * from renamed