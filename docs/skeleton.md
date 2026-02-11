# Mind-Nodes Project Skeleton

> The complete project directory structure defining every package, module, configuration file, and their responsibilities. This is the map a developer uses to know exactly which file to create, find, or modify.

---

## 1. Project Root Structure

```
mind-nodes/
├── .github/
│   ├── workflows/
│   │   ├── ci.yml                         # CI: lint, type-check, test on push/PR
│   │   └── release.yml                    # Build executables + publish on tag
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md                  # Bug report template
│   │   └── feature_request.md             # Feature request template
│   └── pull_request_template.md           # PR description template
│
├── docs/
│   ├── constitution.md                    # Project vision, scope, principles
│   ├── blueprint.md                       # System architecture, components
│   ├── artifacts.md                       # Data models, file formats, APIs
│   ├── implementation-guide.md            # Phased build plan
│   └── skeleton.md                        # This file
│
├── src/
│   └── mindnodes/                         # Main application package
│       ├── __init__.py                    # __version__, public API re-exports
│       ├── __main__.py                    # Entry: python -m mindnodes
│       ├── app.py                         # QApplication subclass, main()
│       ├── constants.py                   # App name, version, paths, defaults
│       │
│       ├── models/                        # Domain model layer
│       │   ├── __init__.py                # Re-exports all model classes
│       │   ├── workbook.py                # Workbook
│       │   ├── sheet.py                   # Sheet
│       │   ├── topic.py                   # Topic + tree traversal utilities
│       │   ├── relationship.py            # Relationship
│       │   ├── boundary.py                # Boundary
│       │   ├── summary.py                 # Summary
│       │   ├── callout.py                 # Callout
│       │   ├── notes.py                   # Notes, PlainContent, HtmlContent
│       │   ├── style.py                   # Style, StyleProperties
│       │   ├── theme.py                   # Theme, MapStyle
│       │   ├── markers.py                 # MarkerRef, MARKER_CATALOG
│       │   ├── enums.py                   # StructureClass, StyleType, Shape
│       │   ├── types.py                   # Position, ImageRef, BranchStyle
│       │   ├── validators.py              # Cross-model validation functions
│       │   └── factory.py                 # create_workbook(), create_topic()
│       │
│       ├── commands/                      # Undo/redo command layer
│       │   ├── __init__.py                # Re-exports command classes
│       │   ├── base.py                    # MindNodeCommand(QUndoCommand)
│       │   ├── topic_commands.py          # Add/Delete/Edit/Move/Reorder/Fold
│       │   ├── relationship_commands.py   # Add/Delete relationship
│       │   ├── style_commands.py          # ChangeStyle, ChangeTheme
│       │   ├── boundary_commands.py       # Add/Delete boundary
│       │   ├── summary_commands.py        # Add/Delete summary
│       │   ├── callout_commands.py        # Add/Delete callout
│       │   ├── marker_commands.py         # Add/Remove marker
│       │   ├── notes_commands.py          # EditNotes
│       │   ├── batch.py                   # BatchCommand (atomic multi-op)
│       │   └── clipboard.py              # Copy/Cut/Paste logic
│       │
│       ├── layout/                        # Layout algorithm engine
│       │   ├── __init__.py                # Re-exports layout classes
│       │   ├── base.py                    # LayoutAlgorithm ABC, LayoutConfig
│       │   ├── types.py                   # NodeGeometry, ConnectorPoint
│       │   ├── registry.py                # LayoutRegistry: structureClass → class
│       │   ├── radial_map.py              # Balanced radial mind map
│       │   ├── logic_chart.py             # Left/right logic chart
│       │   ├── org_chart.py               # Up/down organization chart
│       │   ├── tree_chart.py              # Indented tree (left/right)
│       │   ├── brace_map.py               # Brace-connected grouping
│       │   ├── timeline.py                # Horizontal/vertical timeline
│       │   ├── fishbone.py                # Ishikawa cause-effect diagram
│       │   ├── matrix.py                  # Row/column matrix grid
│       │   ├── tree_table.py              # Tree + table hybrid
│       │   ├── animation.py               # Layout transition animations
│       │   └── utils.py                   # Shared geometry utilities
│       │
│       ├── ui/                            # Presentation layer
│       │   ├── __init__.py
│       │   ├── main_window.py             # QMainWindow subclass
│       │   ├── menu_bar.py                # Menu bar construction + actions
│       │   ├── toolbar.py                 # Toolbar construction
│       │   ├── status_bar.py              # Status bar (zoom, node count)
│       │   ├── tab_manager.py             # QTabWidget for sheet tabs
│       │   ├── shortcuts.py               # Keyboard shortcut manager
│       │   │
│       │   ├── canvas/                    # QGraphicsView/Scene layer
│       │   │   ├── __init__.py
│       │   │   ├── scene.py               # MindMapScene(QGraphicsScene)
│       │   │   ├── view.py                # MindMapView(QGraphicsView)
│       │   │   ├── scene_builder.py       # Model → Scene item sync
│       │   │   ├── minimap.py             # Minimap overlay widget
│       │   │   ├── grid.py                # Background grid/wallpaper
│       │   │   └── items/                 # Visual item classes
│       │   │       ├── __init__.py
│       │   │       ├── base_item.py       # Shared base for all items
│       │   │       ├── topic_item.py      # Topic node rendering
│       │   │       ├── branch_item.py     # Parent-child connector lines
│       │   │       ├── relationship_item.py   # Relationship arrows
│       │   │       ├── boundary_item.py   # Boundary region shapes
│       │   │       ├── summary_item.py    # Summary bracket shapes
│       │   │       ├── callout_item.py    # Callout bubble shapes
│       │   │       └── floating_topic_item.py # Floating topic rendering
│       │   │
│       │   ├── panels/                    # Dock widget panels
│       │   │   ├── __init__.py
│       │   │   ├── properties_panel.py    # Selected-node property editor
│       │   │   ├── outline_panel.py       # QTreeView outline of topics
│       │   │   ├── marker_panel.py        # Marker/icon browser grid
│       │   │   ├── search_panel.py        # Search and find-replace
│       │   │   └── theme_panel.py         # Theme gallery + editor
│       │   │
│       │   ├── dialogs/                   # Modal and modeless dialogs
│       │   │   ├── __init__.py
│       │   │   ├── about_dialog.py        # About Mind-Nodes
│       │   │   ├── settings_dialog.py     # Application preferences
│       │   │   ├── export_dialog.py       # Export format + options
│       │   │   ├── print_dialog.py        # Print configuration
│       │   │   ├── hyperlink_dialog.py    # Hyperlink URL editor
│       │   │   └── image_dialog.py        # Image attachment chooser
│       │   │
│       │   └── widgets/                   # Reusable custom widgets
│       │       ├── __init__.py
│       │       ├── color_picker.py        # Color selector with swatches
│       │       ├── font_picker.py         # Font family/size/weight
│       │       ├── icon_button.py         # Toolbar icon button
│       │       └── zoom_slider.py         # Zoom level slider
│       │
│       ├── io/                            # File I/O layer
│       │   ├── __init__.py
│       │   ├── base.py                    # FileHandler ABC, Exporter ABC
│       │   ├── registry.py                # FileHandlerRegistry
│       │   ├── xmind/                     # XMind format handler
│       │   │   ├── __init__.py            # XMindHandler facade
│       │   │   ├── reader.py              # Parse .xmind ZIP → Workbook
│       │   │   ├── writer.py              # Serialize Workbook → .xmind ZIP
│       │   │   ├── schema.py              # Field name mappings + constants
│       │   │   └── thumbnail.py           # Generate 256x256 thumbnail
│       │   ├── mindnodes_handler.py       # Native .mindnodes format
│       │   ├── freemind_handler.py        # .mm XML import/export
│       │   ├── opml_handler.py            # .opml import/export
│       │   ├── markdown_handler.py        # .md import/export
│       │   └── exporters/                 # Export-only formats
│       │       ├── __init__.py
│       │       ├── png_exporter.py        # PNG raster export
│       │       ├── svg_exporter.py        # SVG vector export
│       │       └── pdf_exporter.py        # PDF document export
│       │
│       ├── plugins/                       # Plugin system
│       │   ├── __init__.py
│       │   ├── base.py                    # MindNodesPlugin ABC
│       │   ├── loader.py                  # Plugin discovery via entry_points
│       │   └── manager.py                 # Plugin lifecycle management
│       │
│       ├── features/                      # Advanced feature modules
│       │   ├── __init__.py
│       │   ├── presentation.py            # Slideshow/presentation mode
│       │   ├── autosave.py                # Auto-save + crash recovery
│       │   ├── recent_files.py            # Recent files tracking
│       │   └── print_support.py           # QPrinter integration
│       │
│       ├── themes/                        # Built-in theme resources
│       │   ├── __init__.py
│       │   ├── manager.py                 # Theme loading + application
│       │   └── builtin/                   # Predefined theme JSON files
│       │       ├── default.json           # Clean neutral theme
│       │       ├── dark.json              # Dark background, light text
│       │       ├── snowbrush.json         # Pastel blues and whites
│       │       ├── robust.json            # Bold professional colors
│       │       ├── business.json          # Corporate blue and gray
│       │       ├── fresh.json             # Bright greens and yellows
│       │       ├── ocean.json             # Blues and teals
│       │       ├── forest.json            # Greens and browns
│       │       ├── sunset.json            # Oranges and reds
│       │       └── monochrome.json        # Grayscale
│       │
│       ├── resources/                     # Static resources
│       │   ├── icons/                     # Application icons
│       │   │   ├── app_icon.svg           # Application icon
│       │   │   ├── toolbar/               # Toolbar action icons (SVG)
│       │   │   │   ├── new.svg
│       │   │   │   ├── open.svg
│       │   │   │   ├── save.svg
│       │   │   │   ├── undo.svg
│       │   │   │   ├── redo.svg
│       │   │   │   ├── add_topic.svg
│       │   │   │   ├── add_subtopic.svg
│       │   │   │   ├── delete.svg
│       │   │   │   ├── zoom_in.svg
│       │   │   │   ├── zoom_out.svg
│       │   │   │   ├── zoom_fit.svg
│       │   │   │   └── export.svg
│       │   │   └── markers/               # 350+ marker icons by category
│       │   │       ├── priority/          # priority-1.svg through priority-9.svg
│       │   │       ├── smiley/            # smiley-smile.svg, etc.
│       │   │       ├── task/              # task-start.svg, etc.
│       │   │       ├── flag/              # flag-red.svg, etc.
│       │   │       ├── star/              # star-red.svg, etc.
│       │   │       ├── arrow/             # arrow-up.svg, etc.
│       │   │       ├── symbol/            # symbol-plus.svg, etc.
│       │   │       ├── month/             # month-jan.svg, etc.
│       │   │       ├── week/              # week-mon.svg, etc.
│       │   │       └── people/            # people-red.svg, etc.
│       │   ├── styles/                    # Default stylesheets
│       │   │   └── default.qss            # Qt stylesheet for app widgets
│       │   └── wallpapers/                # Canvas background images
│       │       ├── grid_light.png
│       │       ├── grid_dark.png
│       │       └── paper.png
│       │
│       └── utils/                         # Shared utilities
│           ├── __init__.py
│           ├── geometry.py                # Point, Rect, Bezier math
│           ├── color.py                   # Color parsing, palette generation
│           ├── signals.py                 # Custom signal/event bus helpers
│           ├── settings.py                # QSettings wrapper, config manager
│           └── logging_config.py          # Logging setup
│
├── tests/                                 # Test suite (mirrors src layout)
│   ├── conftest.py                        # Shared fixtures, sample workbooks
│   ├── test_models/
│   │   ├── test_workbook.py
│   │   ├── test_sheet.py
│   │   ├── test_topic.py
│   │   ├── test_relationship.py
│   │   ├── test_style.py
│   │   ├── test_theme.py
│   │   ├── test_validators.py
│   │   └── test_factory.py
│   ├── test_commands/
│   │   ├── test_topic_commands.py
│   │   ├── test_relationship_commands.py
│   │   ├── test_style_commands.py
│   │   ├── test_batch_command.py
│   │   └── test_clipboard.py
│   ├── test_layout/
│   │   ├── test_radial_map.py
│   │   ├── test_logic_chart.py
│   │   ├── test_org_chart.py
│   │   ├── test_tree_chart.py
│   │   ├── test_brace_map.py
│   │   ├── test_timeline.py
│   │   ├── test_fishbone.py
│   │   ├── test_matrix.py
│   │   ├── test_tree_table.py
│   │   └── test_layout_registry.py
│   ├── test_io/
│   │   ├── test_xmind_reader.py
│   │   ├── test_xmind_writer.py
│   │   ├── test_xmind_roundtrip.py
│   │   ├── test_freemind.py
│   │   ├── test_opml.py
│   │   ├── test_markdown.py
│   │   ├── test_png_exporter.py
│   │   ├── test_svg_exporter.py
│   │   ├── test_pdf_exporter.py
│   │   └── test_registry.py
│   ├── test_ui/
│   │   ├── test_main_window.py
│   │   ├── test_scene.py
│   │   ├── test_topic_item.py
│   │   ├── test_view.py
│   │   ├── test_outline_panel.py
│   │   ├── test_relationship_item.py
│   │   └── test_boundary_item.py
│   ├── test_plugins/
│   │   └── test_loader.py
│   ├── test_features/
│   │   ├── test_presentation.py
│   │   └── test_autosave.py
│   ├── test_themes/
│   │   └── test_theme_manager.py
│   ├── fixtures/                          # Test data files
│   │   ├── sample_basic.xmind            # Simple 3-level map
│   │   ├── sample_complex.xmind          # All feature types
│   │   ├── sample_relationships.xmind    # Map with relationships
│   │   ├── sample_multisheet.xmind       # Workbook with 3 sheets
│   │   ├── sample.mm                     # FreeMind test file
│   │   ├── sample.opml                   # OPML test file
│   │   └── sample.md                     # Markdown test file
│   └── visual_regression/                 # Layout screenshot tests
│       ├── conftest.py                    # Screenshot capture fixtures
│       └── reference/                     # Expected reference screenshots
│           ├── radial_map_basic.png
│           ├── logic_chart_basic.png
│           ├── org_chart_basic.png
│           ├── tree_chart_basic.png
│           ├── brace_map_basic.png
│           ├── timeline_basic.png
│           ├── fishbone_basic.png
│           ├── matrix_basic.png
│           └── tree_table_basic.png
│
├── scripts/                               # Development and build scripts
│   ├── build_exe.py                       # PyInstaller/Nuitka build script
│   ├── generate_markers.py                # Generate marker catalog from SVGs
│   └── create_sample_xmind.py             # Generate test .xmind fixtures
│
├── pyproject.toml                         # Project metadata + all tool config
├── README.md                              # Project overview, install, quickstart
├── CHANGELOG.md                           # Version changelog
├── CONTRIBUTING.md                        # Contribution guidelines
├── LICENSE                                # MIT License
├── .gitignore                             # Git ignore rules
├── .pre-commit-config.yaml                # Pre-commit hooks config
└── Makefile                               # Common dev commands
```

