# 1-2-final-exam-program

이 저장소는 1-2 기말(2학기 기말고사) 대비 물리·화학·생물·지구과학 복습 프로그램이에요.

- 문제 364개: 객관식 227개(보기마다 정답·오답 이유), 계산 단답, 그림·그래프 문제, 서술형
- 타임어택 모의고사: 시간이 끝나면 자동으로 채점돼요.
- 필기·PPT 관련 페이지 보기, 필기 기반 질문 기능
- 수식은 KaTeX(MathML)로 표시돼요. 인터넷 없이도 보여요.

## 폴더 구조

```
src/    문제·자료 원본과 빌드 스크립트
  q_*.yaml, x_*.yaml   문제 (s 과목, u 단원, t 유형, lv 난이도, ...)
  cx.yaml              객관식 보기별 이유 (원래 보기 순서, a번 = 정답 이유)
  kb.yaml              '질문하기'용 필기 요약
  figs.py              문제 그림(SVG) 생성
  mathify.py           v_c 같은 글자 표기를 $수식$으로 바꿈
  template.html        앱 화면
  build_site.py        → docs/ (index.html + data.js)
  build_single.py      → 이미지까지 들어간 HTML 파일 하나
docs/   배포용 웹사이트 (GitHub Pages: main 브랜치 /docs)
  img/  필기·PPT 페이지 이미지(webp)
```

## 빌드

```bash
pip install pyyaml
python3 src/build_site.py                      # docs/ 갱신
python3 src/build_single.py 복습프로그램.html   # 파일 하나짜리 HTML
```

※ `docs/img`에는 수업 자료와 필기 이미지가 들어 있어요. 저장소를 공개로 바꾸면 이 이미지도 같이 공개돼요.
