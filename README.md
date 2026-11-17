# Sid Agent Skills — the all-skills agent bundle

One agent, **37 skills**, covering everything Sid works on: RotiAI outreach and
social media, freelance web development and QA testing, graphics and 3D design,
motion and video, and general assistant work — plus a thinking/reasoning
workflow that makes the agent plan before it builds.

Every skill is a real, openly licensed skill in the `SKILL.md` format
(YAML frontmatter + Markdown instructions). Each skill lives in its own folder
under `skills/<skill-name>/` with its `SKILL.md`, plus any scripts, references
and assets it ships with, and its licence file.

## Quick start

```bash
./install.sh        # checks every skill folder and prints the list
```

Then point your agent at this folder (for example, copy `skills/` into
`~/.claude/skills/`, `.claude/skills/`, or any agent that reads `SKILL.md`
folders), and read `AGENTS.md` for how the agent should behave.

## Skill list (37)

### Thinking & reasoning — plan before you build

| Skill | What it does | Source |
|---|---|---|
| brainstorming | Explore ideas with the user before building anything new | [obra/superpowers](https://github.com/obra/superpowers) (MIT) |
| writing-plans | Write a clear implementation plan before touching code | [obra/superpowers](https://github.com/obra/superpowers) (MIT) |
| systematic-debugging | Find the root cause of any bug before proposing a fix | [obra/superpowers](https://github.com/obra/superpowers) (MIT) |
| test-driven-development | Write the failing test first, then the code | [obra/superpowers](https://github.com/obra/superpowers) (MIT) |
| verification-before-completion | Verify work actually passes before claiming it is done | [obra/superpowers](https://github.com/obra/superpowers) (MIT) |
| writing-skills | Create, edit and verify new agent skills | [obra/superpowers](https://github.com/obra/superpowers) (MIT) |

### Web development

| Skill | What it does | Source |
|---|---|---|
| frontend-design | Distinctive, intentional visual design for new UI | [anthropics/skills](https://github.com/anthropics/skills) (Apache-2.0) |
| webapp-testing | Test local web apps in a real browser with Playwright | [anthropics/skills](https://github.com/anthropics/skills) (Apache-2.0) |
| skill-creator | Create and improve skills, measure their performance | [anthropics/skills](https://github.com/anthropics/skills) (Apache-2.0) |
| mcp-builder | Build high-quality MCP servers for external services | [anthropics/skills](https://github.com/anthropics/skills) (Apache-2.0) |
| tailwind-best-practices | Tailwind CSS patterns, responsive design, dark mode | [AsyrafHussin/agent-skills](https://github.com/AsyrafHussin/agent-skills) (MIT) |
| api-design-patterns | RESTful API design, errors, versioning, OpenAPI | [AsyrafHussin/agent-skills](https://github.com/AsyrafHussin/agent-skills) (MIT) |
| web-design-guidelines | UI/UX best practices and accessibility audits | [AsyrafHussin/agent-skills](https://github.com/AsyrafHussin/agent-skills) (MIT) |

### QA testing

| Skill | What it does | Source |
|---|---|---|
| testing-best-practices | Unit, integration and E2E testing principles | [AsyrafHussin/agent-skills](https://github.com/AsyrafHussin/agent-skills) (MIT) |
| e2e-playwright-testing | End-to-end browser testing with Playwright | [AsyrafHussin/agent-skills](https://github.com/AsyrafHussin/agent-skills) (MIT) |

### Outreach & social media (RotiAI)

| Skill | What it does | Source |
|---|---|---|
| social-media-posting | Create and schedule platform-specific social content | [seb1n/awesome-ai-agent-skills](https://github.com/seb1n/awesome-ai-agent-skills) (MIT) |
| seo-optimization | On-page SEO, technical performance, structured data | [seb1n/awesome-ai-agent-skills](https://github.com/seb1n/awesome-ai-agent-skills) (MIT) |
| content-strategy | Map content to audience needs, funnel stages and goals | [seb1n/awesome-ai-agent-skills](https://github.com/seb1n/awesome-ai-agent-skills) (MIT) |
| keyword-research | Find high-value keywords and map search intent | [seb1n/awesome-ai-agent-skills](https://github.com/seb1n/awesome-ai-agent-skills) (MIT) |
| analytics-reporting | Marketing analytics reports with KPIs and attribution | [seb1n/awesome-ai-agent-skills](https://github.com/seb1n/awesome-ai-agent-skills) (MIT) |
| seo-best-practices | SEO patterns, meta tags, Core Web Vitals, sitemaps | [AsyrafHussin/agent-skills](https://github.com/AsyrafHussin/agent-skills) (MIT) |
| roti-ai-outreach | Sid's own RotiAI outreach + social playbook (WhatsApp, Leadlyze, Quora) | Original — written for this bundle |

### Graphics design

| Skill | What it does | Source |
|---|---|---|
| brand-guidelines | Apply brand colors and typography to artifacts | [anthropics/skills](https://github.com/anthropics/skills) (Apache-2.0) |
| canvas-design | Visual art posters and pieces in PNG/PDF with OFL fonts | [anthropics/skills](https://github.com/anthropics/skills) (Apache-2.0) |
| algorithmic-art | Algorithmic art with p5.js and seeded randomness | [anthropics/skills](https://github.com/anthropics/skills) (Apache-2.0) |
| theme-factory | Style slides, docs and pages with 10 preset themes | [anthropics/skills](https://github.com/anthropics/skills) (Apache-2.0) |
| web-artifacts-builder | Multi-component HTML artifacts with React + Tailwind | [anthropics/skills](https://github.com/anthropics/skills) (Apache-2.0) |
| interface-review | Review changes for interface, accessibility and writing problems | [jakubkrehel/skills](https://github.com/jakubkrehel/skills) (MIT) |
| better-colors | Build and check color systems, palettes and contrast | [jakubkrehel/skills](https://github.com/jakubkrehel/skills) (MIT) |

### Motion & video

| Skill | What it does | Source |
|---|---|---|
| web-motion-auditor | Review web animations, transitions and reduced-motion support | [frankxai/awesome-motion-design-agent-skills](https://github.com/frankxai/awesome-motion-design-agent-skills) (CC0) |
| remotion-video-agent | Create and render Remotion videos and social cutdowns | [frankxai/awesome-motion-design-agent-skills](https://github.com/frankxai/awesome-motion-design-agent-skills) (CC0) |

### 3D & model design

| Skill | What it does | Source |
|---|---|---|
| blender-web-3d | Build and publish 3D models with headless Blender + Three.js | [czlonkowski/blender-web-3d-skill](https://github.com/czlonkowski/blender-web-3d-skill) (MIT) |
| 3dassets | Find and use free CC0 GLB models for three.js, Blender, Godot, Unity | [3dassets-dev/3dassets](https://github.com/3dassets-dev/3dassets) (CC0) |

### General assistant

| Skill | What it does | Source |
|---|---|---|
| internal-comms | Write internal communications in company formats | [anthropics/skills](https://github.com/anthropics/skills) (Apache-2.0) |
| claude-api | Claude API / SDK reference: models, pricing, tools, MCP, caching | [anthropics/skills](https://github.com/anthropics/skills) (Apache-2.0) |
| slack-gif-creator | Animated GIFs optimized for Slack | [anthropics/skills](https://github.com/anthropics/skills) (Apache-2.0) |
| docx | Create, read and edit Word documents (.docx/.dotx) | [anthropics/skills](https://github.com/anthropics/skills) (Apache-2.0) |

## Sources

All skills were fetched from public GitHub repositories on 2026-11-17 and
verified to exist with a readable `SKILL.md`. Each skill folder carries its
licence file. Upstream repos:

- https://github.com/anthropics/skills — Apache-2.0 (per-skill LICENSE.txt)
- https://github.com/obra/superpowers — MIT
- https://github.com/AsyrafHussin/agent-skills — MIT
- https://github.com/seb1n/awesome-ai-agent-skills — MIT
- https://github.com/jakubkrehel/skills — MIT
- https://github.com/frankxai/awesome-motion-design-agent-skills — CC0
- https://github.com/czlonkowski/blender-web-3d-skill — MIT
- https://github.com/3dassets-dev/3dassets — CC0

## What was deliberately left out

- **Quegenx/agent-skills (145 skills)** — no top-level licence found, so its
  skills were not redistributed. Its marketing set (social-media, cold-outreach,
  SEO) is the biggest gap; the bundle covers that ground with the seb1n
  marketing skills, the AsyrafHussin SEO skill, and the original
  `roti-ai-outreach` skill instead.
- **atulrathodc/skills (~300 skills)** — no licence file found anywhere in the
  repo, so none of its skills (including `3d-modeling` and `threejs-3d`) were
  included. 3D is covered by `blender-web-3d` and `3dassets`.
- **anthropics/skills document skills pdf and pptx** — left out to keep the
  bundle lean; `docx` is included. The repo README marks all of its skills as
  demonstration/educational — test each skill before relying on it.
- **anthropics/skills `doc-coauthoring`** — no licence file in its folder, so
  it was excluded.
- **reason-machines/marketing-skills** — a large aggregator of other people's
  marketing skills with unclear provenance; skipped in favour of the
  single-author MIT sources above.
- **citedy/citedy-seo-agent** — MIT, but it requires the paid Citedy platform
  and credits; skipped.

## Layout

```
sid-agent-skills/
├── README.md            # this file
├── AGENTS.md            # agent instructions — how the agent uses the skills
├── install.sh           # verifies the layout and prints the skill list
└── skills/
    └── <skill-name>/
        ├── SKILL.md     # the skill (required)
        ├── LICENSE      # licence for the skill
        └── ...          # scripts, references, assets the skill ships with
```

## Licence of this bundle

The bundle itself is a collection: each skill keeps its own licence (see
`skills/<skill-name>/LICENSE*`). The original skill `roti-ai-outreach` is
Sid's own work. When you redistribute the bundle, keep every skill's licence
file with it.
