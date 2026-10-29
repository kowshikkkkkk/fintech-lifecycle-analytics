import duckdb

con = duckdb.connect()
con.execute("""
    CREATE VIEW ev AS
    SELECT * FROM read_csv_auto('data/processed/events_dedup.csv')
""")

print(con.sql("""
    WITH top AS (
        SELECT user_id FROM ev GROUP BY user_id
        ORDER BY COUNT(*) DESC LIMIT 20
    ),
    gaps AS (
        SELECT user_id, timestamp,
               date_diff('second',
                         LAG(timestamp) OVER (PARTITION BY user_id ORDER BY timestamp, row_id),
                         timestamp) AS gap_s
        FROM ev WHERE user_id IN (SELECT user_id FROM top)
    )
    SELECT user_id,
           COUNT(*)                                           AS n_events,
           COUNT(DISTINCT CAST(timestamp AS DATE))            AS active_days,
           ROUND(COUNT(*) * 1.0 / COUNT(DISTINCT CAST(timestamp AS DATE)), 1) AS events_per_active_day,
           quantile_cont(gap_s, 0.5)                          AS median_gap_s,
           ROUND(AVG((gap_s <= 1)::INT), 3)                   AS share_gap_le_1s
    FROM gaps
    GROUP BY user_id
    ORDER BY n_events DESC
"""))