{{ config(materialized='table') }}

select
    md5(concat(coalesce(b.title, ''), 'Movie')) as content_key,
    b.market,
    b.title,
    b.release_date,
    b.release_year,
    b.original_language,
    b.country,
    b.budget_usd,
    b.revenue_usd,
    case
        when b.budget_usd > 0 and b.revenue_usd is not null
        then round((b.revenue_usd - b.budget_usd) / b.budget_usd, 2)
        else null
    end as roi,
    b.imdb_score
from {{ ref('int_box_office') }} b