---

## 2. Module Descriptions

### 2.1 `src/mindnodes/models/` — Domain Model Layer

**Dependencies:** `pydantic`, `uuid` (stdlib). No project-internal dependencies.

| Module | Responsibility |
|--------|---------------|
| `workbook.py` | `Workbook` class — top-level container with sheets list, metadata |
| `sheet.py` | `Sheet` class — single mind map page with root topic, relationships, theme |
| `topic.py` | `Topic` class — recursive tree node with children, markers, notes, style; tree traversal functions (`walk_depth_first`, `find_topic_by_id`, etc.) |
| `relationship.py` | `Relationship` class — freeform arrow between two topics |
| `boundary.py` | `Boundary` class — visual grouping of sibling topic range |
| `summary.py` | `Summary` class — bracket annotation spanning sibling range |
| `callout.py` | `Callout` class — speech bubble annotation |
| `notes.py` | `Notes`, `PlainContent`, `HtmlContent` — rich text notes |
| `style.py` | `Style`, `StyleProperties` — visual properties for any element |
| `theme.py` | `Theme`, `MapStyle` — complete visual theme with color palette |
| `markers.py` | `MarkerRef` class, `MARKER_CATALOG` dict — marker icon taxonomy |
| `enums.py` | `StructureClass`, `StyleType`, `Shape` enums |
| `types.py` | `Position`, `ImageRef`, `BranchStyle` — value objects |
| `validators.py` | Cross-model validation: cycle detection, ID uniqueness, range bounds |
| `factory.py` | `create_workbook()`, `create_sheet()`, `create_topic()` — convenience constructors |

