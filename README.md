# Decision Explorer

사용자가 선택의 영향을 이해한 뒤 결정하도록 돕는 에이전트 skill입니다.
긴 설명 대신 **입력 → 발생 행위 → 선택 → 조건별 결과**를 작은 사례로 보여줍니다.

## 언제 사용하나요?

- 에이전트의 질문에 답하려면 시스템 동작부터 이해해야 할 때
- 정상 경로와 실패·경계 조건을 비교해야 할 때
- 구현 방향에 사용자 우선순위가 필요할 때

이미 정한 결정, 단순 취향, 에이전트가 조사하면 알 수 있는 사실에는 선택 화면을 만들지 않습니다.

## 사용 예

```text
$decision-explorer 기억 조회가 실패했을 때 사용자에게 다시 물을지,
재시도하도록 안내할지 비교해줘. 사용자도 시간을 잊었거나 재조회도
실패했을 때의 결과까지 보여줘. 실제 로그는 없는 가상 사례야.
```

전체 사용 지침은 [SKILL.md](SKILL.md), 합성 예시는 [기억 조회 사례](references/memory-example.md)에 있습니다. HTML을 지원하지 않는 환경에서는 같은 선택·조건·결과를 텍스트로 제공합니다. 화면에서 B를 눌러보는 행위는 구현 결정이 아닙니다.

## 설치와 버전 고정

이 저장소 루트가 하나의 skill 폴더입니다. 사용 중인 에이전트의 skill 디렉터리 아래 `decision-explorer` 폴더로 복제하거나 복사합니다. 예를 들어 Codex 개인 설치 위치는 `~/.codex/skills/decision-explorer`입니다. 기존 설치가 있다면 먼저 변경 여부를 확인하세요.

```sh
git clone https://github.com/seok-jun/decision-explorer.git decision-explorer
cd decision-explorer
git checkout v0.2.0
```

프로젝트 W에 채택할 때는 사용한 commit과 파일 해시를 기록하고, 프로젝트 고유 권한은 별도 원본으로 유지합니다. upstream 최신판을 자동으로 덮어쓰지 않습니다.

## 검증 책임

| 담당 | 확인 범위 |
| --- | --- |
| Python 검증기 | ID·버전·참조·조합 누락, 선언된 결과 변화, 근거 metadata, 선택 상태 |
| 에이전트 | 인과관계, 근거의 충분성, 의미 있는 차이, 사용자 의도·단서·권한 |
| 브라우저 검사 | 실제 컨트롤 표시·연결·결과 갱신·상태 복원 |

코드 통과는 사실·동의·권한의 증명이 아닙니다. [실행 가능한 계약과 한계](references/mechanical-validation.md)를 참고하세요. Python 3.9 이상이며 검증기와 contract eval에는 외부 의존성이 없습니다.

```sh
python scripts/validate_case.py evals/fixtures/memory-case.json --state evals/fixtures/memory-state.json
python evals/run-contract.py --report contract-report.json
```

브라우저 회귀 검사는 별도 개발 환경에 Playwright를 설치한 뒤 실행합니다.

```sh
npm install --no-save playwright@1.56.1
node evals/run-memory-ui.cjs --browser /absolute/path/to/chromium --report browser-report.json
```

`--browser` 생략 시 Playwright가 설치한 Chromium이 필요합니다. 테스트는 합성 fixture를 사용하며 외부 서비스 요청을 차단합니다.

## 평가 상태

v0.2.0의 로컬 검증: contract 53개, Edge 기반 브라우저 회귀 18개 통과. [에이전트 생성 eval](evals/evals.json) 13개는 정의되어 있으나 생성·채점은 아직 수행하지 않았습니다. 브라우저 검사는 실제 호스트 통합이나 사용자 이해 향상을 입증하지 않습니다. [평가 방법](references/evaluation.md)과 [설계 출처](references/sources.md)를 함께 제공합니다.
