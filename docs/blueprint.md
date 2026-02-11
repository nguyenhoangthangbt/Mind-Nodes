# Mind-Nodes System Architecture Blueprint

> The technical architecture document defining how Mind-Nodes is structured, what components exist, how they interact, and the key technology decisions governing the implementation.

---

## 1. Architectural Overview

### 1.1 Layered Architecture

Mind-Nodes follows a strict 4-layer architecture. Dependencies flow downward only — upper layers depend on lower layers, never the reverse.

```
┌─────────────────────────────────────────────────────────────┐
│                   LAYER 1: PRESENTATION                      │
│  MainWindow │ Canvas (Scene/View) │ Panels │ Dialogs │ Menus │
├─────────────────────────────────────────────────────────────┤
│               LAYER 2: APPLICATION LOGIC                     │
│  Commands (Undo/Redo) │ Controllers │ Services │ Clipboard   │
├─────────────────────────────────────────────────────────────┤
│                  LAYER 3: DOMAIN MODEL                       │
│  Workbook │ Sheet │ Topic │ Relationship │ Style │ Theme     │
├─────────────────────────────────────────────────────────────┤
│                 LAYER 4: INFRASTRUCTURE                      │
│  File I/O │ Layout Engine │ Plugin Loader │ Settings │ Utils  │
└─────────────────────────────────────────────────────────────┘
```

**Layer 1 — Presentation:** PySide6 widgets, QGraphicsView/QGraphicsScene canvas, dock widget panels, dialogs, menus, and toolbars. Handles user input events and visual rendering.

**Layer 2 — Application Logic:** The Command pattern (QUndoStack) for all model mutations, controllers that translate user gestures into commands, services for cross-cutting concerns (auto-save, search, clipboard).

**Layer 3 — Domain Model:** Pure data classes (Pydantic v2 models) representing the mind map structure. Workbook contains Sheets, each Sheet has a root Topic tree and Relationships. Models emit change signals for observers.

**Layer 4 — Infrastructure:** File I/O handlers (read/write various formats), the layout engine (computes node positions), plugin loader, application settings, and shared utilities.

### 1.2 Key Architectural Decisions

| ADR | Decision | Rationale |
|-----|----------|-----------|
| ADR-001 | PySide6 over PyQt6 | LGPL license permits commercial distribution without paid license; identical API surface |
| ADR-002 | QGraphicsView for canvas | Built-in zoom, pan, selection, BSP spatial indexing, item transformation; purpose-built for 2D interactive graphics |
| ADR-003 | Command pattern via QUndoStack | PySide6 provides QUndoStack/QUndoCommand natively; supports command merging, macro commands, and clean undo/redo semantics |
| ADR-004 | Pydantic v2 for domain models | Automatic validation, JSON serialization/deserialization, strong type hints, immutable value objects via `frozen=True` |
| ADR-005 | Plugin architecture via entry_points | Standard Python packaging mechanism; no custom discovery needed; plugins are installable via pip |
| ADR-006 | Strict model/view separation | Domain model classes have zero knowledge of rendering; visual items observe model changes via signals |
| ADR-007 | .xmind as primary format | Industry-standard mind map format; enables interoperability with XMind and other tools |
| ADR-008 | Python 3.11+ minimum | Structural pattern matching, improved type hints, significant performance improvements over 3.10 |

---

## 2. Technology Stack

### 2.1 Core Runtime

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| Language | Python | 3.11+ | Application runtime |
| GUI Framework | PySide6 | 6.6+ | Widgets, graphics, signals/slots |
| Data Models | Pydantic | 2.5+ | Model validation, JSON serialization |

### 2.2 Key Libraries

| Library | Purpose |
|---------|---------|
| `zipfile` (stdlib) | .xmind archive read/write |
| `json` (stdlib) | content.json parsing/generation |
| `uuid` (stdlib) | Topic ID generation |
| `pathlib` (stdlib) | Cross-platform path handling |
| `logging` (stdlib) | Structured application logging |
| `lxml` | FreeMind XML import/export |
| `Pillow` | Image processing, thumbnail generation, PNG export |
| `svgwrite` | SVG export |
| `reportlab` | PDF export |
| `markdown-it-py` | Markdown import/export parsing |

