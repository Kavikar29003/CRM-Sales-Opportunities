SELECT
    deal_stage,

    COUNT(*) AS open_opportunities,

    SUM(sales_price) AS estimated_pipeline_value,

    ROUND(
        AVG(sales_price),
        2
    ) AS avg_product_price

FROM analytics_opportunities

WHERE deal_stage IN ('Prospecting', 'Engaging')

GROUP BY deal_stage

ORDER BY
    CASE deal_stage
        WHEN 'Prospecting' THEN 1
        WHEN 'Engaging' THEN 2
    END;