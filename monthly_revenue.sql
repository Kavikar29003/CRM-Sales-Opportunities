SELECT
    DATE_TRUNC('month', close_date) AS close_month,
    COUNT(*) AS won_opportunities,
    SUM(close_value) AS won_revenue
FROM analytics_opportunities
WHERE deal_stage = 'Won'
GROUP BY close_month
ORDER BY close_month;