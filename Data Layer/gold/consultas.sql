-- ============================================
-- Consultas - Camada Gold
-- Crime Data Analytics (PostgreSQL)
-- ============================================

-- ============================================
-- 1. Total de crimes por área
-- ============================================
SELECT 
    da.area_name,
    da.region,
    COUNT(*) as total_crimes
FROM gold.fato_crimes fc
JOIN gold.dim_area da ON fc.sk_area = da.sk_area
GROUP BY da.area_name, da.region
ORDER BY total_crimes DESC;

-- ============================================
-- 2. Crimes por tipo e categoria
-- ============================================
SELECT 
    dct.crime_category,
    dct.crime_description,
    dct.is_violent,
    COUNT(*) as total_ocorrencias
FROM gold.fato_crimes fc
JOIN gold.dim_crime_type dct ON fc.sk_crime_type = dct.sk_crime_type
GROUP BY dct.crime_category, dct.crime_description, dct.is_violent
ORDER BY total_ocorrencias DESC;

-- ============================================
-- 3. Análise temporal - Crimes por ano e mês
-- ============================================
SELECT 
    dd.year,
    dd.month,
    dd.month_name,
    COUNT(*) as total_crimes,
    SUM(CASE WHEN fc.is_violent THEN 1 ELSE 0 END) as violent_crimes
FROM gold.fato_crimes fc
JOIN gold.dim_date dd ON fc.sk_date = dd.sk_date
GROUP BY dd.year, dd.month, dd.month_name
ORDER BY dd.year, dd.month;

-- ============================================
-- 4. Crimes por período do dia
-- ============================================
SELECT 
    dt.period_of_day,
    dt.hour,
    COUNT(*) as total_crimes
FROM gold.fato_crimes fc
JOIN gold.dim_time dt ON fc.sk_time = dt.sk_time
GROUP BY dt.period_of_day, dt.hour
ORDER BY dt.hour;

-- ============================================
-- 5. Top 10 armas mais utilizadas
-- ============================================
SELECT 
    dw.weapon_description,
    dw.weapon_category,
    dw.lethality_level,
    COUNT(*) as total_uso
FROM gold.fato_crimes fc
JOIN gold.dim_weapon dw ON fc.sk_weapon = dw.sk_weapon
WHERE dw.weapon_code IS NOT NULL
GROUP BY dw.weapon_description, dw.weapon_category, dw.lethality_level
ORDER BY total_uso DESC
LIMIT 10;

-- ============================================
-- 6. Análise de vítimas por faixa etária
-- ============================================
SELECT 
    dv.age_group,
    dv.sex,
    COUNT(*) as total_vitimas
FROM gold.fato_crimes fc
JOIN gold.dim_victim dv ON fc.sk_victim = dv.sk_victim
GROUP BY dv.age_group, dv.sex
ORDER BY total_vitimas DESC;

-- ============================================
-- 7. Crimes em finais de semana vs dias úteis
-- ============================================
SELECT 
    dd.is_weekend,
    COUNT(*) as total_crimes,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) as percentual
FROM gold.fato_crimes fc
JOIN gold.dim_date dd ON fc.sk_date = dd.sk_date
GROUP BY dd.is_weekend;

-- ============================================
-- 8. Locais mais perigosos (Premises)
-- ============================================
SELECT 
    dp.premise_description,
    dp.premise_category,
    dp.is_public,
    COUNT(*) as total_crimes
FROM gold.fato_crimes fc
JOIN gold.dim_premise dp ON fc.sk_premise = dp.sk_premise
GROUP BY dp.premise_description, dp.premise_category, dp.is_public
ORDER BY total_crimes DESC
LIMIT 20;

-- ============================================
-- 9. Mapa de calor - Crimes por localização
-- ============================================
SELECT 
    ROUND(fc.latitude::numeric, 2) as lat_group,
    ROUND(fc.longitude::numeric, 2) as lon_group,
    COUNT(*) as total_crimes
