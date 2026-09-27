CREATE OR REPLACE TABLE analytics_opportunities AS
SELECT
    p.opportunity_id,
    p.sales_agent,
    t.manager,
    t.regional_office,

    p.account,
    a.sector,
    a.office_location,
    a.revenue AS account_revenue,
    a.employees AS account_employees,
    a.year_established,

    p.product,
    pr.series,
    pr.sales_price,

    p.deal_stage,
    p.engage_date,
    p.close_date,
    p.close_value,

    CASE
        WHEN p.deal_stage = 'Won' THEN 1
        ELSE 0
    END AS won_flag,

    CASE
        WHEN p.deal_stage = 'Lost' THEN 1
        ELSE 0
    END AS lost_flag,

    CASE
        WHEN p.deal_stage IN ('Prospecting', 'Engaging') THEN 1
        ELSE 0
    END AS open_flag,

    CASE
        WHEN p.engage_date IS NOT NULL
         AND p.close_date IS NOT NULL
        THEN DATE_DIFF('day', p.engage_date, p.close_date)
        ELSE NULL
    END AS sales_cycle_days

FROM clean_sales_pipeline p

LEFT JOIN clean_accounts a
    ON p.account = a.account

LEFT JOIN clean_products pr
    ON p.product = pr.product

LEFT JOIN clean_sales_teams t
    ON p.sales_agent = t.sales_agent;