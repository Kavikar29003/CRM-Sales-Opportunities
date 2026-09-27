SELECT
    manager,
    regional_office,

    COUNT(*) AS total_opportunities,
    SUM(won_flag) AS won_opportunities,
    SUM(lost_flag) AS lost_opportunities,

    ROUND(
        100.0 * SUM(won_flag)
        / NULLIF(SUM(won_flag) + SUM(lost_flag), 0),
        2
    ) AS win_rate_pct,

    SUM(
        CASE
            WHEN deal_stage = 'Won'
            THEN close_value
            ELSE 0
        END
    ) AS won_revenue,

    ROUND(
        AVG(
            CASE
                WHEN deal_stage = 'Won'
                THEN close_value
            END
        ),
        2
    ) AS avg_won_deal_size

FROM analytics_opportunities

GROUP BY
    manager,
    regional_office

ORDER BY won_revenue DESC;