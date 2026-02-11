# Mind-Nodes Artifacts Specification

> The reference document for all data models, file format specifications, and API contracts. Developers consult this document when implementing serialization, deserialization, model classes, and module interfaces.

---

## 1. Domain Model Schema

### 1.1 Workbook

The top-level container representing a single `.xmind` or `.mindnodes` file.

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `id` | `str` | Yes | `uuid4()` | Unique identifier |
| `title` | `str` | Yes | `"Untitled Workbook"` | Display name |
| `sheets` | `list[Sheet]` | Yes | `[Sheet()]` | Ordered list of sheets (min 1) |
| `created_at` | `datetime` | Yes | `now()` | Creation timestamp |
| `modified_at` | `datetime` | Yes | `now()` | Last modification timestamp |
| `creator` | `str` | Yes | `"Mind-Nodes"` | Creator application name |
| `version` | `str` | Yes | `"1.0.0"` | Creator application version |
| `_extra` | `dict` | No | `{}` | Preserved unknown fields for round-trip fidelity |

**Constraints:**
- Must contain at least one Sheet
- Sheets are ordered; order matters for tab display

### 1.2 Sheet

A single mind map page within a Workbook.

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `id` | `str` | Yes | `uuid4()` | Unique identifier |
| `title` | `str` | Yes | `"Sheet 1"` | Tab display name |
| `root_topic` | `Topic` | Yes | *(required)* | The central root topic |
| `relationships` | `list[Relationship]` | No | `[]` | Freeform connections between topics |
| `theme` | `Theme \| None` | No | `None` | Applied color theme |
| `style_map` | `dict[str, Style]` | No | `{}` | Style definitions keyed by style ID |
| `_extra` | `dict` | No | `{}` | Preserved unknown fields |

**Constraints:**
- Exactly one `root_topic`
- All `Relationship.end1_id` and `end2_id` must reference valid Topic IDs within this Sheet

### 1.3 Topic

The core recursive tree node representing a single idea/concept on the map.

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `id` | `str` | Yes | `uuid4()` | Unique identifier |
| `title` | `str` | Yes | `"Topic"` | Display text |
| `children_attached` | `list[Topic]` | No | `[]` | Child topics managed by layout algorithm |
| `children_detached` | `list[Topic]` | No | `[]` | Floating topics with explicit positions |
| `notes` | `Notes \| None` | No | `None` | Attached rich text notes |
| `labels` | `list[str]` | No | `[]` | Short text tags |
| `markers` | `list[MarkerRef]` | No | `[]` | Icon markers |
| `href` | `str \| None` | No | `None` | Hyperlink URL |
| `style` | `Style \| None` | No | `None` | Override style (inline or reference) |
| `structure_class` | `StructureClass \| None` | No | `None` | Layout algorithm override for subtree |
| `image` | `ImageRef \| None` | No | `None` | Embedded image |
| `position` | `Position \| None` | No | `None` | Explicit x,y (detached topics only) |
| `boundaries` | `list[Boundary]` | No | `[]` | Visual groupings of child ranges |
| `summaries` | `list[Summary]` | No | `[]` | Summary brackets over child ranges |
| `callouts` | `list[Callout]` | No | `[]` | Speech-bubble annotations |
| `branch` | `BranchStyle \| None` | No | `None` | Branch line style override |
| `is_folded` | `bool` | No | `False` | Whether subtree is collapsed |
| `_extra` | `dict` | No | `{}` | Preserved unknown fields |

**Semantics:**
- `children_attached`: Standard children positioned by the layout engine. Corresponds to XMind's `children.attached` array.
- `children_detached`: Floating children with explicit `position` (x, y). Corresponds to XMind's `children.detached` array.
- `structure_class`: When set, the subtree rooted at this topic uses the specified layout algorithm instead of inheriting from the parent.

### 1.4 Relationship

A freeform arrow connection between any two topics in the same Sheet.

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `id` | `str` | Yes | `uuid4()` | Unique identifier |
| `title` | `str \| None` | No | `None` | Label text displayed on the arrow |
| `end1_id` | `str` | Yes | *(required)* | Source topic ID |
| `end2_id` | `str` | Yes | *(required)* | Target topic ID |
| `style` | `Style \| None` | No | `None` | Arrow style override |
| `control_points` | `list[Position]` | No | `[]` | Bezier control points for arrow path |
| `_extra` | `dict` | No | `{}` | Preserved unknown fields |

**Constraints:**
- `end1_id != end2_id` (no self-referencing)
- Both endpoints must reference existing Topic IDs in the parent Sheet

### 1.5 Boundary

A visual container grouping a contiguous range of sibling topics.

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `id` | `str` | Yes | `uuid4()` | Unique identifier |
| `title` | `str \| None` | No | `None` | Boundary label text |
| `range_start` | `int` | Yes | *(required)* | Start index in parent's children_attached |
| `range_end` | `int` | Yes | *(required)* | End index (inclusive) in parent's children_attached |
| `style` | `Style \| None` | No | `None` | Boundary visual style |
| `_extra` | `dict` | No | `{}` | Preserved unknown fields |

