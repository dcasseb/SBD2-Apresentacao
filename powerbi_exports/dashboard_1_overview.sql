
        -- Dashboard 1: Visão Geral
        SELECT
            da.area_name,
            da.region,
            COUNT(*) as total_crimes,
            SUM(CASE WHEN fc.is_violent THEN 1 ELSE 0 END) as violent_crimes,
            ROUND(SUM(CASE WHEN fc.is_violent THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as violent_rate
        FROM gold.fato_crimes fc
        JOIN gold.dim_area da ON fc.sk_area = da.sk_area
        GROUP BY da.area_name, da.region
        ORDER BY total_crimes DESC;
    