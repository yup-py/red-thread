{#
    Reusable lookups against seed mapping tables, so no model needs its own
    hardcoded CASE statement for categorical standardization. Both fall back to
    the original trimmed value when a source produces a code we haven't mapped
    yet, so unmapped values degrade gracefully instead of becoming NULL.
#}

{% macro standardize_rating(rating_expr) %}
    coalesce(
        (
            select m.standardized_rating
            from {{ ref('seed_rating_mapping') }} m
            where m.raw_rating = lower(trim({{ rating_expr }}))
        ),
        trim({{ rating_expr }})
    )
{% endmacro %}

{% macro standardize_genre(genre_expr) %}
    coalesce(
        (
            select m.standardized_genre
            from {{ ref('seed_genre_mapping') }} m
            where m.raw_genre = lower(trim({{ genre_expr }}))
        ),
        initcap(trim({{ genre_expr }}))
    )
{% endmacro %}
