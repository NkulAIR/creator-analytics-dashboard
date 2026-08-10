-- 1:1 cleaned view of raw_patreon members/pledges.

SELECT
    payload ->> 'id'                       AS member_id,
    (payload -> 'attributes' ->> 'pledge_amount_cents')::int / 100.0 AS pledge_amount,
    (payload -> 'attributes' ->> 'last_charge_date')::timestamp      AS last_charge_date,
    payload -> 'attributes' ->> 'patron_status' AS patron_status,
    extracted_at
FROM raw_patreon;