### 2.2 `src/mindnodes/commands/` — Command Layer

**Dependencies:** `models`, `PySide6.QtWidgets.QUndoCommand`

| Module | Responsibility |
|--------|---------------|
| `base.py` | `MindNodeCommand(QUndoCommand)` — base class for all undoable operations |
| `topic_commands.py` | `AddTopicCommand`, `DeleteTopicCommand`, `EditTopicTitleCommand`, `MoveTopicCommand`, `ReorderChildrenCommand`, `ReparentTopicCommand`, `ToggleFoldCommand` |
| `relationship_commands.py` | `AddRelationshipCommand`, `DeleteRelationshipCommand` |
| `style_commands.py` | `ChangeStyleCommand`, `ChangeThemeCommand` |
| `boundary_commands.py` | `AddBoundaryCommand`, `DeleteBoundaryCommand` |
| `summary_commands.py` | `AddSummaryCommand`, `DeleteSummaryCommand` |
| `callout_commands.py` | `AddCalloutCommand`, `DeleteCalloutCommand` |
| `marker_commands.py` | `AddMarkerCommand`, `RemoveMarkerCommand` |
| `notes_commands.py` | `EditNotesCommand` |
| `batch.py` | `BatchCommand` — wraps multiple sub-commands for atomic undo/redo |
| `clipboard.py` | Copy/cut/paste logic — serialize topics to JSON, push to QClipboard |

