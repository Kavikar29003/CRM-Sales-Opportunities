SELECT
    deal_stage,
    COUNT(*) AS opportunities,
    SUM(
        CASE
            WHEN deal_stage IN ('Prospecting', 'Engaging')
            THEN sales_price
            ELSE close_value
        END
    ) AS deal_value
FROM analytics_opportunities
GROUP BY deal_stage
ORDER BY
    CASE deal_stage
        WHEN 'Prospecting' THEN 1
        WHEN 'Engaging' THEN 2
        WHEN 'Won' THEN 3
        WHEN 'Lost' THEN 4
    END;