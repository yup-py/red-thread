{{ config(materialized='table') }}

-- int_imdb can have multiple titles sharing the same (title, release_year)
-- for homonyms/remakes. Joining directly on that pair would fan out this
-- fact and duplicate budget_usd/revenue_usd. Pick the best-attested IMDb
-- match per (title, release_year) -- highest vote count -- before joining.
with imdb_deduped as (
    select *
    from {{ ref('int_imdb') }}
    qualify row_number() over (
        partition by lower(title), release_year
        order by num_votes desc nulls last
    ) = 1
)

select
    c.content_key,
    b.market,
    b.title,
    b.release_date,
    b.release_year,
    b.original_language,
    b.budget_usd,
    b.revenue_usd,
    case
        when b.budget_usd > 0 and b.revenue_usd is not null
        then round((b.revenue_usd - b.budget_usd) / b.budget_usd, 4)
        else null
    end as roi,
    i.imdb_score,
    i.num_votes
from {{ ref('int_box_office') }} b
left join {{ ref('dim_content') }} c
    on lower(b.title) = lower(c.title)
   and c.content_type = 'Movie'
left join imdb_deduped i
    on lower(b.title) = lower(i.title)
   and b.release_year = i.release_year