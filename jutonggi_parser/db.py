from __future__ import annotations

import json
from typing import Iterable

import psycopg

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS vulnerabilities (
    id BIGSERIAL PRIMARY KEY,
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
    raw_json JSONB NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
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
    %(code)s, %(prefix)s, %(domain)s, %(domain_name)s, %(os_type)s, %(category)s,
    %(severity)s, %(title)s, %(target)s, %(check_content)s, %(check_purpose)s,
    %(security_threat)s, %(criteria_good)s, %(criteria_bad)s, %(action)s,
    %(action_impact)s, %(note)s, %(page_start)s, %(pdf_version)s, %(content_hash)s, %(raw_json)s::jsonb
)
ON CONFLICT(code, pdf_version) DO UPDATE SET
    prefix = EXCLUDED.prefix,
    domain = EXCLUDED.domain,
    domain_name = EXCLUDED.domain_name,
    os_type = EXCLUDED.os_type,
    category = EXCLUDED.category,
    severity = EXCLUDED.severity,
    title = EXCLUDED.title,
    target = EXCLUDED.target,
    check_content = EXCLUDED.check_content,
    check_purpose = EXCLUDED.check_purpose,
    security_threat = EXCLUDED.security_threat,
    criteria_good = EXCLUDED.criteria_good,
    criteria_bad = EXCLUDED.criteria_bad,
    action = EXCLUDED.action,
    action_impact = EXCLUDED.action_impact,
    note = EXCLUDED.note,
    page_start = EXCLUDED.page_start,
    content_hash = EXCLUDED.content_hash,
    raw_json = EXCLUDED.raw_json,
    updated_at = CURRENT_TIMESTAMP;
"""


class JutonggiRepository:
    def __init__(self, dsn: str = "postgresql://postgres:postgres@localhost:5432/jutonggi"):
        self.dsn = dsn

    def initialize(self) -> None:
        with psycopg.connect(self.dsn) as conn:
            with conn.cursor() as cur:
                cur.execute(SCHEMA_SQL)
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

        with psycopg.connect(self.dsn) as conn:
            with conn.cursor() as cur:
                cur.executemany(UPSERT_SQL, payload)
            conn.commit()
        return len(payload)