**Semantics:**
- Groups `parent.children_attached[range_start..range_end]` (inclusive)
- Rendered as a rounded rectangle or cloud shape enclosing the grouped topics
- Defined on the parent Topic (stored in `parent.boundaries`)

### 1.6 Summary

A bracket annotation spanning a contiguous range of sibling topics, linking to a summary topic.

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `id` | `str` | Yes | `uuid4()` | Unique identifier |
| `topic_id` | `str` | Yes | *(required)* | ID of the summary Topic (the summarizing node) |
| `range_start` | `int` | Yes | *(required)* | Start index in parent's children_attached |
| `range_end` | `int` | Yes | *(required)* | End index (inclusive) in parent's children_attached |
| `_extra` | `dict` | No | `{}` | Preserved unknown fields |

**Semantics:**
- Renders a bracket `]` spanning `parent.children_attached[range_start..range_end]`
- The bracket points to the summary Topic identified by `topic_id`
- Defined on the parent Topic (stored in `parent.summaries`)

### 1.7 Callout

A speech-bubble annotation attached to a parent topic.

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `id` | `str` | Yes | `uuid4()` | Unique identifier |
| `title` | `str` | Yes | `""` | Callout text content |
| `style` | `Style \| None` | No | `None` | Callout visual style |
| `_extra` | `dict` | No | `{}` | Preserved unknown fields |

### 1.8 Notes

Rich text notes attached to a Topic. Supports both plain text and HTML subset.

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `plain` | `PlainContent` | Yes | *(required)* | Plain text representation |
| `html` | `HtmlContent \| None` | No | `None` | HTML-formatted representation |

**PlainContent:**

| Field | Type | Description |
|-------|------|-------------|
| `content` | `str` | Plain text string |

**HtmlContent:**

| Field | Type | Description |
|-------|------|-------------|
| `content` | `str` | Sanitized HTML subset (bold, italic, underline, lists, links) |

### 1.9 Style

A collection of visual properties that can be applied to topics, relationships, boundaries, or the map itself.

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `id` | `str` | Yes | `uuid4()` | Unique identifier |
| `type` | `StyleType` | Yes | *(required)* | What this style applies to |
| `properties` | `StyleProperties` | Yes | `StyleProperties()` | Visual property values |

**StyleType enum:**

| Value | Applies to |
|-------|-----------|
| `"topic"` | Topic nodes |
| `"relationship"` | Relationship arrows |
| `"boundary"` | Boundary containers |
| `"summary"` | Summary brackets |
| `"map"` | Map/canvas background |

**StyleProperties** (all fields optional — only set fields override defaults):

| Field | Type | Description |
|-------|------|-------------|
| `shape` | `str` | Node shape: `"rect"`, `"rounded-rect"`, `"ellipse"`, `"diamond"`, `"parallelogram"`, `"cloud"`, `"underline"`, `"none"` |
| `background_color` | `str` | Hex color `"#RRGGBB"` or `"#RRGGBBAA"` |
| `border_color` | `str` | Border hex color |
| `border_width` | `float` | Border width in points |
| `border_dash` | `str` | Dash pattern: `"solid"`, `"dash"`, `"dot"`, `"dash-dot"` |
| `font_family` | `str` | Font family name |
| `font_size` | `float` | Font size in points |
| `font_weight` | `str` | `"normal"`, `"bold"` |
| `font_style` | `str` | `"normal"`, `"italic"` |
| `font_color` | `str` | Text hex color |
| `text_align` | `str` | `"left"`, `"center"`, `"right"` |
| `line_color` | `str` | Branch/relationship line hex color |
| `line_width` | `float` | Line width in points |
| `line_dash` | `str` | Line dash pattern |
| `line_style` | `str` | `"straight"`, `"curve"`, `"elbow"`, `"rounded-elbow"` |
| `line_tapered` | `bool` | Whether branch lines taper from thick to thin |
| `arrow_start` | `str` | Arrow head at start: `"none"`, `"normal"`, `"diamond"`, `"circle"` |
| `arrow_end` | `str` | Arrow head at end |
| `shadow_enabled` | `bool` | Whether drop shadow is shown |
| `shadow_color` | `str` | Shadow hex color |
| `shadow_offset_x` | `float` | Shadow horizontal offset |
| `shadow_offset_y` | `float` | Shadow vertical offset |
| `gradient_type` | `str \| None` | `None`, `"linear"`, `"radial"` |
| `gradient_start_color` | `str` | Gradient start hex color |
| `gradient_end_color` | `str` | Gradient end hex color |
| `gradient_angle` | `float` | Linear gradient angle in degrees |
| `padding_top` | `float` | Inner padding (points) |
| `padding_right` | `float` | Inner padding |
| `padding_bottom` | `float` | Inner padding |
| `padding_left` | `float` | Inner padding |
| `margin_top` | `float` | Outer margin (points) |
| `margin_right` | `float` | Outer margin |
| `margin_bottom` | `float` | Outer margin |
| `margin_left` | `float` | Outer margin |

### 1.10 Theme

