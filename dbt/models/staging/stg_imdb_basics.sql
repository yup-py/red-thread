select
    tconst as imdb_id,
    primarytitle as title,
    try_cast(startyear as integer) as release_year,
    genres as raw_genres
from {{ source('raw', 'raw_imdb_basics') }}
where titletype in ('movie', 'tvMovie')