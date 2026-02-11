# Mind-Nodes Implementation Guide

> The phased development plan for building Mind-Nodes from an empty repository to a fully functional XMind-clone mind mapping application. Each phase produces a working, testable increment.

---

## 1. Development Methodology

### 1.1 Iterative Milestones

Development follows 11 sequential phases (0–10). Each phase:
- Produces a **working, testable** application increment
- Has **clear verification criteria** that must pass before proceeding
- Lists the **exact modules** created or modified
- Modules within a phase **can be parallelized** across developers

### 1.2 Testing Strategy

| Test Type | Tool | Coverage Target | What It Tests |
|-----------|------|----------------|---------------|
| Unit tests | `pytest` | 80% on models, commands, layout | Individual classes and functions |
| Integration tests | `pytest` | File round-trip, command sequences | Cross-module interactions |
| UI tests | `pytest-qt` | 60% on UI modules | Widget behavior, signals, rendering |
| Visual regression | Screenshot comparison | All 9+ layouts | Layout algorithm correctness |
| Type checking | `mypy --strict` | 100% pass | Static type safety |
| Linting | `ruff check` | 100% pass | Code style and common errors |

**Test naming convention:** `test_{module}/test_{class}_{method}_{scenario}.py`

### 1.3 CI/CD Pipeline

**GitHub Actions workflow (ci.yml):**
```
Trigger: push to main, pull requests
Matrix: Python {3.11, 3.12, 3.13} × OS {ubuntu-latest, macos-latest, windows-latest}

Steps:
1. Checkout code
2. Set up Python with version from matrix
3. Install dependencies: pip install -e ".[dev]"
4. Lint: ruff check src/ tests/
5. Format check: ruff format --check src/ tests/
6. Type check: mypy src/
7. Test: pytest --cov=mindnodes --cov-report=xml tests/
8. Upload coverage report
```

**Release workflow (release.yml):**
```
Trigger: tag push matching v*
Steps:
1–7. Same as CI
8. Build executables (PyInstaller/Nuitka) for Linux, macOS, Windows
9. Create GitHub release with binaries
10. Publish to PyPI
```

### 1.4 Phase Dependency Matrix

```
Phase 0  ──────────────────────────────────────────────────> All phases
Phase 1  ──────────────────────> Phases 2, 3, 4, 5
Phase 2  ──────────────────────────────────────> Phase 7
Phase 3  ──────────────────────> Phases 4, 5, 6
Phase 4  ──────────────────────────────────────> Phase 8
Phase 5  ──────────────────────> Phase 6
Phases 6, 7, 8 ───────────────────────────────> Phase 9
Phase 9  ──────────────────────────────────────> Phase 10
```

---

## 2. Phase 0 — Project Bootstrap

**Goal:** Set up the project skeleton with tooling, a minimal PySide6 window, and CI pipeline.

### 2.1 Tasks

1. Create `pyproject.toml` with PEP 621 metadata, tool configurations ([tool.ruff], [tool.mypy], [tool.pytest.ini_options]), and entry points
2. Create `src/mindnodes/` package with:
   - `__init__.py` — package version (`__version__ = "0.1.0"`)
   - `__main__.py` — entry point: `from mindnodes.app import main; main()`
   - `app.py` — `QApplication` subclass that opens an empty `QMainWindow` with title "Mind-Nodes"
   - `constants.py` — application name, version, config paths, default settings
3. Create `.gitignore`, `.pre-commit-config.yaml`, `Makefile`
4. Create `.github/workflows/ci.yml`
5. Create `tests/conftest.py` with basic fixtures
6. Create `README.md` with project overview and install instructions

### 2.2 Verification

```bash
# Application launches
python -m mindnodes
# → Opens an empty PySide6 window titled "Mind-Nodes"

# Tests pass
pytest tests/ -v
# → All tests pass (basic smoke test)

# Linting passes
ruff check src/ tests/
ruff format --check src/ tests/

# Type checking passes
mypy src/
```

### 2.3 Modules Created

| Module | Description |
|--------|-------------|
| `src/mindnodes/__init__.py` | Package version |
| `src/mindnodes/__main__.py` | Module entry point |
| `src/mindnodes/app.py` | QApplication, MainWindow shell |
| `src/mindnodes/constants.py` | App-wide constants |
| `pyproject.toml` | Project metadata and tool config |
| `.github/workflows/ci.yml` | CI pipeline |
| `tests/conftest.py` | Test fixtures |

> Cross-reference: Full directory layout in [skeleton.md](skeleton.md) Section 1.

---

## 3. Phase 1 — Domain Model

**Goal:** Implement all Pydantic v2 data model classes with validation, factory functions, and tree traversal utilities.

### 3.1 Tasks

1. Implement all model classes from [artifacts.md](artifacts.md) Section 1:
   - `Workbook`, `Sheet`, `Topic`, `Relationship`, `Boundary`, `Summary`, `Callout`, `Notes` (`PlainContent`, `HtmlContent`), `Style`, `StyleProperties`, `Theme`, `MapStyle`, `MarkerRef`, `ImageRef`, `Position`, `BranchStyle`
2. Implement enums:
   - `StructureClass` — all 17 values from artifacts.md Section 1.15
   - `StyleType` — `topic`, `relationship`, `boundary`, `summary`, `map`
   - `Shape` — `rect`, `rounded-rect`, `ellipse`, `diamond`, `parallelogram`, `cloud`, `underline`, `none`
3. Implement `types.py` — `Position`, `ImageRef`, `BranchStyle` as frozen Pydantic models
4. Implement `factory.py` — convenience constructors:
   - `create_workbook(title?) -> Workbook`
   - `create_sheet(title?) -> Sheet`
   - `create_topic(title?) -> Topic`
   - `create_relationship(end1_id, end2_id, title?) -> Relationship`
