tables = [
    "album", "artist", "customer", "employee", "genre", "invoice",
    "invoice_line", "media_type", "playlist", "playlist_track", "track"
]

columns = {
    "album": ["album_id", "title", "artist_id"],
    "artist": ["artist_id", "name"],
    "customer": [
        "customer_id", "first_name", "last_name", "company", "address",
        "city", "state", "country", "postal_code", "phone",
        "fax", "email", "support_rep_id"
    ],
    "employee": [
        "employee_id", "last_name", "first_name", "title", "reports_to",
        "birth_date", "hire_date", "address", "city", "state",
        "country", "postal_code", "phone", "fax", "email"
    ],
    "genre": ["genre_id", "name"],
    "invoice": [
        "invoice_id", "customer_id", "invoice_date", "billing_address",
        "billing_city", "billing_state", "billing_country",
        "billing_postal_code", "total"
    ],
    "invoice_line": [
        "invoice_line_id", "invoice_id", "track_id",
        "unit_price", "quantity"
    ],
    "media_type": ["media_type_id", "name"],
    "playlist": ["playlist_id", "name"],
    "playlist_track": ["playlist_id", "track_id"],
    "track": [
        "track_id", "name", "album_id", "media_type_id", "genre_id",
        "composer", "milliseconds", "bytes", "unit_price"
    ]
}

# ORIGINAL FK map (compact)
_raw_foreign_keys = {
    "album": [("artist", "artist_id")],
    "customer": [("employee", "support_rep_id")],
    "invoice": [("customer", "customer_id")],
    "invoice_line": [("invoice", "invoice_id"), ("track", "track_id")],
    "playlist_track": [("playlist", "playlist_id"), ("track", "track_id")],
    "track": [
        ("album", "album_id"),
        ("media_type", "media_type_id"),
        ("genre", "genre_id")
    ]
}

##############################################################
# NORMALIZE FKs -> explicit dict list
##############################################################
foreign_keys = []
for from_table, relations in _raw_foreign_keys.items():
    for (to_table, from_col) in relations:
        # infer to_col name (same id name)
        to_col = columns[to_table][0]   # first col is always PK e.g. artist_id
        fk = {
            "from_table": from_table,
            "from_col": from_col,
            "to_table": to_table,
            "to_col": to_col
        }
        foreign_keys.append(fk)

##############################################################
# AUTO-BUILD FK GRAPH FOR REASONING
##############################################################
fk_graph = {t: set() for t in tables}
for fk in foreign_keys:
    fk_graph[fk["from_table"]].add(fk["to_table"])
    fk_graph[fk["to_table"]].add(fk["from_table"])

##############################################################
# FINAL SCHEMA EXPORT
##############################################################
schema_static = {
    "tables": tables,
    "columns": columns,
    "foreign_keys": foreign_keys,
    "fk_graph": fk_graph
}
