from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path

from jutonggi_parser.db import JutonggiRepository
from jutonggi_parser.parser import JutonggiParser


def build_cli() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="주통기 PDF를 JSON/DB로 적재")
    p.add_argument("pdf", help="주통기 가이드 PDF 경로")
    p.add_argument("--json-out", default="parsed_items.json", help="정규화 JSON 저장 경로")
    p.add_argument("--db", default="jutonggi.db", help="SQLite DB 파일 경로")
    return p


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
    args = build_cli().parse_args()

    parser = JutonggiParser(args.pdf)
    items = parser.parse()

    json_path = Path(args.json_out)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")

    repo = JutonggiRepository(args.db)
    repo.initialize()
    inserted = repo.upsert_items(items)

    print(f"items={len(items)}")
    print(f"json={json_path}")
    print(f"db={Path(args.db)}")
    print(f"upserted={inserted}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