5. Implement `validators.py` — cross-model validation:
   - `validate_sheet(sheet)` — ensure all relationship endpoints reference valid topic IDs
   - `validate_no_cycles(topic)` — ensure no circular parent-child references
   - `validate_id_uniqueness(sheet)` — ensure all topic IDs are unique within a sheet
   - `validate_boundary_ranges(topic)` — ensure boundary ranges are within bounds
6. Implement tree traversal utilities on `Topic`:
   - `walk_depth_first(topic) -> Iterator[Topic]`
   - `walk_breadth_first(topic) -> Iterator[Topic]`
   - `find_topic_by_id(root, topic_id) -> Topic | None`
   - `get_all_topic_ids(root) -> set[str]`
   - `get_depth(topic, root) -> int`
   - `count_descendants(topic) -> int`
7. Implement marker catalog in `markers.py`:
   - `MARKER_CATALOG: dict[str, list[str]]` — group name → list of marker IDs
   - `is_valid_marker(marker_id) -> bool`
8. Write comprehensive unit tests (target: 100+ tests)

### 3.2 Key Implementation Details

- All models use `pydantic.BaseModel` with `model_config = ConfigDict(extra="allow")` to preserve unknown fields in `_extra` for round-trip fidelity
- `Topic` uses `children_attached: list[Topic] = []` — Pydantic handles recursive model definitions natively
- IDs default to `str(uuid4())` via `Field(default_factory=lambda: str(uuid4()))`
- `StyleProperties` uses all-optional fields with `None` defaults — only explicitly set properties override theme defaults
- Model mutations will be done through methods (not direct assignment) to enable signal emission in later phases

### 3.3 Verification

```bash
# All model tests pass
pytest tests/test_models/ -v --tb=short

# Can build a 5-level topic tree programmatically
python -c "
from mindnodes.models.factory import create_workbook, create_topic
wb = create_workbook('Test')
root = wb.sheets[0].root_topic
for i in range(5):
    child = create_topic(f'Level {i+1}')
    root.children_attached.append(child)
    root = child
print('5-level tree created successfully')
"

# Can serialize to dict and back
python -c "
from mindnodes.models.factory import create_workbook
wb = create_workbook('Test')
d = wb.model_dump()
from mindnodes.models.workbook import Workbook
wb2 = Workbook.model_validate(d)
assert wb.id == wb2.id
print('Round-trip serialization works')
"

# Type checking passes
mypy src/mindnodes/models/
```

### 3.4 Modules Created

| Module | Key Classes |
|--------|-------------|
| `src/mindnodes/models/__init__.py` | Re-exports all model classes |
| `src/mindnodes/models/workbook.py` | `Workbook` |
| `src/mindnodes/models/sheet.py` | `Sheet` |
| `src/mindnodes/models/topic.py` | `Topic` + tree traversal functions |
| `src/mindnodes/models/relationship.py` | `Relationship` |
| `src/mindnodes/models/boundary.py` | `Boundary` |
| `src/mindnodes/models/summary.py` | `Summary` |
| `src/mindnodes/models/callout.py` | `Callout` |
| `src/mindnodes/models/notes.py` | `Notes`, `PlainContent`, `HtmlContent` |
| `src/mindnodes/models/style.py` | `Style`, `StyleProperties` |
| `src/mindnodes/models/theme.py` | `Theme`, `MapStyle` |
| `src/mindnodes/models/markers.py` | `MarkerRef`, `MARKER_CATALOG` |
| `src/mindnodes/models/enums.py` | `StructureClass`, `StyleType`, `Shape` |
| `src/mindnodes/models/types.py` | `Position`, `ImageRef`, `BranchStyle` |
| `src/mindnodes/models/validators.py` | Validation functions |
| `src/mindnodes/models/factory.py` | Factory constructors |

---

## 4. Phase 2 — File I/O: XMind Format

**Goal:** Read and write `.xmind` ZIP archives with full content.json support. Achieve lossless round-trip for supported features.

### 4.1 Tasks

1. Implement `src/mindnodes/io/base.py` — `FileHandler` and `Exporter` abstract base classes (from [artifacts.md](artifacts.md) Section 3.3)
2. Implement `src/mindnodes/io/registry.py` — `FileHandlerRegistry` class:
   - Register handler by extensions
   - Look up handler by file path
   - Generate file dialog filter strings
3. Implement `src/mindnodes/io/xmind/reader.py` — `XMindReader`:
   - Open ZIP archive with `zipfile.ZipFile`
   - Parse `content.json` → list of Sheet dicts
   - Recursively build `Topic` trees from JSON
   - Map XMind field names to Mind-Nodes field names (see [artifacts.md](artifacts.md) Section 2.1.1 mapping table)
   - Parse `metadata.json` for creator info and active sheet
   - Extract embedded images from `resources/` to temp cache directory
   - Handle missing optional fields gracefully
   - Preserve unknown fields in `_extra` for round-trip fidelity
4. Implement `src/mindnodes/io/xmind/writer.py` — `XMindWriter`:
   - Serialize `Workbook` → `content.json` dict
   - Map Mind-Nodes field names back to XMind field names (reverse mapping)
   - Generate `metadata.json` with Mind-Nodes creator info
   - Generate `manifest.json` listing all archive entries
   - Copy embedded images to `resources/` in archive
   - Write ZIP archive atomically (write to temp file, then rename)
