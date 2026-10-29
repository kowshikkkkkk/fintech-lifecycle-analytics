import duckdb

con = duckdb.connect()
con.execute("""
    CREATE VIEW raw AS
    SELECT * FROM read_csv_auto('data/raw/e_wallet.csv')
""")

# 1) How many exact-duplicate groups, and how many surplus rows?
print(con.sql("""
    SELECT COUNT(*)   AS duplicate_groups,
           SUM(n - 1) AS extra_rows
    FROM (
        SELECT user_id, timestamp, event, COUNT(*) AS n
        FROM raw
        GROUP BY user_id, timestamp, event
        HAVING COUNT(*) > 1
    )
"""))

# 2) Which pages have the most surplus rows?
print(con.sql("""
    SELECT event, SUM(n - 1) AS extra_rows
    FROM (
        SELECT user_id, timestamp, event, COUNT(*) AS n
        FROM raw
        GROUP BY user_id, timestamp, event
        HAVING COUNT(*) > 1
    )
    GROUP BY event
    ORDER BY extra_rows DESC
    LIMIT 15
"""))