### 2.3 `src/mindnodes/layout/` — Layout Engine

**Dependencies:** `models` (for Topic tree), `types` (for NodeGeometry)

| Module | Responsibility |
|--------|---------------|
| `base.py` | `LayoutAlgorithm` ABC with `layout()` and `structure_class()` methods; `LayoutConfig` dataclass |
| `types.py` | `NodeGeometry` dataclass (x, y, width, height, connectors, branch points) |
| `registry.py` | `LayoutRegistry` — maps structureClass strings to algorithm classes |
| `radial_map.py` | `RadialMapLayout` — balanced radial expansion from center (default) |
| `logic_chart.py` | `LogicChartLayout` — horizontal Reingold-Tilford tree |
| `org_chart.py` | `OrgChartLayout` — vertical hierarchy chart |
| `tree_chart.py` | `TreeChartLayout` — indented tree structure |
| `brace_map.py` | `BraceMapLayout` — brace-connected grouping |
| `timeline.py` | `TimelineLayout` — chronological horizontal/vertical |
| `fishbone.py` | `FishboneLayout` — Ishikawa cause-effect diagram |
| `matrix.py` | `MatrixLayout` — grid row/column arrangement |
| `tree_table.py` | `TreeTableLayout` — tree + table hybrid |
| `animation.py` | `LayoutAnimator` — QPropertyAnimation helpers for smooth transitions |
| `utils.py` | `measure_topic_size()`, `compute_subtree_bounds()`, Bezier curve math |

