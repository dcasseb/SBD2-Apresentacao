
        -- Dashboard 3: Análise Geográfica
        SELECT
            da.area_name,
            da.region,
            fc.latitude,
            fc.longitude,
            dct.crime_category,
            dct.crime_description,
            COUNT(*) as crime_count
        FROM gold.fato_crimes fc
        JOIN gold.dim_area da ON fc.sk_area = da.sk_area
        JOIN gold.dim_crime_type dct ON fc.sk_crime_type = dct.sk_crime_type
        WHERE fc.latitude IS NOT NULL AND fc.longitude IS NOT NULL
        GROUP BY da.area_name, da.region, fc.latitude, fc.longitude,
                 dct.crime_category, dct.crime_description;
    