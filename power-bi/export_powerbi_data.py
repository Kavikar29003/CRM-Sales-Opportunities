import duckdb
import os

con = duckdb.connect("../crm_sales.duckdb")
output_folder = "powerbi_data"
os.makedirs(output_folder, exist_ok=True)

queries = {
    "kpi_summary": """
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

        FROM analytics_opportunities
    """,

    "sales_funnel": """
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
            END
    """,

    "monthly_revenue": """
        SELECT
            DATE_TRUNC('month', close_date) AS close_month,
            COUNT(*) AS won_opportunities,
            SUM(close_value) AS won_revenue
        FROM analytics_opportunities
        WHERE deal_stage = 'Won'
        GROUP BY close_month
        ORDER BY close_month
    """,

    "regional_performance": """
        SELECT
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

        GROUP BY regional_office

        ORDER BY regional_office
    """,

    "product_performance": """
        SELECT
            product,
            series,
            sales_price,
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

        GROUP BY product, series, sales_price

        ORDER BY won_revenue DESC
    """,

    "sector_performance": """
        SELECT
            sector,
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

        WHERE sector IS NOT NULL

        GROUP BY sector

        ORDER BY won_revenue DESC
    """,

    "sales_agent_performance": """
        SELECT
            sales_agent,
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

        GROUP BY sales_agent, manager, regional_office

        ORDER BY won_revenue DESC
    """,

    "manager_performance": """
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

        GROUP BY manager, regional_office

        ORDER BY won_revenue DESC
    """,

    "open_pipeline": """
        SELECT
            deal_stage,
            COUNT(*) AS open_opportunities,
            SUM(sales_price) AS estimated_pipeline_value,
            ROUND(AVG(sales_price), 2) AS avg_product_price

        FROM analytics_opportunities

        WHERE deal_stage IN ('Prospecting', 'Engaging')

        GROUP BY deal_stage

        ORDER BY
            CASE deal_stage
                WHEN 'Prospecting' THEN 1
                WHEN 'Engaging' THEN 2
            END
    """
}

for name, query in queries.items():
    output_path = os.path.join(output_folder, f"{name}.csv")

    con.execute(f"""
        COPY ({query})
        TO '{output_path}'
        (HEADER, DELIMITER ',')
    """)

    print(f"Created: {output_path}")

con.close()

print("\nAll Power BI datasets exported successfully.")