### 2.4 `src/mindnodes/ui/` — Presentation Layer

**Dependencies:** `models`, `commands`, `layout`, `io`, `PySide6`

| Module | Responsibility |
|--------|---------------|
| `main_window.py` | `MainWindow(QMainWindow)` — central widget, dock areas, window lifecycle |
| `menu_bar.py` | Menu bar construction, action connections, recent files submenu |
| `toolbar.py` | Toolbar with icon buttons and layout selector dropdown |
| `status_bar.py` | Zoom percentage, node count, modified indicator, auto-save status |
| `tab_manager.py` | `QTabWidget` managing one `MindMapView` per sheet |
| `shortcuts.py` | `ShortcutManager` — load/apply keybindings from settings |
| `canvas/scene.py` | `MindMapScene(QGraphicsScene)` — item management, selection, background |
| `canvas/view.py` | `MindMapView(QGraphicsView)` — zoom, pan, viewport culling |
| `canvas/scene_builder.py` | `SceneBuilder` — creates/updates visual items from model + layout |
| `canvas/minimap.py` | `MindMapMinimap(QWidget)` — overview overlay with viewport indicator |
| `canvas/grid.py` | Background grid and wallpaper rendering |
| `canvas/items/topic_item.py` | `TopicItem(QGraphicsObject)` — renders node shape, text, icons |
| `canvas/items/branch_item.py` | `BranchItem(QGraphicsItem)` — renders connector lines |
| `canvas/items/relationship_item.py` | `RelationshipItem` — renders arrow paths with labels |
| `canvas/items/boundary_item.py` | `BoundaryItem` — renders enclosing shapes |
| `canvas/items/summary_item.py` | `SummaryItem` — renders bracket + summary topic |
| `canvas/items/callout_item.py` | `CalloutItem` — renders speech bubble + connector |
| `canvas/items/floating_topic_item.py` | `FloatingTopicItem` — standalone topic at canvas position |
| `panels/properties_panel.py` | Context-sensitive property editor for selected items |
| `panels/outline_panel.py` | `QTreeView` with bidirectional sync to canvas |
| `panels/marker_panel.py` | Categorized marker icon grid with search |
| `panels/search_panel.py` | Full-text search + find & replace |
| `panels/theme_panel.py` | Theme gallery with preview thumbnails |
| `dialogs/settings_dialog.py` | Tabbed settings: Appearance, Behavior, Keybindings, etc. |
| `dialogs/export_dialog.py` | Export format selector + format-specific options |
| `dialogs/about_dialog.py` | About dialog with version, license info |
| `dialogs/hyperlink_dialog.py` | URL input dialog for topic hyperlinks |
| `dialogs/image_dialog.py` | Image file chooser for topic image attachment |
| `dialogs/print_dialog.py` | Print configuration via QPrintDialog |
| `widgets/color_picker.py` | Color selector with swatch grid and custom picker |
| `widgets/font_picker.py` | Font family, size, weight selector |
| `widgets/icon_button.py` | Styled toolbar button with icon and tooltip |
| `widgets/zoom_slider.py` | Zoom level slider (10%–500%) |

### 2.5 `src/mindnodes/io/` — File I/O Layer