### 2.3 Development Tools

| Tool | Purpose |
|------|---------|
| `pytest` + `pytest-qt` | Unit, integration, and UI testing |
| `pytest-cov` | Test coverage measurement |
| `mypy` | Static type checking (strict mode) |
| `ruff` | Linting and code formatting |
| `pre-commit` | Git hook management |
| `sphinx` + `sphinx-rtd-theme` | API documentation generation |
| `nuitka` or `PyInstaller` | Standalone executable packaging |

---

## 3. Component Architecture

### 3.1 Domain Model Layer

The domain model is a tree of pure data objects with no rendering or UI logic.

```
Workbook
├── id: UUID
├── title: str
├── sheets: list[Sheet]        ─── ordered, at least one
├── created_at: datetime
└── modified_at: datetime

Sheet
├── id: UUID
├── title: str
├── root_topic: Topic          ─── exactly one root
├── relationships: list[Relationship]
├── theme: Theme | None
└── style_map: dict[str, Style]

Topic (recursive tree node)
├── id: UUID
├── title: str
├── children_attached: list[Topic]    ─── layout-managed children
├── children_detached: list[Topic]    ─── floating topics (explicit x,y)
├── notes: Notes | None
├── labels: list[str]
├── markers: list[MarkerRef]
├── href: str | None
├── style: Style | None
├── structure_class: StructureClass | None
├── image: ImageRef | None
├── position: Position | None         ─── only for detached/floating topics
├── boundaries: list[Boundary]
├── summaries: list[Summary]
├── callouts: list[Callout]
├── branch: BranchStyle | None
└── is_folded: bool
```

**Key design rules:**
- All domain objects are Pydantic v2 models with validation
- IDs are UUID4 by default but accept any string for XMind compatibility
- Topic tree traversal utilities: `walk_depth_first()`, `walk_breadth_first()`, `find_topic_by_id()`, `get_ancestors()`, `get_descendants()`
- Model mutations emit change signals for observer notification
- Unknown/extension JSON fields are preserved in a `_extra` dict for lossless round-trip

> Cross-reference: Full schema definitions in [artifacts.md](artifacts.md) Section 1.

### 3.2 Command System (Undo/Redo Engine)

Every model mutation goes through a Command object. No code outside the command system directly modifies model state.

```
MindNodeCommand(QUndoCommand)
├── redo()     ─── apply the change
├── undo()     ─── reverse the change
├── id()       ─── command type ID (for merging)
└── mergeWith() ─── merge with previous command of same type
```

**Command classes:**

| Category | Commands |
|----------|----------|
| Topic | `AddTopicCommand`, `DeleteTopicCommand`, `EditTopicTitleCommand`, `MoveTopicCommand`, `ReorderChildrenCommand`, `ReparentTopicCommand`, `ToggleFoldCommand` |
| Relationship | `AddRelationshipCommand`, `DeleteRelationshipCommand` |
| Style | `ChangeStyleCommand`, `ChangeThemeCommand` |
| Boundary | `AddBoundaryCommand`, `DeleteBoundaryCommand` |
| Summary | `AddSummaryCommand`, `DeleteSummaryCommand` |
| Callout | `AddCalloutCommand`, `DeleteCalloutCommand` |
| Marker | `AddMarkerCommand`, `RemoveMarkerCommand` |
| Notes | `EditNotesCommand` |
| Compound | `BatchCommand` (wraps multiple commands for atomic undo), `PasteSubtreeCommand` |

**Stack architecture:**
- One `QUndoStack` per Sheet
- One `QUndoGroup` at the Workbook level, switching active stack with active sheet tab
- Command merging for rapid-fire edits (e.g., typing text merges consecutive `EditTopicTitleCommand` instances into a single undo step)

### 3.3 Layout Engine

The layout engine computes (x, y, width, height) coordinates for every topic node given the tree structure and the active layout algorithm.

```
LayoutAlgorithm (ABC)
├── layout(root: Topic, config: LayoutConfig) -> dict[str, NodeGeometry]
└── structure_class() -> str

NodeGeometry
├── x, y: float              ─── top-left corner position
├── width, height: float     ─── node bounding box
├── connector_in: Point      ─── incoming branch attachment point
├── connector_out: Point     ─── outgoing branch attachment point
└── branch_points: list[Point]  ─── intermediate branch path control points
```

