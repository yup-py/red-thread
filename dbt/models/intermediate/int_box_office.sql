with bollywood as (
    select
        'Bollywood' as market,
        title,
        release_date,
        extract(year from release_date) as release_year,
        genre as raw_genres,
        original_language,
        country,
        budget_usd,
        revenue_usd,
        imdb_score
    from {{ ref('stg_bollywood') }}
),

hollywood as (
    select
        'Hollywood' as market,
        title,
        release_date,
        extract(year from release_date) as release_year,
        genre as raw_genres,
        original_language,
        country,
        budget_usd,
        revenue_usd,
        imdb_score
    from {{ ref('stg_hollywood') }}
),

combined as (
    select * from bollywood
    union all
    select * from hollywood
)

select * from combined