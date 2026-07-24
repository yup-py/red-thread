with source as (
    select * from {{ source('raw', 'RAW_AMAZON_PRIME') }}
),

renamed as (
    select
        trim(show_id) as show_id,
        trim(type) as content_type,
        trim(title) as title,
        trim(director) as director,
        trim("cast") as cast_members,
        trim(country) as country,
        try_to_date(date_added, 'Month DD, YYYY') as date_added,
        cast(release_year as integer) as release_year,
        trim(rating) as rating,
        trim(duration) as duration,
        trim(listed_in) as listed_in,
        trim(description) as description
    from source
)

select * from renamed