A complete visual theme defining default styles for all element types.

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `id` | `str` | Yes | *(required)* | Unique theme identifier |
| `name` | `str` | Yes | *(required)* | Display name |
| `central_topic_style` | `Style` | Yes | *(required)* | Style for root/central topic |
| `main_topic_style` | `Style` | Yes | *(required)* | Style for first-level children |
| `sub_topic_style` | `Style` | Yes | *(required)* | Style for second-level and deeper children |
| `floating_topic_style` | `Style` | Yes | *(required)* | Style for detached/floating topics |
| `relationship_style` | `Style` | Yes | *(required)* | Default style for relationship arrows |
| `boundary_style` | `Style` | Yes | *(required)* | Default style for boundaries |
| `summary_style` | `Style` | Yes | *(required)* | Default style for summary brackets |
| `callout_style` | `Style` | Yes | *(required)* | Default style for callouts |
| `map_style` | `MapStyle` | Yes | *(required)* | Canvas/background style |
| `color_palette` | `list[str]` | Yes | *(required)* | Hex colors for auto-assigning branch colors |

**MapStyle:**

| Field | Type | Description |
|-------|------|-------------|
| `background_color` | `str` | Canvas background hex color |
| `wallpaper_key` | `str \| None` | Built-in wallpaper identifier |
| `grid_visible` | `bool` | Whether to show canvas grid |
| `grid_spacing` | `float` | Grid cell size in points |

### 1.11 MarkerRef

A reference to a marker icon applied to a Topic.

| Field | Type | Description |
|-------|------|-------------|
| `marker_id` | `str` | Marker identifier following XMind's naming convention |

**Marker taxonomy (complete list):**

| Group | Marker IDs |
|-------|-----------|
| Priority | `priority-1` through `priority-9` |
| Smiley | `smiley-smile`, `smiley-laugh`, `smiley-angry`, `smiley-cry`, `smiley-surprise`, `smiley-boring`, `smiley-embarrass` |
| Task | `task-start`, `task-quarter`, `task-half`, `task-3quarter`, `task-done`, `task-pause` |
| Flag | `flag-red`, `flag-orange`, `flag-yellow`, `flag-green`, `flag-blue`, `flag-purple` |
| Star | `star-red`, `star-orange`, `star-yellow`, `star-green`, `star-blue`, `star-purple` |
| People | `people-red`, `people-orange`, `people-yellow`, `people-green`, `people-blue`, `people-purple` |
| Arrow | `arrow-up`, `arrow-up-right`, `arrow-right`, `arrow-down-right`, `arrow-down`, `arrow-down-left`, `arrow-left`, `arrow-up-left`, `arrow-refresh` |
| Symbol | `symbol-plus`, `symbol-minus`, `symbol-question`, `symbol-exclam`, `symbol-info`, `symbol-wrong`, `symbol-right`, `symbol-pause`, `symbol-no-entry` |
| Month | `month-jan` through `month-dec` |
| Week | `week-mon` through `week-sun` |
| Half-star | `half-star-red`, `half-star-orange`, `half-star-yellow`, `half-star-green`, `half-star-blue`, `half-star-purple` |

### 1.12 ImageRef

A reference to an embedded image in the resources directory.

| Field | Type | Description |
|-------|------|-------------|
| `src` | `str` | Resource path: `"xap:resources/{filename}"` |
| `width` | `int` | Display width in pixels |
| `height` | `int` | Display height in pixels |

### 1.13 Position

A 2D coordinate point.

| Field | Type | Description |
|-------|------|-------------|
| `x` | `float` | Horizontal coordinate |
| `y` | `float` | Vertical coordinate |

### 1.14 BranchStyle

Branch line style overrides for a topic's connection to its parent.

| Field | Type | Description |
|-------|------|-------------|
| `line_color` | `str \| None` | Branch line hex color |
| `line_width` | `float \| None` | Line width in points |
| `line_style` | `str \| None` | `"curve"`, `"straight"`, `"elbow"`, `"rounded-elbow"` |
| `line_tapered` | `bool \| None` | Whether line tapers |

### 1.15 StructureClass Enum

Layout algorithm identifiers matching XMind's internal naming convention.

| Value | Layout | Direction |
|-------|--------|-----------|
| `org.xmind.ui.map` | Balanced radial mind map | Bidirectional (default) |
| `org.xmind.ui.map.clockwise` | Radial, clockwise only | Clockwise |
| `org.xmind.ui.map.anticlockwise` | Radial, counterclockwise only | Counterclockwise |
| `org.xmind.ui.map.unbalanced` | Radial, unbalanced (all right) | Right |
| `org.xmind.ui.logic.right` | Logic chart | Rightward |
| `org.xmind.ui.logic.left` | Logic chart | Leftward |
| `org.xmind.ui.org-chart.down` | Org chart | Downward |
| `org.xmind.ui.org-chart.up` | Org chart | Upward |
| `org.xmind.ui.tree.right` | Tree chart | Rightward |
| `org.xmind.ui.tree.left` | Tree chart | Leftward |
| `org.xmind.ui.timeline.horizontal` | Timeline | Horizontal |
| `org.xmind.ui.timeline.vertical` | Timeline | Vertical |
| `org.xmind.ui.fishbone.leftHeaded` | Fishbone/Ishikawa | Left-headed |
| `org.xmind.ui.fishbone.rightHeaded` | Fishbone/Ishikawa | Right-headed |
| `org.xmind.ui.spreadsheet` | Matrix | Rows |
| `org.xmind.ui.spreadsheet.column` | Matrix/Tree Table | Columns |
| `org.xmind.ui.brace.right` | Brace map | Rightward |

