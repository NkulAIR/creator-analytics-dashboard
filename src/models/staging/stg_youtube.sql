-- 1:1 cleaned view of raw_youtube: pull fields out of the JSONB payload,
-- cast types, rename to consistent snake_case. No business logic here.

SELECT
    payload ->> 'video_id'          AS video_id,
    payload ->> 'title'             AS title,
    (payload ->> 'published_at')::timestamp AS published_at,
    (payload -> 'statistics' ->> 'viewCount')::int    AS view_count,
    (payload -> 'statistics' ->> 'likeCount')::int    AS like_count,
    (payload -> 'statistics' ->> 'commentCount')::int AS comment_count,
    extracted_at
FROM raw_youtube;
