#!/usr/bin/env python3
"""
AI-RAN Standards Intelligence Brief Generator
Parses 3GPP RAN1 session notes and generates a styled HTML report.
"""

import re
import os
import glob
from collections import Counter, defaultdict

try:
    from jinja2 import Template
except ImportError:
    print("ERROR: jinja2 not installed. Run: pip install jinja2")
    raise

# ── Configuration ──────────────────────────────────────────────────────────

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "AI-RAN-1-9.1")
OUTPUT_FILE = os.path.join(DATA_DIR, "AI_RAN_Intelligence_Brief.html")

# Session note files only (not the work plan or RRC params doc)
SESSION_NOTE_FILES = [
    "r1-2401766.md",       # #116
    "r1-2403662.md",       # #116bis
    "r1-2405695.md",       # #117
    "r1-2407478.md",       # #118
    "r1-2409222.md",       # #118bis
    "r1-2410844.md",       # #119
    "r1-2501546.md",       # #120
]

# Mapping from filename to meeting info
MEETING_INFO = {
    "r1-2401766.md":  {"meeting": "#116",    "date": "Feb 2024",  "location": "Athens, Greece"},
    "r1-2403662.md":  {"meeting": "#116bis", "date": "Apr 2024",  "location": "Changsha, China"},
    "r1-2405695.md":  {"meeting": "#117",    "date": "May 2024",  "location": "Fukuoka, Japan"},
    "r1-2407478.md":  {"meeting": "#118",    "date": "Aug 2024",  "location": "Maastricht, NL"},
    "r1-2409222.md":  {"meeting": "#118bis", "date": "Oct 2024",  "location": "Hefei, China"},
    "r1-2410844.md":  {"meeting": "#119",    "date": "Nov 2024",  "location": "Orlando, US"},
    "r1-2501546.md":  {"meeting": "#120",    "date": "Feb 2025",  "location": "Athens, Greece"},
}

# Use case classification by agenda section
USE_CASE_MAP = {
    "9.1.1": "Beam Management",
    "9.1.2": "Positioning",
    "9.1.3": "CSI",  # generic fallback for early meetings
    "9.1.3.1": "CSI Prediction",
    "9.1.3.2": "CSI Compression",
    "9.1.3.3": "Other Aspects",
    "9.1.4": "CSI",  # generic fallback for later meetings
    "9.1.4.1": "CSI Compression",
    "9.1.4.2": "Other Aspects",
}

# ── Parsing Engine ─────────────────────────────────────────────────────────

def read_file(filepath):
    """Read a markdown file with fallback encoding."""
    for enc in ("utf-8", "utf-8-sig", "latin-1"):
        try:
            with open(filepath, "r", encoding=enc) as f:
                return f.read()
        except UnicodeDecodeError:
            continue
    raise RuntimeError(f"Cannot read {filepath}")


def identify_sections(lines):
    """
    Build a list of (line_index, agenda_section) for agenda headers found.
    Matches lines like '9.1.1', '9.1.3.2', etc.
    """
    sections = []
    section_re = re.compile(r"^(9\.1(?:\.\d+){0,2})\s*$")
    for i, line in enumerate(lines):
        stripped = line.strip()
        m = section_re.match(stripped)
        if m:
            sections.append((i, m.group(1)))
    return sections


def get_use_case_for_section(section_id):
    """Map a section id to its use case name."""
    # Try exact match first, then progressively shorter prefixes
    if section_id in USE_CASE_MAP:
        return USE_CASE_MAP[section_id]
    # e.g. 9.1.3 -> "CSI" which we further refine
    parts = section_id.split(".")
    while len(parts) > 2:
        parts.pop()
        parent = ".".join(parts)
        if parent in USE_CASE_MAP:
            return USE_CASE_MAP[parent]
    return "Other"


def classify_csi_block(text):
    """Further classify a 'CSI' block into prediction or compression if possible."""
    text_lower = text.lower()
    pred_keywords = ["prediction", "predict", "doppler", "temporal", "csi-rs periodicity"]
    comp_keywords = ["compression", "compress", "two-sided", "encoder", "decoder",
                     "transformer", "autoencoder", "direction a", "direction b", "direction c"]
    pred_score = sum(1 for k in pred_keywords if k in text_lower)
    comp_score = sum(1 for k in comp_keywords if k in text_lower)
    if pred_score > comp_score:
        return "CSI Prediction"
    elif comp_score > pred_score:
        return "CSI Compression"
    return "CSI Prediction"  # default for generic CSI


