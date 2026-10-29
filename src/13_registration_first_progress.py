import pandas as pd

ev = pd.read_csv("data/processed/events_dedup.csv", parse_dates=["timestamp"])
co = pd.read_csv("data/processed/cohort.csv", parse_dates=["entry_ts"], index_col="user_id")
co = co[co.full_window & co.registration_first]

m = ev.merge(co[["entry_ts"]], left_on="user_id", right_index=True)
m = m[(m.timestamp >= m.entry_ts) & (m.timestamp <= m.entry_ts + pd.Timedelta(days=7))]

app = ["main", "account", "account_details", "account_info", "accounts_main",
       "accounts_kids", "profile", "profile_edit", "order_history", "order_statistics",
       "support", "special_offers", "referral_program", "loyalty_program",
       "subscriptions", "tariff_plans", "wallet", "wallet_deposit", "payment_selection",
       "wallet_deposit_success", "wallet_deposit_fail", "wallet_transfer", "wallet_withdrawal"]
signup = ["verify_email", "email_confirmed", "open_account_main",
          "open_account_kids", "id_verification"]

def users_with(pages):
    return m[m.event.isin(pages)]["user_id"].nunique()

only_reg = m.groupby("user_id")["event"].apply(lambda s: set(s) <= {"registration"}).sum()

print("users:", len(co))
print("reached main:", users_with(["main"]))
print("reached any app or money page:", users_with(app))
print("reached any signup-stage page:", users_with(signup))
print("reached either:", users_with(app + signup))
print("only registration views in window:", only_reg)