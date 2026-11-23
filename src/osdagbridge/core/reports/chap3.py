# =============================================================================
# Chapter 3: Loads and Load Combinations
# Refactored for:
# - Scope Item 1: Repeating LongTable headers across page breaks
# - Scope Item 2: Spacing & footer collision prevention
# - Scope Item 3: Separated Vehicle Live Loads & Footpath Live Loads tables
# =============================================================================

from osdagbridge.core.utils.common import (
    KEY_CB_LOAD,
    KEY_LL_CUSTOM_VEHICLES,
    KEY_LL_FOOTPATH_PRESSURE_MODE,
    KEY_LL_FOOTPATH_PRESSURE_VALUE,
    KEY_LL_IRC_70R_BOGIE,
    KEY_LL_IRC_70R_TRACKED,
    KEY_LL_IRC_70R_WHEELED,
    KEY_LL_IRC_AA_TRACKED,
    KEY_LL_IRC_AA_WHEELED,
    KEY_LL_IRC_CLASS_A,
    KEY_LL_IRC_CLASS_FATIGUE,
    KEY_LL_IRC_CLASS_SV,
    KEY_MATERIAL_DECK_DENSITY,
    KEY_MATERIAL_GIRDER_DENSITY,
    KEY_PL_SELF_WEIGHT_FACTOR,
    KEY_RL_LOAD_VALUE,
    KEY_SL_DAMPING,
    KEY_SL_DEAD_LOAD_MODE,
    KEY_SL_DEAD_LOAD_VALUE,
    KEY_SL_HORIZONTAL_COEFF,
    KEY_SL_IMPORTANCE_FACTOR,
    KEY_SL_LIVE_LOAD_MODE,
    KEY_SL_LIVE_LOAD_VALUE,
    KEY_SL_SEISMIC_ZONE,
    KEY_SL_SOIL_TYPE,
    KEY_SL_SPECTRAL_COEFF,
    KEY_SL_TIME_PERIOD,
    KEY_SL_VERTICAL_COEFF,
    KEY_SL_ZONE_FACTOR,
    KEY_SPAN,
    KEY_TL_BRIDGE_TEMP_MAX,
    KEY_TL_BRIDGE_TEMP_MIN,
    KEY_TL_HIGHEST_MAX_TEMP,
    KEY_TL_LOWEST_MIN_TEMP,
    KEY_TL_TEMP_FALL,
    KEY_TL_TEMP_RISE,
    KEY_WC_LD_LANE_TABLE_COUNT,
    KEY_WC_MATERIAL,
    KEY_WC_THICKNESS,
    KEY_WL_AVG_EXPOSED_HEIGHT,
    KEY_WL_BASIC_WIND_SPEED,
    KEY_WL_HOURLY_MEAN_WIND,
    KEY_WL_HOURLY_WIND_PRESSURE,
    KEY_WL_LONGITUDINAL_WIND_FORCE,
    KEY_WL_TERRAIN_TYPE,
    KEY_WL_TRANSVERSE_WIND_FORCE,
    KEY_WL_VERTICAL_WIND_FORCE
)

from osdagbridge.core.reports.report_utils import _tex, _render_value
from osdagbridge.core.reports.styles import format_longtable_header


