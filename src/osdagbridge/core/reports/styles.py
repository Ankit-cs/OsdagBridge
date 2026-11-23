"""Centralized Styling & Theming System for OsdagBridge PDF Reports.

This module acts as the Single Source of Truth (SSOT) for:
- Color palette (Osdag brand colors, status indicators, chart themes)
- Document geometry and spacing (margins, header/footer spacing, footskip)
- Typography and line heights
- Table formatting (padding, rules, LongTable headers and continuation bars)
- Chart visual styles (Matplotlib palettes, DPI, dimensions)
"""

from dataclasses import dataclass
from typing import List, Optional, Tuple

# ==============================================================================
# 1. COLOR PALETTE
# ==============================================================================
# Brand & Accent Colors
COLOR_PRIMARY_HEX = "#91B014"         # Osdag Green
COLOR_PRIMARY_LATEX = "91B014"
COLOR_PRIMARY_NAME = "osdagGreen"

COLOR_DARK_TEXT_HEX = "#222222"
COLOR_MUTED_TEXT_HEX = "#555555"
COLOR_LIGHT_BG_HEX = "#F8F9FA"
COLOR_BORDER_HEX = "#D0D5DD"

# Status Colors
COLOR_PASS_HEX = "#2E7D32"           # Forest Green for UR <= 1.0
COLOR_FAIL_HEX = "#D32F2F"           # Deep Red for UR > 1.0
COLOR_ALERT_HEX = "#F57C00"          # Amber/Orange for warnings
COLOR_THRESHOLD_HEX = "#C62828"      # Red dashed reference line at UR = 1.0

# Secondary Chart Colors
CHART_BAR_COLORS = [
    "#91B014",  # Osdag Green
    "#2E7D32",  # Dark Green
    "#1976D2",  # Tech Blue
    "#0288D1",  # Sky Blue
    "#7B1FA2",  # Purple
    "#E65100",  # Dark Orange
]

# ==============================================================================
# 2. DOCUMENT GEOMETRY & LAYOUT
# ==============================================================================
# Page Geometry - Increased bottom margin and footskip to prevent footer bleed (Issue #2)
GEOMETRY_TOP = "1.0in"
GEOMETRY_BOTTOM = "1.25in"            # Generous clearance before footer line
GEOMETRY_LEFT = "1.0in"
GEOMETRY_RIGHT = "1.0in"
GEOMETRY_HEADHEIGHT = "18pt"
GEOMETRY_HEADSEP = "12pt"
GEOMETRY_FOOTSKIP = "36pt"            # Prevents last table row colliding with footer rule

# Document Class & Typography
DOCUMENT_CLASS = "report"
BASE_FONT_SIZE = "12pt"
LINE_STRETCH = 1.15

# ==============================================================================
# 3. TABLE FORMATTING & PADDING
# ==============================================================================
TABLE_TABCOLSEP = "6pt"              # Horizontal cell padding
TABLE_ARRAYSTRETCH = 1.15            # Vertical row height scaling
TABLE_EXTRAROWHEIGHT = "0.8pt"       # Minimum extra row spacing
TABLE_RULE_WIDTH = "0.5pt"           # Outline thickness
TABLE_LT_PRE = "0pt"                 # Pre-skip before longtable
TABLE_LT_POST = "6pt"                # Post-skip after longtable
NEEDSPACE_TABLE = "5\\baselineskip"  # Space required before breaking a table to next page

# ==============================================================================
# 4. CHART & VISUALIZATION CONFIGURATION
# ==============================================================================
CHART_DPI = 300
CHART_FIGSIZE_WIDE = (7.5, 3.8)      # Width x Height in inches for report
CHART_FIGSIZE_SQUARE = (6.0, 4.0)
CHART_FONT_FAMILY = "sans-serif"
CHART_TITLE_FONTSIZE = 11
CHART_LABEL_FONTSIZE = 10
CHART_TICK_FONTSIZE = 9


# ==============================================================================
# 5. LATEX STYLE SNIPPETS & HELPERS
# ==============================================================================

