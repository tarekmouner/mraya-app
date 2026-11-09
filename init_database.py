import miraya_core as db
if __name__ == "__main__":
    db.init_db()
    print("MIRAYA database initialized.")
    print(db.get_dashboard_stats())
