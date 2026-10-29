import duckdb

con = duckdb.connect()
con.execute("""
    CREATE VIEW ev AS
    SELECT * FROM read_csv_auto('data/processed/events_dedup.csv')
""")

print(con.sql("""
    WITH u AS (SELECT user_id, COUNT(*) AS n FROM ev GROUP BY user_id),
    r AS (
        SELECT n,
               ROW_NUMBER() OVER (ORDER BY n DESC) AS rk,
               COUNT(*)     OVER ()                AS tot,
               SUM(n)       OVER ()                AS all_ev
        FROM u
    )
    SELECT ROUND(SUM(CASE WHEN rk <= tot * 0.001 THEN n END) * 1.0 / MAX(all_ev), 3) AS share_top_0_1pct,
           ROUND(SUM(CASE WHEN rk <= tot * 0.01  THEN n END) * 1.0 / MAX(all_ev), 3) AS share_top_1pct,
           ROUND(SUM(CASE WHEN rk <= tot * 0.10  THEN n END) * 1.0 / MAX(all_ev), 3) AS share_top_10pct
    FROM r
"""))