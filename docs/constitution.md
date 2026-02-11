# Mind-Nodes Project Constitution

> The foundational document defining why Mind-Nodes exists, what it aims to achieve, and the principles guiding its development.

---

## 1. Project Identity

### 1.1 Name and Tagline

- **Name:** Mind-Nodes
- **Tagline:** *An open-source Python mind mapping application with full XMind compatibility*

### 1.2 Version Designation

| Version Range | Meaning |
|---------------|---------|
| `v0.1.0` – `v0.9.x` | Pre-release development milestones |
| `v1.0.0` | Feature-complete parity with XMind core capabilities |
| `v1.x.x` | Stability, performance, and polish releases |
| `v2.0.0+` | Next-generation features (collaboration, AI, etc.) |

### 1.3 License

**MIT License** — chosen for maximum adoption. Permits commercial use, modification, distribution, and private use with minimal restrictions. Compatible with the LGPL-licensed PySide6 dependency.

---

## 2. Vision and Mission

### 2.1 Vision Statement

A fully open-source, cross-platform, Python-native mind mapping desktop application that matches XMind's feature set while providing extensibility through plugins and scriptability through Python APIs.

### 2.2 Mission Statement

Deliver a performant, visually polished mind mapping tool built entirely in Python, capable of reading and writing `.xmind` files natively, supporting 9+ layout algorithms, full theming, and a plugin architecture that empowers the community to extend every aspect of the application.

### 2.3 Target Users

| User Group | Primary Need |
|------------|-------------|
| Knowledge workers | Brainstorming, organizing ideas, meeting notes |
| Project managers | Work breakdown structures, task visualization |
| Students & educators | Study guides, lecture notes, curriculum mapping |
| Software developers | Architecture diagrams, feature planning, documentation |
| Researchers | Literature mapping, concept analysis, taxonomy building |
| Open-source advocates | XMind-compatible tooling without proprietary lock-in |

---

## 3. Core Principles

### 3.1 XMind Fidelity

Feature parity with XMind is the north star. Every core XMind capability must have a corresponding Mind-Nodes implementation. The `.xmind` file format is treated as the primary interchange format — files created in XMind must open correctly in Mind-Nodes, and vice versa.

### 3.2 Python-Native

The entire application is built in Python. C/C++ extensions are permitted only for performance-critical rendering paths where pure Python cannot meet the 60fps target. All business logic, data models, and algorithms remain in Python for readability and contributor accessibility.

### 3.3 Separation of Concerns

The application follows a strict 4-layer architecture. The data model knows nothing about rendering. The layout engine knows nothing about UI widgets. The file I/O layer operates on model objects, not visual items. This separation enables independent testing, replacement, and extension of each layer.

> Cross-reference: Layer definitions in [blueprint.md](blueprint.md) Section 1.

### 3.4 Extensibility First

The plugin architecture is not an afterthought — it is a first-class design concern from day one. Layout algorithms, file format handlers, exporters, theme packs, marker packs, and UI panels are all pluggable. The core application itself uses the same plugin interfaces that third-party extensions use.

### 3.5 Cross-Platform

Windows, macOS, and Linux are all first-class citizens. No platform-specific code in the core application. Platform-specific behavior (file dialogs, native menus, system tray) is handled through PySide6's cross-platform abstractions.

### 3.6 File Format Compatibility

Native `.xmind` (Zen format) read/write with lossless round-trip as the goal. Unknown fields in `.xmind` files are preserved during load/save to avoid data loss when Mind-Nodes encounters features it doesn't yet support.

### 3.7 Performance

The application must feel responsive on modern hardware. Maps with hundreds of nodes must render smoothly. Layout algorithms must complete in sub-second time. The application must not block the UI thread during file I/O or export operations.

### 3.8 Accessibility

Full keyboard navigation for all operations. Screen reader compatibility via Qt accessibility APIs. High-contrast theme included by default. Color choices in themes must meet WCAG AA contrast ratios for text readability.

---

## 4. Scope — Features In

### 4.1 Core Mind Mapping (MVP)