**Dependencies:** `models`, `zipfile`, `json`, `lxml`, `Pillow`, `svgwrite`, `reportlab`, `markdown-it-py`

| Module | Responsibility |
|--------|---------------|
| `base.py` | `FileHandler` ABC (bidirectional) and `Exporter` ABC (export-only) |
| `registry.py` | `FileHandlerRegistry` — maps extensions to handlers, generates file filters |
| `xmind/__init__.py` | `XMindHandler(FileHandler)` — facade combining reader + writer |
| `xmind/reader.py` | `XMindReader` — parse .xmind ZIP → Workbook model |
| `xmind/writer.py` | `XMindWriter` — serialize Workbook → .xmind ZIP |
| `xmind/schema.py` | Field name mapping constants (camelCase ↔ snake_case, style properties) |
| `xmind/thumbnail.py` | Render scene to 256x256 PNG thumbnail for ZIP archive |
| `mindnodes_handler.py` | `MindNodesHandler` — extended .xmind format with callouts, plugin data |
| `freemind_handler.py` | `FreeMindHandler` — .mm XML import/export |
| `opml_handler.py` | `OPMLHandler` — .opml XML import/export |
| `markdown_handler.py` | `MarkdownHandler` — .md heading/list import/export |
| `exporters/png_exporter.py` | `PNGExporter` — render scene to PNG image |
| `exporters/svg_exporter.py` | `SVGExporter` — generate SVG from scene items |
| `exporters/pdf_exporter.py` | `PDFExporter` — render to PDF via reportlab |

### 2.6 `src/mindnodes/plugins/` — Plugin System

**Dependencies:** `models`, `layout.base`, `io.base`, `importlib.metadata`

| Module | Responsibility |
|--------|---------------|
| `base.py` | `MindNodesPlugin` ABC — plugin interface with lifecycle hooks and extension point methods |
| `loader.py` | `PluginLoader` — discovers plugins via `entry_points(group="mindnodes.plugins")` |
| `manager.py` | `PluginManager` — enable/disable plugins, manage lifecycle, dependency resolution |

### 2.7 `src/mindnodes/features/` — Advanced Features

**Dependencies:** `models`, `ui`, `io`, `PySide6`

| Module | Responsibility |
|--------|---------------|
| `presentation.py` | `PresentationMode` — slideshow walk-through with zoom-to-fit per subtree |
| `autosave.py` | `AutoSaveManager` — timer-based saves to recovery directory, startup restore |
| `recent_files.py` | `RecentFilesManager` — track and display recently opened files |
| `print_support.py` | `PrintManager` — QPrintDialog integration, page setup |

### 2.8 `src/mindnodes/themes/` — Theme Resources

**Dependencies:** `models.theme`, `json`

| Module | Responsibility |
|--------|---------------|
| `manager.py` | `ThemeManager` — load built-in and custom themes, smart color generation |
| `builtin/*.json` | 10 predefined theme files defining styles for all element types |

### 2.9 `src/mindnodes/utils/` — Shared Utilities

**Dependencies:** `stdlib` only. No project-internal dependencies.

| Module | Responsibility |
|--------|---------------|
| `geometry.py` | Point arithmetic, rectangle operations, Bezier curve computation, line intersection |
| `color.py` | Hex color parsing, HSL conversion, complementary color generation, palette creation |
| `signals.py` | Custom signal/event bus helpers for model-to-UI notification |
| `settings.py` | `SettingsManager` — QSettings wrapper with typed getters and defaults |
| `logging_config.py` | Configure Python logging with structured format, file rotation |

---

## 3. Dependency Graph

Dependencies flow strictly downward. No circular dependencies are permitted.

```
                    ┌───────────┐
                    │   utils   │  ← No project dependencies
                    └─────┬─────┘
                          │
                    ┌─────▼─────┐
                    │  models   │  ← Depends on: utils
                    └─────┬─────┘
                          │
              ┌───────────┼───────────┐
              │           │           │
        ┌─────▼─────┐ ┌──▼───┐ ┌────▼────┐
        │ commands  │ │layout│ │   io    │  ← Depend on: models
        └─────┬─────┘ └──┬───┘ └────┬────┘
              │           │          │
              └───────────┼──────────┘
                          │
                    ┌─────▼─────┐
                    │    ui     │  ← Depends on: models, commands, layout, io
                    └─────┬─────┘
                          │
                    ┌─────▼─────┐
                    │   app     │  ← Depends on: ui, io, models, plugins
                    └───────────┘

        ┌───────────┐
        │  plugins  │  ← Can access all layers (parallel dependency)
        └───────────┘

        ┌───────────┐
        │ features  │  ← Can access: models, ui, io
        └───────────┘

        ┌───────────┐
        │  themes   │  ← Depends on: models.theme
        └───────────┘
```

