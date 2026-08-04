with source as (
    select * from {{ source('raw', 'RAW_APPLE') }}
),

renamed as (
    select
        trim(id) as content_id,
        trim(title) as title,
        case
            when upper(trim(type)) = 'MOVIE' then 'Movie'
            when upper(trim(type)) = 'SHOW' then 'TV Show'
            else initcap(trim(type))
        end as content_type,
        trim(description) as description,
        cast(release_year as integer) as release_year,
        trim(age_certification) as rating,
        cast(runtime as integer) as duration_minutes,
        trim(genres) as genres,
        trim(production_countries) as country,
        cast(seasons as integer) as seasons,
        trim(imdb_id) as imdb_id,
        cast(imdb_score as float) as imdb_score,
        cast(imdb_votes as integer) as imdb_votes,
        cast(tmdb_popularity as float) as tmdb_popularity,
        cast(tmdb_score as float) as tmdb_score
    from source
)

select * from renamed