### 1.16 Entity Relationship Diagram

```mermaid
erDiagram
    Workbook ||--o{ Sheet : contains
    Sheet ||--|| Topic : "has root"
    Sheet ||--o{ Relationship : contains
    Sheet }o--o| Theme : "applies"
    Sheet ||--o{ Style : "defines in style_map"

    Topic ||--o{ Topic : "children_attached"
    Topic ||--o{ Topic : "children_detached"
    Topic ||--o{ Boundary : has
    Topic ||--o{ Summary : has
    Topic ||--o{ Callout : has
    Topic ||--o{ MarkerRef : has
    Topic }o--o| Notes : has
    Topic }o--o| Style : "styled by"
    Topic }o--o| ImageRef : has
    Topic }o--o| Position : "positioned at"
    Topic }o--o| BranchStyle : "branch styled by"

    Relationship }o--|| Topic : "end1 (source)"
    Relationship }o--|| Topic : "end2 (target)"
    Relationship }o--o| Style : "styled by"

    Boundary }o--o| Style : "styled by"

    Summary }o--|| Topic : "summarizes into"

    Callout }o--o| Style : "styled by"

    Theme ||--|| Style : "central_topic_style"
    Theme ||--|| Style : "main_topic_style"
    Theme ||--|| Style : "sub_topic_style"
    Theme ||--|| Style : "floating_topic_style"
    Theme ||--|| Style : "relationship_style"
    Theme ||--|| Style : "boundary_style"
    Theme ||--|| Style : "summary_style"
    Theme ||--|| Style : "callout_style"
    Theme ||--|| MapStyle : has

    Style ||--|| StyleProperties : has

    Notes }o--|| PlainContent : has
    Notes }o--o| HtmlContent : has
```

---

## 2. File Format Specifications

### 2.1 Native .xmind Format (XMind Zen Compatible)

The `.xmind` file is a standard ZIP archive with the following structure:

```
file.xmind (ZIP archive)
├── content.json          # Array of Sheet objects — the mind map data
├── metadata.json         # Creator and version metadata
├── manifest.json         # File registry with MIME types
├── Thumbnails/
│   └── thumbnail.png     # 256x256 preview image of the first sheet
└── resources/
    ├── {uuid1}.png       # Embedded image referenced by a Topic
    ├── {uuid2}.jpg       # Another embedded image
    └── ...
```

#### 2.1.1 content.json Schema

The `content.json` file is a JSON array where each element represents a Sheet.

```json
[
  {
    "id": "sheet-uuid-1",
    "class": "sheet",
    "title": "Sheet 1",
    "rootTopic": {
      "id": "topic-uuid-root",
      "class": "topic",
      "title": "Central Topic",
      "structureClass": "org.xmind.ui.map",
      "children": {
        "attached": [
          {
            "id": "topic-uuid-child1",
            "class": "topic",
            "title": "Main Topic 1",
            "children": {
              "attached": [
                {
                  "id": "topic-uuid-sub1",
                  "class": "topic",
                  "title": "Subtopic 1.1",
                  "markers": [
                    { "markerId": "priority-1" }
                  ],
                  "notes": {
                    "plain": { "content": "This is a note" },
                    "html": { "content": "<p>This is a <b>note</b></p>" }
                  },
                  "labels": ["important"]
                }
              ]
            },
            "boundaries": [
              {
                "id": "boundary-uuid-1",
                "title": "Group A",
                "range": "(0,0)"
              }
            ],
            "style": {
              "id": "style-uuid-1",
              "properties": {
                "svg:fill": "#FF6600",
                "fo:color": "#FFFFFF",
                "fo:font-family": "Arial",
                "fo:font-size": "14pt",
                "border-line-color": "#CC5500",
                "border-line-width": "2pt",
                "shape-class": "org.xmind.topicShape.roundedRect",
                "line-color": "#FF6600"
              }
            }
          },
          {
            "id": "topic-uuid-child2",
            "class": "topic",
            "title": "Main Topic 2",
            "href": "https://example.com",
            "image": {
              "src": "xap:resources/abc123.png",
              "width": 200,
              "height": 150
            }
          }
        ],
        "detached": [
          {
            "id": "topic-uuid-floating",
            "class": "topic",
            "title": "Floating Note",
            "position": { "x": 300, "y": -200 }
          }
        ]
      },
      "summaries": [
        {
          "id": "summary-uuid-1",
          "range": "(0,1)",
          "topicId": "topic-uuid-summary"
        }
      ]
    },
    "relationships": [
      {
        "id": "rel-uuid-1",
        "title": "relates to",
        "end1Id": "topic-uuid-child1",
        "end2Id": "topic-uuid-child2",
        "controlPoints": [
          { "x": 100, "y": 50 },
          { "x": 200, "y": -30 }
        ]
      }
    ],
    "theme": {
      "id": "theme-uuid-1",
      "centralTopic": { "properties": { "svg:fill": "#2196F3" } },
      "mainTopic": { "properties": { "svg:fill": "#42A5F5" } },
      "subTopic": { "properties": { "svg:fill": "#FFFFFF" } }
    }
  }
]
```

