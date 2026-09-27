CREATE OR REPLACE TABLE clean_sales_pipeline AS
SELECT
    opportunity_id,
    sales_agent,
    CASE
        WHEN product = 'GTXPro' THEN 'GTX Pro'
        ELSE product
    END AS product,
    account,
    deal_stage,
    engage_date,
    close_date,
    close_value
FROM raw_sales_pipeline;