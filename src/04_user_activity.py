import duckdb

con = duckdb.connect()
con.execute("""
    CREATE VIEW ev AS
    SELECT * FROM read_csv_auto('data/processed/events_dedup.csv')
""")

print(con.sql("""
    SELECT COUNT(*)                    AS users,
           quantile_cont(n, 0.5)       AS p50,
           quantile_cont(n, 0.9)       AS p90,
           quantile_cont(n, 0.99)      AS p99,
           quantile_cont(n, 0.999)     AS p999,
           MAX(n)                      AS max_events
    FROM (SELECT user_id, COUNT(*) AS n FROM ev GROUP BY user_id)
"""))

print(con.sql("""
    SELECT user_id,
           COUNT(*)                          AS n_events,
           COUNT(DISTINCT event)             AS n_distinct_pages,
           MIN(timestamp)                    AS first_ts,
           MAX(timestamp)                    AS last_ts
    FROM ev
    GROUP BY user_id
    ORDER BY n_events DESC
    LIMIT 10
"""))