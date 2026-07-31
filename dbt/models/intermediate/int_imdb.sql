with basics as (
    select * from {{ ref('stg_imdb_basics') }}
),

ratings as (
    select * from {{ ref('stg_imdb_ratings') }}
)

select
    b.imdb_id,
    b.title,
    b.release_year,
    b.raw_genres,
    r.imdb_score,
    r.num_votes
from basics b
inner join ratings r
    on b.imdb_id = r.imdb_id