# Sid Agent Skills — the all-skills agent bundle

One agent, **159 skills**, covering everything Sid works on: RotiAI outreach and
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

## Skill list (159)

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

### Automation — browsers, workflows, scheduled jobs, no-code tools

| Skill | What it does | Source |
|---|---|---|
| task-automation | Automate repetitive tasks and workflows using scripting, file watchers, scheduled jobs, CI triggers, and… | [seb1n/awesome-ai-agent-skills](https://github.com/seb1n/awesome-ai-agent-skills) (MIT) |
| workflow-automation | Covers automating multi-step operational workflows — event-driven triggers, orchestrating steps across… | [arjunprabhulal/devops-skills](https://github.com/arjunprabhulal/devops-skills) (MIT) |
| scheduled-jobs | Covers cron and scheduled work done right — idempotency, preventing overlapping runs, monitoring for… | [arjunprabhulal/devops-skills](https://github.com/arjunprabhulal/devops-skills) (MIT) |
| scripting-automation | Covers writing operational scripts that survive contact with production — idempotency, real error handling… | [arjunprabhulal/devops-skills](https://github.com/arjunprabhulal/devops-skills) (MIT) |
| zapier | Zapier is a cloud automation platform that connects thousands of apps with no-code workflows called Zaps… | [TerminalSkills/skills](https://github.com/TerminalSkills/skills) (Apache-2.0) |
| make-com | Make.com (formerly Integromat) is a visual automation platform that connects apps into scenarios of… | [TerminalSkills/skills](https://github.com/TerminalSkills/skills) (Apache-2.0) |
| n8n | n8n is a fair-code workflow automation platform with a visual editor, webhook and schedule triggers,… | [TerminalSkills/skills](https://github.com/TerminalSkills/skills) (Apache-2.0) |
| cron | Schedule recurring tasks with cron on Linux/macOS. Use when a user asks to run scripts on a schedule, set… | [TerminalSkills/skills](https://github.com/TerminalSkills/skills) (Apache-2.0) |
| browser-use | Drive a real browser programmatically — for testing, scraping, agent workflows, automation — using… | [ryan-evans-git/ai-skills](https://github.com/ryan-evans-git/ai-skills) (MIT) |
| web-scraper | Smart agentic web data extraction with multi-strategy scraping (Crawl4AI v4, Firecrawl), LLM extraction… | [aradiw/vibes-plug](https://github.com/aradiw/vibes-plug) (MIT) |
| n8n-automation-expert | Expert guide for workflow automation (n8n, Zapier, Make), custom nodes, webhook triggers, and AI-powered… | [aradiw/vibes-plug](https://github.com/aradiw/vibes-plug) (MIT) |
| n8n-api-shape | Use this skill when working with the n8n REST API — read, update, or verify workflows on ANY n8n instance.… | [JPeetz/agent-skills](https://github.com/JPeetz/agent-skills) (MIT, per-skill licence) |
| computer-use-and-browser-agents | 'Build agents that operate browsers and desktop GUIs via screenshots and actions. Covers Anthropic… | [jnPiyush/AgentX](https://github.com/jnPiyush/AgentX) (Apache-2.0) |

### Agent-building & multi-agent systems

| Skill | What it does | Source |
|---|---|---|
| subagent-driven-development | Use when executing implementation plans with independent tasks in the current session | [obra/superpowers](https://github.com/obra/superpowers) (MIT) |
| dispatching-parallel-agents | Use when facing 2+ independent tasks that can be worked on without shared state or sequential dependencies | [obra/superpowers](https://github.com/obra/superpowers) (MIT) |
| executing-plans | Use when executing an implementation plan in the current session as the implementer yourself — your human… | [obra/superpowers](https://github.com/obra/superpowers) (MIT) |
| agent-builder | Build PRODUCTION agentic systems — design for the failure path, eval + observe from commit one, one… | [GopalGB/codex-upgrade](https://github.com/GopalGB/codex-upgrade) (MIT) |
| swarm | Fan ONE task across multiple expert lenses IN PARALLEL — a swarm of isolated Codex workers (one per… | [GopalGB/codex-upgrade](https://github.com/GopalGB/codex-upgrade) (MIT) |
| multi-agent-orchestration | Expert guide for designing and orchestrating multi-agent systems, agent swarms, graph-based workflows… | [aradiw/vibes-plug](https://github.com/aradiw/vibes-plug) (MIT) |
| agent-memory | Add persistent memory to AI coding agents — file-based, vector, and semantic search memory systems that… | [TerminalSkills/skills](https://github.com/TerminalSkills/skills) (Apache-2.0) |
| agent-memory-management | Use this skill when designing, implementing, or debugging AI agent memory systems — long-term memory,… | [JPeetz/agent-skills](https://github.com/JPeetz/agent-skills) (MIT, per-skill licence) |
| agentic-eval | Use this skill when setting up or improving evaluation for AI agents and LLM outputs. Activates on "agent… | [JPeetz/agent-skills](https://github.com/JPeetz/agent-skills) (MIT, per-skill licence) |
| ai-agent-architecture | Use this skill when designing, auditing, or diagnosing an AI agent's system architecture. Activates on… | [JPeetz/agent-skills](https://github.com/JPeetz/agent-skills) (MIT, per-skill licence) |
| ai-llm-integration-expert | Expert guide for integrating Large Language Models (LLMs), Model Context Protocol (MCP), RAG architecture,… | [aradiw/vibes-plug](https://github.com/aradiw/vibes-plug) (MIT) |
| mcp-server-architect | Ultimate guide for designing, building, and security-hardening modern AI Tools/Bots via Model Context… | [aradiw/vibes-plug](https://github.com/aradiw/vibes-plug) (MIT) |
| mcp-server-building | Use this skill when building, scaffolding or shipping an MCP server: deciding tools vs resources vs… | [JPeetz/agent-skills](https://github.com/JPeetz/agent-skills) (MIT, per-skill licence) |
| vector-db-rag-expert | Expert guide for high-performance Vector Databases, RAG architectures, pgvector HNSW indexing, hybrid… | [aradiw/vibes-plug](https://github.com/aradiw/vibes-plug) (MIT) |
| self-evolving-memory-graph | Grants the AI long-term episodic memory. The agent autonomously documents the user's coding preferences,… | [aradiw/vibes-plug](https://github.com/aradiw/vibes-plug) (MIT) |
| prompt-engineering-concepts | Use this skill when choosing or fixing a prompt — the 20 core techniques (zero-shot, few-shot,… | [JPeetz/agent-skills](https://github.com/JPeetz/agent-skills) (MIT, per-skill licence) |
| ai-prompt-engineering-expert | Expert guide for systematic Prompt Engineering, Chain-of-Thought, few-shot prompting, structured output… | [aradiw/vibes-plug](https://github.com/aradiw/vibes-plug) (MIT) |
| token-optimizer | 'Use when managing instruction/context budgets, cache-aware tokenomics and cost estimates while preserving… | [jnPiyush/AgentX](https://github.com/jnPiyush/AgentX) (Apache-2.0) |
| crewai | CrewAI is a Python framework for building multi-agent AI systems: you define agents with roles, goals and… | [TerminalSkills/skills](https://github.com/TerminalSkills/skills) (Apache-2.0) |
| langgraph | Build stateful, multi-step AI agents and workflows with LangGraph. Use when a user asks to create AI… | [TerminalSkills/skills](https://github.com/TerminalSkills/skills) (Apache-2.0) |

### 3D & model design (more)

| Skill | What it does | Source |
|---|---|---|
| blender-modeling | Create and edit 3D meshes in Blender — primitives, hard-surface modeling, mesh operators, modifier stacks… | [RobLe3/cc-blender-skill](https://github.com/RobLe3/cc-blender-skill) (MIT) |
| blender-animation | Animate objects, cameras, lights, and properties in Blender — keyframes, F-curves, easing (Bezier, Linear,… | [RobLe3/cc-blender-skill](https://github.com/RobLe3/cc-blender-skill) (MIT) |
| blender-rendering | Render Blender scenes with the right engine and settings — Cycles for photoreal, EEVEE for speed/stylized,… | [RobLe3/cc-blender-skill](https://github.com/RobLe3/cc-blender-skill) (MIT) |
| blender-materials | Create and assign PBR materials in Blender via Principled BSDF — metals, glass, plastic, fabric, skin,… | [RobLe3/cc-blender-skill](https://github.com/RobLe3/cc-blender-skill) (MIT) |
| blender-lighting | Light Blender scenes professionally — three-point setups, HDRI environments, studio/cinematic/dramatic… | [RobLe3/cc-blender-skill](https://github.com/RobLe3/cc-blender-skill) (MIT) |
| blender-cameras | Set up Blender cameras with cinematic intent — focal length, depth of field (f-stop / focus object),… | [RobLe3/cc-blender-skill](https://github.com/RobLe3/cc-blender-skill) (MIT) |
| blender-export | Export Blender scenes to glTF/GLB (web/AR), FBX (game engines), OBJ (universal), USD (VFX pipelines), STL… | [RobLe3/cc-blender-skill](https://github.com/RobLe3/cc-blender-skill) (MIT) |
| blender-pro-workflow | End-to-end production workflow guidance for Blender — the order to assemble scenes (block-out → camera →… | [RobLe3/cc-blender-skill](https://github.com/RobLe3/cc-blender-skill) (MIT) |
| blender-scripting | Write and run Blender Python scripts for 3D automation and procedural modeling. Use when the user wants to… | [TerminalSkills/skills](https://github.com/TerminalSkills/skills) (Apache-2.0) |
| threejs | Three.js is a JavaScript library for building interactive 3D graphics in the browser with WebGL and… | [TerminalSkills/skills](https://github.com/TerminalSkills/skills) (Apache-2.0) |
| babylonjs | Babylon.js is an open-source 3D engine for the browser that renders with WebGL or WebGPU and includes a… | [TerminalSkills/skills](https://github.com/TerminalSkills/skills) (Apache-2.0) |
| web-3d-graphics-expert | Expert guide for WebGL and 3D graphics in the browser using Three.js, Babylon.js, React Three Fiber (R3F),… | [aradiw/vibes-plug](https://github.com/aradiw/vibes-plug) (MIT) |

### DevOps & infrastructure

| Skill | What it does | Source |
|---|---|---|
| ci-pipelines | Designs continuous integration pipelines that give a fast, honest merge signal — stage ordering,… | [arjunprabhulal/devops-skills](https://github.com/arjunprabhulal/devops-skills) (MIT) |
| deployment-strategies | Chooses and implements the deployment technique — blue-green, canary, rolling, or shadow — that buys the… | [arjunprabhulal/devops-skills](https://github.com/arjunprabhulal/devops-skills) (MIT) |
| terraform | 'Provision cloud infrastructure safely and consistently using Terraform and Infrastructure as Code… | [jnPiyush/AgentX](https://github.com/jnPiyush/AgentX) (Apache-2.0) |
| terraform-modules | Covers designing Terraform modules that are reusable and composable rather than copy-pasted or… | [arjunprabhulal/devops-skills](https://github.com/arjunprabhulal/devops-skills) (MIT) |
| github-actions-workflows | 'Create GitHub Actions workflows, reusable workflows, custom actions, and workflow automation. Use when… | [jnPiyush/AgentX](https://github.com/jnPiyush/AgentX) (Apache-2.0) |
| incident-response | Runs a live incident from first alert to resolution — assigning clear roles, mitigating before diagnosing,… | [arjunprabhulal/devops-skills](https://github.com/arjunprabhulal/devops-skills) (MIT) |
| secrets-management | Keeps credentials, API keys, and certificates out of code, images, and logs, and moves them into a real… | [arjunprabhulal/devops-skills](https://github.com/arjunprabhulal/devops-skills) (MIT) |
| maintenance | Use this skill when operating a self-hosted customer web stack (Cal.diy / Typebot / n8n / Postgres /… | [JPeetz/agent-skills](https://github.com/JPeetz/agent-skills) (MIT, per-skill licence) |
| git-workflow | Git best practices, branching strategies, commit conventions, and PR workflows. Use when reviewing git… | [AsyrafHussin/agent-skills](https://github.com/AsyrafHussin/agent-skills) (MIT) |
| using-git-worktrees | Use when starting feature work that needs isolation from current workspace or before executing… | [obra/superpowers](https://github.com/obra/superpowers) (MIT) |
| finishing-a-development-branch | Use when implementation is complete, all tests pass, and you need to decide how to integrate the work | [obra/superpowers](https://github.com/obra/superpowers) (MIT) |
| rollback-plan | Document how to roll back a specific deploy — code revert path, migration reversal or compatibility plan,… | [ryan-evans-git/ai-skills](https://github.com/ryan-evans-git/ai-skills) (MIT) |
| incident-postmortem | Author a blameless postmortem for a production incident — timeline, root cause, contributing factors,… | [ryan-evans-git/ai-skills](https://github.com/ryan-evans-git/ai-skills) (MIT) |
| deploy-checklist | Walk through a pre-deploy verification checklist — tests, migrations, rollback plan, feature flag,… | [ryan-evans-git/ai-skills](https://github.com/ryan-evans-git/ai-skills) (MIT) |

### Security

| Skill | What it does | Source |
|---|---|---|
| threat-modeling | Conduct structured threat modeling for software systems using established methodologies to identify,… | [seb1n/awesome-ai-agent-skills](https://github.com/seb1n/awesome-ai-agent-skills) (MIT) |
| security-audit | Perform a broad, authorized security audit across application, infrastructure, identity, dependencies, and… | [seb1n/awesome-ai-agent-skills](https://github.com/seb1n/awesome-ai-agent-skills) (MIT) |
| security-auditor | Run the security gate — secret scanning, SAST, and dependency-vuln audit — using already-installed… | [GopalGB/codex-upgrade](https://github.com/GopalGB/codex-upgrade) (MIT) |
| secrets-hygiene | Audit the repo for accidentally committed secrets, verify .env handling and .gitignore coverage, and… | [ryan-evans-git/ai-skills](https://github.com/ryan-evans-git/ai-skills) (MIT) |
| security-review | Review a diff or PR for security issues — OWASP Top 10, injection, broken auth, secrets, unsafe… | [ryan-evans-git/ai-skills](https://github.com/ryan-evans-git/ai-skills) (MIT) |

### QA & testing (more)

| Skill | What it does | Source |
|---|---|---|
| test-automation | 'Build and maintain automated test infrastructure for continuous testing. Use when setting up test… | [jnPiyush/AgentX](https://github.com/jnPiyush/AgentX) (Apache-2.0) |
| test-pyramid-audit | Audit the test suite's shape — ratio of unit / integration / end-to-end tests, mocking patterns, test… | [ryan-evans-git/ai-skills](https://github.com/ryan-evans-git/ai-skills) (MIT) |
| qa-test-plan | Author a QA test plan for a feature — manual and automated cases, prerequisites, data setup, edge cases,… | [ryan-evans-git/ai-skills](https://github.com/ryan-evans-git/ai-skills) (MIT) |
| bug-investigation | Systematically investigate a bug — reproduce, minimize, root-cause, fix, regression-test, write up. Use… | [ryan-evans-git/ai-skills](https://github.com/ryan-evans-git/ai-skills) (MIT) |
| visual-regression-testing | Set up and maintain visual regression tests — snapshot diffing per component and per page, with discipline… | [ryan-evans-git/ai-skills](https://github.com/ryan-evans-git/ai-skills) (MIT) |
| debugging-and-error-recovery | Use this skill when tests fail, builds break, runtime behavior doesn't match expectations, a bug report… | [JPeetz/agent-skills](https://github.com/JPeetz/agent-skills) (MIT, per-skill licence) |

### Web development (more)

| Skill | What it does | Source |
|---|---|---|
| typescript-react-patterns | TypeScript best practices for React development. Use when writing typed React components, hooks, events,… | [AsyrafHussin/agent-skills](https://github.com/AsyrafHussin/agent-skills) (MIT) |
| technical-debt | Technical debt inventory, prioritization, and audit for PHP/Laravel (MySQL) and Node/TypeScript/React… | [AsyrafHussin/agent-skills](https://github.com/AsyrafHussin/agent-skills) (MIT) |
| state-management | React Query and Zustand patterns for state management. Use when implementing data fetching, caching,… | [AsyrafHussin/agent-skills](https://github.com/AsyrafHussin/agent-skills) (MIT) |
| react-vite-best-practices | React and Vite performance optimization guidelines. Use when writing, reviewing, or optimizing React… | [AsyrafHussin/agent-skills](https://github.com/AsyrafHussin/agent-skills) (MIT) |
| project-docs | Project documentation lifecycle for PHP/Laravel and Node/TypeScript/React projects — bootstrapping… | [AsyrafHussin/agent-skills](https://github.com/AsyrafHussin/agent-skills) (MIT) |
| prd-writing | Step-by-step workflow for writing Product Requirements Documents. Use when creating PRDs, documenting… | [AsyrafHussin/agent-skills](https://github.com/AsyrafHussin/agent-skills) (MIT) |
| prd-creation | Author a Product Requirements Document for a new feature, epic, or product. Use whenever the user asks for… | [ryan-evans-git/ai-skills](https://github.com/ryan-evans-git/ai-skills) (MIT) |
| clean-code-principles | SOLID principles, design patterns, DRY, KISS, and clean code fundamentals. Use when reviewing… | [AsyrafHussin/agent-skills](https://github.com/AsyrafHussin/agent-skills) (MIT) |
| code-slop | Detect AI-generated code patterns ("slop") in PHP/Laravel and TypeScript/React source — comment narration,… | [AsyrafHussin/agent-skills](https://github.com/AsyrafHussin/agent-skills) (MIT) |
| laravel-best-practices | Laravel 13 conventions and best practices. Use when creating controllers, models, migrations, validation,… | [AsyrafHussin/agent-skills](https://github.com/AsyrafHussin/agent-skills) (MIT) |
| wordpress-headless-expert | Expert guide for headless WordPress architecture — WPGraphQL, ACF Pro, Faust.js, Next.js/Astro frontend,… | [aradiw/vibes-plug](https://github.com/aradiw/vibes-plug) (MIT) |
| diagram-as-code | Author, review, and maintain diagrams as code across Mermaid, PlantUML, Structurizr DSL, Graphviz DOT, and… | [jnPiyush/AgentX](https://github.com/jnPiyush/AgentX) (Apache-2.0) |
| readme-generator | Generate or refresh a project README with a consistent structure — what it is, why it exists, how to… | [ryan-evans-git/ai-skills](https://github.com/ryan-evans-git/ai-skills) (MIT) |
| requesting-code-review | Use when completing tasks, implementing major features, or before merging to verify work meets requirements | [obra/superpowers](https://github.com/obra/superpowers) (MIT) |
| receiving-code-review | Use when receiving code review feedback, before implementing suggestions, especially if feedback seems… | [obra/superpowers](https://github.com/obra/superpowers) (MIT) |
| safe-refactor | Use this skill when refactoring code — change structure without changing behavior, in small verified steps… | [JPeetz/agent-skills](https://github.com/JPeetz/agent-skills) (MIT, per-skill licence) |

### Writing & content

| Skill | What it does | Source |
|---|---|---|
| technical-writing | Write clear, concise, and accurate technical documentation including API references, user guides,… | [seb1n/awesome-ai-agent-skills](https://github.com/seb1n/awesome-ai-agent-skills) (MIT) |
| proofreading | Proofread and correct text for grammar, spelling, punctuation, style, clarity, and consistency, with… | [seb1n/awesome-ai-agent-skills](https://github.com/seb1n/awesome-ai-agent-skills) (MIT) |
| copywriting | Write compelling, persuasive marketing and sales copy using proven frameworks like AIDA, PAS, BAB, and… | [seb1n/awesome-ai-agent-skills](https://github.com/seb1n/awesome-ai-agent-skills) (MIT) |
| blog-post-writing | Write high-quality, SEO-optimized blog posts in multiple formats including how-to guides, listicles,… | [seb1n/awesome-ai-agent-skills](https://github.com/seb1n/awesome-ai-agent-skills) (MIT) |
| better-writing | Writes and reviews interface copy, from labels and errors to empty states and confirmations, so it matches… | [jakubkrehel/skills](https://github.com/jakubkrehel/skills) (MIT) |
| summarization | Summarize text using extractive, abstractive, hierarchical, and multi-document techniques, producing… | [seb1n/awesome-ai-agent-skills](https://github.com/seb1n/awesome-ai-agent-skills) (MIT) |
| deep-research | Conduct in-depth, multi-step research on a given topic by decomposing queries, finding diverse sources,… | [seb1n/awesome-ai-agent-skills](https://github.com/seb1n/awesome-ai-agent-skills) (MIT) |
| fact-checking | Verify the accuracy of claims and statements by extracting individual assertions, identifying… | [seb1n/awesome-ai-agent-skills](https://github.com/seb1n/awesome-ai-agent-skills) (MIT) |
| discernment-nudge | After you give a substantive answer or draft that the user may act on — advice or recommendations, drafted… | [anthropics/skills](https://github.com/anthropics/skills) (Apache-2.0) |

### Sales, business & productivity

| Skill | What it does | Source |
|---|---|---|
| sales-email-sequences | Design multi-touch outbound email sequences with personalized messaging, timing cadences, and… | [seb1n/awesome-ai-agent-skills](https://github.com/seb1n/awesome-ai-agent-skills) (MIT) |
| proposal-generation | Create tailored sales proposals and RFP responses that address prospect needs, articulate solution value,… | [seb1n/awesome-ai-agent-skills](https://github.com/seb1n/awesome-ai-agent-skills) (MIT) |
| lead-scoring | Score and prioritize leads based on firmographic fit and behavioral engagement signals, producing ranked… | [seb1n/awesome-ai-agent-skills](https://github.com/seb1n/awesome-ai-agent-skills) (MIT) |
| go-to-market-launch | Use this skill when planning a launch, beta, or GTM push. | [JPeetz/agent-skills](https://github.com/JPeetz/agent-skills) (MIT, per-skill licence) |
| project-management | Manages software projects end-to-end — decomposing work into tasks, tracking progress across sprints,… | [seb1n/awesome-ai-agent-skills](https://github.com/seb1n/awesome-ai-agent-skills) (MIT) |
| file-organization | Automatically organizes files in a directory into a clean structure based on configurable rules — by file… | [seb1n/awesome-ai-agent-skills](https://github.com/seb1n/awesome-ai-agent-skills) (MIT) |

### Documents & spreadsheets

| Skill | What it does | Source |
|---|---|---|
| pdf | Use this skill whenever the user wants to do anything with PDF files. This includes reading or extracting… | [anthropics/skills](https://github.com/anthropics/skills) (Apache-2.0) |
| pptx | Use this skill any time a .pptx or .potx file is involved in any way — as input, output, or both. This… | [anthropics/skills](https://github.com/anthropics/skills) (Apache-2.0) |
| xlsx | Use this skill any time a spreadsheet file is the primary input or output. This means any task where the… | [anthropics/skills](https://github.com/anthropics/skills) (Apache-2.0) |
| xlsx-wrangler | Read, inspect, transform, and export large Excel (.xlsx) files WITHOUT loading them fully into memory and… | [GopalGB/codex-upgrade](https://github.com/GopalGB/codex-upgrade) (MIT) |

### Design (more)

| Skill | What it does | Source |
|---|---|---|
| better-ui | Polishes surfaces, icons and motion with exact values for border radius, optical alignment, shadows, icon… | [jakubkrehel/skills](https://github.com/jakubkrehel/skills) (MIT) |
| better-typography | Sets and reviews how text renders, from the type scale and spacing to font features, wrapping, truncation… | [jakubkrehel/skills](https://github.com/jakubkrehel/skills) (MIT) |
| better-layout | Sets grouping, alignment, reading order, responsive structure and room for translated text, so a layout… | [jakubkrehel/skills](https://github.com/jakubkrehel/skills) (MIT) |
| better-interface | Reviews a screen, flow or whole interface across accessibility, layout, writing, typography, color and UI… | [jakubkrehel/skills](https://github.com/jakubkrehel/skills) (MIT) |
| better-accessibility | Reviews and fixes keyboard and focus behavior, ARIA, accessible names, forms, screen-reader announcements,… | [jakubkrehel/skills](https://github.com/jakubkrehel/skills) (MIT) |
| state-machine | Renders every state of a component you choose on a throwaway page, with mock data and a switcher, so you… | [jakubkrehel/skills](https://github.com/jakubkrehel/skills) (MIT) |
| explain-interface | Explains how a website, a visual effect or an animation was built, from a live URL or a screenshot. | [jakubkrehel/skills](https://github.com/jakubkrehel/skills) (MIT) |
| build-design | Builds UI from a Figma file or a design image so it matches the design, using the project's existing… | [jakubkrehel/skills](https://github.com/jakubkrehel/skills) (MIT) |
| site-motion-excellence-director | Use when planning, auditing, specifying, implementing, or improving premium website/app motion across… | [frankxai/awesome-motion-design-agent-skills](https://github.com/frankxai/awesome-motion-design-agent-skills) (CC0) |
| motion-director | Use when designing motion concepts, animation systems, choreography, timing, easing, reduced-motion… | [frankxai/awesome-motion-design-agent-skills](https://github.com/frankxai/awesome-motion-design-agent-skills) (CC0) |
| generative-media-director | Use when planning, prompting, generating, editing, routing, finishing, or QAing AI-created images, GIFs,… | [frankxai/awesome-motion-design-agent-skills](https://github.com/frankxai/awesome-motion-design-agent-skills) (CC0) |
| ui-ux-engineer | Distinctive, production-grade, taste-driven UI/UX engineering — the OPPOSITE of generic AI-slop. Use for… | [GopalGB/codex-upgrade](https://github.com/GopalGB/codex-upgrade) (MIT) |

### Video & audio

| Skill | What it does | Source |
|---|---|---|
| ai-video-generator | Generate short-form videos with AI — script writing, text-to-speech narration, stock footage selection,… | [TerminalSkills/skills](https://github.com/TerminalSkills/skills) (Apache-2.0) |
| ffmpeg | Transcode, convert, edit, and process audio and video with FFmpeg. Use when a user asks to convert video… | [TerminalSkills/skills](https://github.com/TerminalSkills/skills) (Apache-2.0) |

### System design

| Skill | What it does | Source |
|---|---|---|
| sde-system-design-method | Drive any system-design problem through the canonical 5-step flow: requirements, estimation, API, data… | [GopalGB/codex-upgrade](https://github.com/GopalGB/codex-upgrade) (MIT) |
| sde-scalability-horizontal-scaling | Scale out with stateless services, vertical vs horizontal tradeoffs, and the path from single server to… | [GopalGB/codex-upgrade](https://github.com/GopalGB/codex-upgrade) (MIT) |
| sde-refactoring | Improve code structure without changing behavior - small safe steps under test coverage, smell-driven,… | [GopalGB/codex-upgrade](https://github.com/GopalGB/codex-upgrade) (MIT) |

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
- https://github.com/obra/superpowers — MIT (already listed above)
- https://github.com/GopalGB/codex-upgrade — MIT
- https://github.com/ryan-evans-git/ai-skills — MIT
- https://github.com/jnPiyush/AgentX — Apache-2.0
- https://github.com/aradiw/vibes-plug — MIT
- https://github.com/arjunprabhulal/devops-skills — MIT
- https://github.com/TerminalSkills/skills — Apache-2.0
- https://github.com/JPeetz/agent-skills — MIT (per-skill licence files)
- https://github.com/RobLe3/cc-blender-skill — MIT

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
- **alib8b8/awesome-ai-agent-tools** — no licence file anywhere in the repo,
  so none of its skills were used (most are copies of obra/superpowers anyway).
- **SamyakJ05/skills-and-agents (314 skills)** — a vendored aggregator; the
  useful 3D part (RobLe3/cc-blender-skill) was taken directly from upstream
  instead.
- **JPeetz/agent-skills** — only 10 of its 110 skills were taken (the best
  agent, data, security and DevOps ones); the rest overlap the bundle or are
  too niche. Its per-skill LICENSE files were kept.
- **TerminalSkills/skills (~1000 skills)** — only 12 were taken; the rest
  overlap the bundle or are single-tool reference skills. Apache-2.0.
- **GopalGB/codex-upgrade** — only 8 of its 383 skills were taken; the
  xls/vba series (40+ Excel/VBA skills) was left out except `xlsx-wrangler`.
- **anthropics/skills `doc-coauthoring`** — still no licence file in its
  folder, so it stays excluded. `academy-guide` is a learning-hub guide, not
  a task skill, so it was left out too.

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
