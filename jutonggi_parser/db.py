from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Iterable

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS vulnerabilities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT NOT NULL,
    prefix TEXT NOT NULL,
    domain TEXT NOT NULL,
    domain_name TEXT NOT NULL,
    os_type TEXT NOT NULL,
    category TEXT NOT NULL,
    severity TEXT NOT NULL,
    title TEXT NOT NULL,
    target TEXT NOT NULL,
    check_content TEXT NOT NULL,
    check_purpose TEXT NOT NULL,
    security_threat TEXT NOT NULL,
    criteria_good TEXT NOT NULL,
    criteria_bad TEXT NOT NULL,
    action TEXT NOT NULL,
    action_impact TEXT NOT NULL,
    note TEXT NOT NULL,
    page_start INTEGER NOT NULL,
    pdf_version TEXT NOT NULL,
    content_hash TEXT NOT NULL,
    raw_json TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(code, pdf_version)
);
"""

UPSERT_SQL = """
INSERT INTO vulnerabilities (
    code, prefix, domain, domain_name, os_type, category,
    severity, title, target, check_content, check_purpose,
    security_threat, criteria_good, criteria_bad, action,
    action_impact, note, page_start, pdf_version, content_hash, raw_json
)
VALUES (
    :code, :prefix, :domain, :domain_name, :os_type, :category,
    :severity, :title, :target, :check_content, :check_purpose,
    :security_threat, :criteria_good, :criteria_bad, :action,
    :action_impact, :note, :page_start, :pdf_version, :content_hash, :raw_json
)
ON CONFLICT(code, pdf_version) DO UPDATE SET
    prefix = excluded.prefix,
    domain = excluded.domain,
    domain_name = excluded.domain_name,
    os_type = excluded.os_type,
    category = excluded.category,
    severity = excluded.severity,
    title = excluded.title,
    target = excluded.target,
    check_content = excluded.check_content,
    check_purpose = excluded.check_purpose,
    security_threat = excluded.security_threat,
    criteria_good = excluded.criteria_good,
    criteria_bad = excluded.criteria_bad,
    action = excluded.action,
    action_impact = excluded.action_impact,
    note = excluded.note,
    page_start = excluded.page_start,
    content_hash = excluded.content_hash,
    raw_json = excluded.raw_json,
    updated_at = CURRENT_TIMESTAMP;
"""


class JutonggiRepository:
    def __init__(self, db_path: str | Path = "jutonggi.db"):
        self.db_path = Path(db_path)

    def initialize(self) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(SCHEMA_SQL)
            conn.commit()

    def upsert_items(self, items: Iterable[dict]) -> int:
        payload = []
        for item in items:
            row = dict(item)
            row["raw_json"] = json.dumps(item, ensure_ascii=False)
            row.setdefault("note", "")
            payload.append(row)

        if not payload:
            return 0

        with sqlite3.connect(self.db_path) as conn:
            conn.executemany(UPSERT_SQL, payload)
            conn.commit()
        return len(payload)