5. Implement `src/mindnodes/io/xmind/schema.py` — field name mapping constants:
   - `XMIND_TO_MINDNODES: dict[str, str]` — camelCase → snake_case mappings
   - `MINDNODES_TO_XMIND: dict[str, str]` — reverse mappings
   - `XMIND_SHAPE_MAP: dict[str, str]` — XMind shape classes → shape enum values
   - `XMIND_STYLE_PROPERTY_MAP` — XMind CSS property names → StyleProperties fields
6. Implement `XMindHandler(FileHandler)` facade combining reader and writer
7. Create test fixture files:
   - `tests/fixtures/sample_basic.xmind` — 3-level map with basic structure
   - `tests/fixtures/sample_complex.xmind` — map with relationships, boundaries, summaries, markers, notes, styles, images
   - `tests/fixtures/sample_multisheet.xmind` — workbook with 3 sheets
8. Write round-trip integration tests

### 4.2 Key Implementation Details

- **ZIP bomb protection:** Check total decompressed size before extraction; abort if > 100 MB
- **Path traversal protection:** Sanitize all paths from ZIP entries; reject `..` components and absolute paths
- **Unknown field preservation:** When reading, store any JSON fields not in our schema in `_extra`; when writing, merge `_extra` back into the output JSON
- **Atomic writes:** Write to `{path}.tmp` first, then `os.replace()` to the final path — prevents corruption on crash during save
- **Style property parsing:** XMind uses SVG/XSL-FO property names (e.g., `svg:fill`, `fo:color`, `fo:font-size`); parse these to Mind-Nodes property names and vice versa
- **Range parsing:** Boundary/Summary ranges in XMind are strings like `"(0,2)"`; parse to `range_start=0, range_end=2`

### 4.3 Verification

```bash
# Round-trip test: load → save → reload → compare
pytest tests/test_io/test_xmind_roundtrip.py -v

# Load real XMind files
pytest tests/test_io/test_xmind_reader.py -v

# Save and verify ZIP structure
pytest tests/test_io/test_xmind_writer.py -v

# Verify generated .xmind files can be opened by xmindparser (Python library)
python -c "
from mindnodes.io.xmind import XMindHandler
from pathlib import Path
handler = XMindHandler()
wb = handler.load(Path('tests/fixtures/sample_basic.xmind'))
handler.save(wb, Path('/tmp/test_output.xmind'))
wb2 = handler.load(Path('/tmp/test_output.xmind'))
assert wb.sheets[0].root_topic.title == wb2.sheets[0].root_topic.title
print('Round-trip successful')
"
```

### 4.4 Modules Created

| Module | Description |
|--------|-------------|
| `src/mindnodes/io/__init__.py` | Package init |
| `src/mindnodes/io/base.py` | `FileHandler`, `Exporter` ABCs |
| `src/mindnodes/io/registry.py` | `FileHandlerRegistry` |
| `src/mindnodes/io/xmind/__init__.py` | `XMindHandler` facade |
| `src/mindnodes/io/xmind/reader.py` | `XMindReader` |
| `src/mindnodes/io/xmind/writer.py` | `XMindWriter` |
| `src/mindnodes/io/xmind/schema.py` | Field mapping constants |

---

## 5. Phase 3 — Canvas Rendering Foundation

**Goal:** Render topic nodes and branch lines on an interactive QGraphicsScene canvas with zoom, pan, and selection.

### 5.1 Tasks

1. Implement `MindMapScene(QGraphicsScene)`:
   - Item management: add/remove TopicItems, BranchItems
   - Selection handling: single click, Ctrl+click multi-select
   - Background rendering: solid color, optional grid
   - Signal emissions for selection changes
2. Implement `MindMapView(QGraphicsView)`:
   - Zoom: mouse wheel with Ctrl (10%–500%), smooth zoom animation
   - Pan: middle-mouse-button drag, Space+left-click drag
   - Viewport culling: `setViewportUpdateMode(MinimalViewportUpdate)`
   - Rubber-band selection on empty canvas drag
   - `setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)`
3. Implement `TopicItem(QGraphicsObject)`:
   - Paint method: background shape → border → text → markers row → labels → fold indicator
   - Text rendering via `QTextDocument` (supports rich text)
   - Shape rendering: rect, rounded-rect, ellipse (using QPainterPath)
   - Selection visual: blue outline, resize handles
   - Double-click to edit title (inline `QGraphicsTextItem`)
   - Size computation: measure text + markers + image + padding → bounding rect
4. Implement `BranchItem(QGraphicsItem)`:
   - Renders connector line from parent TopicItem to child TopicItem
   - Line styles: `curve` (cubic Bezier), `straight`, `elbow`, `rounded-elbow`
   - Updates automatically when parent or child item moves
   - Color and width from style
5. Implement `SceneBuilder`:
   - Takes `Workbook` model + layout geometry results
   - Creates `TopicItem` for each Topic, positioned according to geometry
   - Creates `BranchItem` for each parent-child connection
   - Provides `rebuild(sheet)` to clear and recreate all items
   - Provides `update_positions(geometry)` to move existing items (for animation)
6. Implement `base_item.py` — shared base class for all canvas items with common utilities

### 5.2 Key Implementation Details

- `TopicItem` uses `QGraphicsObject` (not `QGraphicsItem`) because `QGraphicsObject` supports Qt signals, which are needed for position-change notifications
- `BranchItem` connects to parent/child `TopicItem.geometryChanged` signals to update its path when nodes move
- Scene uses `setItemIndexMethod(QGraphicsScene.NoIndex)` because nodes move frequently during layout animations — BSP tree rebuilds would be expensive
- Use `QGraphicsDropShadowEffect` for node shadows (when style has `shadow_enabled=True`)
- Inline title editing: on double-click, create a `QGraphicsTextItem` positioned over the topic title; on focus-out or Enter, emit `title_edit_finished` signal

### 5.3 Verification