**XMind JSON field → Mind-Nodes model field mappings:**

| XMind JSON Field | Mind-Nodes Model Field | Notes |
|-----------------|----------------------|-------|
| `rootTopic` | `root_topic` | camelCase → snake_case |
| `children.attached` | `children_attached` | Nested object → flat list |
| `children.detached` | `children_detached` | Nested object → flat list |
| `structureClass` | `structure_class` | camelCase → snake_case |
| `markerId` | `marker_id` | camelCase → snake_case |
| `end1Id` / `end2Id` | `end1_id` / `end2_id` | camelCase → snake_case |
| `topicId` | `topic_id` | camelCase → snake_case |
| `controlPoints` | `control_points` | camelCase → snake_case |
| `isFolded` | `is_folded` | camelCase → snake_case |
| `style.properties["svg:fill"]` | `style.properties.background_color` | XMind uses SVG/XSL-FO property names |
| `style.properties["fo:color"]` | `style.properties.font_color` | XSL-FO naming |
| `style.properties["fo:font-family"]` | `style.properties.font_family` | XSL-FO naming |
| `style.properties["fo:font-size"]` | `style.properties.font_size` | Parse "14pt" → 14.0 |
| `style.properties["shape-class"]` | `style.properties.shape` | Map XMind shape class → shape enum |
| `style.properties["line-color"]` | `style.properties.line_color` | Direct mapping |
| `style.properties["border-line-color"]` | `style.properties.border_color` | Rename |
| `style.properties["border-line-width"]` | `style.properties.border_width` | Parse "2pt" → 2.0 |
| `range` (boundaries/summaries) | `range_start`, `range_end` | Parse "(0,2)" → start=0, end=2 |

**XMind shape class → Mind-Nodes shape enum:**

| XMind shape-class | Mind-Nodes shape |
|-------------------|-----------------|
| `org.xmind.topicShape.rect` | `"rect"` |
| `org.xmind.topicShape.roundedRect` | `"rounded-rect"` |
| `org.xmind.topicShape.ellipse` | `"ellipse"` |
| `org.xmind.topicShape.diamond` | `"diamond"` |
| `org.xmind.topicShape.parallelogram` | `"parallelogram"` |
| `org.xmind.topicShape.cloud` | `"cloud"` |
| `org.xmind.topicShape.underline` | `"underline"` |
| `org.xmind.topicShape.noBorder` | `"none"` |

#### 2.1.2 metadata.json Schema

```json
{
  "creator": {
    "name": "Mind-Nodes",
    "version": "1.0.0"
  },
  "activeSheetId": "sheet-uuid-1"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `creator.name` | `str` | Application name that created the file |
| `creator.version` | `str` | Application version |
| `activeSheetId` | `str` | ID of the last-active sheet (for restoring tab) |

#### 2.1.3 manifest.json Schema

```json
{
  "file-entries": {
    "content.json": { "media-type": "application/json" },
    "metadata.json": { "media-type": "application/json" },
    "Thumbnails/thumbnail.png": { "media-type": "image/png" },
    "resources/abc123.png": { "media-type": "image/png" }
  }
}
```

| Field | Type | Description |
|-------|------|-------------|
| `file-entries` | `dict[str, MediaEntry]` | Maps ZIP entry paths to their MIME types |
| `MediaEntry.media-type` | `str` | MIME type string |

### 2.2 Native .mindnodes Format

Same ZIP structure as `.xmind` with extensions:

| Extension | Description |
|-----------|-------------|
| `content.json` extended fields | `callouts` array on topics, `plugin_data` dict per sheet |
| `manifest.json` | Includes plugin resource entries |
| File extension | `.mindnodes` instead of `.xmind` |

The `.mindnodes` format is a strict **superset** of `.xmind`. Any `.mindnodes` file can be saved as `.xmind` by stripping extension fields.

### 2.3 FreeMind XML Format (.mm)

FreeMind files are XML documents following the FreeMind DTD.

**Mapping rules:**

| FreeMind XML | Mind-Nodes Model |
|-------------|-----------------|
| `<map version="1.0.1">` | Workbook with one Sheet |
| `<node TEXT="...">` | Topic with `title=TEXT` |
| Nested `<node>` elements | `children_attached` |
| `<node POSITION="right">` | Radial layout hint (right side) |
| `<node FOLDED="true">` | `is_folded=True` |
| `<richcontent TYPE="NOTE">` | `notes` (HTML content) |
| `<icon BUILTIN="...">` | `markers` (map FreeMind icon names to Mind-Nodes marker IDs) |
| `<edge COLOR="..." WIDTH="...">` | `branch` style |
| `<arrowlink DESTINATION="...">` | `Relationship` |
| `<font NAME="..." SIZE="..." BOLD="true">` | Style font properties |
| `BACKGROUND_COLOR`, `COLOR` attributes | Style color properties |

### 2.4 OPML Format (.opml)

OPML (Outline Processor Markup Language) is a simple XML outline format.

**Mapping rules:**

| OPML XML | Mind-Nodes Model |
|----------|-----------------|
| `<opml version="2.0">` | Workbook container |
| `<head><title>...</title></head>` | Workbook title |
| `<body>` | Sheet |
| `<outline text="...">` | Topic with `title=text` |
| Nested `<outline>` elements | `children_attached` |
| `_note` attribute | Notes (plain text) |

**Limitations:** OPML only preserves text hierarchy; no styling, markers, relationships, or layout information.

### 2.5 Markdown Format (.md)

Mind-Nodes uses a heading-and-list convention for Markdown:

**Export rules:**
```markdown
# Root Topic Title