**Layout implementations:**

| Class | Algorithm | Key Technique |
|-------|-----------|--------------|
| `RadialMapLayout` | Balanced radial expansion | Modified Reingold-Tilford; angular sectors proportional to descendant count; left/right balancing for first-level children |
| `LogicChartLayout` | Horizontal tree | Standard Reingold-Tilford; parent on left, children stacked vertically on right; configurable direction |
| `OrgChartLayout` | Vertical hierarchy | Top-down Reingold-Tilford; parent centered above children |
| `TreeChartLayout` | Indented tree | Each child indented below parent; siblings stacked vertically |
| `BraceMapLayout` | Brace grouping | Brace connector between parent and child group; horizontal arrangement |
| `TimelineLayout` | Chronological sequence | Linear horizontal/vertical axis with alternating above/below placement |
| `FishboneLayout` | Cause-effect diagonal | Spine axis with angled branches at 45/135 degrees; sub-causes branch orthogonally |
| `MatrixLayout` | Grid arrangement | Row-column grid; headers define axes; cells contain topics |
| `TreeTableLayout` | Tree + table hybrid | Tree structure on left; table columns extend to the right |

**Layout registry:**
- Maps `structureClass` strings (e.g., `"org.xmind.ui.map"`) to layout algorithm classes
- Supports mixed layouts: each Topic can override the layout for its subtree
- Default layout: `RadialMapLayout` for root topics without explicit `structureClass`

**Layout animation:**
- When layout changes (node added, structure changed), new positions are computed
- `QPropertyAnimation` smoothly interpolates items from old positions to new positions
- Animation duration: 300ms with ease-in-out curve

### 3.4 Canvas / Rendering Layer

The canvas uses Qt's QGraphicsView framework — a proven architecture for 2D interactive graphics applications.

**Scene (`MindMapScene : QGraphicsScene`):**
- Owns all visual items (topics, branches, relationships, boundaries, summaries, callouts)
- Manages selection state (single, multi-select, rubber-band)
- Handles drag-and-drop zones for topic reparenting
- Renders canvas background (solid color, grid, wallpaper)
- Coordinate system: scene coordinates in logical units (not pixels)

**View (`MindMapView : QGraphicsView`):**
- Zoom: mouse wheel + Ctrl+scroll, pinch gesture, toolbar slider (10%–500%)
- Pan: middle-mouse-button drag, Space+left-click drag, scroll bars
- Viewport culling: only renders items visible in the current viewport
- Minimap: overlay widget showing the full map with viewport indicator
- Rubber-band selection: drag on empty canvas area to select multiple items

**Visual items (`QGraphicsObject` subclasses):**

| Item | Renders |
|------|---------|
| `TopicItem` | Node shape, text (rich text via QTextDocument), icons/markers row, labels bar, image, fold indicator (+/- button) |
| `BranchItem` | Curved/straight/elbow/rounded-elbow connector lines between parent and child topic items, with optional tapering |
| `RelationshipItem` | Arrow path with optional label between any two topic items, with control point handles for editing |
| `BoundaryItem` | Enclosing rounded-rectangle or cloud shape around a group of sibling topic items |
| `SummaryItem` | Bracket shape spanning sibling items, connecting to a summary topic item |
| `CalloutItem` | Speech-bubble shape with connector to parent topic item |
| `FloatingTopicItem` | Standalone topic item at explicit canvas coordinates (subclass of TopicItem) |

**Rendering pipeline:**
```
User action
  → Controller creates Command
    → Command.redo() mutates Domain Model
      → Model emits change signal
        → Layout engine computes new geometry
          → SceneBuilder updates item positions
            → View repaints affected region
```

### 3.5 UI Shell (Main Window)

