<h1 align="center" style="font-size: 32px;">
  RustaSea Documentation 🌊
</h1>

<p align="center" style="font-size: 20px;">
  <strong>Laravel ergonomics. Rust safety.</strong>
</p>

<p align="center">
  The documentation site for <a href="https://github.com/rustasea/framework">RustaSea</a> —
  a web application framework for Rust. Built with
  <a href="https://www.docubook.pro/">DocuBook Flame</a>, compiled to flat static HTML.
</p>

---

## What this repo is

A documentation-only project. There is no framework code here — the content
describes the RustaSea framework, sourced from the upstream
[`rustasea/framework`](https://github.com/rustasea/framework) repository.

`docu.json` is the single source of truth for site identity, landing page, and
navigation. Every `.mdx` file in `docs/` compiles to a matching static page.

## Site configuration

Everything below is driven by `docu.json`.

| Area           | Setting                             |
| -------------- | ----------------------------------- |
| Title          | RustaSea                            |
| Tagline        | Laravel ergonomics. Rust safety.    |
| Tagline (hero) | `#RustaSea`                         |
| Accent colour  | `#EE4712` (`themes.colors.primary`) |
| Sidebar style  | `separator` (`sidebar.context`)     |
| Base URL       | `http://localhost:3000`             |
| Logo           | `docs/assets/images/logo.svg`       |
| Favicon        | `docs/assets/images/favicon.ico`    |
| OG image       | `docs/assets/images/og.png`         |

### Landing page

The hero offers two actions: **Get Started** → `/docs/getting-started/overview`
and **GitHub** → the upstream repository. It is followed by three feature
cards:

| Card                | Icon       | Links to                    |
| ------------------- | ---------- | --------------------------- |
| Typed Routing       | `Route`    | `/docs/guide/routing`       |
| Fluent ORM          | `Database` | `/docs/guide/orm`           |
| Agentic Development | `Bot`      | `/docs/getting-started/mcp` |

### Repository links

`repo` points at [`rustasea/framework`](https://github.com/rustasea/framework)
on `blob/master/{filePath}`, with **`edit: true`** — every page renders an
"edit this page" link. Because the docs live in this repo but the source lives
upstream, those links resolve against the framework repository rather than the
MDX file being edited. Set `edit: false` if that is not the intent.

## Navigation

15 pages across three sections, defined explicitly in `docu.json.routes`:

| Section         | Icon       | Pages                                                                                                                                                                                                                                                                                                                                           |
| --------------- | ---------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Getting Started | `Rocket`   | [Overview](/docs/getting-started/overview) · [Installation](/docs/getting-started/installation) · [Configuration](/docs/getting-started/configuration) · [AI Agents & MCP](/docs/getting-started/mcp)                                                                                                                                           |
| Guide           | `BookOpen` | [Architecture](/docs/guide/architecture) · [Routing & HTTP](/docs/guide/routing) · [ORM & Database](/docs/guide/orm) · [Auth & Validation](/docs/guide/auth) · [Queues, Cache & Events](/docs/guide/queues) · [CLI & Testing](/docs/guide/cli-testing) · [Storage, AI & Real-time](/docs/guide/advanced) · [Deployment](/docs/guide/deployment) |
| Reference       | `Library`  | [Artisan Commands](/docs/reference/artisan) · [Tech Stack](/docs/reference/tech-stack) · [Milestones](/docs/reference/milestones)                                                                                                                                                                                                               |

Section headers use `noLink: true`, so they group pages without being
navigable targets themselves.

## Content conventions

- **Every claim is source-backed** from the upstream README and `docs/`.
- **Milestone status is labelled explicitly.** M2 is complete; M0, M1, and
  M3–M6 are partial. Pages carry `:::info` / `:::warning` callouts pointing to
  upstream `docs/milestones.md` as authoritative.
- **The roadmap timeline is marked aspirational**, not a commitment.
- Each page is **self-contained** — navigation is handled by pagination, so
  pages do not end with manual "Next" lists.

## Local development

**Bun** (used in this repo)

```bash
bun install
bun run dev        # http://localhost:3000
bun run build      # static output in .docu/dist/
bun run preview
```

## Writing docs

1. Create `docs/<section>/<page>.mdx` with `title` and `description` frontmatter.
2. Register it in `docu.json.routes` — routes drive the sidebar, the file alone
   is not enough.
3. Add feature cards, hero copy, or `repo` changes in `docu.json` as needed.

Pages support MDX plus directive components (`:::tip`, `:::warning`, `::::tabs`,
`::::cards`) and Mermaid diagrams (`flowchart`, `sequenceDiagram`, `journey`,
`classDiagram`).

## Deployment

Flame emits flat static HTML to `.docu/dist/` — deploy to any static host.

```bash
bun run deploy     # builds + GitHub Pages workflow
bun run build      # then upload .docu/dist/ anywhere
```

---

## License

MIT
