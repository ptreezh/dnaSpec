# DNASPEC Context Engineering Skills - 공식 오픈 소스 릴리스 v1.0.1

## 🎉 출시 안내

AI 페르소나 랩 2025에서 발표합니다: **DNASPEC (Dynamic Specification Growth System) 컨텍스트 엔지니어링 스킬**이 성공적으로 오픈 소스로 공개되었습니다!

### 📋 프로젝트 정보
- **릴리스 버전**: v1.0.1
- **공식 레포지토리**: https://github.com/ptreezh/dnaSpec
- **라이센스**: MIT 라이센스
- **작성자**: pTree Dr.Zhang (AI 페르소나 랩 2025)
- **연락처**: 3061176@qq.com
- **웹사이트**: https://AgentPsy.com

## ✨ 주요 기능

### 1. 통합 스킬 아키텍처
- **표준/강화 모드 통합**: 동일한 스킬에서 `mode` 파라미터로 기능 조절
- **플랫 디렉토리 구조**: 각 스킬이 별도 디렉토리(중첩 없음)
- **AI 보안 워크플로우**: 임시 작업 공간으로 AI 생성 파일 오염 방지

### 2. 핵심 스킬
- **컨텍스트 분석**: 5차원(명확성, 관련성, 완전성, 일관성, 효율성) 평가
- **인지 템플릿**: 사고의 사슬, 적은 샘플 학습, 검증 등 프레임워크 적용
- **컨텍스트 최적화**: 명확성, 관련성, 완전성 기반 내용 최적화
- **아키텍처 설계**: 시스템 아키텍처 설계 지원
- **Git 운영**: 전체 Git 작업 흐름 지원
- **임시 작업 관리**: AI 보안 워크플로우

### 3. 다국어 지원
- 중국어
- 영어
- 러시아어
- 스페인어
- 프랑스어
- 일본어
- 한국어

## 🚀 설치 방법

```bash
# 레포지토리 클론
git clone https://github.com/ptreezh/dnaSpec.git
cd dnaspec-context-engineering

# 패키지 설치
pip install -e .
```

## 🔧 사용 예제

### CLI 명령어
```
/speckit.dnaspec.context-analysis "요구사항 문서 분석" mode=enhanced
/speckit.dnaspec.cognitive-template "성능 개선 방법" template=verification
/speckit.dnaspec.context-optimization "요구사항 명확화" optimization_goals=clarity,relevance
/speckit.dnaspec.architect "전자상거래 시스템 설계"
/speckit.dnaspec.git-skill operation=status
/speckit.dnaspec.temp-workspace operation=create-workspace
```

### 파이썬 API
```python
from clean_skills.context_analysis import execute as context_analysis_execute

# 표준 모드
result = context_analysis_execute({
    'context': '사용자 로그인 기능 설계',
    'mode': 'standard'
})

# 강화 모드
result = context_analysis_execute({
    'context': '보안 강화 사용자 인증 설계',
    'mode': 'enhanced'
})
```

## 🛡️ AI 보안 워크플로우

1. **생성 단계**: AI 출력은 임시 작업 공간에 저장
2. **정리 단계**: 임시 파일이 20개 초과 시 자동 알림
3. **승인 단계**: 인적 검증 후 주 프로젝트로 이동
4. **제출 단계**: 검증된 파일만 Git 저장소로 제출
5. **정리 단계**: 임시 작업 공간 자동 정리

## 📚 문서 가이드

- `QUICK_START_CN.md`: 중국어 빠른 시작 안내서
- `QUICK_START_EN.md`: 영어 빠른 시작 안내서
- `QUICK_START_RU.md`: 러시아어 빠른 시작 안내서
- `QUICK_START_ES.md`: 스페인어 빠른 시작 안내서
- `QUICK_START_FR.md`: 프랑스어 빠른 시작 안내서
- `QUICK_START_JA.md`: 일본어 빠른 시작 안내서
- `QUICK_START_KO.md`: 한국어 빠른 시작 안내서
- `INSTALL_GUIDE.md`: 설치 안내서
- `AI_SAFETY_GUIDELINES.md`: AI 보안 가이드라인
- `WORKFLOW_EXAMPLE.md`: 워크플로우 예시

## 🏗️ 프로젝트 구조

```
dnaspec-context-engineering/
├── src/
│   └── dnaspec_spec_kit_integration/    # 핵심 모듈
├── dist/                             # 배포판
│   └── clean_skills/                 # 통합 스킬
├── docs/                             # 문서
├── tests/                            # 테스트
├── QUICK_START_*.md                  # 다국어 시작 가이드
├── pyproject.toml                    # 프로젝트 설정
├── README.md                         # 프로젝트 설명
└── LICENSE                          # MIT 라이센스
```

## ⚡ 성능 특징

- **빠른 응답**: 로컬 작업 즉시 응답
- **경량 설계**: 200KB 미만의 최적화된 배포 패키지
- **AI 안전**: 내장된 임시 작업 공간 매니저
- **교차 호환**: Claude/Gemini/Qwen CLI 호환
- **확장 가능**: 새로운 스킬 간편 추가

## 🤝 기여하기

기여를 환영합니다! 다음 지침을 참고하세요:

1. 포크(Fork)하고 복제(Clone)
2. 새 기능 브랜치 만들기
3. 변경 사항 커밋
4. 브랜치에 푸시(Push)
5. 풀 리퀘스트(Pull Request) 열기

## 📞 지원 정보

- **이슈 제출**: https://github.com/ptreezh/dnaSpec/issues
- **이메일 문의**: 3061176@qq.com
- **제품 웹사이트**: https://AgentPsy.com

## 📄 라이센스

MIT License - 상업용 및 개인용 자유 사용 가능

---

*AI 페르소나 랩 2025*  
*작성자: pTree Dr.Zhang*  
*출시일: 2025년 1월*