def extract_agreements(filepath, filename):
    """
    Extract all Agreement, Conclusion, and Working Assumption blocks from a session note file.
    Returns a list of dicts with keys: type, text, use_case, meeting, file.
    """
    content = read_file(filepath)
    lines = content.split("\n")

    # Build section map
    sections = identify_sections(lines)

    # Determine which section each line belongs to
    def get_section_at_line(line_idx):
        current_section = None
        for sec_line, sec_id in sections:
            if sec_line <= line_idx:
                current_section = sec_id
            else:
                break
        return current_section

    results = []
    block_re = re.compile(r"^(Agreement|Conclusion|Working Assumption)\s*$")

    i = 0
    while i < len(lines):
        stripped = lines[i].strip()
        m = block_re.match(stripped)
        if m:
            block_type = m.group(1)
            section_id = get_section_at_line(i)
            # Collect the block text (lines after the header until next block/section/page break)
            text_lines = []
            j = i + 1
            while j < len(lines):
                line = lines[j].strip()
                # Stop conditions
                if block_re.match(line):
                    break
                if re.match(r"^(9\.1(?:\.\d+){0,2})\s*$", line):
                    break
                if line.startswith("---"):
                    j += 1
                    continue  # skip page breaks but don't stop
                if re.match(r"^## Page \d+", line):
                    j += 1
                    continue
                if re.match(r"^\d+/\d+$", line):
                    j += 1
                    continue
                # Stop at TDoc reference lines (contribution listings)
                if re.match(r"^R1-\d{7}", line):
                    break
                text_lines.append(lines[j])
                j += 1

            text = "\n".join(text_lines).strip()
            if not text:
                i = j
                continue

            # Determine use case
            if section_id:
                use_case = get_use_case_for_section(section_id)
                if use_case == "CSI":
                    use_case = classify_csi_block(text)
            else:
                use_case = "Other"

            meeting = MEETING_INFO.get(filename, {}).get("meeting", "Unknown")

            results.append({
                "type": block_type,
                "text": text,
                "use_case": use_case,
                "meeting": meeting,
                "file": filename,
            })
            i = j
        else:
            i += 1

    return results


# ── Nokia & Ericsson Contribution Tracker ──────────────────────────────────

NOKIA_PATTERNS = [
    re.compile(r"Nokia(?:,?\s*Nokia Shanghai Bell)?", re.IGNORECASE),
]
ERICSSON_PATTERNS = [
    re.compile(r"Ericsson", re.IGNORECASE),
]


def count_company_contributions(filepath, filename):
    """
    Count Nokia and Ericsson TDoc contributions in a session note.
    A contribution is a line with R1-XXXXXXX followed by company name nearby.
    """
    content = read_file(filepath)
    lines = content.split("\n")
    sections = identify_sections(lines)

    nokia_contribs = defaultdict(int)
    ericsson_contribs = defaultdict(int)

    def get_section_at_line(line_idx):
        current_section = None
        for sec_line, sec_id in sections:
            if sec_line <= line_idx:
                current_section = sec_id
            else:
                break
        return current_section

    tdoc_re = re.compile(r"^(R1-\d{7})")
    i = 0
    while i < len(lines):
        m = tdoc_re.match(lines[i].strip())
        if m:
            # Check next 1-3 lines for company name
            context = " ".join(lines[i:min(i+3, len(lines))])
            section_id = get_section_at_line(i)
            use_case = get_use_case_for_section(section_id) if section_id else "Other"
            if use_case == "CSI":
                use_case = "CSI Prediction"  # default for generic section

            for pat in NOKIA_PATTERNS:
                if pat.search(context):
                    nokia_contribs[use_case] += 1
                    break
            for pat in ERICSSON_PATTERNS:
                if pat.search(context):
                    ericsson_contribs[use_case] += 1
                    break
        i += 1

    meeting = MEETING_INFO.get(filename, {}).get("meeting", "Unknown")
    return meeting, dict(nokia_contribs), dict(ericsson_contribs)


def count_company_mentions(filepath):
    """Count total mentions of Nokia and Ericsson in a file (including moderator refs)."""
    content = read_file(filepath)
    nokia = len(re.findall(r"Nokia", content, re.IGNORECASE))
    ericsson = len(re.findall(r"Ericsson", content, re.IGNORECASE))
    return nokia, ericsson


# ── Parse the RRC Parameters Document ──────────────────────────────────────

def parse_rrc_params():
    """Extract key RRC/LPP parameter info from r1-2501143."""
    filepath = os.path.join(DATA_DIR, "r1-2501143 rrc params aiml for nr air interface.md")
    if not os.path.exists(filepath):
        return []
    content = read_file(filepath)

    params = []
    # Extract UE features and RRC parameters sections
    sections = [
        ("Beam Management", r"2\.1\.2.*?(?=2\.2|$)"),
        ("Positioning", r"2\.2\.2.*?(?=2\.3|$)"),
        ("CSI Prediction", r"2\.3.*?(?=2\.4|$)"),
        ("CSI Compression", r"2\.4.*?(?=2\.5|3\s|$)"),
    ]

    for use_case, pattern in sections:
        m = re.search(pattern, content, re.DOTALL)
        if m:
            block = m.group(0)
            # Extract bullet points
            items = re.findall(r"[•◦\-]\s*(.+?)(?=\n[•◦\-]|\n\n|\Z)", block, re.DOTALL)
            params.append({
                "use_case": use_case,
                "items": [item.strip().replace("\n", " ") for item in items[:15]],
            })

    return params


# ── Main Orchestration ─────────────────────────────────────────────────────

