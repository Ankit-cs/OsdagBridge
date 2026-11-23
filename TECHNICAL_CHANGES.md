# OsdagBridge LaTeX Report Generator Refactoring — Technical Changes Document

## 1. Executive Summary
This document provides a detailed technical overview of the refactoring and enhancements applied to the OsdagBridge design report generation module. The changes address multi-page table formatting, vertical geometry and footer margin collisions, load table separation, dynamic chart visualizations, and establish a centralized styling architecture.

---

## 2. Key Files Altered & Created

| File | Status | Description |
|---|---|---|
| `src/osdagbridge/core/reports/styles.py` | **New** | Centralized styling architecture (Single Source of Truth) defining brand colors, document geometry, table rules, and LongTable header helpers. |
| `src/osdagbridge/core/reports/chart_utils.py` | **New** | Programmatic matplotlib chart generator for Section 5.5 (Utilization Ratios) and Chapter 7 (Material Quantities). |
| `src/osdagbridge/core/reports/report_generator.py` | **Modified** | Integrated centralized styles into the LaTeX preamble, fixed footskip/margin geometries, and wired temporary image asset pipelines. |
| `src/osdagbridge/core/reports/chap2.py` | **Modified** | Converted input parameter tables to repeating `LongTable` environments with page continuation footers. |
| `src/osdagbridge/core/reports/chap3.py` | **Modified** | Separated Vehicle Live Loads and Footpath Live Loads into distinct tables with unit columns and dynamic UI vehicle mappings. |
| `src/osdagbridge/core/reports/chap4.py` | **Modified** | Applied repeating headers to analysis reaction and deflection tables. |
| `src/osdagbridge/core/reports/chap5.py` | **Modified** | Extracted governing component URs, dynamically generated Figure 5.1, and embedded repeating headers for Table 5.22. |
| `src/osdagbridge/core/reports/chap7.py` | **Modified** | Dynamically generated Figures 7.1 and 7.2 (steel tonnage & concrete vs rebar), and added repeating table headers to Table 7.1. |

---

## 3. Detailed Scope of Work & Implementation Details

### 3.1 Centralized Formatting & Style System (`styles.py`)
- **Problem:** Colors, padding, table styles, and margins were scattered and hardcoded across individual chapter files.
- **Solution:** Created `styles.py` as the single source of truth.
  - **Brand & Semantic Colors:** `COLOR_PRIMARY_HEX` (`#91B014` - Osdag Green), `COLOR_PASS_HEX` (`#2E7D32`), `COLOR_FAIL_HEX` (`#D32F2F`), and `COLOR_THRESHOLD_HEX` (`#C62828`).
  - **Document Geometry:** Standardized `top=1.0in`, `bottom=1.25in`, `left=1.0in`, `right=1.0in`, `headheight=18pt`, `footskip=36pt`.
  - **Table Layout:** `tabcolsep=6pt`, `arraystretch=1.15`, `extrarowheight=0.8pt`, `arrayrulewidth=0.5pt`.
  - **Buffer Controls:** Configured `\BeforeBeginEnvironment{longtable}{\needspace{5\baselineskip}}` to eliminate orphaned headers.

### 3.2 Repeated Table Headers Across Page Breaks
- **Problem:** Multi-page tables split across pages without repeating column headers, confusing readers.
- **Solution:** Implemented `format_longtable_header()` in `styles.py` and adopted across all chapter tables:
  - `\endfirsthead`: Initial header with table caption.
  - `\endhead`: Repeated column headers on every subsequent page with continuation title (`[Table Name] (continued)`).
  - `\endfoot`: Bottom rule with *"Continued on next page..."* notation.
  - `\endlastfoot`: Clean closing line on final page.

### 3.3 Layout, Footer Overlap, and Vertical Spacing Fixes
- **Problem:** Content bled directly into the footer margin (e.g., text/rows on Page 30 overlapping green footer rules).
- **Solution:** 
  - Increased bottom page margin to `1.25in` and enlarged `footskip` to `36pt`.
  - Adjusted table padding and vertical cell spacing to prevent overlap with standard header/footer boxes.

### 3.4 Load & Geometry Table Refactoring (Chapter 3)
- **Problem:** Vehicle live loads and footway loads were merged and lacked clear unit structures.
- **Solution:** 
  - **Table 3.3 (Vehicle Live Load Parameters):** Separated into a dedicated multi-column table displaying Vehicle Class (dynamically filtered by user selection in the UI), Standard Reference (IRC 6), Impact Factor ($1+i$), Braking Load ($kN$), and Centrifugal Force ($kN$).
  - **Table 3.4 (Footpath Live Load):** Separated into an independent table detailing loading mode (IRC 6 Cl. 206 vs Custom), pedestrian pressure intensity ($kN/m^2$), and linear load parameters.

### 3.5 Utilization Ratio (UR) Summary Visualizations (Section 5.5)
- **Requirement:** Dynamic bar chart for $\text{UR} = \text{Demand} / \text{Capacity}$ across primary bridge components.
- **Implementation:**
  - Evaluated governing URs for **Steel Plate Girders**, **Concrete Deck Slab**, **Cross Bracing**, and **End Diaphragms**.
  - Programmatically generated a high-DPI bar chart with a distinct **red dashed threshold line at $\text{UR} = 1.0$**.
  - Color-coded bars (Green for $\le 1.0$, Red for $> 1.0$) with explicit value and status annotations.
  - Dynamically embedded as **Figure 5.1** into Section 5.5 preceding Table 5.22.

### 3.6 Material Quantity Bar Charts (Chapter 7)
- **Requirement:** Visual summaries of BOM quantities.
- **Implementation:**
  - **Figure 7.1:** Structural steel tonnage breakdown across Girders, Cross Bracing, and End Diaphragms in MT.
  - **Figure 7.2:** Concrete volume ($m^3$) vs. Reinforcement steel weight (MT).
  - Both figures auto-saved to temporary image assets and cleanly embedded into Chapter 7.

---

## 4. Verification & Testing
- Successfully compiled and verified against the OsdagBridge Python 3.11 environment (`osdagbridge-env`).
- GUI desktop application verified with 3D OpenCASCADE/OpenGL viewport rendering.
