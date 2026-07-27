with netflix as (
    select
        'Netflix' as platform,
        null as platform_id,
        content_type,
        title,
        director,
        cast_members,
        country,
        date_added,
        release_year,
        rating as age_rating,
        duration,
        listed_in as raw_genres,
        description
    from {{ ref('stg_netflix') }}
),

amazon as (
    select
        'Amazon Prime' as platform,
        show_id as platform_id,
        content_type,
        title,
        director,
        cast_members,
        country,
        date_added,
        release_year,
        rating as age_rating,
        duration,
        listed_in as raw_genres,
        description
    from {{ ref('stg_amazon_prime') }}
),

apple as (
    select
        'Apple TV' as platform,
        content_id as platform_id,
        content_type,
        title,
        null as director,
        null as cast_members,
        country,
        null as date_added,
        release_year,
        rating as age_rating,
        cast(duration_minutes as string) as duration,
        genres as raw_genres,
        description
    from {{ ref('stg_apple') }}
),

hotstar as (
    select
        'Hotstar' as platform,
        null as platform_id,
        content_type,
        title,
        null as director,
        null as cast_members,
        null as country,
        null as date_added,
        release_year,
        age_rating,
        cast(duration_minutes as string) as duration,
        genre as raw_genres,
        description
    from {{ ref('stg_hotstar') }}
),

combined as (
    select * from netflix
    union all
    select * from amazon
    union all
    select * from apple
    union all
    select * from hotstar
)

select * from combined