- **Node/Topic CRUD** — Create, read, update, delete topics at any level in the hierarchy
- **Unlimited hierarchy depth** — No artificial limit on nesting levels
- **Root nodes** — Each sheet has exactly one central root topic
- **Child topics** — Attached children that follow the layout algorithm
- **Floating topics** — Detached topics with explicit x,y positions on the canvas
- **Callouts** — Speech-bubble annotations attached to any topic
- **Relationship arrows** — Freeform connections between any two topics with optional text labels
- **Boundaries** — Visual grouping containers around a range of sibling topics
- **Summaries** — Bracket annotations spanning a range of siblings, linking to a summary topic
- **Notes** — Rich text notes attached to individual topics (plain text + HTML subset)
- **Labels** — Short text tags displayed on topics
- **Markers/Icons** — 350+ categorized icons assignable to topics (priority, task progress, flags, stars, smileys, arrows, symbols, months, weekdays, people)
- **Hyperlinks** — URL links attached to topics, openable in the system browser
- **Images** — Embedded images within topic nodes
- **Folding** — Collapse/expand subtrees to manage visual complexity

### 4.2 Layout Algorithms (9+ Structures)

| Layout | Structure Class | Description |
|--------|----------------|-------------|
| Mind Map (Radial) | `org.xmind.ui.map` | Balanced radial expansion from center |
| Logic Chart | `org.xmind.ui.logic.right/left` | Horizontal tree flow |
| Org Chart | `org.xmind.ui.org-chart.down/up` | Vertical hierarchy |
| Tree Chart | `org.xmind.ui.tree.right/left` | Indented tree structure |
| Brace Map | `org.xmind.ui.brace.right` | Brace-connected groupings |
| Timeline | `org.xmind.ui.timeline.horizontal/vertical` | Chronological sequence |
| Fishbone | `org.xmind.ui.fishbone.leftHeaded/rightHeaded` | Ishikawa cause-effect diagram |
| Matrix | `org.xmind.ui.spreadsheet` | Grid/row-column arrangement |
| Tree Table | `org.xmind.ui.spreadsheet.column` | Hybrid tree + table columns |

Each topic can specify its own `structureClass`, allowing mixed layouts within a single map (e.g., radial root with org-chart subtrees).

### 4.3 Visual and Styling

- **Color themes** — Predefined themes, custom theme creation, smart auto-generation from a seed color
- **Node shapes** — Rectangle, rounded rectangle, ellipse, diamond, parallelogram, cloud, underline, no border
- **Text formatting** — Font family, size, weight (bold), style (italic), underline, color, alignment
- **Border styling** — Color, width, dash pattern per node
- **Shadow effects** — Drop shadows on nodes for depth
- **Gradient backgrounds** — Linear gradient fills on nodes
- **Branch line styling** — Color, width, dash pattern, curve style (Bezier, straight, elbow, rounded elbow), tapered lines
- **Canvas backgrounds** — Solid color, wallpaper images, optional grid overlay
- **350+ built-in marker icons** — Organized by category (priority, task, flag, star, smiley, arrow, symbol, month, week, people)
- **Custom images** — Embed images into topics from local files

### 4.4 File I/O

**Primary format:**
- Native `.xmind` format (ZIP archive with `content.json`, `metadata.json`, `manifest.json`, thumbnails, and embedded resources)

**Export formats:**
- PNG (raster image)
- SVG (vector graphic)
- PDF (paginated document)
- Markdown (hierarchical text outline)
- OPML (Outline Processor Markup Language)
- FreeMind XML (`.mm`)

**Import formats:**
- XMind (`.xmind`)
- FreeMind (`.mm`)
- OPML (`.opml`)
- Markdown (`.md`)

> Cross-reference: File format specifications in [artifacts.md](artifacts.md) Section 2.

### 4.5 Advanced Features

- **Multiple sheets per workbook** — Tabbed interface for multiple maps in one file
- **Outline view** — Hierarchical text view of the map, fully editable, bidirectionally synced with canvas
- **Presentation mode** — Full-screen slideshow walking through the map branch by branch
- **Unlimited undo/redo** — Every operation reversible via Command pattern
- **Auto-save** — Periodic background saves with crash recovery
- **Full-text search** — Find topics by text content, highlight matches on canvas
- **Find and replace** — Bulk text replacement across all topics
- **Keyboard shortcuts** — Comprehensive keybindings for all operations, user-customizable
- **Drag-and-drop** — Reparent topics by dragging on canvas
- **Context menus** — Right-click menus for topics, relationships, and canvas
- **Minimap** — Overview widget for navigating large maps
- **Zoom** — Smooth zoom from 10% to 500% via mouse wheel, pinch, or toolbar

### 4.6 Post-MVP Features (v2.0+)

