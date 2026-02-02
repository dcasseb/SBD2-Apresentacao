
        -- Dashboard 2: Análise Temporal
        SELECT
            dd.year,
            dd.month,
            dd.month_name,
            dd.day_of_week,
            dd.is_weekend,
            dt.hour,
            dt.period_of_day,
            COUNT(*) as total_crimes,
            SUM(CASE WHEN fc.is_violent THEN 1 ELSE 0 END) as violent_crimes
        FROM gold.fato_crimes fc
        JOIN gold.dim_date dd ON fc.sk_date = dd.sk_date
        JOIN gold.dim_time dt ON fc.sk_time = dt.sk_time
        GROUP BY dd.year, dd.month, dd.month_name, dd.day_of_week, dd.is_weekend,
                 dt.hour, dt.period_of_day
        ORDER BY dd.year, dd.month, dt.hour;
    