```
┌──────────────────────────────────────────────────────────────┐
│  Menu Bar: File │ Edit │ View │ Insert │ Format │ Map │ Help │
├──────────────────────────────────────────────────────────────┤
│  Toolbar: [New] [Open] [Save] │ [Undo] [Redo] │ [Add Topic] │
│           [Add Subtopic] [Delete] │ [Zoom] │ [Layout ▼]     │
├────────────┬─────────────────────────────────┬───────────────┤
│            │                                 │               │
│  Outline   │     Canvas (MindMapView)        │  Properties   │
│  Panel     │                                 │  Panel        │
│            │     ┌──────────────┐            │               │
│  - Root    │     │  Root Topic  │            │  Title: ___   │
│    - Child │     │     / \      │            │  Style: ___   │
│      - Sub │     │  Ch1  Ch2   │            │  Notes: ___   │
│    - Child │     │   |    |    │            │  Markers: ___ │
│            │     │  Sub  Sub   │            │  Link: ___    │
│            │     └──────────────┘            │               │
│            │                                 │               │
├────────────┴───────────────────┬─────────────┴───────────────┤
│  Sheet Tabs: [Sheet 1] [Sheet 2] [+]                        │
├─────────────────────────────────────────────────────────────┤
│  Status Bar: Zoom: 100% │ Nodes: 42 │ Modified │ Auto-saved │
└─────────────────────────────────────────────────────────────┘
```

**Dock panels (all QDockWidget — user can rearrange, float, close, resize):**

| Panel | Description |
|-------|-------------|
| `PropertiesPanel` | Context-sensitive editor for the selected item(s): title, style properties, notes, markers, labels, hyperlink, image |
| `OutlinePanel` | QTreeView showing hierarchical text outline of the map; fully editable; bidirectionally synced with canvas |
| `MarkerPanel` | Categorized grid of all 350+ marker icons; click to apply to selected topic, or drag onto a topic |
| `SearchPanel` | Full-text search box, results list, highlight/navigate matching nodes on canvas; find-and-replace mode |
| `ThemePanel` | Theme gallery, style presets, color palette editor |

**Sheet tabs:**
- `QTabWidget` with one `MindMapView` per sheet
- Tab context menu: rename, duplicate, delete, move left/right
- "+" button to add new sheet

### 3.6 File I/O Subsystem

Abstract handler pattern with a registry for format discovery.

```
FileHandler (ABC)
├── can_load(path: Path) -> bool
├── load(path: Path) -> Workbook
├── can_save(path: Path) -> bool
├── save(workbook: Workbook, path: Path) -> None
└── supported_extensions() -> list[str]

Exporter (ABC)    ─── export-only (no import)
├── export(workbook: Workbook, path: Path, options: ExportOptions) -> None
└── supported_extensions() -> list[str]
```

**Concrete handlers:**

| Handler | Extensions | Direction |
|---------|-----------|-----------|
| `XMindHandler` | `.xmind` | Read + Write |
| `MindNodesHandler` | `.mindnodes` | Read + Write |
| `FreeMindHandler` | `.mm` | Read + Write |
| `OPMLHandler` | `.opml` | Read + Write |
| `MarkdownHandler` | `.md` | Read + Write |
| `PNGExporter` | `.png` | Export only |
| `SVGExporter` | `.svg` | Export only |
| `PDFExporter` | `.pdf` | Export only |

**Handler registry:**
- Maps file extensions to handler classes
- Auto-detection: check file extension first, then sniff ZIP magic bytes for `.xmind`
- File dialogs dynamically built from registered handlers' supported extensions

> Cross-reference: File format specifications in [artifacts.md](artifacts.md) Section 2.

### 3.7 Plugin Architecture

Plugins extend Mind-Nodes through standard Python packaging conventions.

**Plugin discovery:**
- Uses `importlib.metadata.entry_points(group="mindnodes.plugins")`
- Plugins are standard Python packages installable via pip
- No need for custom plugin directories or manifest files

**Plugin interface:**
```python
class MindNodesPlugin(ABC):
    def activate(self, app: MindNodesApp) -> None: ...
    def deactivate(self) -> None: ...
    def get_layouts(self) -> list[type[LayoutAlgorithm]]: ...
    def get_file_handlers(self) -> list[type[FileHandler]]: ...
    def get_commands(self) -> list[type[MindNodeCommand]]: ...
    def get_menu_actions(self) -> list[QAction]: ...
    def get_toolbar_actions(self) -> list[QAction]: ...
    def get_panel_widgets(self) -> list[type[QDockWidget]]: ...
    def get_marker_packs(self) -> list[MarkerPack]: ...
    def get_themes(self) -> list[Theme]: ...
```

