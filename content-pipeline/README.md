# Content Pipeline Automation

**목표**: 그노의 보안 연구/분석 → 블로그, 트윗, LinkedIn 포스트로 자동 변환하는 파이프라인

**왜 필요한가**:
- 기술은 파는데 글 쓰는 건 귀찮음 → 아웃풋 일관성 떨어짐
- 꾸준한 콘텐츠 발행 = 업계 인지도 = 커리어 기회
- 한 번 분석한 걸 여러 포맷으로 재활용 → ROI 극대화

---

## Phase 0: 기획 ✅ (2026-02-01)

**현재 상태**: 컨셉 정의 완료

---

## MVP (Minimum Viable Product)

**v0.1 목표**: CVE 분석 노트 1개 → 블로그 초안 자동 생성

**워크플로우**:
```
Input: raw-notes/CVE-2024-XXXXX.md (그노의 분석 메모)
  ↓
Process: 
  - 구조화 (배경 → 취약점 → 영향 → 분석 → 교훈)
  - 불필요한 부분 제거 (중간 삽질 과정)
  - SEO 키워드 추가
  ↓
Output: blog-drafts/CVE-2024-XXXXX-analysis.md (퍼블리시 가능한 초안)
```

**핵심 기능**:
1. **템플릿 기반 변환**
   - `templates/blog-cve-analysis.md` - CVE 분석용 블로그 구조
   - `templates/blog-project-summary.md` - 프로젝트 회고용 구조
2. **자동 생성 스크립트** (`generate-draft.py`)
   - raw 노트 읽기
   - LLM API로 구조화/다듬기
   - 초안 저장
3. **리뷰 인터페이스**
   - Telegram으로 "초안 완성! 확인해줘" 알림
   - 그노가 수정 후 퍼블리시

---

## 다음 스텝 (TODO)

### Step 1: 템플릿 설계
- [ ] 블로그 글 템플릿 만들기 (CVE 분석용)
- [ ] 예시 raw 노트 준비 (실제 그노가 분석한 거 1개)
- [ ] 원하는 최종 결과물 샘플 작성

### Step 2: 변환 스크립트 작성
- [ ] `generate-draft.py` - LLM으로 raw → draft 변환
- [ ] 프롬프트 엔지니어링 (그노의 톤/스타일 유지)
- [ ] 테스트 (샘플 노트로 돌려보기)

### Step 3: 멀티 포맷 확장
- [ ] 트위터 스레드 생성 (`generate-tweet-thread.py`)
- [ ] LinkedIn 포스트 생성 (좀 더 formal하게)
- [ ] 한/영 버전 자동 생성

---

## 미래 확장 (v0.2+)

- **자동 발행**: 그노 승인 후 자동으로 블로그/SNS 포스팅
- **분석 ↔ 콘텐츠 양방향**: "다음 주 블로그 뭐 쓸까?" → 미완성 분석 리스트 제안
- **SEO 최적화**: 키워드 밀도, 메타 태그 자동 생성
- **이미지 자동 생성**: 취약점 다이어그램, 코드 하이라이트 스크린샷

---

## 폴더 구조 (예정)

```
projects/content-pipeline/
├── raw-notes/           # 그노의 원본 분석 메모
├── blog-drafts/         # 생성된 블로그 초안
├── tweet-threads/       # 트위터 스레드
├── templates/           # 콘텐츠 템플릿
└── scripts/
    ├── generate-draft.py
    └── publish.sh
```

---

**마지막 업데이트**: 2026-02-01  
**상태**: 기획 완료, Step 1 대기 중