**Enforcement:** The module dependency rules should be verified by linting rules that prevent imports from upper layers in lower layers. For example, `models/` must never import from `ui/`.

---

## 4. Python Package Dependencies

### 4.1 Runtime Dependencies

```toml
[project]
dependencies = [
    "PySide6>=6.6.0",
    "pydantic>=2.5.0",
    "Pillow>=10.0.0",
    "lxml>=5.0.0",
    "svgwrite>=1.4.0",
    "reportlab>=4.0.0",
    "markdown-it-py>=3.0.0",
]
```

| Package | Purpose | Used by |
|---------|---------|---------|
| `PySide6` | GUI framework: widgets, graphics, signals, undo stack | `ui/`, `commands/`, `app.py` |
| `pydantic` | Data model validation and JSON serialization | `models/` |
| `Pillow` | Image processing, PNG export, thumbnail generation | `io/exporters/`, `io/xmind/` |
| `lxml` | XML parsing for FreeMind and OPML formats | `io/freemind_handler.py`, `io/opml_handler.py` |
| `svgwrite` | SVG document generation | `io/exporters/svg_exporter.py` |
| `reportlab` | PDF document generation | `io/exporters/pdf_exporter.py` |
| `markdown-it-py` | Markdown parsing | `io/markdown_handler.py` |

### 4.2 Development Dependencies

```toml
[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-qt>=4.2.0",
    "pytest-cov>=4.1.0",
    "mypy>=1.7.0",
    "ruff>=0.1.0",
    "pre-commit>=3.5.0",
    "sphinx>=7.2.0",
    "sphinx-rtd-theme>=2.0.0",
    "nuitka>=1.9.0",
]
```

| Package | Purpose |
|---------|---------|
| `pytest` | Test framework |
| `pytest-qt` | Qt widget testing utilities |
| `pytest-cov` | Test coverage measurement |
| `mypy` | Static type checking (strict mode) |
| `ruff` | Linting and code formatting |
| `pre-commit` | Git hook management |
| `sphinx` + `sphinx-rtd-theme` | API documentation generation |
| `nuitka` | Standalone executable compilation |

---

## 5. Configuration File Templates

### 5.1 pyproject.toml

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "mindnodes"
version = "0.1.0"
description = "An open-source Python mind mapping application with full XMind compatibility"
readme = "README.md"
license = "MIT"
requires-python = ">=3.11"
authors = [
    { name = "Mind-Nodes Contributors" },
]
keywords = ["mindmap", "xmind", "mind-mapping", "brainstorming", "visualization"]
classifiers = [
    "Development Status :: 3 - Alpha",
    "Environment :: X11 Applications :: Qt",
    "Intended Audience :: End Users/Desktop",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: 3.13",
    "Topic :: Office/Business",
]
dependencies = [
    "PySide6>=6.6.0",
    "pydantic>=2.5.0",
    "Pillow>=10.0.0",
    "lxml>=5.0.0",
    "svgwrite>=1.4.0",
    "reportlab>=4.0.0",
    "markdown-it-py>=3.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-qt>=4.2.0",
    "pytest-cov>=4.1.0",
    "mypy>=1.7.0",
    "ruff>=0.1.0",
    "pre-commit>=3.5.0",
    "sphinx>=7.2.0",
    "sphinx-rtd-theme>=2.0.0",
    "nuitka>=1.9.0",
]

[project.scripts]
mindnodes = "mindnodes.app:main"

[project.entry-points."mindnodes.plugins"]
# Example: my_plugin = "my_plugin_package:MyPlugin"

[tool.ruff]
target-version = "py311"
line-length = 100
src = ["src"]

[tool.ruff.lint]
select = [
    "E",    # pycodestyle errors
    "W",    # pycodestyle warnings
    "F",    # pyflakes
    "I",    # isort
    "N",    # pep8-naming
    "UP",   # pyupgrade
    "B",    # flake8-bugbear
    "SIM",  # flake8-simplify
    "TCH",  # flake8-type-checking
    "RUF",  # ruff-specific rules
]

[tool.ruff.lint.isort]
known-first-party = ["mindnodes"]

[tool.mypy]
python_version = "3.11"
strict = true
warn_return_any = true
warn_unused_configs = true
plugins = ["pydantic.mypy"]

[[tool.mypy.overrides]]
module = ["PySide6.*", "lxml.*", "svgwrite.*", "reportlab.*"]
ignore_missing_imports = true

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-ra -q --tb=short"
qt_api = "pyside6"

[tool.coverage.run]
source = ["mindnodes"]

