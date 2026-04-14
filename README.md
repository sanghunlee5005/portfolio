# portfolio

이상훈의 데이터 엔지니어 포트폴리오.

https://sanghunlee5005.github.io/portfolio/

## 데이터 소스

이 포트폴리오의 콘텐츠는 **career 레포**의 master 원본을 기반으로 한다.

| 원본 (career 레포) | 포트폴리오 반영 위치 |
|---|---|
| `master/resume.md` | Hero, About, Tech Stack, Career 타임라인, Contact |
| `master/career.md` | Projects 카드 + 상세 페이지 (`projects/*.html`) |
| `master/format.md` | 직접 반영 안 함 (경력기술서 작성 포맷 가이드) |

career 레포의 master 데이터가 업데이트되면 이 포트폴리오도 싱크를 맞춰야 한다.

## 아키텍처 다이어그램

`scripts/` 안의 Python 스크립트로 아키텍처 다이어그램을 생성한다.

```bash
# 의존성
brew install graphviz
python3 -m venv .venv && source .venv/bin/activate && pip install diagrams

# 다이어그램 생성
python3 scripts/diagram_pipeline.py   # → images/data-pipeline.png
python3 scripts/diagram_airflow.py    # → images/airflow-platform.png
```

- AWS 아이콘: `images/aws-icons/` (AWS 공식 Architecture Icons 2026.01.30 버전)
- 서드파티 아이콘: `images/third-party/`
