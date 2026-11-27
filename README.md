# 너와 나의 마지막 계절 — Streamlit

## GitHub에 올릴 파일
- `app.py`
- `requirements.txt`

## 내 PC에서 실행
```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

## GitHub에 올리는 방법
1. GitHub에서 새 Repository를 만듭니다.
2. `app.py`, `requirements.txt`, `README.md`를 업로드합니다.
3. Streamlit Community Cloud에 로그인합니다.
4. **Create app**을 누르고 Repository, Branch, Main file path(`app.py`)를 선택합니다.
5. Deploy를 누릅니다.

## 현재 구현된 기능
- 17명 캐릭터 선택
- 캐릭터별 첫 대화와 선택지
- 선택에 따른 호감도·신뢰도·추억 변화
- 관계 단계 표시
- 최근 선택 기록
- 진행 데이터 JSON 내보내기

## 참고
이 버전은 시작용 프로토타입입니다. 진행 상황은 현재 브라우저 세션에 유지됩니다. JSON 내보내기는 가능하지만, 계정 기반 영구 저장/불러오기, 전체 학년·계절 시나리오, 캐릭터별 다중 이벤트, 엔딩 분기, 이미지 에셋은 아직 추가해야 합니다.