def get_preamble_styles() -> str:
    """Returns the unified LaTeX style definitions to be injected into the preamble."""
    return f"""
% --- Centralized OsdagBridge Style Definitions (from styles.py) ---
\\usepackage[a4paper,
  top={GEOMETRY_TOP},
  bottom={GEOMETRY_BOTTOM},
  left={GEOMETRY_LEFT},
  right={GEOMETRY_RIGHT},
  headheight={GEOMETRY_HEADHEIGHT},
  headsep={GEOMETRY_HEADSEP},
  footskip={GEOMETRY_FOOTSKIP}
]{{geometry}}

\\definecolor{{{COLOR_PRIMARY_NAME}}}{{HTML}}{{{COLOR_PRIMARY_LATEX}}}
\\definecolor{{passGreen}}{{HTML}}{{2E7D32}}
\\definecolor{{failRed}}{{HTML}}{{D32F2F}}
\\definecolor{{tableHeaderBg}}{{HTML}}{{F4F6F8}}

\\setlength{{\\tabcolsep}}{{{TABLE_TABCOLSEP}}}
\\renewcommand{{\\arraystretch}}{{{TABLE_ARRAYSTRETCH}}}
\\setlength{{\\extrarowheight}}{{{TABLE_EXTRAROWHEIGHT}}}
\\setlength{{\\arrayrulewidth}}{{{TABLE_RULE_WIDTH}}}
\\setlength{{\\LTpre}}{{{TABLE_LT_PRE}}}
\\setlength{{\\LTpost}}{{{TABLE_LT_POST}}}
\\setlength{{\\LTleft}}{{\\fill}}
\\setlength{{\\LTright}}{{\\fill}}

% Buffer control: prevent table header/first rows from breaking immediately above footer
\\BeforeBeginEnvironment{{table}}{{\\needspace{{{NEEDSPACE_TABLE}}}}}
\\BeforeBeginEnvironment{{longtable}}{{\\needspace{{{NEEDSPACE_TABLE}}}}}
"""


def format_longtable_header(
    col_headers: List[str],
    caption: str = "",
    label: Optional[str] = None,
    table_num_name: str = "Table",
) -> str:
    """
    Generates a full, standardized repeating header for PyLaTeX / LaTeX LongTable.
    
    Includes:
    - Initial caption and column headers (\\endfirsthead)
    - Repeated column headers on every page break with continuation label (\\endhead)
    - 'Continued on next page...' footer note on broken pages (\\endfoot)
    - Clean closing line on final page (\\endlastfoot)
    
    This guarantees zero loss of column context across page breaks (Scope of Work #1).
    """
    ncols = len(col_headers)
    caption_tex = ""
    if caption:
        lbl = f"\\label{{{label}}}" if label else ""
        caption_tex = f"\\caption{{\\textbf{{{caption}}}}}{lbl} \\\\\n"

    header_cells = " & ".join([f"\\textbf{{{h}}}" for h in col_headers])
    
    return f"""{caption_tex}\\hline
{header_cells} \\\\[4pt]
\\hline
\\endfirsthead

\\hline
\\multicolumn{{{ncols}}}{{c}}{{\\small\\textit{{{caption} (continued)}}}} \\\\[4pt]
\\hline
{header_cells} \\\\[4pt]
\\hline
\\endhead

\\hline
\\multicolumn{{{ncols}}}{{r}}{{\\footnotesize\\textit{{Continued on next page\\dots}}}} \\\\
\\endfoot

\\hline
\\endlastfoot
"""


def format_ur_cell(value: float, threshold: float = 1.0) -> str:
    """Format Utilization Ratio with appropriate status color highlighting."""
    try:
        val = float(value)
    except (TypeError, ValueError):
        return str(value)
    
    s = f"{val:.3f}"
    if val > threshold:
        return f"\\textcolor{{failRed}}{{\\textbf{{{s}}}}} \\textcolor{{failRed}}{{$\\times$}}"
    return f"\\textcolor{{passGreen}}{{{s}}} \\textcolor{{passGreen}}{{\\checkmark}}"
