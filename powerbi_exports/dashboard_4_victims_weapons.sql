
        -- Dashboard 4: Perfil de Vítimas e Armas
        SELECT
            dv.age_group,
            dv.sex,
            dv.descent,
            dw.weapon_description,
            dw.weapon_category,
            dct.crime_category,
            COUNT(*) as total_crimes,
            SUM(CASE WHEN fc.is_violent THEN 1 ELSE 0 END) as violent_crimes
        FROM gold.fato_crimes fc
        JOIN gold.dim_victim dv ON fc.sk_victim = dv.sk_victim
        LEFT JOIN gold.dim_weapon dw ON fc.sk_weapon = dw.sk_weapon
        JOIN gold.dim_crime_type dct ON fc.sk_crime_type = dct.sk_crime_type
        GROUP BY dv.age_group, dv.sex, dv.descent,
                 dw.weapon_description, dw.weapon_category, dct.crime_category;
    