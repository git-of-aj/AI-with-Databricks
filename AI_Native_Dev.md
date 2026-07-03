| Your goal                                   | Recommended setup                   |
| ------------------------------------------- | ----------------------------------- |
| Learning AI-native development              | Claude Code + Sonnet                |
| Building production software                | Claude Code + Opus                  |
| Maximum autonomy                            | Codex CLI + GPT-5 Codex             |
| Working in an IDE all day                   | Cursor + Claude Opus                |
| Lowest cost with good quality               | Claude Code + Sonnet                |
| Very large repositories (>1M-token context) | Gemini Pro in an agent-capable tool |

> The notable trend is that the gap between the top contenders is now small. Choice increasingly depends on your workflow (CLI agent vs IDE vs autonomous execution), budget, and repository size rather than a single universally superior model.
```mermaid
flowchart TD
    A[Claude Code]
    B[Claude Opus<br/>(Planning)]
    C[Claude Sonnet<br/>(Implementation)]
    D[Git]
    E[CI/CD]

    A --> B
    B --> C
    C --> D
    D --> E
```
## AI Native Development Techniques:
# AI Development Techniques Using One Consistent Example

Let's use one consistent example throughout:

**Use case:** Convert a React + Node.js web application into a desktop application using Electron.

This highlights how each technique differs in what you provide to the AI.

| Technique | Primary input to AI | Typical files |
|-----------|----------------------|---------------|
| Prompt-driven | Prompt | None |
| Vibe coding | Conversation | None |
| Spec-driven | Specification | `spec.md`, `requirements.md` |
| Intent-driven | Business goals | `intent.md` |
| Context engineering | Entire project knowledge | Specs + ADRs + architecture + rules |
| Agentic development | Goal + tools | Repository + task |
| Test-driven AI | Tests | Test files |
| Verification-first | Validation rules | CI, lint, tests, security rules |

---

## 1. Prompt-Driven Development

### User gives

> Convert my React web app into an Electron desktop application.
>
> Preserve routing.
>
> Support Windows and macOS.

### Files

None

### AI does

- Creates Electron
- Guesses project structure
- Adds main process
- Adds preload
- Updates `package.json`

Everything is inferred from one prompt.

---

## 2. Vibe Coding

Conversation might look like:

**User**

> Make this a desktop app.

**AI asks**

> Should it support auto updates?

**User**

> Sure.

**AI**

> Should it work offline?

**User**

> Yes.

AI keeps making decisions.

### Files

None

Everything emerges from conversation.

---

## 3. Spec-Driven Development

Instead of prompts, user writes:

### `spec.md`

```text
Goal

Convert web application into Electron.

Requirements

- Keep existing React UI
- Use Electron 38
- Auto updater
- Windows installer
- macOS dmg
- Secure IPC
- No Node integration
- Context isolation enabled
- Existing REST backend remains unchanged

Acceptance Criteria

App installs.
App launches.
Authentication works.
Printing works.
```

### Prompt becomes

> Implement `spec.md`

### Files

- `spec.md`

AI follows specification instead of guessing.

---

## 4. Intent-Driven Development

Instead of implementation details:

### `intent.md`

```text
Business Objective

Sales representatives work without internet.

Current Problem

Browser version requires internet.

Success

Desktop app works offline.

Constraints

No UI redesign.
Migration should finish in four weeks.
```

### Prompt

> Read `intent.md` and produce a technical implementation plan.

### Files

- `intent.md`

**Notice:**

Intent explains **why**, not **how**.

---

## 5. Context Engineering

Now AI receives much more than one document.

```text
/
docs
├── architecture.md
├── coding-standards.md
├── electron-security.md
├── adrs/
│   ├── ADR-001-routing.md
│   └── ADR-002-auth.md
├── spec.md
├── intent.md
└── api.md
```

### Prompt

> Use every document under `docs` as project context. Implement the desktop migration.

### AI knows

- architecture
- standards
- security
- previous decisions
- APIs
- constraints

No repeated prompting needed.

---

## 6. Agentic Development

### User says

> Convert this repository into an Electron application.
>
> Commit changes in logical commits.
>
> Run tests after every milestone.
>
> Stop if authentication breaks.

AI agent then

```text
Analyze repository
        ↓
Create plan
        ↓
Modify code
        ↓
Run npm test
        ↓
Fix failures
        ↓
Run Electron
        ↓
Commit
        ↓
Repeat
```

### Files

Entire repository.

The AI behaves like a junior engineer.

---

## 7. Test-Driven AI Development

Instead of implementation first:

### `desktop.test.ts`

```text
should launch Electron

should preserve authentication

should open settings

should print invoices

should update automatically
```

### Prompt

> Make every test pass.

### Files

- `desktop.test.ts`

AI writes implementation after seeing tests.

---

## 8. Verification-First Development

User provides:

### `verification.md`

```text
No lint errors

100% Electron security checklist

No npm audit vulnerabilities

Build succeeds

Tests pass

Bundle under 150 MB
```

### Prompt

> Implement desktop migration.
>
> Do not finish until `verification.md` passes completely.

### Files

- `verification.md`

AI continuously checks its work before declaring success.

---

# How These Techniques Build on One Another

Modern AI-native teams often combine them rather than choosing one.

```text
Business Goal
        │
        ▼
intent.md
(Why are we doing this?)

        │
        ▼
spec.md
(What exactly should be built?)

        │
        ▼
architecture.md
coding-standards.md
ADR-*.md
api.md
(Context for the AI)

        │
        ▼
AI Agent
(Plans and executes the work)

        │
        ▼
Prompt
("Implement the desktop migration.")

        │
        ▼
Generated Code

        │
        ▼
Tests
(Security, unit, integration)

        │
        ▼
Verification
(Lint, CI, audits, acceptance criteria)

        │
        ▼
Production
```

---

# A Real-World Workflow

A mature team converting a monolith to microservices or a web app to a desktop app would typically:

1. Write `intent.md` (business rationale and success metrics).
2. Create `spec.md` (functional and technical requirements).
3. Supply architecture docs, ADRs, coding standards, and API documentation as context.
4. Ask an AI agent to execute the migration.
5. Require it to satisfy existing and newly added tests.
6. Gate completion on verification checks (CI, security scans, linting, performance, and acceptance criteria).

This layered workflow minimizes ambiguity, makes AI outputs more predictable, and scales much better than relying on increasingly detailed prompts alone.