```bash
# Visual smoke test: render a hardcoded 3-level tree
python -c "
from mindnodes.app import create_app
from mindnodes.models.factory import create_workbook, create_topic
from mindnodes.ui.canvas.scene import MindMapScene
from mindnodes.ui.canvas.view import MindMapView
# ... create app, build model, create scene, show view
"
# → Window shows topic nodes with branch lines

# Canvas interaction tests
pytest tests/test_ui/test_scene.py -v
pytest tests/test_ui/test_topic_item.py -v
pytest tests/test_ui/test_view.py -v

# Zoom and pan work smoothly (manual verification)
```

### 5.4 Modules Created

| Module | Key Classes |
|--------|-------------|
| `src/mindnodes/ui/__init__.py` | Package init |
| `src/mindnodes/ui/canvas/__init__.py` | Package init |
| `src/mindnodes/ui/canvas/scene.py` | `MindMapScene` |
| `src/mindnodes/ui/canvas/view.py` | `MindMapView` |
| `src/mindnodes/ui/canvas/scene_builder.py` | `SceneBuilder` |
| `src/mindnodes/ui/canvas/items/__init__.py` | Package init |
| `src/mindnodes/ui/canvas/items/base_item.py` | `BaseItem` |
| `src/mindnodes/ui/canvas/items/topic_item.py` | `TopicItem` |
| `src/mindnodes/ui/canvas/items/branch_item.py` | `BranchItem` |

---

## 6. Phase 4 — Layout Engine

**Goal:** Implement the layout algorithm framework and the 4 most important layout algorithms. Wire layout results to the canvas.

### 6.1 Tasks

1. Implement `LayoutAlgorithm` ABC and `LayoutConfig` dataclass (from [artifacts.md](artifacts.md) Section 3.2)
2. Implement `NodeGeometry` dataclass
3. Implement `LayoutRegistry`:
   - Register layout class by `structure_class` string
   - Look up layout by structure class
   - Default fallback: `RadialMapLayout`
4. Implement **RadialMapLayout** (`org.xmind.ui.map`):
   - Modified Reingold-Tilford for radial placement
   - Root at center; first-level children distributed left and right
   - Angular sectors proportional to descendant count
   - Subtree spacing to prevent overlap
5. Implement **LogicChartLayout** (`org.xmind.ui.logic.right`, `.left`):
   - Standard Reingold-Tilford horizontal tree
   - Parent on left/right, children stacked vertically on opposite side
   - Configurable direction (left or right)
6. Implement **OrgChartLayout** (`org.xmind.ui.org-chart.down`, `.up`):
   - Top-down/bottom-up Reingold-Tilford
   - Parent centered above/below children
7. Implement **TreeChartLayout** (`org.xmind.ui.tree.right`, `.left`):
   - Indented tree: each child indented below parent
   - Siblings stacked vertically
8. Implement `utils.py` — shared geometry utilities:
   - `measure_topic_size(topic, style) -> (width, height)` — compute node size from content
   - `compute_subtree_bounds(geometries) -> (x, y, w, h)` — bounding box of all nodes
9. Wire layout engine to SceneBuilder:
   - After model changes, SceneBuilder calls `LayoutEngine.layout(root, config)`
   - SceneBuilder updates `TopicItem` positions from returned `NodeGeometry` dict
   - Animate transitions with `QPropertyAnimation` (300ms ease-in-out)
10. Implement `animation.py` — layout transition animation helpers

### 6.2 Algorithm Details

#### RadialMapLayout (Primary)

```
                    ┌─────┐
              ┌─────│Root │─────┐
              │     └─────┘     │
         ┌────┴────┐      ┌────┴────┐
         │ Child 1 │      │ Child 2 │
         └────┬────┘      └────┬────┘
          ┌───┴───┐        ┌───┴───┐
          │Sub 1.1│        │Sub 2.1│
          └───────┘        └───────┘
```

**Algorithm steps:**
1. **Measure** all node sizes (text + markers + padding)
2. **Assign sides:** first-level children split left/right for balance (by total descendant count)
3. **Compute subtree sizes:** bottom-up, each node's subtree height = max(children heights) + gaps
4. **Position left subtrees:** walk tree top-down, assign y-offsets based on subtree sizes, x = parent.x - gap - width
5. **Position right subtrees:** mirror of left
6. **Compute branch paths:** Bezier control points from parent connector_out to child connector_in

#### LogicChartLayout

```
  ┌──────┐     ┌─────────┐
  │ Root ├────►│ Child 1 │
  └──┬───┘     └─────────┘
     │         ┌─────────┐
     └────────►│ Child 2 │
               └────┬────┘
                    │     ┌───────────┐
                    ├────►│ Sub 2.1   │
                    │     └───────────┘
                    │     ┌───────────┐
                    └────►│ Sub 2.2   │
                          └───────────┘
```

**Algorithm steps (Reingold-Tilford adaptation):**
1. **Post-order traversal:** compute each node's subtree height (sum of children heights + gaps)
2. **Assign preliminary y-positions:** children centered on parent's y; first child at top, each subsequent child offset by its predecessor's subtree height
3. **Assign x-positions:** each depth level gets incrementing x based on horizontal spacing
4. **Compact:** shift subtrees to minimize whitespace while preventing overlap

### 6.3 Verification

```bash
# Layout algorithm tests
pytest tests/test_layout/ -v

# No overlap test: generate layout, check no bounding boxes intersect
pytest tests/test_layout/test_radial_map.py::test_no_overlap -v
pytest tests/test_layout/test_logic_chart.py::test_no_overlap -v

# Performance test: layout 500-node tree in < 1 second
pytest tests/test_layout/test_radial_map.py::test_performance_500_nodes -v

# Visual regression (if reference images exist)
pytest tests/visual_regression/ -v

# Integrated test: model → layout → scene renders correctly
python -c "
from mindnodes.models.factory import create_workbook, create_topic
from mindnodes.layout.registry import LayoutRegistry
# Build tree, compute layout, verify positions
"
```