[tool.coverage.report]
show_missing = true
fail_under = 60
```

### 5.2 .pre-commit-config.yaml

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.7.0
    hooks:
      - id: mypy
        additional_dependencies:
          - pydantic>=2.5.0
        args: [--strict]
```

### 5.3 .gitignore

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.egg-info/
dist/
build/
*.egg
.eggs/

# Virtual environments
.venv/
venv/
env/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Testing
.pytest_cache/
.coverage
htmlcov/
.mypy_cache/

# OS
.DS_Store
Thumbs.db

# Build artifacts
*.spec
*.dmg
*.msi
*.deb
*.rpm
*.AppImage

# Auto-generated docs
docs/api/

# Recovery files
*.recovery

# Environment
.env
```

### 5.4 Makefile

```makefile
.PHONY: install dev test lint typecheck format build docs clean

install:
	pip install -e .

dev:
	pip install -e ".[dev]"
	pre-commit install

test:
	pytest tests/ -v --tb=short

test-cov:
	pytest tests/ --cov=mindnodes --cov-report=html --cov-report=term

lint:
	ruff check src/ tests/

typecheck:
	mypy src/

format:
	ruff format src/ tests/
	ruff check --fix src/ tests/

build:
	python scripts/build_exe.py

docs:
	sphinx-build -b html docs/api docs/api/_build

clean:
	rm -rf build/ dist/ *.egg-info .pytest_cache .mypy_cache htmlcov .coverage
	find . -type d -name __pycache__ -exec rm -rf {} +

run:
	python -m mindnodes
```

### 5.5 GitHub Actions CI (.github/workflows/ci.yml)

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
        python-version: ["3.11", "3.12", "3.13"]
      fail-fast: false

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install system dependencies (Linux)
        if: runner.os == 'Linux'
        run: |
          sudo apt-get update
          sudo apt-get install -y libgl1-mesa-dev libegl1 libxkbcommon0

      - name: Install dependencies
        run: pip install -e ".[dev]"

      - name: Lint
        run: ruff check src/ tests/

      - name: Format check
        run: ruff format --check src/ tests/

      - name: Type check
        run: mypy src/

      - name: Test
        run: pytest tests/ --cov=mindnodes --cov-report=xml -v

      - name: Upload coverage
        if: matrix.os == 'ubuntu-latest' && matrix.python-version == '3.12'
        uses: codecov/codecov-action@v3
        with:
          file: coverage.xml
```

---

## 6. Entry Point Configuration

### 6.1 Console Script

```toml
[project.scripts]
mindnodes = "mindnodes.app:main"
```

After `pip install`, the `mindnodes` command is available system-wide.

### 6.2 Module Execution

```bash
python -m mindnodes
```

This invokes `src/mindnodes/__main__.py`, which calls `mindnodes.app.main()`.

### 6.3 Plugin Entry Points

Third-party plugins register via `pyproject.toml`:

```toml
# In the plugin's own pyproject.toml:
[project.entry-points."mindnodes.plugins"]
my_plugin = "my_plugin_package:MyPlugin"
```

Mind-Nodes discovers these at startup via:
```python
from importlib.metadata import entry_points
plugins = entry_points(group="mindnodes.plugins")
```

---

## 7. CONTRIBUTING.md Template

```markdown
# Contributing to Mind-Nodes

## Development Setup

1. Clone the repository:
   git clone https://github.com/your-org/mind-nodes.git
   cd mind-nodes

2. Create a virtual environment:
   python -m venv .venv
   source .venv/bin/activate  # Linux/macOS
   .venv\Scripts\activate     # Windows

3. Install in development mode:
   make dev

4. Verify setup:
   make test
   make lint
   make typecheck

## Code Style

- Code is formatted and linted with ruff (enforced by pre-commit hooks)
- Type annotations are required on all public functions (enforced by mypy strict)
- Follow existing patterns in the codebase

## Testing

- Write tests for all new functionality
- Place tests in tests/ mirroring the src/ structure
- Use pytest-qt for UI component tests
- Run full test suite before submitting: make test

## Pull Request Process

1. Create a feature branch from main
2. Make your changes with tests
3. Ensure CI passes: make test && make lint && make typecheck
4. Submit PR with description of changes
5. Address review feedback
```

---

## 8. Document Cross-References

| Topic | Document |
|-------|----------|
| Why these technologies were chosen | [blueprint.md](blueprint.md) Section 1.2, Section 2 |
| What the project aims to build | [constitution.md](constitution.md) Section 4 |
| Data model details for each module | [artifacts.md](artifacts.md) Section 1 |
| Build order and phase sequencing | [implementation-guide.md](implementation-guide.md) |