**Extension points:**
- Custom layout algorithms
- Custom file importers/exporters
- Custom toolbar and menu actions
- Custom dock panel widgets
- Custom marker icon packs
- Custom color themes

**Plugin manager:**
- Discovers installed plugins at startup
- Enable/disable plugins via settings
- Dependency resolution between plugins
- Plugin manager UI in settings dialog

### 3.8 Settings and Configuration

**Storage:** `QSettings` with INI backend for cross-platform compatibility.

**Settings categories:**

| Category | Examples |
|----------|----------|
| Appearance | Default theme, canvas background, show grid, grid size |
| Behavior | Auto-save interval, undo limit, default structure class |
| Keybindings | Action-to-key-sequence mappings (150+ shortcuts) |
| File | Recent files list (max 20), default save format, export defaults |
| Plugins | Enable/disable map per plugin ID |
| Window | Window geometry, dock panel arrangement, last active sheet |

**Settings dialog:** Categorized tab interface for editing all settings with live preview.

---

## 4. Data Flow Diagrams

### 4.1 User Interaction Flow

```
User clicks "Add Subtopic"
  │
  ▼
MenuBar/Toolbar/Shortcut handler
  │
  ▼
Controller creates AddTopicCommand(parent_id, new_topic)
  │
  ▼
QUndoStack.push(command)  ──── triggers command.redo()
  │
  ▼
command.redo():
  ├── parent_topic.children_attached.append(new_topic)
  └── sheet.emit(topic_added, parent_id, new_topic)
        │
        ▼
      SceneBuilder receives signal
        ├── Creates TopicItem for new topic
        ├── Creates BranchItem connecting parent to child
        ├── Requests layout recomputation
        │     │
        │     ▼
        │   LayoutEngine.layout(root_topic, config)
        │     │
        │     ▼
        │   Returns dict[topic_id -> NodeGeometry]
        │
        ├── Animates all items to new positions
        └── View repaints
```

### 4.2 File Open Flow

```
User selects File > Open > "project.xmind"
  │
  ▼
FileHandlerRegistry.get_handler(".xmind")
  │
  ▼
XMindHandler.load("project.xmind")
  ├── zipfile.ZipFile opens archive
  ├── Reads content.json → parses JSON
  ├── Builds Workbook model from JSON
  │     ├── Creates Sheet objects
  │     ├── Recursively builds Topic trees
  │     ├── Creates Relationship objects
  │     └── Applies Style and Theme objects
  ├── Extracts resources/ images to temp cache
  └── Returns Workbook
        │
        ▼
App receives Workbook
  ├── Creates MindMapScene per Sheet
  ├── SceneBuilder populates items
  ├── LayoutEngine computes geometry per Sheet
  ├── Creates tabs in TabManager
  └── View renders first sheet
```

### 4.3 File Save Flow

```
User selects File > Save (or auto-save triggers)
  │
  ▼
FileHandlerRegistry.get_handler(current_path.suffix)
  │
  ▼
XMindHandler.save(workbook, path)  ──── runs on QThread worker
  ├── Serializes Workbook → content.json dict
  │     ├── Iterates sheets
  │     ├── Recursively serializes Topic trees
  │     ├── Serializes Relationships, Styles, Themes
  │     └── Preserves _extra fields for lossless round-trip
  ├── Generates metadata.json
  ├── Generates manifest.json
  ├── Renders thumbnail PNG (256x256)
  ├── Copies resource images
  ├── Writes ZIP archive atomically (write to temp, then rename)
  └── Emits save_complete signal
        │
        ▼
Main thread receives signal
  ├── Updates window title (removes "Modified" indicator)
  ├── Updates status bar
  └── Resets auto-save timer
```

### 4.4 Undo/Redo Flow

```
User presses Ctrl+Z
  │
  ▼
QUndoStack.undo()
  │
  ▼
Last command's undo() executes
  ├── Reverts model to pre-command state
  │     (e.g., removes the added topic, restores deleted topic)
  └── Emits model change signals
        │
        ▼
SceneBuilder receives signals
  ├── Updates/creates/removes visual items as needed
  ├── Requests layout recomputation
  └── Animates items to new positions
```