### 6.4 Modules Created

| Module | Key Classes |
|--------|-------------|
| `src/mindnodes/layout/__init__.py` | Package init |
| `src/mindnodes/layout/base.py` | `LayoutAlgorithm` ABC, `LayoutConfig` |
| `src/mindnodes/layout/types.py` | `NodeGeometry`, `ConnectorPoint` |
| `src/mindnodes/layout/registry.py` | `LayoutRegistry` |
| `src/mindnodes/layout/radial_map.py` | `RadialMapLayout` |
| `src/mindnodes/layout/logic_chart.py` | `LogicChartLayout` |
| `src/mindnodes/layout/org_chart.py` | `OrgChartLayout` |
| `src/mindnodes/layout/tree_chart.py` | `TreeChartLayout` |
| `src/mindnodes/layout/utils.py` | Geometry utilities |
| `src/mindnodes/layout/animation.py` | Transition animation helpers |

---

## 7. Phase 5 — Command System and Editing

**Goal:** Implement the undo/redo command framework and all editing operations. Wire all user interactions to go through commands.

### 7.1 Tasks

1. Implement `MindNodeCommand(QUndoCommand)` base class
2. Implement topic commands:
   - `AddTopicCommand(parent_id, new_topic, index)` — insert child at index
   - `DeleteTopicCommand(parent_id, topic_id)` — remove child (captures entire subtree for undo)
   - `EditTopicTitleCommand(topic_id, old_title, new_title)` — with command merging for keystrokes
   - `MoveTopicCommand(topic_id, old_parent_id, new_parent_id, new_index)` — drag-drop reparenting
   - `ReorderChildrenCommand(parent_id, old_order, new_order)` — reorder siblings
   - `ToggleFoldCommand(topic_id)` — fold/unfold subtree
3. Implement relationship commands:
   - `AddRelationshipCommand(sheet_id, relationship)`
   - `DeleteRelationshipCommand(sheet_id, relationship_id)`
4. Implement style commands:
   - `ChangeStyleCommand(target_id, old_style, new_style)` — works for topics, relationships, boundaries
   - `ChangeThemeCommand(sheet_id, old_theme, new_theme)`
5. Implement boundary commands:
   - `AddBoundaryCommand(parent_topic_id, boundary)`
   - `DeleteBoundaryCommand(parent_topic_id, boundary_id)`
6. Implement summary commands:
   - `AddSummaryCommand(parent_topic_id, summary, summary_topic)`
   - `DeleteSummaryCommand(parent_topic_id, summary_id)`
7. Implement callout commands:
   - `AddCalloutCommand(parent_topic_id, callout)`
   - `DeleteCalloutCommand(parent_topic_id, callout_id)`
8. Implement marker commands:
   - `AddMarkerCommand(topic_id, marker_ref)`
   - `RemoveMarkerCommand(topic_id, marker_id)`
9. Implement notes command:
   - `EditNotesCommand(topic_id, old_notes, new_notes)`
10. Implement `BatchCommand` — wraps multiple sub-commands for atomic undo
11. Implement clipboard (`clipboard.py`):
    - Copy: serialize selected topic subtree to JSON, put on `QClipboard`
    - Cut: copy + `DeleteTopicCommand`
    - Paste: deserialize JSON from clipboard, `AddTopicCommand` under selected parent
12. Set up `QUndoStack` per Sheet, `QUndoGroup` at Workbook level
13. Wire all canvas interactions (double-click edit, drag reparent, keyboard shortcuts) to create and push commands

### 7.2 Key Implementation Details

- Each command stores: reference to the model being modified, old state snapshot, new state values
- `DeleteTopicCommand` captures the **entire subtree** (deep copy) so undo can restore it with all children, boundaries, summaries, and callouts intact
- `EditTopicTitleCommand.mergeWith()`: if the next command edits the same topic's title within 500ms, merge them into a single undo step (prevents per-keystroke undo entries)
- `BatchCommand` constructor takes a list of sub-commands; `redo()` executes all in order; `undo()` reverses all in reverse order
- Clipboard JSON format: serialized Topic subtree using `topic.model_dump()`

### 7.3 Verification

```bash
# Command unit tests
pytest tests/test_commands/ -v

# Undo/redo correctness: execute command → verify state → undo → verify original → redo → verify again
pytest tests/test_commands/test_topic_commands.py -v

# Stress test: 50 random commands, undo all, verify model matches original
pytest tests/test_commands/test_topic_commands.py::test_random_command_sequence -v

# Clipboard round-trip
pytest tests/test_commands/test_clipboard.py -v

# No memory leaks: check that undone commands don't hold zombie references
pytest tests/test_commands/test_batch_command.py::test_memory_cleanup -v
```

### 7.4 Modules Created

| Module | Key Classes |
|--------|-------------|
| `src/mindnodes/commands/__init__.py` | Package init |
| `src/mindnodes/commands/base.py` | `MindNodeCommand` |
| `src/mindnodes/commands/topic_commands.py` | All topic commands |
| `src/mindnodes/commands/relationship_commands.py` | Relationship commands |
| `src/mindnodes/commands/style_commands.py` | Style/theme commands |
| `src/mindnodes/commands/boundary_commands.py` | Boundary commands |
| `src/mindnodes/commands/summary_commands.py` | Summary commands |
| `src/mindnodes/commands/callout_commands.py` | Callout commands |
| `src/mindnodes/commands/marker_commands.py` | Marker commands |
| `src/mindnodes/commands/notes_commands.py` | Notes command |
| `src/mindnodes/commands/batch.py` | `BatchCommand` |
| `src/mindnodes/commands/clipboard.py` | Copy/cut/paste logic |