def ch3_loads(input_dict):
    from osdagbridge.core.utils.codes.irc6_2017 import IRC6_2017

    span = input_dict.get(KEY_SPAN)
    span_m = 0.0
    if span not in (None, ""):
        try:
            span_m = float(span)
        except Exception:
            span_m = 0.0

    lanes = input_dict.get(KEY_WC_LD_LANE_TABLE_COUNT)
    braking_force_str = "N/A"
    if lanes not in (None, ""):
        try:
            lanes_int = int(lanes)
            braking_force_t = IRC6_2017.cl_211_2_braking_force(lanes_int)
            braking_force_kN = braking_force_t * 9.81
            braking_force_str = f"{braking_force_kN:.2f} kN"
        except Exception:
            braking_force_str = "N/A"

    # --- Scope Item 3: Build Structured Vehicle Live Loads Table Rows ---
    vehicle_rows = []
    
    if input_dict.get(KEY_LL_IRC_CLASS_A):
        im_a = f"{1.0 + IRC6_2017.cl_208_2_impact_factor(span_m):.3f}" if span_m > 0 else "1.150"
        vehicle_rows.append(("IRC Class A", "IRC 6 Cl. 204.1", im_a, braking_force_str, "As per Cl. 212"))
    
    if input_dict.get(KEY_LL_IRC_70R_WHEELED):
        im_70rw = f"{1.0 + IRC6_2017.cl_208_3_impact_factor(span_m):.3f}" if span_m > 0 else "1.100"
        vehicle_rows.append(("IRC Class 70R (Wheeled)", "IRC 6 Cl. 204.1", im_70rw, braking_force_str, "As per Cl. 212"))

    if input_dict.get(KEY_LL_IRC_70R_TRACKED):
        im_70rt = f"{1.0 + IRC6_2017.cl_208_3_impact_factor(span_m):.3f}" if span_m > 0 else "1.100"
        vehicle_rows.append(("IRC Class 70R (Tracked)", "IRC 6 Cl. 204.1", im_70rt, braking_force_str, "N/A (Tracked)"))

    if input_dict.get(KEY_LL_IRC_AA_WHEELED):
        im_aaw = f"{1.0 + IRC6_2017.cl_208_3_impact_factor(span_m):.3f}" if span_m > 0 else "1.100"
        vehicle_rows.append(("IRC Class AA (Wheeled)", "IRC 6 Cl. 204.1", im_aaw, braking_force_str, "As per Cl. 212"))

    if input_dict.get(KEY_LL_IRC_AA_TRACKED):
        im_aat = f"{1.0 + IRC6_2017.cl_208_3_impact_factor(span_m):.3f}" if span_m > 0 else "1.100"
        vehicle_rows.append(("IRC Class AA (Tracked)", "IRC 6 Cl. 204.1", im_aat, braking_force_str, "N/A (Tracked)"))

    if input_dict.get(KEY_LL_IRC_CLASS_SV):
        vehicle_rows.append(("IRC Class SV", "IRC 6 Annexure B", "1.000 (No Impact)", braking_force_str, "N/A"))

    if input_dict.get(KEY_LL_IRC_70R_BOGIE):
        im_bogie = f"{1.0 + IRC6_2017.cl_208_3_impact_factor(span_m):.3f}" if span_m > 0 else "1.100"
        vehicle_rows.append(("IRC Class 70R (Bogie)", "IRC 6 Cl. 204.1", im_bogie, braking_force_str, "As per Cl. 212"))

    if input_dict.get(KEY_LL_IRC_CLASS_FATIGUE):
        vehicle_rows.append(("IRC Fatigue Vehicle", "IRC 6 Cl. 216", "1.000", "N/A", "N/A"))

    custom = input_dict.get(KEY_LL_CUSTOM_VEHICLES)
    if custom and isinstance(custom, list):
        for c in custom:
            c_name = c.get('name') if isinstance(c, dict) else str(c)
            vehicle_rows.append((c_name, "User Defined", "1.000", braking_force_str, "N/A"))

    # Fallback to standard baseline if no vehicle selected
    if not vehicle_rows:
        im_a = f"{1.0 + IRC6_2017.cl_208_2_impact_factor(span_m):.3f}" if span_m > 0 else "1.150"
        im_70r = f"{1.0 + IRC6_2017.cl_208_3_impact_factor(span_m):.3f}" if span_m > 0 else "1.100"
        vehicle_rows = [
            ("IRC Class A", "IRC 6 Cl. 204.1", im_a, braking_force_str, "As per Cl. 212"),
            ("IRC Class 70R (Wheeled)", "IRC 6 Cl. 204.1", im_70r, braking_force_str, "As per Cl. 212"),
        ]

    veh_table_lines = []
    for vname, code_ref, imp_fact, brk_ld, cent_fc in vehicle_rows:
        veh_table_lines.append(
            f"\\textnormal{{{_tex(vname)}}} & \\textnormal{{{_tex(code_ref)}}} & {imp_fact} & {_tex(brk_ld)} & \\textnormal{{{_tex(cent_fc)}}} \\\\[6pt]\n\\hline"
        )
    veh_table_rows_str = "\n".join(veh_table_lines)

    # --- Footpath Live Load values ---
    fp_mode = input_dict.get(KEY_LL_FOOTPATH_PRESSURE_MODE, "As per IRC 6")
    fp_value = input_dict.get(KEY_LL_FOOTPATH_PRESSURE_VALUE, "")
    if str(fp_mode).strip().lower() in ("as per irc 6", "as per irc6", "automatic"):
        try:
            fp_intensity = f"{IRC6_2017.cl_206_1_footway_load():.2f} kN/m\\textsuperscript{{2}}"
        except Exception:
            fp_intensity = "4.00 kN/m\\textsuperscript{2}"
    elif fp_value not in (None, ""):
        fp_intensity = f"{fp_value} kN/m\\textsuperscript{{2}}"
    else:
        fp_intensity = "4.00 kN/m\\textsuperscript{2} (IRC 6 Cl. 206.1)"

    # Wind Load
    vz_val = input_dict.get(KEY_WL_HOURLY_MEAN_WIND)
    pz_val = input_dict.get(KEY_WL_HOURLY_WIND_PRESSURE)
    if not vz_val or not pz_val:
        try:
            _vb = input_dict.get(KEY_WL_BASIC_WIND_SPEED) or input_dict.get('wind_speed')
            _h = input_dict.get(KEY_WL_AVG_EXPOSED_HEIGHT)
            _ter = {
                "Plain Terrain": "plain",
                "Terrain with Obstructions": "obstructed",
            }.get(str(input_dict.get(KEY_WL_TERRAIN_TYPE, "")).strip(), "plain")
            _res = IRC6_2017.table_12(float(_h), _ter, float(_vb))
            if not vz_val:
                vz_val = _res.get("Vz")
            if not pz_val:
                pz_val = _res.get("Pz")
        except Exception:
            pass

    # Seismic Load
    sl_zone_factor = input_dict.get(KEY_SL_ZONE_FACTOR)
    sl_spectral = input_dict.get(KEY_SL_SPECTRAL_COEFF)
    sl_ah = input_dict.get(KEY_SL_HORIZONTAL_COEFF)
    sl_av = input_dict.get(KEY_SL_VERTICAL_COEFF)
    if not sl_ah or not sl_zone_factor:
        try:
            _zone = input_dict.get(KEY_SL_SEISMIC_ZONE) or input_dict.get('seismic_zone')
            _zmap = {"1": "I", "2": "II", "3": "III", "4": "IV", "5": "V"}
            _z = str(_zone).strip().upper()
            if _z.isdigit():
                _z = _zmap.get(_z)
            _smap = {"Type I – Rocky or Hard": 1, "Type II – Medium Soil": 2, "Type III – Soft Soil": 3}
            _st = _smap.get(str(input_dict.get(KEY_SL_SOIL_TYPE, "")), 1)
            _tp = input_dict.get(KEY_SL_TIME_PERIOD)
            _damp = input_dict.get(KEY_SL_DAMPING) or "5"
            _dl_v = input_dict.get(KEY_SL_DEAD_LOAD_VALUE)
            _ll_v = input_dict.get(KEY_SL_LIVE_LOAD_VALUE)
            _dead = float(_dl_v) if str(input_dict.get(KEY_SL_DEAD_LOAD_MODE, "")) == "Custom" and _dl_v else 0.0
            _live = float(_ll_v) if str(input_dict.get(KEY_SL_LIVE_LOAD_MODE, "")) == "Custom" and _ll_v else 0.0
            _res = IRC6_2017.cl_218_5_1(
                zone=f"Zone {_z}", soil_type=_st, dead_load_kN=_dead,
                live_load_kN=_live, period_T=float(_tp) if _tp else None,
                damping_percent=float(_damp)
            )
            if not sl_zone_factor:
                sl_zone_factor = _res.get("Z")
            if not sl_spectral:
                sl_spectral = _res.get("Sa_g_adjusted")
            if not sl_ah:
                sl_ah = _res.get("Ah")
            if not sl_av:
                sl_av = round(_res.get("Ah", 0) * 2 / 3, 4)
        except Exception:
            pass

    # Load Combinations
    _LOAD_LABEL_MAP = {
        'dead_load': 'DL',
        'surfacing': 'SIDL',
        'live_load': 'LL',
        'wind_load': 'WL',
        'thermal_load': 'TL',
        'vehicle_collision': 'VC',
        'barge_impact': 'BI',
        'floating_bodies': 'FB',
        'seismic': 'EQ',
    }

    def _fmt_factors(factors):
        parts = []
        for load, val in factors.items():
            label = _LOAD_LABEL_MAP.get(load, load.upper())
            if isinstance(val, dict):
                add = val.get('adding')
                rel = val.get('relieving')
                add_s = f"{add:.2f}" if add is not None else '--'
                rel_s = f"{rel:.2f}" if rel is not None else '--'
                parts.append(f"{label}({add_s}/{rel_s})")
            else:
                if val is None:
                    continue
                parts.append(f"{label}({val:.2f})")
        return ' + '.join(parts)

    uls_combos = IRC6_2017.uls_load_combinations()
    sls_combos = IRC6_2017.sls_load_combinations()
    lc_rows = []
    for i, combo in enumerate(uls_combos, start=1):
        cases = _fmt_factors(combo['factors'])
        lc_rows.append(f"ULS-{i:02d} & {cases} \\\\[6pt]\n\\hline")
    for i, combo in enumerate(sls_combos, start=1):
        cases = _fmt_factors(combo['factors'])
        lc_rows.append(f"SLS-{i:02d} & {cases} \\\\[6pt]\n\\hline")

    lc_rows_str = "\n".join(lc_rows)

    # Standard repeating table headers
    hdr_t31 = format_longtable_header(["Parameter", "Value"], caption="Dead Load -- Self Weight")
    hdr_t32 = format_longtable_header(["Parameter", "Value"], caption="Dead Load for Surfacing (DW)")
    hdr_t33 = format_longtable_header(
        ["Vehicle Class", "Standard Reference", "Impact Factor (1+i)", "Braking Load", "Centrifugal Force"],
        caption="Vehicle Live Load Parameters (per IRC 6:2017)"
    )
    hdr_t34 = format_longtable_header(["Footpath Load Parameter", "Value / Design Limit"], caption="Footpath Live Load (per IRC 6 Cl. 206)")
    hdr_t35 = format_longtable_header(["Parameter", "Value"], caption="Wind Load (WL) --- per IRC 6")
    hdr_t36 = format_longtable_header(["Parameter", "Value"], caption="Earthquake Load (EL) --- per IRC 6")
    hdr_t37 = format_longtable_header(["Parameter", "Value"], caption="Temperature Load (TL) --- per IRC 6")
    hdr_t38 = format_longtable_header(["Combination ID", "Load Cases & Partial Safety Factors"], caption="Design Load Combinations (IRC 6 Table B.1-B.4)")

    return r"""
\chapter{Loads and Load Combinations}

This section summarizes all permanent, live, environmental, and accidental loads applied to the bridge structure, along with the ultimate and serviceability limit state load combinations considered for design.

\vspace{1em}
\begin{longtable}{|L{5.5cm}|p{10.0cm}|}
""" + hdr_t31 + r"""
\textnormal{Steel Self-Weight Applied} & """ + (_render_value(input_dict, KEY_MATERIAL_GIRDER_DENSITY, ' kN/m\\textsuperscript{3}')) + r""" \\[6pt]
\hline
\textnormal{Concrete Deck Weight} & """ + (_render_value(input_dict, KEY_MATERIAL_DECK_DENSITY, ' kN/m\\textsuperscript{3}')) + r""" \\[6pt]
\hline
\textnormal{Self-Weight Factor} & """ + (_render_value(input_dict, KEY_PL_SELF_WEIGHT_FACTOR)) + r""" \\[6pt]
\hline
\end{longtable}

\vspace{1em}
\begin{longtable}{|L{5.5cm}|p{10.0cm}|}
""" + hdr_t32 + r"""
\textnormal{Wearing Course Load} & """ + (_render_value(input_dict, KEY_WC_MATERIAL)) + r""" x """ + (_render_value(input_dict, KEY_WC_THICKNESS)) + r""" \\[6pt]
\hline
\textnormal{Additional SIDL (Crash Barrier)} & """ + (_render_value(input_dict, KEY_CB_LOAD)) + r""" kN/m per barrier \\[6pt]
\hline
\textnormal{Railing Load} & """ + (_render_value(input_dict, KEY_RL_LOAD_VALUE)) + r""" kN/m\sdstar{} \\[6pt]
\hline
\end{longtable}

\vspace{1em}
% --- Refactored Vehicle Live Loads Table (Scope Item 3) ---
\begin{longtable}{|L{3.6cm}|L{3.4cm}|C{2.4cm}|C{2.6cm}|L{3.5cm}|}
""" + hdr_t33 + r"""
""" + veh_table_rows_str + r"""
\end{longtable}

\vspace{1em}
% --- Distinct Footpath Live Loads Table (Scope Item 3) ---
\begin{longtable}{|L{5.5cm}|p{10.0cm}|}
""" + hdr_t34 + r"""
\textnormal{Footway Loading Mode} & """ + _tex(str(fp_mode)) + r""" \\[6pt]
\hline
\textnormal{Pedestrian Live Load Intensity} & """ + fp_intensity + r""" \\[6pt]
\hline
\textnormal{Code Reference} & IRC 6:2017 Clause 206.1 \\[6pt]
\hline
\textnormal{Live Load Reduction Factor} & Evaluated based on effective footway width and span \\[6pt]
\hline
\end{longtable}

\vspace{1em}
\begin{longtable}{|L{5.5cm}|p{10.0cm}|}
""" + hdr_t35 + r"""
\textnormal{Basic Wind Speed, Vb} & """ + (_render_value(input_dict,'wind_speed', ' m/s')) + r""" [from Project Location] \\[6pt]
\hline
\textnormal{Terrain Type} & """ + (_render_value(input_dict, KEY_WL_TERRAIN_TYPE)) + r""" \\[6pt]
\hline
\textnormal{Average Exposed Height, H (m)} & """ + (_render_value(input_dict, KEY_WL_AVG_EXPOSED_HEIGHT, ' m')) + r""" \\[6pt]
\hline
\textnormal{Hourly Mean Wind Speed, Vz} & """ + (_render_value(input_dict, KEY_WL_HOURLY_MEAN_WIND, ' m/s')) + r""" \\[6pt]
\hline
\textnormal{Hourly Wind Pressure, Pz} & """ + (_render_value(input_dict, KEY_WL_HOURLY_WIND_PRESSURE, ' N/m\\textsuperscript{2}')) + r""" \\[6pt]
\hline
\textnormal{Transverse Wind Force} & """ + (_render_value(input_dict, KEY_WL_TRANSVERSE_WIND_FORCE, ' kN')) + r""" \\[6pt]
\hline
\textnormal{Longitudinal Wind Force} & """ + (_render_value(input_dict, KEY_WL_LONGITUDINAL_WIND_FORCE, ' kN')) + r""" \\[6pt]
\hline
\textnormal{Vertical Wind Force} & """ + (_render_value(input_dict, KEY_WL_VERTICAL_WIND_FORCE, ' kN')) + r""" \\[6pt]
\hline
\end{longtable}

\vspace{1em}
\begin{longtable}{|L{5.5cm}|p{10.0cm}|}
""" + hdr_t36 + r"""
\textnormal{Seismic Zone} & """ + (_render_value(input_dict,'seismic_zone')) + r""" [from Project Location] \\[6pt]
\hline
\textnormal{Zone Factor, Z} & """ + (_render_value(input_dict, KEY_SL_ZONE_FACTOR)) + r""" \\[6pt]
\hline
\textnormal{Importance Factor, I} & """ + (_render_value(input_dict, KEY_SL_IMPORTANCE_FACTOR)) + r""" \\[6pt]
\hline
\textnormal{Type of Soil} & """ + (_render_value(input_dict, KEY_SL_SOIL_TYPE)) + r""" \\[6pt]
\hline
\textnormal{Sa/g} & """ + (_render_value(input_dict, KEY_SL_SPECTRAL_COEFF)) + r""" \\[6pt]
\hline
\textnormal{Horizontal Seismic Coefficient, Ah} & """ + (_render_value(input_dict, KEY_SL_HORIZONTAL_COEFF)) + r""" \\[6pt]
\hline
\textnormal{Vertical Seismic Coefficient, Av} & """ + (_render_value(input_dict, KEY_SL_VERTICAL_COEFF)) + r""" \\[6pt]
\hline
\end{longtable}

\vspace{1em}
\begin{longtable}{|L{5.5cm}|p{10.0cm}|}
""" + hdr_t37 + r"""
\textnormal{Maximum Shade Temperature} & """ + (_render_value(input_dict,'shade_temp_max')) + r""" $^\circ$C \\[6pt]
\hline
\textnormal{Minimum Shade Temperature} & """ + (_render_value(input_dict,'shade_temp_min')) + r""" $^\circ$C \\[6pt]
\hline
\textnormal{Effective Bridge Temp. Range} & """ + (_render_value(input_dict, KEY_TL_BRIDGE_TEMP_MIN)) + r""" to """ + (_render_value(input_dict, KEY_TL_BRIDGE_TEMP_MAX)) + r""" $^\circ$C \\[6pt]
\hline
\textnormal{Temperature Rise / Fall for Design} & +""" + (_render_value(input_dict, KEY_TL_TEMP_RISE)) + r""" $^\circ$C / \textminus{}""" + (_render_value(input_dict, KEY_TL_TEMP_FALL)) + r""" $^\circ$C \\[6pt]
\hline
\end{longtable}

\vspace{1em}
\begin{longtable}{|C{4.0cm}|p{11.5cm}|}
""" + hdr_t38 + r"""
""" + lc_rows_str + r"""
\end{longtable}

\noindent\textit{Note: All IRC 6 load combinations are auto-generated by OsdagBridge according to Table B.1 to B.4. User-defined custom combinations, if any, are appended.}
"""
