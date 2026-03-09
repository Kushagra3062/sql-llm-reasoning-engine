tables = [
    "financial_statements",
    "metadata_versions",
    "companies",
    "market_prices"
]

columns = {
    "financial_statements": [
        "id",
        "company_id",
        "year",
        "market_cap_billion",
        "revenue",
        "gross_profit",
        "net_income",
        "earning_per_share",
        "ebitda",
        "shareholder_equity",
        "cashflow_operating",
        "cashflow_investing",
        "cashflow_financing",
        "current_ratio",
        "debt_equity_ratio",
        "roe",
        "roa",
        "roi",
        "net_profit_margin",
        "free_cashflow_per_share",
        "return_on_tangible_equity",
        "number_of_employees",
        "inflation_rate_us",
        "version",
        "scrape_timestamp",
        "source"
    ],
    "metadata_versions": [
        "version_id",
        "version",
        "scrape_timestamp",
        "source",
        "notes",
        "data_type"
    ],
    "companies": [
        "company_id",
        "company_name",
        "category",
        "symbol"
    ],
    "market_prices": [
        "id",
        "company_id",
        "date",
        "open",
        "high",
        "low",
        "close",
        "volume",
        "version",
        "scrape_timestamp",
        "source",
        "daily_pct_change",
        "ma_7",
        "ma_30",
        "volume_spike"
    ]
}

foreign_keys = [
    {"from_table": "financial_statements", "from_column": "company_id", "to_table": "companies", "to_column": "company_id"},
    {"from_table": "market_prices", "from_column": "company_id", "to_table": "companies", "to_column": "company_id"}
]

fk_graph = {
    "financial_statements": {"companies"},
    "metadata_versions": set(),
    "companies": {"financial_statements", "market_prices"},
    "market_prices": {"companies"}
}

schema_static = {
    "tables": tables,
    "columns": columns,
    "foreign_keys": foreign_keys,
    "fk_graph": fk_graph
}