---

## 8. Phase 6 — UI Shell

**Goal:** Build the complete application UI: main window, menus, toolbars, dock panels, and wire everything together.

### 8.1 Tasks

1. Implement `MainWindow(QMainWindow)`:
   - Central widget: `QTabWidget` with `MindMapView` per sheet
   - Menu bar, toolbars, status bar
   - Dock widget areas for panels
   - Window title: "filename - Mind-Nodes" (with * for unsaved changes)
   - Recent files in File menu
2. Implement `MenuBar`:
   - **File:** New, Open, Open Recent >, Save, Save As, Export >, Print, Exit
   - **Edit:** Undo, Redo, Cut, Copy, Paste, Delete, Select All, Find, Find & Replace
   - **View:** Zoom In/Out/Fit/100%, Toggle Grid, Toggle Minimap, Toggle Panels >
   - **Insert:** Topic, Subtopic, Parent Topic, Floating Topic, Relationship, Boundary, Summary, Callout, Marker, Note, Image, Hyperlink
   - **Format:** Style >, Theme >, Structure >, Fold/Unfold
   - **Map:** New Sheet, Duplicate Sheet, Delete Sheet, Rename Sheet
   - **Help:** About, Keyboard Shortcuts, Documentation
3. Implement `Toolbar`:
   - Icon buttons for common actions: New, Open, Save, Undo, Redo, Add Topic, Add Subtopic, Delete
   - Layout selector dropdown
   - Zoom slider
4. Implement `StatusBar`:
   - Zoom percentage display
   - Node count
   - Modified indicator
   - Auto-save status
5. Implement `PropertiesPanel(QDockWidget)`:
   - Context-sensitive: shows relevant fields based on what's selected
   - Title editor, style properties (shape, colors, font), notes editor, markers, labels, hyperlink
   - Multi-selection: shows common properties that can be bulk-edited
6. Implement `OutlinePanel(QDockWidget)`:
   - `QTreeView` with custom `QAbstractItemModel` backed by the Topic tree
   - Fully editable: rename topics in-place
   - Bidirectional sync: edits in outline → canvas updates; edits on canvas → outline updates
   - Drag-and-drop reparenting within the tree view
7. Implement `MarkerPanel(QDockWidget)`:
   - Categorized grid of marker icons
   - Click to apply to selected topic
   - Search/filter box
8. Implement `SearchPanel(QDockWidget)`:
   - Search text input with Enter to search
   - Results list showing matching topic titles
   - Click result to select and center on canvas
   - Find & Replace mode
9. Implement `ThemePanel(QDockWidget)`:
   - Gallery of available themes with preview thumbnails
   - Click to apply theme to current sheet
10. Implement keyboard shortcuts via `ShortcutManager`:
    - Load keybindings from settings
    - Register all actions with their shortcuts
    - Support user customization in settings dialog
11. Implement context menus:
    - Right-click on topic: Edit, Add Subtopic, Add Sibling, Delete, Cut/Copy/Paste, Add Marker, Add Note, Style
    - Right-click on canvas: Add Floating Topic, Paste, Select All, Zoom
    - Right-click on relationship: Edit Label, Delete
12. Implement `SettingsDialog`:
    - Categorized tabs: Appearance, Behavior, Keybindings, Files, Plugins
    - Live preview where applicable
13. Implement `ExportDialog`:
    - Format selector, output path, format-specific options

### 8.2 Verification

```bash
# UI tests
pytest tests/test_ui/ -v

# End-to-end test
# 1. Launch app
# 2. Create new workbook
# 3. Add 10 topics with various nesting levels
# 4. Apply styles to some topics
# 5. Add 2 relationships
# 6. Add a boundary
# 7. Save as .xmind
# 8. Close and reopen the file
# 9. Verify all content is identical

# All menu actions are connected
# All keyboard shortcuts work
# All dock panels open and function
```

### 8.3 Modules Created

| Module | Description |
|--------|-------------|
| `src/mindnodes/ui/main_window.py` | `MainWindow` |
| `src/mindnodes/ui/menu_bar.py` | Menu bar construction |
| `src/mindnodes/ui/toolbar.py` | Toolbar construction |
| `src/mindnodes/ui/status_bar.py` | Status bar |
| `src/mindnodes/ui/tab_manager.py` | Sheet tab management |
| `src/mindnodes/ui/shortcuts.py` | Keyboard shortcut manager |
| `src/mindnodes/ui/panels/properties_panel.py` | Properties panel |
| `src/mindnodes/ui/panels/outline_panel.py` | Outline panel |
| `src/mindnodes/ui/panels/marker_panel.py` | Marker panel |
| `src/mindnodes/ui/panels/search_panel.py` | Search panel |
| `src/mindnodes/ui/panels/theme_panel.py` | Theme panel |
| `src/mindnodes/ui/dialogs/settings_dialog.py` | Settings dialog |
| `src/mindnodes/ui/dialogs/export_dialog.py` | Export dialog |
| `src/mindnodes/ui/dialogs/about_dialog.py` | About dialog |
| `src/mindnodes/ui/dialogs/hyperlink_dialog.py` | Hyperlink editor |
| `src/mindnodes/ui/dialogs/image_dialog.py` | Image chooser |
| `src/mindnodes/ui/widgets/color_picker.py` | Color selector |
| `src/mindnodes/ui/widgets/font_picker.py` | Font selector |
| `src/mindnodes/ui/widgets/icon_button.py` | Toolbar button |
| `src/mindnodes/ui/widgets/zoom_slider.py` | Zoom slider |