## Main Topic 1

- Subtopic 1.1
  - Sub-subtopic 1.1.1
  - Sub-subtopic 1.1.2
- Subtopic 1.2

## Main Topic 2

- Subtopic 2.1
```

| Markdown Element | Mind-Nodes Model |
|-----------------|-----------------|
| `# Heading 1` | Root topic title |
| `## Heading 2` | First-level children |
| `- List item` (under heading) | Second-level children |
| Nested `- List item` (indented) | Deeper-level children |
| `> Blockquote` after a topic line | Notes attached to preceding topic |

**Import parsing rules:**
1. First `# H1` becomes the root topic
2. Each `## H2` becomes a first-level child
3. Bullet lists under headings become deeper children
4. Indentation level determines nesting depth
5. Blockquotes are parsed as notes on the preceding topic

**Limitations:** Only text hierarchy is preserved; no styling, markers, relationships, or layout information.

### 2.6 Export-Only Format Specifications

#### PNG Export

| Parameter | Default | Description |
|-----------|---------|-------------|
| Resolution | 2x (Retina) | Scale factor for crisp rendering |
| DPI | 144 | Dots per inch in PNG metadata |
| Background | White (`#FFFFFF`) | Canvas background color |
| Padding | 40px | Margin around the map |
| Max dimension | 16384px | Maximum width or height |
| Format | RGBA PNG | 32-bit with alpha channel |

**Process:** Render QGraphicsScene to QImage at specified scale → save as PNG via Pillow.

#### SVG Export

| Parameter | Default | Description |
|-----------|---------|-------------|
| Units | Points (pt) | SVG coordinate units |
| Font embedding | Reference only | Fonts referenced by name, not embedded |
| CSS classes | Yes | Each element type gets a CSS class for external styling |

**Structure:**
```xml
<svg xmlns="http://www.w3.org/2000/svg">
  <defs><!-- gradient definitions, marker definitions --></defs>
  <g class="mindmap-canvas">
    <g class="topic" id="topic-uuid">
      <rect class="topic-shape" .../>
      <text class="topic-title" ...>Topic Text</text>
      <g class="topic-markers">...</g>
    </g>
    <path class="branch" .../>
    <g class="relationship" .../>
    <g class="boundary" .../>
  </g>
</svg>
```

#### PDF Export

| Parameter | Default | Description |
|-----------|---------|-------------|
| Page size | A4 landscape | Paper size |
| Margins | 20mm all sides | Page margins |
| Multi-page | Auto-tile | Large maps split across pages with overlap |
| Font embedding | Yes | Fonts embedded in PDF |
| DPI | 300 | Rendering resolution |

**Process:** Render via `reportlab` with canvas operations, or use `QPrinter` with `QPainter`.

---

## 3. Internal API Contracts

### 3.1 Command Interface

```python
from PySide6.QtWidgets import QUndoCommand

class MindNodeCommand(QUndoCommand):
    """Base class for all undoable operations."""

    def redo(self) -> None:
        """Apply the change. Called on initial execution and on redo."""
        ...

    def undo(self) -> None:
        """Reverse the change. Must be a perfect inverse of redo()."""
        ...

    def id(self) -> int:
        """Return command type ID for merging. Return -1 to disable merging."""
        return -1

    def mergeWith(self, other: QUndoCommand) -> bool:
        """Attempt to merge with a subsequent command of the same id().
        Return True if merged successfully, False otherwise."""
        return False
```

**Contract rules:**
1. `redo()` and `undo()` must be **perfect inverses** — executing redo then undo must leave the model in its original state
2. Commands must capture **all state needed** to reverse the operation at construction time
3. Commands must **not hold references** to visual items — only model references
4. A command's constructor must **not** execute the operation; `redo()` handles that
5. After `QUndoStack.push(command)`, the stack calls `redo()` automatically

### 3.2 Layout Algorithm Interface

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class LayoutConfig:
    """Configuration for layout computation."""
    spacing_h: float = 50.0       # Horizontal spacing between nodes
    spacing_v: float = 30.0       # Vertical spacing between nodes
    padding: float = 20.0         # Padding around node content
    compact_mode: bool = False    # Whether to use compact spacing
    node_size_calculator: Callable[[Topic], tuple[float, float]] | None = None

