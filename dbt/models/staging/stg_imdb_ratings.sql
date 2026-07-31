select
    tconst as imdb_id,
    averagerating::float as imdb_score,
    numvotes::integer as num_votes
from {{ source('raw', 'raw_imdb_ratings') }}