---

## 9. Phase 7 — Additional File Formats

**Goal:** Implement all remaining file format importers and exporters.

### 9.1 Tasks

1. Implement `PNGExporter`:
   - Render `MindMapScene` to `QImage` at configured scale factor
   - Add padding around the map
   - Save via `Pillow` with DPI metadata
2. Implement `SVGExporter`:
   - Use `svgwrite` to generate SVG from scene items
   - One `<g>` group per topic, with CSS classes
   - Branch paths as `<path>` elements
3. Implement `PDFExporter`:
   - Use `reportlab` to render the map to PDF
   - Support multi-page tiling for large maps
   - Embed fonts
4. Implement `MarkdownHandler`:
   - **Export:** walk topic tree depth-first, generate headings for first two levels, bullet lists for deeper levels
   - **Import:** parse markdown headings and bullet lists, build Topic tree
5. Implement `OPMLHandler`:
   - **Export:** generate OPML XML with `<outline>` elements
   - **Import:** parse OPML XML, build Topic tree
6. Implement `FreeMindHandler`:
   - **Export:** generate FreeMind `.mm` XML
   - **Import:** parse FreeMind XML, map node attributes to Topic properties
   - Map FreeMind icon names to Mind-Nodes marker IDs
7. Implement `MindNodesHandler`:
   - Extended `.xmind` format with callouts and plugin data
   - Subclass or delegate to `XMindHandler` with extensions
8. Wire all handlers to `FileHandlerRegistry`
9. Wire Export menu and file dialogs

### 9.2 Verification

```bash
# Each exporter produces valid output
pytest tests/test_io/test_png_exporter.py -v    # Verify PNG headers and dimensions
pytest tests/test_io/test_svg_exporter.py -v    # Validate SVG XML
pytest tests/test_io/test_pdf_exporter.py -v    # Verify PDF structure

# Import-export round-trip for bidirectional formats
pytest tests/test_io/test_markdown.py -v
pytest tests/test_io/test_opml.py -v
pytest tests/test_io/test_freemind.py -v

# Registry returns correct handler for each extension
pytest tests/test_io/test_registry.py -v
```

### 9.3 Modules Created

| Module | Description |
|--------|-------------|
| `src/mindnodes/io/exporters/__init__.py` | Package init |
| `src/mindnodes/io/exporters/png_exporter.py` | PNG export |
| `src/mindnodes/io/exporters/svg_exporter.py` | SVG export |
| `src/mindnodes/io/exporters/pdf_exporter.py` | PDF export |
| `src/mindnodes/io/markdown_handler.py` | Markdown import/export |
| `src/mindnodes/io/opml_handler.py` | OPML import/export |
| `src/mindnodes/io/freemind_handler.py` | FreeMind import/export |
| `src/mindnodes/io/mindnodes_handler.py` | Native .mindnodes format |

---

## 10. Phase 8 — Remaining Layouts

**Goal:** Implement the 5 remaining layout algorithms.

### 10.1 Tasks

1. Implement **BraceMapLayout** (`org.xmind.ui.brace.right`):
   - Brace connector between parent and grouped children
   - Children arranged vertically, connected by a brace `{` or `}`
2. Implement **TimelineLayout** (`org.xmind.ui.timeline.horizontal`, `.vertical`):
   - Linear axis (horizontal or vertical)
   - Topics alternate above/below (or left/right) the axis
   - Chronological ordering
3. Implement **FishboneLayout** (`org.xmind.ui.fishbone.leftHeaded`, `.rightHeaded`):
   - Central spine axis (horizontal)
   - Main branches at 45°/135° angles from spine
   - Sub-branches perpendicular to main branches
4. Implement **MatrixLayout** (`org.xmind.ui.spreadsheet`):
   - Grid arrangement with row and column headers
   - First-level children define rows; second-level define columns (or vice versa)
5. Implement **TreeTableLayout** (`org.xmind.ui.spreadsheet.column`):
   - Left side: indented tree structure
   - Right side: table columns extending horizontally
6. Add layout switching:
   - User can change `structure_class` on any topic from the Format > Structure menu or properties panel
   - Change triggers re-layout with smooth animation
7. Register all new layouts in `LayoutRegistry`

### 10.2 Verification

```bash
# Layout algorithm tests (no overlap, correct positioning)
pytest tests/test_layout/test_brace_map.py -v
pytest tests/test_layout/test_timeline.py -v
pytest tests/test_layout/test_fishbone.py -v
pytest tests/test_layout/test_matrix.py -v
pytest tests/test_layout/test_tree_table.py -v

# Visual regression for all 9+ layouts
pytest tests/visual_regression/ -v

# Layout switching animation is smooth (manual verification)
```

### 10.3 Modules Created

| Module | Description |
|--------|-------------|
| `src/mindnodes/layout/brace_map.py` | `BraceMapLayout` |
| `src/mindnodes/layout/timeline.py` | `TimelineLayout` |
| `src/mindnodes/layout/fishbone.py` | `FishboneLayout` |
| `src/mindnodes/layout/matrix.py` | `MatrixLayout` |
| `src/mindnodes/layout/tree_table.py` | `TreeTableLayout` |

---

## 11. Phase 9 — Advanced Features

**Goal:** Implement presentation mode, auto-save, themes, plugin system, and remaining features.

### 11.1 Presentation Mode

- `PresentationMode` class manages slideshow state
- Each "slide" focuses on a subtree: zoom-to-fit with animation, dim other nodes
- Navigation: Right/Down = next branch, Left/Up = previous branch, Escape = exit
- Full-screen mode via `QMainWindow.showFullScreen()`
- **Module:** `src/mindnodes/features/presentation.py`

