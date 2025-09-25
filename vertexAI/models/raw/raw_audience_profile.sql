SELECT * 
FROM {{ source('campaign_data', 'test_master_customer_profilingv3')}} 
WHERE preferred_store_postcode IS NOT NULL
LIMIT 1000