FROM gold.fato_crimes fc
WHERE fc.latitude IS NOT NULL AND fc.longitude IS NOT NULL
GROUP BY ROUND(fc.latitude::numeric, 2), ROUND(fc.longitude::numeric, 2)
ORDER BY total_crimes DESC;

-- ============================================
-- 10. Tendência anual de crimes violentos
-- ============================================
SELECT
    dd.year,
    COUNT(*) as total_crimes,
    SUM(CASE WHEN fc.is_violent THEN 1 ELSE 0 END) as violent_crimes,
    ROUND(SUM(CASE WHEN fc.is_violent THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as pct_violent
FROM gold.fato_crimes fc
JOIN gold.dim_date dd ON fc.sk_date = dd.sk_date
GROUP BY dd.year
ORDER BY dd.year;

-- ============================================
-- 11. Áreas com crimes acima da média (SUBQUERY)
-- ============================================
SELECT
    da.area_name,
    da.region,
    COUNT(*) as total_crimes,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM gold.fato_crimes), 2) as pct_total
FROM gold.fato_crimes fc
JOIN gold.dim_area da ON fc.sk_area = da.sk_area
GROUP BY da.area_name, da.region
HAVING COUNT(*) > (
    SELECT AVG(crime_count)
    FROM (
        SELECT COUNT(*) as crime_count
        FROM gold.fato_crimes
        GROUP BY sk_area
    ) subq
)
ORDER BY total_crimes DESC;

-- ============================================
-- 12. Análise temporal com CTE - Comparação mensal
-- ============================================
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
    ROUND((ms.total_crimes - ma.avg_monthly_crimes) / ma.avg_monthly_crimes * 100, 2) as pct_diff_from_avg,
    CASE
        WHEN ms.total_crimes > ma.avg_monthly_crimes THEN 'Acima da Média'
        ELSE 'Abaixo da Média'
    END as status
FROM monthly_stats ms
CROSS JOIN monthly_avg ma
ORDER BY ms.year, ms.month;

-- ============================================
-- 13. Ranking de crimes por tipo com CTE
-- ============================================
WITH crime_ranking AS (
    SELECT
        dct.crime_code,
        dct.crime_description,
        dct.crime_category,
        dct.is_violent,
        COUNT(*) as total_occurrences,
        RANK() OVER (PARTITION BY dct.crime_category ORDER BY COUNT(*) DESC) as rank_in_category,
        ROW_NUMBER() OVER (ORDER BY COUNT(*) DESC) as overall_rank
    FROM gold.fato_crimes fc
    JOIN gold.dim_crime_type dct ON fc.sk_crime_type = dct.sk_crime_type
    GROUP BY dct.crime_code, dct.crime_description, dct.crime_category, dct.is_violent
)
SELECT
    crime_category,
    crime_description,
    total_occurrences,
    rank_in_category,
    overall_rank,
    is_violent
FROM crime_ranking
WHERE rank_in_category <= 5
ORDER BY crime_category, rank_in_category;

