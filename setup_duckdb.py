import duckdb

con = duckdb.connect("crm_sales.duckdb")

tables = {
    "raw_accounts": "accounts.csv",
    "raw_products": "products.csv",
    "raw_sales_pipeline": "sales_pipeline.csv",
    "raw_sales_teams": "sales_teams.csv",
}

for table, file in tables.items():
    con.execute(
        f"""
        CREATE OR REPLACE TABLE {table} AS
        SELECT *
        FROM read_csv_auto('{file}')
        """
    )

print("Tables created:")
print(con.execute("SHOW TABLES").fetchall())

con.close()