SELECT
    deal_stage,
    COUNT(*) AS opportunities,

    CASE
        WHEN deal_stage = 'Won'
            THEN SUM(close_value)

        WHEN deal_stage IN ('Prospecting', 'Engaging')
            THEN SUM(sales_price)

        ELSE 0
    END AS value

FROM analytics_opportunities

GROUP BY deal_stage

ORDER BY
    CASE deal_stage
        WHEN 'Prospecting' THEN 1
        WHEN 'Engaging' THEN 2
        WHEN 'Won' THEN 3
        WHEN 'Lost' THEN 4
    END;