---

## 5. Concurrency Model

### 5.1 Threading Rules

| Thread | Responsibilities |
|--------|-----------------|
| **Main thread** | All UI rendering, scene operations, model mutations, command execution, signal/slot dispatch |
| **File I/O worker** (QThread) | Loading and saving large files; emits signals back to main thread on completion |
| **Export worker** (QThread) | Rendering PNG, SVG, PDF exports; progress reported via signals |
| **Auto-save worker** (QThread) | Background periodic saves; serializes model snapshot, writes to recovery directory |
| **Plugin loader** (QThread) | Plugin discovery and initialization at startup (avoids blocking app launch) |

### 5.2 Thread Safety Rules

1. **The domain model is main-thread-only.** No worker thread may read or write model objects directly.
2. Worker threads operate on **serialized copies** (JSON dicts, byte buffers) — not live model references.
3. All **worker-to-main communication** uses Qt's signal/slot mechanism with `Qt.QueuedConnection` (the default for cross-thread signals).
4. File save workers receive a **deep-copied snapshot** of the model's serialized form, so the user can continue editing while the save completes.
5. Progress reporting uses signals: `progress_updated(int)`, `operation_complete(result)`, `operation_failed(error)`.

---

## 6. Error Handling Strategy

### 6.1 Exception Hierarchy

```
MindNodesError (base)
├── FileFormatError          ─── corrupt/unsupported file format
│   ├── XMindFormatError     ─── specific to .xmind parsing
│   └── ImportFormatError    ─── import format parsing errors
├── LayoutError              ─── layout algorithm failures
├── PluginError              ─── plugin load/activation failures
│   ├── PluginLoadError
│   └── PluginActivationError
├── CommandError             ─── command execution failures
└── ValidationError          ─── model validation failures
```

### 6.2 Error Presentation

| Severity | Presentation | Examples |
|----------|-------------|----------|
| Info | Status bar message (auto-dismiss 5s) | "Auto-saved", "3 topics found" |
| Warning | Status bar message (persistent) | "Unknown markers ignored during import" |
| Error (recoverable) | Modal dialog with details | "Failed to export PNG: permission denied" |
| Error (data risk) | Modal dialog + recovery options | "File appears corrupted. Open recovery file?" |
| Fatal | Modal dialog + graceful shutdown | "Qt rendering context lost" |

### 6.3 Crash Recovery

1. **Auto-save timer** runs every 60 seconds (configurable)
2. Auto-save writes to `~/.mindnodes/recovery/{workbook_id}.mindnodes.recovery`
3. On startup, the app checks for recovery files newer than their corresponding saved files
4. If recovery files found: dialog offers "Restore recovered version" or "Discard recovery"
5. Recovery files are deleted after successful manual save

---

## 7. Security Considerations

### 7.1 File Handling

| Threat | Mitigation |
|--------|-----------|
| ZIP bomb | Enforce max decompressed size (100 MB default); abort extraction if exceeded |
| Path traversal | Sanitize all file paths from ZIP entries; reject paths containing `..` or absolute paths |
| Malformed JSON | Validate content.json against expected schema before deserialization; catch and report parse errors |
| Oversized images | Limit embedded image dimensions (max 4096x4096) and file size (max 10 MB per image) |
| Resource exhaustion | Limit max nodes per map (configurable, default 10,000); warn user when approaching limit |

### 7.2 Plugin Security

- **v1.0:** Plugins run in-process with full Python capabilities (no sandboxing)
- **Post-v1.0:** Plugin signing and verification system
- **Mitigation:** Plugins are installed via pip, so standard PyPI security practices apply; users are warned when enabling third-party plugins

---

## 8. Document Cross-References

| Topic | Document |
|-------|----------|
| Project principles, scope, and success criteria | [constitution.md](constitution.md) |
| Data model schemas (full field definitions) | [artifacts.md](artifacts.md) Section 1 |
| File format specifications | [artifacts.md](artifacts.md) Section 2 |
| API interface contracts | [artifacts.md](artifacts.md) Section 3 |
| Phased build order | [implementation-guide.md](implementation-guide.md) |
| Directory structure and module listing | [skeleton.md](skeleton.md) |
