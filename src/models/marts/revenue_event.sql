-- Unified revenue fact table: every dollar a creator earns, regardless
-- of platform, in one comparable shape. This is the reconciliation step
-- referenced in the ERD -- Shopify orders and Patreon pledges become
-- rows in the same table.

SELECT
    order_id       AS source_record_id,
    'shopify'      AS source,
    order_date::date AS event_date,
    total_price    AS amount,
    'sale'         AS event_type
FROM stg_shopify
WHERE financial_status = 'paid'

UNION ALL

SELECT
    member_id      AS source_record_id,
    'patreon'      AS source,
    last_charge_date::date AS event_date,
    pledge_amount  AS amount,
    'pledge'       AS event_type
FROM stg_patreon
WHERE patron_status = 'active_patron';
