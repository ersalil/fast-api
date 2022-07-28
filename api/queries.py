def emb_data(limit):
    return f"""SELECT
            es.voyage_id,
            es.added_date,
            es.oci_completed_core,
            es.moci_completed_core,
            es.checkedin_couch,
            es.onboard_couch,
            es.expected_couch,
            SUBSTRING( v2."number", 0, 3) as code,
            v2."number" as number
            FROM
            embark_summary es
            JOIN
                voyage v2
                ON es.voyage_id = v2.voyage_id
            WHERE
            es.voyage_id IN
            (
                WITH CTE (rw, vid, eid, edate, sid, sname, scode) AS
                (
                    SELECT
                        ROW_NUMBER() OVER ( PARTITION BY v.environment_id
                    ORDER BY
                        v.embark_date DESC) RN,
                        v.voyage_id,
                        v.environment_id,
                        v.embark_date,
                        s2.ship_id,
                        s2."name",
                        s2.code
                    FROM
                        voyage v
                        JOIN
                        environment e2
                        ON v.environment_id = e2.environment_id
                        JOIN
                        ship s2
                        ON e2.ship_id = s2.ship_id
                    WHERE
                        v.environment_id IN
                        (
                        SELECT
                            environment_id
                        FROM
                            environment e
                            JOIN
                                ship s
                                ON e.ship_id = s.ship_id
                        WHERE
                            e.ship_id IS NOT NULL
                        ) 
                        AND v.embark_date < (
                        SELECT 
                            es.added_date 
                        FROM 
                            embark_summary es 
                        ORDER BY 
                            es.added_date DESC 
                        LIMIT 
                            1
                        )
                )
                SELECT
                    cte.vid
                FROM
                    cte
                WHERE
                    rw <= {limit}
            )
            ORDER BY
            es.added_date DESC"""