tables = [
    "companies"
]

columns = {
    "companies": [
        "company_id",
        "company",
        "symbol",
        "year",
        "category",
        "market_cap",
        "revenue",
        "gross_profit",
        "net_income",
        "eps",
        "ebitda",
        "holder_equity",
        "cash_flow_operating",
        "cash_flow_investing",
        "cash_flow_finance",
        "current_ratio",
        "debt_equity_ratio",
        "roe",
        "roa",
        "roi",
        "net_profit_margin",
        "free_cash_flow_per_share",
        "return_on_tangible_equity",
        "number_of_employees",
        "inflation_rate"
    ]
}

# No foreign keys since it's a single flat table
foreign_keys = []

fk_graph = {t: set() for t in tables}

schema_static = {
    "tables": tables,
    "columns": columns,
    "foreign_keys": foreign_keys,
    "fk_graph": fk_graph
}