@dataclass
class NodeGeometry:
    """Computed geometry for a single node."""
    x: float                      # Top-left X coordinate
    y: float                      # Top-left Y coordinate
    width: float                  # Node bounding box width
    height: float                 # Node bounding box height
    connector_in: tuple[float, float]   # Incoming branch attachment point
    connector_out: tuple[float, float]  # Outgoing branch attachment point
    branch_points: list[tuple[float, float]]  # Branch path control points

class LayoutAlgorithm(ABC):
    """Abstract base class for mind map layout algorithms."""

    @abstractmethod
    def layout(
        self,
        root: Topic,
        config: LayoutConfig,
    ) -> dict[str, NodeGeometry]:
        """Compute positions for all topics in the tree.

        Args:
            root: The root Topic of the tree to layout.
            config: Layout configuration parameters.

        Returns:
            Mapping of topic ID -> computed NodeGeometry.
        """
        ...

    @abstractmethod
    def structure_class(self) -> str:
        """Return the structureClass string this layout handles.
        E.g., 'org.xmind.ui.map' for radial mind map."""
        ...
```

**Contract rules:**
1. `layout()` must produce coordinates for **every** topic in the tree (recursive)
2. No two nodes may **overlap** in the returned geometry
3. The algorithm must handle **empty children** (leaf nodes) gracefully
4. The algorithm must handle **folded topics** — folded subtrees are excluded from layout
5. `node_size_calculator` in config is used to determine each node's intrinsic size based on its content (text, markers, image); if `None`, use sensible defaults

### 3.3 File Handler Interface

```python
from abc import ABC, abstractmethod
from pathlib import Path

class FileHandler(ABC):
    """Abstract base class for file format handlers (bidirectional)."""

    @abstractmethod
    def can_load(self, path: Path) -> bool:
        """Return True if this handler can load the given file."""
        ...

    @abstractmethod
    def load(self, path: Path) -> Workbook:
        """Load a file and return a Workbook model."""
        ...

    @abstractmethod
    def can_save(self, path: Path) -> bool:
        """Return True if this handler can save to the given path."""
        ...

    @abstractmethod
    def save(self, workbook: Workbook, path: Path) -> None:
        """Save a Workbook model to the given file path."""
        ...

    @abstractmethod
    def supported_extensions(self) -> list[str]:
        """Return list of file extensions (e.g., ['.xmind'])."""
        ...

    def file_filter(self) -> str:
        """Return file dialog filter string.
        E.g., 'XMind Files (*.xmind)'"""
        ...


class Exporter(ABC):
    """Abstract base class for export-only format handlers."""

    @abstractmethod
    def export(
        self,
        workbook: Workbook,
        path: Path,
        options: dict | None = None,
    ) -> None:
        """Export a Workbook to the given path with optional parameters."""
        ...

    @abstractmethod
    def supported_extensions(self) -> list[str]:
        """Return list of file extensions (e.g., ['.png'])."""
        ...
```

### 3.4 Plugin Interface

```python
from abc import ABC, abstractmethod