### 11.2 Auto-Save and Crash Recovery

- `AutoSaveManager` with configurable timer (default 60s)
- Saves to `~/.mindnodes/recovery/{workbook_id}.recovery`
- On startup: scan recovery directory, compare timestamps with actual files, offer restore
- Auto-save runs on QThread worker (serializes model snapshot, writes ZIP)
- **Module:** `src/mindnodes/features/autosave.py`

### 11.3 Built-in Themes

- Create 10 built-in theme JSON files:
  - `default.json` — clean neutral theme
  - `dark.json` — dark background, light text
  - `snowbrush.json` — pastel blues and whites
  - `robust.json` — bold professional colors
  - `business.json` — corporate blue and gray
  - `fresh.json` — bright greens and yellows
  - `ocean.json` — blues and teals
  - `forest.json` — greens and browns
  - `sunset.json` — oranges and reds
  - `monochrome.json` — grayscale
- `ThemeManager` loads built-in themes and user-created themes
- Smart color auto-generation: given a seed color, generate 6 complementary branch colors
- **Modules:** `src/mindnodes/themes/manager.py`, `src/mindnodes/themes/builtin/*.json`

### 11.4 Plugin System

- `PluginLoader` uses `importlib.metadata.entry_points(group="mindnodes.plugins")`
- `PluginManager` handles enable/disable/lifecycle
- Plugin manager UI in Settings dialog: list of discovered plugins with enable/disable toggles
- **Modules:** `src/mindnodes/plugins/loader.py`, `src/mindnodes/plugins/manager.py`, `src/mindnodes/plugins/base.py`

### 11.5 Additional Canvas Items

- Implement `RelationshipItem` — arrow with label between any two topics
- Implement `BoundaryItem` — rounded-rect or cloud shape enclosing grouped topics
- Implement `SummaryItem` — bracket spanning siblings, pointing to summary topic
- Implement `CalloutItem` — speech bubble attached to parent topic
- Implement `FloatingTopicItem` — topic at explicit canvas position
- **Modules:** `src/mindnodes/ui/canvas/items/relationship_item.py`, `boundary_item.py`, `summary_item.py`, `callout_item.py`, `floating_topic_item.py`

### 11.6 Remaining Features

- **Find & Replace:** extend `SearchPanel` with replace functionality
- **Hyperlink following:** Ctrl+click on topic with href opens URL in system browser
- **Image attachment:** file dialog to choose image, embed into topic
- **Print support:** `QPrintDialog` integration
- **Minimap widget:** `MindMapMinimap(QWidget)` overlay in the view corner
- **Modules:** `src/mindnodes/ui/canvas/minimap.py`, `src/mindnodes/features/print_support.py`, `src/mindnodes/features/recent_files.py`

### 11.7 Verification

```bash
# Presentation mode
pytest tests/test_features/test_presentation.py -v

# Auto-save and recovery
pytest tests/test_features/test_autosave.py -v

# Plugin loading
pytest tests/test_plugins/test_loader.py -v

# Canvas items for relationships, boundaries, etc.
pytest tests/test_ui/test_relationship_item.py -v
pytest tests/test_ui/test_boundary_item.py -v

# Theme loading
pytest tests/test_themes/ -v
```

---

## 12. Phase 10 — Polish and Release

**Goal:** Performance optimization, accessibility, cross-platform testing, packaging, and release.

### 12.1 Performance Optimization

- Profile with `cProfile` and `py-spy`
- Optimize hot paths: layout algorithms, scene rendering, model serialization
- Implement viewport culling optimizations in MindMapView
- Lazy loading for large maps: only create visual items for visible nodes
- Benchmark targets from [constitution.md](constitution.md) Section 6.2

### 12.2 Accessibility

- Add `QAccessible` descriptions to all interactive widgets
- Ensure all actions are keyboard-accessible
- Include high-contrast theme
- Test with screen readers (NVDA on Windows, VoiceOver on macOS)

### 12.3 Cross-Platform Testing

- Test on: Windows 10/11, macOS 12+, Ubuntu 22.04/24.04
- Fix platform-specific rendering differences
- Ensure native file dialogs work on all platforms
- Verify font rendering consistency

### 12.4 Packaging

- **PyPI:** `python -m build` → upload to PyPI
- **Linux:** AppImage and .deb packages via PyInstaller
- **macOS:** .dmg installer via PyInstaller + create-dmg
- **Windows:** .msi installer via PyInstaller + NSIS or Inno Setup
- **Module:** `scripts/build_exe.py`

### 12.5 Documentation

- Generate Sphinx API docs from docstrings
- Write user manual (basic Getting Started guide)
- Update README.md with final installation instructions

### 12.6 Release Checklist

- [ ] All tests pass on CI matrix (3 Python versions × 3 OSes)
- [ ] Performance benchmarks pass
- [ ] .xmind round-trip works with real XMind files
- [ ] All 9 layouts render correctly
- [ ] Packaging builds work on all platforms
- [ ] README updated
- [ ] CHANGELOG written
- [ ] Git tag created: `v1.0.0`
- [ ] GitHub release published with binaries
- [ ] PyPI package published

---

## 13. Document Cross-References

| Topic | Document |
|-------|----------|
| Success criteria and performance targets | [constitution.md](constitution.md) Section 6 |
| Component architecture and interactions | [blueprint.md](blueprint.md) |
| Data model field definitions | [artifacts.md](artifacts.md) Section 1 |
| File format specifications | [artifacts.md](artifacts.md) Section 2 |
| API interface contracts | [artifacts.md](artifacts.md) Section 3 |
| Module file paths | [skeleton.md](skeleton.md) |
