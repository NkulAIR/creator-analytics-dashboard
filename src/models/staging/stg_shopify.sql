-- 1:1 cleaned view of raw_shopify orders.

SELECT
    payload ->> 'id'                AS order_id,
    (payload ->> 'created_at')::timestamp AS order_date,
    (payload ->> 'total_price')::decimal  AS total_price,
    payload ->> 'financial_status'  AS financial_status,
    extracted_at
FROM raw_shopify;
