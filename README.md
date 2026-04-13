# jutonggi-parser

codex/parse-jutonggi-pdf-to-json-1hciar
주요정보통신기반시설(주통기) 기술적 취약점 분석/평가 가이드 PDF를 파싱해 정규화 JSON으로 만들고 PostgreSQL DB를 **비교/이력형**으로 업데이트합니다.

 main

## 설치

```bash
pip install -r requirements.txt
```

## 사용

```bash
python -m jutonggi_parser.ingest /path/to/jutonggi_guide.pdf \
  --json-out ./data/parsed_items.json \
codex/parse-jutonggi-pdf-to-json-1hciar
  --db-dsn postgresql://postgres:postgres@localhost:5432/jutonggi
```

## DB 구조

- `vulnerabilities`: 최신 상태 (API 조회용, `code` 유니크)
- `vulnerabilities_history`: 버전별 스냅샷 (`code + pdf_version` 유니크)
- `item_changelog`: 추가/수정/삭제 로그

## 동작 방식

새 PDF를 적재하면 아래를 자동 수행합니다.

1. 기존 `vulnerabilities`와 신규 파싱 결과를 `code` 기준으로 비교
2. `added/updated/deleted/unchanged` 분류
3. `vulnerabilities` 최신 상태로 upsert + 삭제 반영
4. `vulnerabilities_history`에 버전 스냅샷 upsert
5. `item_changelog`에 변경 로그 insert

CLI 출력으로 `added`, `updated`, `deleted`, `unchanged` 개수를 확인할 수 있습니다.

  --db ./data/jutonggi.db
```

## 저장 스키마

`vulnerabilities` 테이블 기준으로 `code + pdf_version` unique upsert를 수행합니다.
main
