import duckdb

con = duckdb.connect()
con.execute("""
    CREATE VIEW raw AS
    SELECT * FROM read_csv_auto('data/raw/e_wallet.csv', all_varchar=true)
""")

print(con.sql("DESCRIBE raw"))

print(con.sql("""
    SELECT COUNT(*)                                   AS n_rows,
           COUNT(DISTINCT user_id)                    AS n_users,
           COUNT(*) - COUNT(user_id)                  AS null_user_id,
           COUNT(*) - COUNT(event)                    AS null_event,
           COUNT(*) - COUNT(timestamp)                AS null_timestamp,
           SUM((timestamp IS NOT NULL
                AND TRY_CAST(timestamp AS TIMESTAMP) IS NULL)::INT) AS unparseable_ts,
           MIN(TRY_CAST(timestamp AS TIMESTAMP))      AS min_ts,
           MAX(TRY_CAST(timestamp AS TIMESTAMP))      AS max_ts
    FROM raw
"""))

print(con.sql("""
    SELECT event,
           COUNT(*)                AS n_events,
           COUNT(DISTINCT user_id) AS n_users
    FROM raw
    GROUP BY event
    ORDER BY n_events DESC
"""))