-- ============================================
-- 14. Análise de vítimas - Perfil de risco (SUBQUERY + CTE)
-- ============================================
WITH victim_profile AS (
    SELECT
        dv.age_group,
        dv.sex,
        dv.descent,
        COUNT(*) as total_crimes,
        SUM(CASE WHEN fc.is_violent THEN 1 ELSE 0 END) as violent_crimes,
        ROUND(SUM(CASE WHEN fc.is_violent THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as violent_rate
    FROM gold.fato_crimes fc
    JOIN gold.dim_victim dv ON fc.sk_victim = dv.sk_victim
    GROUP BY dv.age_group, dv.sex, dv.descent
)
SELECT
    age_group,
    sex,
    descent,
    total_crimes,
    violent_crimes,
    violent_rate,
    CASE
        WHEN violent_rate >= (SELECT AVG(violent_rate) FROM victim_profile) * 1.5
        THEN 'Alto Risco'
        WHEN violent_rate >= (SELECT AVG(violent_rate) FROM victim_profile)
        THEN 'Risco Médio'
        ELSE 'Baixo Risco'
    END as risk_level
FROM victim_profile
WHERE total_crimes > 50
ORDER BY violent_rate DESC;

-- ============================================
-- 15. Hotspots geográficos com agregação recursiva (CTE)
-- ============================================
WITH crime_locations AS (
    SELECT
        da.area_name,
        da.region,
        ROUND(fc.latitude::numeric, 2) as lat_rounded,
        ROUND(fc.longitude::numeric, 2) as lon_rounded,
        COUNT(*) as crime_count
    FROM gold.fato_crimes fc
    JOIN gold.dim_area da ON fc.sk_area = da.sk_area
    WHERE fc.latitude IS NOT NULL AND fc.longitude IS NOT NULL
    GROUP BY da.area_name, da.region, ROUND(fc.latitude::numeric, 2), ROUND(fc.longitude::numeric, 2)
),
hotspot_classification AS (
    SELECT
        area_name,
        region,
        lat_rounded,
        lon_rounded,
        crime_count,
        NTILE(10) OVER (ORDER BY crime_count DESC) as hotspot_decile,
        CASE
            WHEN crime_count >= (SELECT PERCENTILE_CONT(0.9) WITHIN GROUP (ORDER BY crime_count) FROM crime_locations)
            THEN 'Hotspot Crítico'
            WHEN crime_count >= (SELECT PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY crime_count) FROM crime_locations)
            THEN 'Hotspot Alto'
            WHEN crime_count >= (SELECT PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY crime_count) FROM crime_locations)
            THEN 'Hotspot Médio'
            ELSE 'Área Normal'
        END as hotspot_level
    FROM crime_locations
)
SELECT
    area_name,
    region,
    lat_rounded,
    lon_rounded,
    crime_count,
    hotspot_level,
    hotspot_decile
FROM hotspot_classification
WHERE hotspot_level IN ('Hotspot Crítico', 'Hotspot Alto')
ORDER BY crime_count DESC
LIMIT 20;

-- ============================================
-- 16. Evolução temporal por região (CTE com múltiplos níveis)
-- ============================================
WITH yearly_crimes AS (
    SELECT
        dd.year,
        da.region,
        COUNT(*) as total_crimes,
        SUM(CASE WHEN fc.is_violent THEN 1 ELSE 0 END) as violent_crimes
    FROM gold.fato_crimes fc
    JOIN gold.dim_date dd ON fc.sk_date = dd.sk_date
    JOIN gold.dim_area da ON fc.sk_area = da.sk_area
    GROUP BY dd.year, da.region
),
year_over_year AS (
    SELECT
        year,
        region,
        total_crimes,
        violent_crimes,
        LAG(total_crimes) OVER (PARTITION BY region ORDER BY year) as prev_year_crimes,
        LAG(violent_crimes) OVER (PARTITION BY region ORDER BY year) as prev_year_violent
    FROM yearly_crimes
),
growth_calculation AS (
    SELECT
        year,
        region,
        total_crimes,
        violent_crimes,
        prev_year_crimes,
        prev_year_violent,
        CASE
            WHEN prev_year_crimes IS NOT NULL
            THEN ROUND((total_crimes - prev_year_crimes) * 100.0 / prev_year_crimes, 2)
            ELSE NULL
        END as yoy_growth,
        CASE
            WHEN prev_year_violent IS NOT NULL
            THEN ROUND((violent_crimes - prev_year_violent) * 100.0 / prev_year_violent, 2)
            ELSE NULL
        END as yoy_violent_growth
    FROM year_over_year
)
SELECT
    year,
    region,
    total_crimes,
    violent_crimes,
    prev_year_crimes,
    yoy_growth,
    yoy_violent_growth,
    CASE
        WHEN yoy_growth > 10 THEN 'Crescimento Alto'
        WHEN yoy_growth > 0 THEN 'Crescimento Moderado'
        WHEN yoy_growth > -10 THEN 'Decréscimo Moderado'
        WHEN yoy_growth IS NOT NULL THEN 'Decréscimo Alto'
        ELSE 'Primeiro Ano'
    END as trend
FROM growth_calculation
ORDER BY region, year;