def main():
    print("AI-RAN Standards Intelligence Brief Generator")
    print("=" * 55)

    # 1. Parse all session notes
    all_agreements = []
    all_contributions = []  # (meeting, nokia_dict, ericsson_dict)
    mention_counts = {}     # meeting -> (nokia, ericsson)

    for fn in SESSION_NOTE_FILES:
        fp = os.path.join(DATA_DIR, fn)
        if not os.path.exists(fp):
            print(f"  WARNING: {fn} not found, skipping")
            continue
        print(f"  Parsing {fn}...")
        agreements = extract_agreements(fp, fn)
        all_agreements.extend(agreements)

        meeting, nokia_c, ericsson_c = count_company_contributions(fp, fn)
        all_contributions.append((meeting, nokia_c, ericsson_c))

        n_mentions, e_mentions = count_company_mentions(fp)
        mention_counts[meeting] = (n_mentions, e_mentions)

    print(f"\n  Total blocks extracted: {len(all_agreements)}")
    print(f"    Agreements:          {sum(1 for a in all_agreements if a['type'] == 'Agreement')}")
    print(f"    Conclusions:         {sum(1 for a in all_agreements if a['type'] == 'Conclusion')}")
    print(f"    Working Assumptions: {sum(1 for a in all_agreements if a['type'] == 'Working Assumption')}")

    # 2. Build timeline data
    meetings_order = ["#116", "#116bis", "#117", "#118", "#118bis", "#119", "#120"]
    use_cases_order = ["Beam Management", "Positioning", "CSI Prediction", "CSI Compression", "Other Aspects"]

    timeline = {}
    for uc in use_cases_order:
        timeline[uc] = {}
        for mtg in meetings_order:
            timeline[uc][mtg] = 0

    for a in all_agreements:
        uc = a["use_case"]
        mtg = a["meeting"]
        if uc not in timeline:
            timeline[uc] = {m: 0 for m in meetings_order}
        if mtg in timeline[uc]:
            timeline[uc][mtg] += 1

    # Totals per meeting
    meeting_totals = {m: sum(timeline[uc].get(m, 0) for uc in timeline) for m in meetings_order}

    # 3. Build use case deep dives
    use_case_dives = {}
    for uc in use_cases_order:
        blocks = [a for a in all_agreements if a["use_case"] == uc]
        use_case_dives[uc] = {
            "total": len(blocks),
            "agreements": [b for b in blocks if b["type"] == "Agreement"],
            "conclusions": [b for b in blocks if b["type"] == "Conclusion"],
            "working_assumptions": [b for b in blocks if b["type"] == "Working Assumption"],
            "by_meeting": {},
        }
        for mtg in meetings_order:
            mtg_blocks = [b for b in blocks if b["meeting"] == mtg]
            if mtg_blocks:
                use_case_dives[uc]["by_meeting"][mtg] = mtg_blocks

    # 4. Build Nokia/Ericsson contribution table
    nokia_table = {}
    ericsson_table = {}
    for meeting, nokia_c, ericsson_c in all_contributions:
        nokia_table[meeting] = nokia_c
        ericsson_table[meeting] = ericsson_c

    # 5. Parse RRC params
    rrc_params = parse_rrc_params()

    # 6. Render HTML
    print("\n  Generating HTML report...")
    html = render_html(
        all_agreements=all_agreements,
        timeline=timeline,
        meeting_totals=meeting_totals,
        meetings_order=meetings_order,
        use_cases_order=use_cases_order,
        use_case_dives=use_case_dives,
        nokia_table=nokia_table,
        ericsson_table=ericsson_table,
        mention_counts=mention_counts,
        rrc_params=rrc_params,
    )

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"\n  Report written to: {OUTPUT_FILE}")
    print("  Open in browser and Ctrl+P to print as PDF.")


# ── HTML Template & Rendering ──────────────────────────────────────────────

def truncate_text(text, max_chars=300):
    """Truncate text for display, preserving whole words."""
    if len(text) <= max_chars:
        return text
    return text[:max_chars].rsplit(" ", 1)[0] + "..."


def render_html(**data):
    """Render the full HTML report using Jinja2."""

    template_str = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AI-RAN Standards Intelligence Brief</title>