- Real-time multi-user collaboration via CRDT/OT
- Share by link with permission management
- Comments and activity log
- Export to Word/DOCX, PowerPoint/PPTX, Excel/CSV
- Plugin marketplace/registry
- Localization/internationalization (i18n)
- ICS calendar export for task dates
- Gantt chart view (simplified task timeline)

---

## 5. Scope — Non-Goals

The following are explicitly **out of scope** for Mind-Nodes:

| Non-Goal | Rationale |
|----------|-----------|
| Mobile applications (iOS/Android) | Desktop-only focus; mobile would require different UI paradigm |
| Web-based version | This is a native desktop application; web would require entirely different tech stack |
| Full project management (Gantt, resource allocation, budgets) | Mind mapping tool, not a PM suite; simplified task view only |
| AI-powered features (auto-suggestion, content generation, smart layout) | Keep core deterministic and predictable; AI can be a future plugin |
| Cloud storage backend | Local-first philosophy; cloud sync deferred as a future plugin |
| Electron/web technology stack | Python + Qt only; no JavaScript runtime |
| Video/audio embedding | Out of scope for a mind mapping tool |
| Real-time whiteboarding/freehand drawing | Mind mapping is structured; freehand is a different tool category |

---

## 6. Success Criteria

### 6.1 Functional Criteria

- [ ] Can open any `.xmind` file created by XMind 2020+ and render it with correct structure, styling, and layout
- [ ] Can save files that XMind 2024 can open without data loss on supported features
- [ ] All 9 layout algorithms produce visually correct, non-overlapping results
- [ ] Undo/redo works for every single operation without model corruption
- [ ] All file format importers/exporters produce valid output matching their format specifications
- [ ] Outline view stays perfectly synchronized with canvas edits and vice versa
- [ ] Presentation mode correctly walks through all branches

### 6.2 Performance Criteria

| Metric | Target |
|--------|--------|
| Cold startup time | < 2 seconds on modern hardware |
| Canvas panning/zooming | Smooth 60fps with 500 nodes visible |
| Node operation response (add/delete/move) | < 100ms |
| Full re-layout of 1000-node map | < 5 seconds |
| File open (100-node .xmind) | < 1 second |
| File save (100-node .xmind) | < 1 second |
| PNG export (500-node map) | < 3 seconds |
| Memory usage (500-node map) | < 500 MB |

### 6.3 Quality Criteria

- [ ] \> 80% unit test coverage on model and layout engine modules
- [ ] \> 60% test coverage on UI modules (via pytest-qt)
- [ ] Zero known data-loss bugs at any release
- [ ] Passes `mypy --strict` type checking on all source files
- [ ] Passes `ruff check` and `ruff format --check` with zero violations
- [ ] All public APIs documented with docstrings
- [ ] CI pipeline green on Python 3.11, 3.12, 3.13 across Linux, macOS, Windows

### 6.4 Compatibility Criteria

- [ ] Runs on Windows 10+, macOS 12+, Ubuntu 22.04+
- [ ] Installs via `pip install mindnodes` from PyPI
- [ ] Installable via standalone executable on all three platforms (PyInstaller/Nuitka)
- [ ] `.xmind` files created by Mind-Nodes are accepted by XMind 2024 without errors

---

## 7. Stakeholders and Governance

### 7.1 Decision-Making Process

During the `v0.x` development phase, the project follows a single-maintainer model with decisions made pragmatically. For major architectural changes, decisions are documented as Architecture Decision Records (ADRs) in [blueprint.md](blueprint.md).

Post `v1.0`, the project will adopt an RFC (Request for Comments) process for significant changes, where proposals are discussed in GitHub issues before implementation begins.

### 7.2 Contribution Guidelines

Community contributions are welcome from day one. All contributions must:
- Pass the CI pipeline (lint, type-check, test)
- Include tests for new functionality
- Follow existing code patterns and architecture
- Not introduce new dependencies without discussion

> Cross-reference: Contribution setup in [skeleton.md](skeleton.md) Section 7.

---

## 8. Document Cross-References

| Topic | Document |
|-------|----------|
| System architecture and component design | [blueprint.md](blueprint.md) |
| Data model schemas and file format specs | [artifacts.md](artifacts.md) |
| Phased build plan and testing strategy | [implementation-guide.md](implementation-guide.md) |
| Project directory structure and dependencies | [skeleton.md](skeleton.md) |