class MindNodesPlugin(ABC):
    """Abstract base class for Mind-Nodes plugins."""

    @property
    @abstractmethod
    def id(self) -> str:
        """Unique plugin identifier (e.g., 'com.example.myplugin')."""
        ...

    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable plugin name."""
        ...

    @property
    def version(self) -> str:
        """Plugin version string."""
        return "0.0.0"

    @abstractmethod
    def activate(self, app: "MindNodesApp") -> None:
        """Called when the plugin is enabled. Register extensions here."""
        ...

    @abstractmethod
    def deactivate(self) -> None:
        """Called when the plugin is disabled. Clean up resources."""
        ...

    def get_layouts(self) -> list[type[LayoutAlgorithm]]:
        """Return custom layout algorithm classes to register."""
        return []

    def get_file_handlers(self) -> list[type[FileHandler]]:
        """Return custom file handler classes to register."""
        return []

    def get_exporters(self) -> list[type[Exporter]]:
        """Return custom exporter classes to register."""
        return []

    def get_menu_actions(self) -> list["QAction"]:
        """Return custom menu actions to add."""
        return []

    def get_toolbar_actions(self) -> list["QAction"]:
        """Return custom toolbar actions to add."""
        return []

    def get_panel_widgets(self) -> list[type["QDockWidget"]]:
        """Return custom dock panel widget classes."""
        return []

    def get_marker_packs(self) -> list["MarkerPack"]:
        """Return custom marker icon packs."""
        return []

    def get_themes(self) -> list[Theme]:
        """Return custom themes."""
        return []
```

### 3.5 Signal Contracts (Model Notifications)

The domain model emits signals when mutated by commands. UI components observe these signals to stay synchronized.

**Topic signals:**

| Signal | Parameters | Emitted when |
|--------|-----------|-------------|
| `topic_added` | `parent_id: str, topic: Topic, index: int` | A child topic is added |
| `topic_removed` | `parent_id: str, topic_id: str, index: int` | A child topic is removed |
| `topic_modified` | `topic_id: str, field: str, old_value: Any, new_value: Any` | Any topic field changes |
| `topic_moved` | `topic_id: str, old_parent_id: str, new_parent_id: str, new_index: int` | Topic reparented |
| `children_reordered` | `parent_id: str, old_order: list[str], new_order: list[str]` | Child order changed |
| `fold_changed` | `topic_id: str, is_folded: bool` | Topic folded/unfolded |

**Sheet signals:**

| Signal | Parameters | Emitted when |
|--------|-----------|-------------|
| `relationship_added` | `relationship: Relationship` | Relationship created |
| `relationship_removed` | `relationship_id: str` | Relationship deleted |
| `theme_changed` | `old_theme: Theme \| None, new_theme: Theme \| None` | Sheet theme changed |
| `layout_requested` | `topic_id: str \| None` | Layout recomputation needed (None = full sheet) |

**Workbook signals:**

| Signal | Parameters | Emitted when |
|--------|-----------|-------------|
| `sheet_added` | `sheet: Sheet, index: int` | Sheet added to workbook |
| `sheet_removed` | `sheet_id: str, index: int` | Sheet removed |
| `sheet_reordered` | `old_index: int, new_index: int` | Sheet tab moved |
| `active_sheet_changed` | `sheet_id: str` | Active sheet tab changed |
| `dirty_changed` | `is_dirty: bool` | Unsaved changes status changed |

---

## 4. Configuration Schemas

### 4.1 Application Settings

```json
{
  "appearance": {
    "default_theme": "default",
    "canvas_background": "#FFFFFF",
    "show_grid": false,
    "grid_size": 20.0,
    "show_minimap": true,
    "animation_enabled": true,
    "animation_duration_ms": 300
  },
  "behavior": {
    "auto_save_enabled": true,
    "auto_save_interval_seconds": 60,
    "undo_limit": 200,
    "default_structure_class": "org.xmind.ui.map",
    "double_click_action": "edit_title",
    "scroll_zoom_enabled": true,
    "confirm_delete": true
  },
  "files": {
    "recent_files_max": 20,
    "recent_files": [],
    "default_save_format": ".xmind",
    "auto_open_last": false,
    "backup_on_save": true
  },
  "export": {
    "png_scale": 2.0,
    "png_dpi": 144,
    "png_background": "#FFFFFF",
    "png_padding": 40,
    "pdf_page_size": "A4",
    "pdf_orientation": "landscape",
    "pdf_margins_mm": 20,
    "svg_embed_fonts": false
  },
  "plugins": {
    "enabled": {}
  },
  "window": {
    "geometry": null,
    "state": null,
    "last_directory": null
  }
}
```

### 4.2 Default Keybinding Table

| Action | Default Shortcut | Context |
|--------|-----------------|---------|
| New Workbook | `Ctrl+N` | Global |
| Open File | `Ctrl+O` | Global |
| Save | `Ctrl+S` | Global |
| Save As | `Ctrl+Shift+S` | Global |
| Undo | `Ctrl+Z` | Global |
| Redo | `Ctrl+Shift+Z` | Global |
| Add Sibling Topic | `Enter` | Canvas (topic selected) |
| Add Child Topic | `Tab` | Canvas (topic selected) |
| Add Parent Topic | `Shift+Tab` | Canvas (topic selected) |
| Delete Topic | `Delete` | Canvas (topic selected) |
| Edit Topic Title | `F2` or `Space` | Canvas (topic selected) |
| Copy | `Ctrl+C` | Canvas |
| Cut | `Ctrl+X` | Canvas |
| Paste | `Ctrl+V` | Canvas |
| Select All | `Ctrl+A` | Canvas |
| Fold/Unfold | `Ctrl+/` | Canvas (topic selected) |
| Zoom In | `Ctrl+=` | Canvas |
| Zoom Out | `Ctrl+-` | Canvas |
| Zoom to Fit | `Ctrl+Shift+F` | Canvas |
| Zoom 100% | `Ctrl+0` | Canvas |
| Find | `Ctrl+F` | Global |
| Find & Replace | `Ctrl+H` | Global |
| Add Relationship | `Ctrl+Shift+R` | Canvas |
| Add Boundary | `Ctrl+Shift+B` | Canvas (multiple topics selected) |
| Add Notes | `F4` | Canvas (topic selected) |
| Navigate Up | `Up Arrow` | Canvas |
| Navigate Down | `Down Arrow` | Canvas |
| Navigate Left | `Left Arrow` | Canvas |
| Navigate Right | `Right Arrow` | Canvas |
| Center Selected | `F5` | Canvas |
| Presentation Mode | `F6` | Global |
| Export | `Ctrl+E` | Global |
| Print | `Ctrl+P` | Global |
| Preferences | `Ctrl+,` | Global |
| Close Tab | `Ctrl+W` | Global |
| Next Tab | `Ctrl+Tab` | Global |
| Previous Tab | `Ctrl+Shift+Tab` | Global |

---

## 5. Document Cross-References

| Topic | Document |
|-------|----------|
| Architecture decisions explaining these schemas | [blueprint.md](blueprint.md) |
| Project scope and feature list | [constitution.md](constitution.md) |
| Build order for implementing these models | [implementation-guide.md](implementation-guide.md) |
| Source file locations for these schemas | [skeleton.md](skeleton.md) |
