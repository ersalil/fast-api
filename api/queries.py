
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
                WITH CTE (rw, vid) AS
                (
                    SELECT
                        ROW_NUMBER() OVER ( PARTITION BY v.environment_id
                    ORDER BY
                        v.embark_date DESC) RN,
                        v.voyage_id
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
                        AND v.embark_date < NOW()

                )
                SELECT
                    cte.vid
                FROM
                    cte
                WHERE
                    rw <= {limit}
            )
            and es.added_date <= (select (v3.embark_date + interval '1 day') from voyage v3 where v3.voyage_id = es.voyage_id)
            and es.checkedin_couch > 0
            ORDER BY
            es.added_date DESC"""


def emb_data_bar(limit):
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


def voyage_data():
    return f"""With CTE (rw, vid, eid, edate, ddate, sid, sname, scode) AS (
        select row_number() over ( partition by v.environment_id order by v.embark_date desc) RN , v.voyage_id, v.environment_id, v.embark_date, v.debark_date , s2.ship_id , s2."name", s2.code
        from voyage v join environment e2  on v.environment_id = e2.environment_id join ship s2 on e2.ship_id = s2.ship_id
        where v.environment_id in
        (select environment_id from environment e join ship s on e.ship_id = s.ship_id where e.ship_id is not null) and v.embark_date < (select es.added_date  from embark_summary es order by es.added_date desc limit 1)
    )
Select cte.vid, cte.edate, cte.ddate from cte where rw <=10"""

def getAppLimit():
    return f"""select value from application_setting where application_setting_id = 'da1dfaf2-1989-4071-b01c-47ad2a6b559a'"""

def a(vid, start, end):
    return f"""select es2.voyage_id , es2.added_date , es2.checkedin_couch , es2.onboard_couch , v."number"
                from embark_summary es2  join voyage v on v.voyage_id = es2.voyage_id where es2.added_date in
                    (
                    select
                        (
                            select max(added_date)::timestamp
                            from embark_summary es
                            where voyage_id = '{vid}'
                            and (added_date between x::timestamp and (x::timestamp +'30 minute'::interval))
                        )
                    from generate_series(timestamp '{start}' , timestamp '{end}' , interval  '30 min') t(x)
                    )
                order by v."number" """
