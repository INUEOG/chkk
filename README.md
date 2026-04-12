# jutonggi-parser

주요정보통신기반시설(주통기) 기술적 취약점 분석/평가 가이드 PDF를 파싱해 정규화 JSON으로 만들고 SQLite DB에 저장합니다.

## 설치

```bash
pip install -r requirements.txt
```

## 사용

```bash
python -m jutonggi_parser.ingest /path/to/jutonggi_guide.pdf \
  --json-out ./data/parsed_items.json \
  --db ./data/jutonggi.db
```

## 저장 스키마

`vulnerabilities` 테이블 기준으로 `code + pdf_version` unique upsert를 수행합니다.
