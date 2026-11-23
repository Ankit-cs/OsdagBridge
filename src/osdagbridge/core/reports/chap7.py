# =============================================================================
# Chapter 7: Material Take-off & Quantity Summary
# Refactored for:
# - Scope Item 1: Repeating LongTable headers across page breaks
# - Scope Item 5: Programmatic Material Quantity Bar Charts
#   * Structural Steel tonnage (Girders, Cross Bracing, End Diaphragms)
#   * Concrete volume (m³) vs. Reinforcement Steel weight (MT)
# =============================================================================

import os
from typing import Optional, Dict, Any

from osdagbridge.core.reports.styles import format_longtable_header
from osdagbridge.core.reports.chart_utils import generate_material_quantity_charts


def ch7_quantities(input_dict: Dict[str, Any], images_dir: Optional[str] = None) -> str:
    # ── Scope Item 5: Generate Quantity Bar Charts ──
    charts_tex = ""
    if images_dir:
        steel_chart, concrete_chart = generate_material_quantity_charts(input_dict, images_dir)
        
        figures_parts = []
        if steel_chart and os.path.exists(steel_chart):
            p1 = steel_chart.replace('\\', '/')
            figures_parts.append(
                r"\begin{figure}[H]" + "\n"
                r"\centering" + "\n"
                r"\includegraphics[width=0.88\textwidth]{" + p1 + r"}" + "\n"
                r"\caption*{\textbf{Figure 7.1: Structural Steel Tonnage Breakdown by Element (Metric Tonnes)}}" + "\n"
                r"\end{figure}"
            )
            
        if concrete_chart and os.path.exists(concrete_chart):
            p2 = concrete_chart.replace('\\', '/')
            figures_parts.append(
                r"\begin{figure}[H]" + "\n"
                r"\centering" + "\n"
                r"\includegraphics[width=0.88\textwidth]{" + p2 + r"}" + "\n"
                r"\caption*{\textbf{Figure 7.2: Concrete Volume (m\textsuperscript{3}) vs. Rebar Weight (MT) Summary}}" + "\n"
                r"\end{figure}"
            )
            
        if figures_parts:
            charts_tex = "\n\\vspace{0.5em}\n" + "\n\\vspace{1em}\n".join(figures_parts) + "\n\\vspace{1.5em}\n"

    # ── Scope Item 1: Repeating Table Header for Table 7.1 ──
    col_headers = [
        "S.N.",
        "Item Description",
        "Volume Formula",
        "Qty",
        "Total Vol. (m\\textsuperscript{3})",
        "Unit Wt. (MT)",
        "Total Wt. (MT)"
    ]
    hdr_t71 = format_longtable_header(col_headers, caption="Bill of Materials (Steel, Concrete, and Reinforcement Quantities)")

    return r"""
\chapter{Material Take-off \& Quantity Summary}
\label{ch:material-takeoff}

This chapter details the material consumption, volume estimates, and structural component weights computed for the bridge structure. All steel tonnages are based on structural steel density of 7850~kg/m\textsuperscript{3}, and concrete volumes correspond to grade M40 specified in the structural parameters.

""" + charts_tex + r"""

\noindent\textbf{Detailed Bill of Quantities}

\begingroup
\setlength{\tabcolsep}{3.5pt}
\begin{longtable}{|C{1.0cm}|L{3.8cm}|C{2.6cm}|C{1.8cm}|C{1.8cm}|C{1.8cm}|C{1.8cm}|}
""" + hdr_t71 + r"""
1 & Structural Steel (IS 2062) for Girders & """ + str(input_dict.get("steel_girders_vol_formula", "N.A.")) + r""" & """ + str(input_dict.get("steel_girders_qty", "N.A.")) + r""" & """ + str(input_dict.get("steel_girders_vol_total", "N.A.")) + r""" & """ + str(input_dict.get("steel_girders_wt_single", "N.A.")) + r""" & """ + str(input_dict.get("steel_girders_wt_total", "N.A.")) + r""" \\
\hline
2(a) & Cross Bracing - Top Chord & """ + str(input_dict.get("bracing_top_vol_formula", "N.A.")) + r""" & """ + str(input_dict.get("bracing_top_qty", "N.A.")) + r""" & """ + str(input_dict.get("bracing_top_vol_total", "N.A.")) + r""" & """ + str(input_dict.get("bracing_top_wt_single", "N.A.")) + r""" & """ + str(input_dict.get("bracing_top_wt_total", "N.A.")) + r""" \\
\hline
2(b) & Cross Bracing - Bottom Chord & """ + str(input_dict.get("bracing_bot_vol_formula", "N.A.")) + r""" & """ + str(input_dict.get("bracing_bot_qty", "N.A.")) + r""" & """ + str(input_dict.get("bracing_bot_vol_total", "N.A.")) + r""" & """ + str(input_dict.get("bracing_bot_wt_single", "N.A.")) + r""" & """ + str(input_dict.get("bracing_bot_wt_total", "N.A.")) + r""" \\
\hline
2(c) & Cross Bracing - Diagonal Chord & """ + str(input_dict.get("bracing_diag_vol_formula", "N.A.")) + r""" & """ + str(input_dict.get("bracing_diag_qty", "N.A.")) + r""" & """ + str(input_dict.get("bracing_diag_vol_total", "N.A.")) + r""" & """ + str(input_dict.get("bracing_diag_wt_single", "N.A.")) + r""" & """ + str(input_dict.get("bracing_diag_wt_total", "N.A.")) + r""" \\
\hline
3 & Concrete (M40) for Deck Slab & """ + str(input_dict.get("concrete_deck_vol_formula", "N.A.")) + r""" & """ + str(input_dict.get("concrete_deck_qty", "N.A.")) + r""" & """ + str(input_dict.get("concrete_deck_vol_total", "N.A.")) + r""" & """ + str(input_dict.get("concrete_deck_wt_single", "N.A.")) + r""" & """ + str(input_dict.get("concrete_deck_wt_total", "N.A.")) + r""" \\
\hline
4 & Reinforcement Steel (Fe 500) & """ + str(input_dict.get("rebar_deck_vol_formula", "N.A.")) + r""" & """ + str(input_dict.get("rebar_deck_qty", "N.A.")) + r""" & """ + str(input_dict.get("rebar_deck_vol_total", "N.A.")) + r""" & """ + str(input_dict.get("rebar_deck_wt_single", "N.A.")) + r""" & """ + str(input_dict.get("rebar_deck_wt_total", "N.A.")) + r""" \\
\hline
5 & Shear Stud Connectors & """ + str(input_dict.get("shear_studs_vol_formula", "N.A.")) + r""" & """ + str(input_dict.get("shear_studs_qty", "N.A.")) + r""" & """ + str(input_dict.get("shear_studs_vol_total", "N.A.")) + r""" & """ + str(input_dict.get("shear_studs_wt_single", "N.A.")) + r""" & """ + str(input_dict.get("shear_studs_wt_total", "N.A.")) + r""" \\
\hline
6 & Crash Barrier & """ + str(input_dict.get("crash_barrier_vol_formula", "N.A.")) + r""" & """ + str(input_dict.get("crash_barrier_qty", "N.A.")) + r""" & """ + str(input_dict.get("crash_barrier_vol_total", "N.A.")) + r""" & """ + str(input_dict.get("crash_barrier_wt_single", "N.A.")) + r""" & """ + str(input_dict.get("crash_barrier_wt_total", "N.A.")) + r""" \\
\hline
\end{longtable}
\endgroup
"""
