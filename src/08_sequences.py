import duckdb

con = duckdb.connect()
con.execute("""
    CREATE VIEW ev AS
    SELECT * FROM read_csv_auto('data/processed/events_dedup.csv')
""")

def check(later, earlier_list):
    earlier = ",".join(f"'{e}'" for e in earlier_list)
    return con.sql(f"""
        WITH l AS (SELECT user_id, MIN(timestamp) AS t
                   FROM ev WHERE event = '{later}' GROUP BY user_id)
        SELECT '{later}' AS later_page,
               COUNT(*) AS users_with_later,
               SUM((EXISTS (SELECT 1 FROM ev e
                            WHERE e.user_id = l.user_id
                              AND e.event IN ({earlier})
                              AND e.timestamp <= l.t))::INT) AS had_earlier
        FROM l
    """)

print(check("wallet_deposit_success", ["payment_selection"]))
print(check("wallet_deposit_success", ["wallet_deposit"]))
print(check("email_confirmed", ["verify_email"]))
print(check("main", ["login", "registration", "open_account_main"]))