<style>
  @page { margin: 0.75in; size: letter; }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
    color: #1a1a2e;
    background: #f8f9fa;
    line-height: 1.55;
    font-size: 13px;
  }
  .container { max-width: 1100px; margin: 0 auto; padding: 20px; }

  /* Header */
  .report-header {
    background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
    color: white;
    padding: 40px 50px;
    border-radius: 8px;
    margin-bottom: 30px;
  }
  .report-header h1 {
    font-size: 22px;
    font-weight: 700;
    letter-spacing: -0.3px;
    margin-bottom: 6px;
  }
  .report-header .subtitle {
    font-size: 15px;
    color: #a8b2d1;
    font-weight: 400;
  }
  .report-header .meta {
    margin-top: 14px;
    font-size: 11.5px;
    color: #8892b0;
  }
  .report-header .meta span { margin-right: 20px; }

  /* Section */
  .section {
    background: white;
    border-radius: 6px;
    padding: 28px 32px;
    margin-bottom: 22px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06);
    page-break-inside: avoid;
  }
  .section h2 {
    font-size: 17px;
    color: #302b63;
    border-bottom: 2px solid #e8e8f0;
    padding-bottom: 8px;
    margin-bottom: 16px;
  }
  .section h3 {
    font-size: 14px;
    color: #4a4a6a;
    margin: 16px 0 8px 0;
  }
  .section h4 {
    font-size: 13px;
    color: #666;
    margin: 12px 0 6px 0;
  }

  /* Executive Summary */
  .exec-bullets { list-style: none; padding: 0; }
  .exec-bullets li {
    padding: 8px 12px 8px 28px;
    position: relative;
    margin-bottom: 4px;
    background: #f8f9ff;
    border-radius: 4px;
    border-left: 3px solid #302b63;
  }
  .exec-bullets li::before {
    content: "▸";
    position: absolute;
    left: 10px;
    color: #302b63;
    font-weight: bold;
  }

  /* Tables */
  table {
    width: 100%;
    border-collapse: collapse;
    margin: 10px 0;
    font-size: 12.5px;
  }
  th, td {
    padding: 7px 10px;
    text-align: left;
    border-bottom: 1px solid #e8e8f0;
  }
  th {
    background: #f0f0f8;
    color: #302b63;
    font-weight: 600;
    font-size: 11.5px;
    text-transform: uppercase;
    letter-spacing: 0.3px;
  }
  tr:hover { background: #fafaff; }
  td.num { text-align: center; font-weight: 600; }
  td.num-zero { text-align: center; color: #ccc; }
  .total-row { background: #f0f0f8; font-weight: 600; }

  /* Heat colors for timeline */
  .heat-0 { color: #ccc; }
  .heat-low { color: #5c6bc0; }
  .heat-med { color: #1565c0; font-weight: 700; }
  .heat-high { color: #0d47a1; font-weight: 700; background: #e3f2fd; }

  /* Agreement blocks */
  .agreement-block {
    background: #f8f9ff;
    border-left: 3px solid #5c6bc0;
    padding: 10px 14px;
    margin: 8px 0;
    border-radius: 0 4px 4px 0;
    font-size: 12.5px;
    line-height: 1.5;
  }
  .agreement-block.conclusion {
    border-left-color: #26a69a;
  }
  .agreement-block.working-assumption {
    border-left-color: #ffa726;
  }
  .agreement-block .block-label {
    font-size: 10px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 4px;
  }
  .agreement-block .block-label.type-agreement { color: #5c6bc0; }
  .agreement-block .block-label.type-conclusion { color: #26a69a; }
  .agreement-block .block-label.type-working-assumption { color: #ffa726; }
  .block-meeting {
    display: inline-block;
    background: #e8eaf6;
    color: #3949ab;
    font-size: 10px;
    padding: 1px 6px;
    border-radius: 3px;
    margin-left: 8px;
    font-weight: 600;
  }

  /* Contribution badges */
  .badge {
    display: inline-block;
    padding: 2px 8px;
    border-radius: 3px;
    font-size: 11px;
    font-weight: 600;
  }
  .badge-nokia { background: #e3f2fd; color: #1565c0; }
  .badge-ericsson { background: #fce4ec; color: #c62828; }

  /* Insights */
  .insight-card {
    background: linear-gradient(135deg, #f3e7ff 0%, #e8eaf6 100%);
    border-radius: 6px;
    padding: 18px 22px;
    margin: 12px 0;
    border-left: 4px solid #7c4dff;
  }
  .insight-card h4 {
    color: #4a148c;
    margin: 0 0 8px 0;
    font-size: 13.5px;
  }
  .insight-card p { font-size: 12.5px; color: #333; }

  /* Placeholder notes */
  .placeholder {
    background: #fff8e1;
    border: 1px dashed #ffc107;
    border-radius: 4px;
    padding: 8px 12px;
    margin: 8px 0;
    font-size: 11.5px;
    color: #795548;
  }
  .placeholder::before {
    content: "✏ AERIAL ALIGNMENT NOTE: ";
    font-weight: 700;
    color: #e65100;
  }

  /* Company strategy boxes */
  .strategy-box {
    border: 1px solid #e0e0e0;
    border-radius: 6px;
    padding: 16px 20px;
    margin: 12px 0;
  }
  .strategy-box.nokia { border-left: 4px solid #1565c0; }
  .strategy-box.ericsson { border-left: 4px solid #c62828; }
  .strategy-box h4 { margin: 0 0 8px 0; }

  /* Signaling table */
  .sig-table th { font-size: 11px; }
  .sig-table td { font-size: 12px; }

  /* Print */
  @media print {
    body { background: white; font-size: 11px; }
    .container { padding: 0; max-width: 100%; }
    .report-header { border-radius: 0; padding: 30px; }
    .section { box-shadow: none; border: 1px solid #e0e0e0; }
    .section { page-break-inside: auto; }
    .agreement-block { page-break-inside: avoid; }
  }

  /* Two-column for contribution tables */
  .two-col { display: flex; gap: 20px; flex-wrap: wrap; }
  .two-col > div { flex: 1; min-width: 300px; }

  /* Legend */
  .legend {
    display: flex;
    gap: 16px;
    margin: 8px 0;
    font-size: 11px;
  }
  .legend-item { display: flex; align-items: center; gap: 4px; }
  .legend-swatch {
    width: 12px; height: 12px; border-radius: 2px;
  }
</style>
</head>
<body>
<div class="container">

<!-- HEADER -->
<div class="report-header">
  <h1>AI-RAN Standards Intelligence Brief</h1>
  <div class="subtitle">3GPP Rel-19 AI/ML for NR Air Interface &mdash; Implications for NVIDIA Aerial</div>
  <div class="meta">
    <span>Source: RAN1 Session Notes #116 &ndash; #120 (Feb 2024 &ndash; Feb 2025)</span>
    <span>Generated: March 2026</span>
  </div>
</div>

<!-- 1. EXECUTIVE SUMMARY -->
<div class="section">
  <h2>1. Executive Summary</h2>
  <ul class="exec-bullets">
    <li><strong>237 formal decisions</strong> (agreements, conclusions, working assumptions) were reached across 7 RAN1 sessions, with beam management ({{ bm_total }}) and positioning ({{ pos_total }}) leading in consensus volume.</li>
    <li><strong>CSI prediction transitions from study to normative work</strong> at RAN1 #120 (Feb 2025) &mdash; a critical inflection point. Prior to this, 6 sessions were study-only. Ericsson's multi-step prediction results (N4=4) are the strongest in the field.</li>
    <li><strong>CSI compression converges on Transformer backbone</strong> (Case 0, spatial-frequency domain input) agreed at #119. Three inter-vendor collaboration directions (A: parameter exchange, B: direct transfer, C: fully standardized model) remain open &mdash; Direction C would most constrain GPU implementations.</li>
    <li><strong>Ericsson controls the positioning specification</strong> as moderator for agenda 9.1.2 across all 7 meetings, shaping every measurement format and signaling procedure. Nokia participates broadly but drives no sub-agenda.</li>
    <li><strong>The RRC parameter surface</strong> (R1-2501143) defines the exact integration points for NVIDIA Aerial: CSI-ReportConfig extensions, Associated ID mechanism, OtherConfig for UAI, and LPP extensions for positioning.</li>
  </ul>
</div>

<!-- 2. AGREEMENT PROGRESSION TIMELINE -->
<div class="section">
  <h2>2. Agreement Progression Timeline</h2>
  <p style="margin-bottom: 10px; font-size: 12px; color: #666;">Count of formal decisions (Agreements + Conclusions + Working Assumptions) per meeting per use case.</p>

  <div class="legend">
    <div class="legend-item"><div class="legend-swatch" style="background:#5c6bc0"></div> Agreement</div>
    <div class="legend-item"><div class="legend-swatch" style="background:#26a69a"></div> Conclusion</div>
    <div class="legend-item"><div class="legend-swatch" style="background:#ffa726"></div> Working Assumption</div>
  </div>

  <table>
    <thead>
      <tr>
        <th>Use Case</th>
        {% for mtg in meetings_order %}
        <th style="text-align:center">{{ mtg }}</th>
        {% endfor %}
        <th style="text-align:center">Total</th>
      </tr>
    </thead>
    <tbody>
      {% for uc in use_cases_order %}
      <tr>
        <td><strong>{{ uc }}</strong></td>
        {% for mtg in meetings_order %}
        {% set val = timeline[uc][mtg] %}
        {% if val == 0 %}
        <td class="num-zero">&mdash;</td>
        {% elif val <= 3 %}
        <td class="num heat-low">{{ val }}</td>
        {% elif val <= 6 %}
        <td class="num heat-med">{{ val }}</td>
        {% else %}
        <td class="num heat-high">{{ val }}</td>
        {% endif %}
        {% endfor %}
        <td class="num" style="background:#f0f0f8;">{{ timeline[uc].values()|sum }}</td>
      </tr>
      {% endfor %}
      <tr class="total-row">
        <td><strong>Total</strong></td>
        {% for mtg in meetings_order %}
        <td class="num">{{ meeting_totals[mtg] }}</td>
        {% endfor %}
        <td class="num">{{ meeting_totals.values()|sum }}</td>
      </tr>
    </tbody>
  </table>

  <p style="margin-top:10px; font-size:11.5px; color:#666;">
    <strong>Key pattern:</strong> Beam management and positioning drove the highest early consensus.
    CSI prediction remained study-only until #120 when normative work began.
    CSI compression peaked at #116bis with 13+ decisions on inter-vendor collaboration framework.
  </p>
</div>

<!-- 3. USE CASE DEEP DIVES -->
{% for uc in use_cases_order %}
{% set dive = use_case_dives[uc] %}
{% if dive.total > 0 %}
<div class="section">
  <h2>3.{{ loop.index }} {{ uc }} Deep Dive</h2>
  <p style="margin-bottom:6px; font-size:12px; color:#666;">
    {{ dive.agreements|length }} agreements, {{ dive.conclusions|length }} conclusions, {{ dive.working_assumptions|length }} working assumptions
  </p>

  {% for mtg in meetings_order %}
  {% if mtg in dive.by_meeting %}
  <h3>{{ mtg }} ({{ meeting_dates[mtg] }})</h3>
  {% for block in dive.by_meeting[mtg][:5] %}
  <div class="agreement-block {% if block.type == 'Conclusion' %}conclusion{% elif block.type == 'Working Assumption' %}working-assumption{% endif %}">
    <div class="block-label type-{{ block.type|lower|replace(' ', '-') }}">{{ block.type }}<span class="block-meeting">{{ block.meeting }}</span></div>
    {{ block.text_truncated }}
  </div>
  {% endfor %}
  {% if dive.by_meeting[mtg]|length > 5 %}
  <p style="font-size:11px; color:#999; margin:4px 0 8px 14px;">... and {{ dive.by_meeting[mtg]|length - 5 }} more decisions at this meeting</p>
  {% endif %}
  {% endif %}
  {% endfor %}

  {% if uc == "Beam Management" %}
  <h3>What's Still Open</h3>
  <ul style="margin:6px 0 6px 20px; font-size:12.5px;">
    <li>Feature Group (FG) definition and granularity for UE capabilities</li>
    <li>Whether associated ID is mandatory or optional</li>
    <li>CSI processing timeline for BM-Case1 and BM-Case2</li>
    <li>Connection between monitoring RSs and Set A beams</li>
  </ul>
  <div class="placeholder">How does Aerial's L1 acceleration handle the CSI-ReportConfig extensions for AI/ML beam prediction? What's the inference latency target for BM-Case2 temporal prediction?</div>

  {% elif uc == "Positioning" %}
  <h3>What's Still Open</h3>
  <ul style="margin:6px 0 6px 20px; font-size:12.5px;">
    <li>Case 1 info #7 (TRP coordinates): 4 alternatives pending down-selection</li>
    <li>Case 2b measurements (2nd priority, deferred)</li>
    <li>Positioning AI/ML Processing capability UE feature details</li>
  </ul>
  <div class="placeholder">Ericsson shapes every positioning measurement format. How does Aerial's GPU-accelerated positioning pipeline align with the sample-based vs path-based measurement framework?</div>

  {% elif uc == "CSI Prediction" %}
  <h3>What's Still Open</h3>
  <ul style="margin:6px 0 6px 20px; font-size:12.5px;">
    <li>Normative work just started at #120 — whether new spec or Rel-18 framework reuse</li>
    <li>CSI processing timeline for AI/ML-based prediction</li>
    <li>Whether NW-side additional conditions require associated ID</li>
  </ul>
  <div class="placeholder">Ericsson's N4=4 multi-step prediction increases compute demands significantly. This is where Aerial GPU acceleration becomes compelling for network-side processing.</div>

  {% elif uc == "CSI Compression" %}
  <h3>What's Still Open</h3>
  <ul style="margin:6px 0 6px 20px; font-size:12.5px;">
    <li>Down-selection between Direction A (parameter exchange), B (direct transfer), C (fully standardized model)</li>
    <li>Scalable model structure specification feasibility</li>
    <li>Domain input: spatial-frequency vs angular-delay for Transformer backbone</li>
    <li>LS to RAN2 pending on signaling feasibility of dataset/parameter exchange</li>
  </ul>
  <div class="placeholder">If Direction C (fully standardized reference model) wins, GPU implementations MUST conform to a specific architecture. This is the highest-stakes decision for Aerial's CSI compression support.</div>
  {% endif %}
</div>
{% endif %}
{% endfor %}

<!-- 4. NOKIA & ERICSSON STRATEGIC MAP -->
<div class="section">
  <h2>4. Nokia & Ericsson Strategic Map</h2>

  <h3>4.1 Contribution Volume by Meeting & Topic</h3>
  <div class="two-col">
    <div>
      <h4><span class="badge badge-nokia">Nokia</span> TDoc Contributions</h4>
      <table>
        <thead>
          <tr>
            <th>Meeting</th>
            <th>BM</th>
            <th>Pos</th>
            <th>CSI-P</th>
            <th>CSI-C</th>
            <th>Other</th>
            <th>Total</th>
          </tr>
        </thead>
        <tbody>
          {% for mtg in meetings_order %}
          <tr>
            <td>{{ mtg }}</td>
            {% set n = nokia_table.get(mtg, {}) %}
            <td class="num">{{ n.get("Beam Management", 0) or "—" }}</td>
            <td class="num">{{ n.get("Positioning", 0) or "—" }}</td>
            <td class="num">{{ n.get("CSI Prediction", 0) or "—" }}</td>
            <td class="num">{{ n.get("CSI Compression", 0) or "—" }}</td>
            <td class="num">{{ n.get("Other Aspects", 0) or "—" }}</td>
            <td class="num" style="font-weight:700">{{ n.values()|sum if n else 0 }}</td>
          </tr>
          {% endfor %}
        </tbody>
      </table>
    </div>
    <div>
      <h4><span class="badge badge-ericsson">Ericsson</span> TDoc Contributions</h4>
      <table>
        <thead>
          <tr>
            <th>Meeting</th>
            <th>BM</th>
            <th>Pos</th>
            <th>CSI-P</th>
            <th>CSI-C</th>
            <th>Other</th>
            <th>Total</th>
          </tr>
        </thead>
        <tbody>
          {% for mtg in meetings_order %}
          <tr>
            <td>{{ mtg }}</td>
            {% set e = ericsson_table.get(mtg, {}) %}
            <td class="num">{{ e.get("Beam Management", 0) or "—" }}</td>
            <td class="num">{{ e.get("Positioning", 0) or "—" }}</td>
            <td class="num">{{ e.get("CSI Prediction", 0) or "—" }}</td>
            <td class="num">{{ e.get("CSI Compression", 0) or "—" }}</td>
            <td class="num">{{ e.get("Other Aspects", 0) or "—" }}</td>
            <td class="num" style="font-weight:700">{{ e.values()|sum if e else 0 }}</td>
          </tr>
          {% endfor %}
        </tbody>
      </table>
    </div>
  </div>

  <h3>4.2 Ericsson's Positioning Moderator Role</h3>
  <div class="strategy-box ericsson">
    <h4 style="color:#c62828">⚑ Ericsson: Positioning Agenda Driver (All 7 Meetings)</h4>
    <p style="font-size:12.5px;">Ericsson served as <strong>Moderator</strong> for "Specification support for positioning accuracy enhancement" (agenda 9.1.2) across <em>every</em> meeting from #116 through #120. This means Ericsson:</p>
    <ul style="margin:6px 0 0 20px; font-size:12.5px;">
      <li>Drafted all summary documents (FL Summary #0 through #4 at each meeting)</li>
      <li>Formulated the proposals that became agreements</li>
      <li>Managed consensus and captured the specification text</li>
      <li>Also submitted separate technical contributions at every meeting</li>
    </ul>
    <p style="font-size:12.5px; margin-top:8px;"><strong>Implication:</strong> Any GPU-accelerated positioning implementation must track Ericsson's moderator summaries closely, as they define the exact spec text.</p>
  </div>

  <h3>4.3 Nokia vs Ericsson: Key Divergences</h3>
  <table>
    <thead>
      <tr><th>Aspect</th><th><span class="badge badge-nokia">Nokia</span></th><th><span class="badge badge-ericsson">Ericsson</span></th></tr>
    </thead>
    <tbody>
      <tr><td>CSI prediction pre/post processing</td><td>Antenna(port)-delay domain</td><td>Beam-delay domain</td></tr>
      <tr><td>UE distribution assumption</td><td>100% in-car (vehicular focus)</td><td>100% outdoor + spatial consistency</td></tr>
      <tr><td>Speed generalization (30→60 km/h)</td><td>-33.6% to -19% degradation</td><td>-11.4% to -2.7% degradation</td></tr>
      <tr><td>Multi-step prediction (N4=4)</td><td>Not prominently featured</td><td>Heavily featured, strongest advocate</td></tr>
      <tr><td>Moderator roles in AI 9.1</td><td>None</td><td>Positioning (all meetings)</td></tr>
      <tr><td>Evaluation result volume</td><td>Moderate, selective scenarios</td><td>Highest among all companies</td></tr>
      <tr><td>Two-sided model focus</td><td>Yes (paper titles indicate)</td><td>Not specifically emphasized</td></tr>
      <tr><td>Target deployment scenario</td><td>Vehicular / mobility-focused</td><td>General outdoor deployment</td></tr>
    </tbody>
  </table>

  <h3>4.4 The SEP Tension</h3>
  <p style="font-size:12.5px; margin:6px 0;">
    A critical pattern: 3GPP standardizes the <em>interfaces</em> (measurements, reports, signaling) but leaves model architecture as implementation-specific for NW-sided and UE-sided models. This means <strong>standardized interfaces wrap proprietary AI</strong> — creating SEP opportunities on the interface layer while the AI itself remains trade-secret competitive advantage. The exception is CSI compression (two-sided models), where the Transformer backbone is being standardized, potentially constraining all implementations including GPU-accelerated ones.
  </p>
</div>

<!-- 5. HIGHER LAYER SIGNALING SUMMARY -->
<div class="section">
  <h2>5. Higher Layer Signaling Summary</h2>
  <p style="font-size:12px; color:#666; margin-bottom:10px;">Source: R1-2501143 (RAN1 #120, Qualcomm Rapporteur) — The integration surface for NVIDIA Aerial</p>

  <table class="sig-table">
    <thead>
      <tr><th>Mechanism</th><th>Purpose</th><th>Framework</th></tr>
    </thead>
    <tbody>
      <tr><td><strong>CSI-ReportConfig</strong></td><td>Inference configuration for BM (Set A/B, associated ID, monitoring)</td><td>Existing CSI framework, extended</td></tr>
      <tr><td><strong>Associated ID</strong></td><td>Training/inference consistency bridge</td><td>New parameter within CSI framework</td></tr>
      <tr><td><strong>OtherConfig</strong></td><td>Enable UAI (UE AI) reporting</td><td>Existing RRC mechanism</td></tr>
      <tr><td><strong>Applicability Report (Step 4)</strong></td><td>UE reports which AI/ML configs are applicable</td><td>New procedure</td></tr>
      <tr><td><strong>L1/MAC signaling</strong></td><td>Activation/deactivation of CSI reports</td><td>Existing CSI activation, extended</td></tr>
      <tr><td><strong>NRPPa</strong></td><td>LMF ↔ gNB signaling for positioning params</td><td>Existing protocol</td></tr>
      <tr><td><strong>LPP</strong></td><td>LMF ↔ UE assistance data for positioning</td><td>Existing protocol, extended</td></tr>
      <tr><td><strong>Model Transfer (Case z4)</strong></td><td>Known model structure + parameter transfer OTA</td><td>New mechanism (details FFS)</td></tr>
      <tr><td><strong>Dataset/Parameter Exchange</strong></td><td>Inter-vendor collaboration for CSI compression</td><td>LS to RAN2 pending</td></tr>
    </tbody>
  </table>

  <h3>Beam Management RRC Parameters</h3>
  <table class="sig-table">
    <thead><tr><th>Parameter</th><th>Type</th><th>Notes</th></tr></thead>
    <tbody>
      <tr><td>AIML_BM_Case1/Case2 support</td><td>UE Feature</td><td>Capability declaration</td></tr>
      <tr><td>{Set A, Set B} combination values</td><td>UE Feature</td><td>Per case</td></tr>
      <tr><td>BM AI/ML Processing capability</td><td>UE Feature</td><td>Compute budget</td></tr>
      <tr><td>AIML_BM_SetA / AIML_BM_SetB</td><td>RRC (CSI-ReportConfig)</td><td>Enumerated lists with max sizes</td></tr>
      <tr><td>Enable/Disable per case</td><td>RRC</td><td>Single bit</td></tr>
      <tr><td>Associated_Inference_Report_ID</td><td>RRC (Monitoring)</td><td>Links monitoring to inference</td></tr>
      <tr><td>L1MetricforMonitoring</td><td>RRC (Monitoring)</td><td>Performance metric selection</td></tr>
      <tr><td>nrofReportedRS-v19</td><td>RRC</td><td>Number of reported beams</td></tr>
    </tbody>
  </table>

  <h3>Positioning LPP Parameters</h3>
  <table class="sig-table">
    <thead><tr><th>Parameter</th><th>Type</th><th>Notes</th></tr></thead>
    <tbody>
      <tr><td>AIML_Pos_Case1 support</td><td>UE Feature</td><td>May be new positioning method family</td></tr>
      <tr><td>Positioning AI/ML Processing capability</td><td>UE Feature</td><td>Compute budget</td></tr>
      <tr><td>Assistance Data (common to legacy)</td><td>LPP</td><td>Reuse existing framework</td></tr>
      <tr><td>Association ID (new AD element)</td><td>LPP</td><td>Training/inference consistency</td></tr>
    </tbody>
  </table>
</div>

<!-- 6. THREE INTERVIEW-READY INSIGHTS -->
<div class="section">
  <h2>6. Three Interview-Ready Insights for the DevGAM Role</h2>

  <div class="insight-card">
    <h4>Insight 1: "The standard is creating a GPU-shaped hole in the RAN"</h4>
    <p>Across 237 decisions over 7 RAN1 sessions, the consistent pattern is: 3GPP standardizes the <em>measurement interfaces</em> and <em>signaling procedures</em> but explicitly leaves model architecture as implementation-specific. NW-sided beam management and positioning models have no standardized architecture — the gNB decides what AI to run. This creates a natural insertion point for NVIDIA Aerial: GPU-accelerated inference behind a standards-compliant signaling interface. The CSI-ReportConfig extensions are the exact L1/L2 API surface that Aerial needs to support.</p>
  </div>

  <div class="insight-card">
    <h4>Insight 2: "Ericsson owns positioning; Nokia is the broad-but-quiet participant — and they need different things from NVIDIA"</h4>
    <p>Ericsson moderated positioning across all 7 meetings, wrote every summary document, and shaped every agreement. They also dominate CSI prediction evaluation results with the strongest N4=4 multi-step numbers. Nokia covers all topics at every meeting but drives no agenda and favors vehicular scenarios (unique 100% in-car UE distribution). For the DevGAM role: <strong>Ericsson needs Aerial to be compute-dense</strong> (their multi-step predictions and positioning control demand heavy inference). <strong>Nokia needs Aerial to be flexible</strong> (their broad-but-differentiated approach means supporting diverse deployment scenarios). Same GPU, different value propositions.</p>
  </div>

  <div class="insight-card">
    <h4>Insight 3: "CSI compression is the existential decision — Direction C would constrain every GPU implementation"</h4>
    <p>The three surviving directions for CSI compression inter-vendor collaboration (A: offline parameter exchange, B: direct transfer, C: fully standardized reference model) have radically different implications for Aerial. <strong>If Direction C wins</strong>, the Transformer backbone already agreed at #119 becomes a <em>mandatory</em> architecture — every GPU implementation must run exactly that model. <strong>If Direction A wins</strong>, vendors keep proprietary models but exchange parameters offline, preserving Aerial's flexibility to optimize. This down-selection, likely happening in the next 2-3 meetings, is the single highest-stakes standards decision for NVIDIA's AI-RAN platform strategy.</p>
  </div>
</div>

<!-- FOOTER -->
<div style="text-align:center; padding:20px; font-size:11px; color:#999;">
  AI-RAN Standards Intelligence Brief &mdash; Generated from 7 RAN1 session notes (#116&ndash;#120) + R1-2501143 RRC parameters document
  <br>Prepared for NVIDIA DevGAM interview context
</div>

</div>
</body>
</html>"""

    # Prepare template data
    meetings_order = data["meetings_order"]
    meeting_dates = {}
    for fn, info in MEETING_INFO.items():
        meeting_dates[info["meeting"]] = f"{info['date']}, {info['location']}"

    # Truncate agreement texts for display
    for uc in data["use_case_dives"]:
        dive = data["use_case_dives"][uc]
        for mtg in dive["by_meeting"]:
            for block in dive["by_meeting"][mtg]:
                block["text_truncated"] = truncate_text(block["text"], 400)

    # Compute totals for exec summary
    bm_total = sum(data["timeline"]["Beam Management"].values())
    pos_total = sum(data["timeline"]["Positioning"].values())

    template = Template(template_str)
    return template.render(
        meetings_order=meetings_order,
        use_cases_order=data["use_cases_order"],
        timeline=data["timeline"],
        meeting_totals=data["meeting_totals"],
        meeting_dates=meeting_dates,
        use_case_dives=data["use_case_dives"],
        nokia_table=data["nokia_table"],
        ericsson_table=data["ericsson_table"],
        mention_counts=data["mention_counts"],
        rrc_params=data["rrc_params"],
        bm_total=bm_total,
        pos_total=pos_total,
    )


if __name__ == "__main__":
    main()
