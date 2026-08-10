-- Unified engagement fact table. Only YouTube feeds this for now --
-- unpivoted so views/likes/comments are comparable rows, making it easy
-- to add another engagement source (e.g. Twitch) later without changing
-- the shape.

SELECT video_id AS source_record_id, 'youtube' AS source, published_at::date AS event_date, 'views' AS metric_name, view_count AS metric_value FROM stg_youtube
UNION ALL
SELECT video_id AS source_record_id, 'youtube' AS source, published_at::date AS event_date, 'likes' AS metric_name, like_count AS metric_value FROM stg_youtube
UNION ALL
SELECT video_id AS source_record_id, 'youtube' AS source, published_at::date AS event_date, 'comments' AS metric_name, comment_count AS metric_value FROM stg_youtube;
