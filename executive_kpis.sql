SELECT
    COUNT(*) AS total_opportunities,

    SUM(
        CASE
            WHEN deal_stage = 'Won'
            THEN close_value
            ELSE 0
        END
    ) AS won_revenue,

    SUM(
        CASE
            WHEN deal_stage IN ('Prospecting', 'Engaging')
            THEN sales_price
            ELSE 0
        END
    ) AS open_pipeline_value,

    ROUND(
        100.0 * SUM(won_flag)
        / NULLIF(SUM(won_flag) + SUM(lost_flag), 0),
        2
    ) AS win_rate_pct,

    ROUND(
        AVG(
            CASE
                WHEN deal_stage = 'Won'
                THEN close_value
            END
        ),
        2
    ) AS avg_won_deal_size,

    ROUND(
        AVG(
            CASE
                WHEN deal_stage IN ('Won', 'Lost')
                THEN sales_cycle_days
            END
        ),
        2
    ) AS avg_sales_cycle_days,

    SUM(
        CASE
            WHEN deal_stage IN ('Prospecting', 'Engaging')
            THEN 1
            ELSE 0
        END
    ) AS open_opportunities

FROM analytics_opportunities;