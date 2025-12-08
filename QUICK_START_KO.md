# DNASPEC 컨텍스트 엔지니어링 스킬 - 빠른 시작 안내서 (Korean)

## 프로젝트 개요

DNASPEC (Dynamic Specification Growth System) Context Engineering Skills는 AI CLI 플랫폼을 위해 특별히 설계된 전문 AI 보조 개발 툴킷으로, 컨텍스트 분석, 최적화, 인지 템플릿 기능 및 AI 안전 작업 흐름을 제공합니다.

## 주요 개선 사항

### 1. 통합 스킬 아키텍처
- **통합 구현**: 표준 모드와 강화 모드 스킬이 단일 구현으로 통합됨
- **모드 전환**: `mode` 파라미터를 사용하여 기능 수준 제어 ('standard' 또는 'enhanced')
- **단일 인터페이스**: 중복 기능을 피하는 단순화된 인터페이스

### 2. 평면 디렉토리 구조
- **1개 스킬당 1개 디렉토리**: 각 스킬이 자체 디렉토리에 포함, 불필요한 중첩 없음
- **단순화된 조직**: 직관적인 스킬 배치, 유지 관리 용이성
- **혼동 감소**: 명확한 스킬 경계, 기능 중복 없음

### 3. AI 보안 작업 흐름
- **임시 작업공간**: AI 생성 콘텐츠가 먼저 임시 영역에 저장
- **자동 관리**: 파일 수가 20개를 초과하면 자동 알림
- **확인 메커니즘**: 주 프로젝트에 포함 전에 콘텐츠 확인 필요
- **자동 정리**: 작업 완료 후 임시 작업 공간 자동 정리

## 설치

```bash
# 리포지토리 클론
git clone https://github.com/ptreezh/dnaSpec.git
cd dnaspec-context-engineering

# 설치
pip install -e .
```

## 사용법

### CLI 명령어
```
/speckit.dnaspec.context-analysis "요구사항 문서의 품질 분석" mode=enhanced
/speckit.dnaspec.cognitive-template "성능 개선 방법" template=verification
/speckit.dnaspec.context-optimization "요구사항 최적화" optimization_goals=clarity,relevance
/speckit.dnaspec.architect "전자상거래 시스템 아키텍처 설계"
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
    'context': '보안 사용자 인증 기능 설계',
    'mode': 'enhanced'
})
```

## AI 보안 모범 사례

1. **AI 생성 전** : 항상 임시 작업 공간을 우선 생성
2. **콘텐츠 검증** : 확인 메커니즘 사용하여 AI 생성 콘텐츠 검증
3. **정기 청소** : 임시 파일 수량 모니터링
4. **워크스페이스 정리** : 작업 완료 후 임시 영역 정리

---
*저자: pTree 장 박사*  
*기관: AI 페르소나 랩 2025*  
*연락처: 3061176@qq.com*  
*웹사이트: https://AgentPsy.com*