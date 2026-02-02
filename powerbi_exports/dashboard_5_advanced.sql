
        -- Dashboard 5: Análise Avançada (CTE)
        WITH monthly_stats AS (
            SELECT
                dd.year,
                dd.month,
                dd.month_name,
                COUNT(*) as total_crimes,
                SUM(CASE WHEN fc.is_violent THEN 1 ELSE 0 END) as violent_crimes
            FROM gold.fato_crimes fc
            JOIN gold.dim_date dd ON fc.sk_date = dd.sk_date
            GROUP BY dd.year, dd.month, dd.month_name
        ),
        monthly_avg AS (
            SELECT
                AVG(total_crimes) as avg_monthly_crimes,
                AVG(violent_crimes) as avg_monthly_violent
            FROM monthly_stats
        )
        SELECT
            ms.year,
            ms.month,
            ms.month_name,
            ms.total_crimes,
            ms.violent_crimes,
            ma.avg_monthly_crimes,
            ma.avg_monthly_violent,
            ROUND((ms.total_crimes - ma.avg_monthly_crimes) / ma.avg_monthly_crimes * 100, 2) as pct_diff_from_avg
        FROM monthly_stats ms
        CROSS JOIN monthly_avg ma
        ORDER BY ms.year, ms.month;
    