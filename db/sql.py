app_setting = """SELECT
                    value
                FROM
                    application_setting
                WHERE
                    application_setting_id = 'da1dfaf2-1989-4071-b01c-47ad2a6b559a'"""

ship_data = """SELECT
                    ship.name,
                    ship.code
                FROM
                    ship"""

def embarkData(limit: int):
    return f"""SELECT
                es.voyage_id,
                es.added_date,
                es.oci_completed_core,
                es.moci_completed_core,
                es.checkedin_couch,
                es.onboard_couch,
                es.expected_couch,
                SUBSTRING(v2."number", 0, 3) as code,
                v2."number" as number
            FROM
                embark_summary es
                JOIN voyage v2 ON es.voyage_id = v2.voyage_id
            WHERE
                es.voyage_id IN (
                    WITH CTE (rw, vid) AS (
                        SELECT
                            ROW_NUMBER() OVER (
                                PARTITION BY v.environment_id
                                ORDER BY
                                    v.embark_date DESC
                            ) RN,
                            v.voyage_id
                        FROM
                            voyage v
                            JOIN environment e2 ON v.environment_id = e2.environment_id
                            JOIN ship s2 ON e2.ship_id = s2.ship_id
                        WHERE
                            v.environment_id IN (
                                SELECT
                                    environment_id
                                FROM
                                    environment e
                                    JOIN ship s ON e.ship_id = s.ship_id
                                WHERE
                                    e.ship_id IS NOT NULL
                            )
                            AND v.embark_date < NOW()
                    )
                    SELECT
                        cte.vid
                    FROM
                        cte
                    WHERE
                        rw <= {limit}
                )
                AND es.added_date <= (
                    SELECT
                        (v3.embark_date + interval '1 day')
                    FROM
                        voyage v3
                    WHERE
                        v3.voyage_id = es.voyage_id
                )
                AND es.checkedin_couch > 0
            ORDER BY
                es.added_date DESC"""