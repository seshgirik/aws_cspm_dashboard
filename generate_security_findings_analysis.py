#!/usr/bin/env python3
"""
Generate an HTML deep-dive view of the AWS CSPM findings dataset.
"""

from __future__ import annotations

import json
from collections import Counter
from datetime import datetime, timezone
from html import escape
from pathlib import Path

DIAGRAM_MAX_IMPACT = 96
DIAGRAM_LINE_WRAP = 22
DATA_PATH = Path("security_findings_all.json")
OUTPUT_PATH = Path("security_findings_analysis.html")


def load_findings() -> list[dict]:
    raw = json.loads(DATA_PATH.read_text())
    return [
        finding
        for event in raw
        for finding in event.get("detail", {}).get("findings", [])
    ]


def percent(part: int, whole: int) -> float:
    if not whole:
        return 0.0
    return (part / whole) * 100


def truncate(text: str, limit: int = 48) -> str:
    if len(text) <= limit:
        return text
    return text[: limit - 3] + "..."


def wrap_text(text: str, line_len: int = DIAGRAM_LINE_WRAP) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current: list[str] = []
    for word in words:
        prospective = " ".join(current + [word])
        if len(prospective) > line_len and current:
            lines.append(" ".join(current))
            current = [word]
        else:
            current.append(word)
    if current:
        lines.append(" ".join(current))
    return lines or [text]


def build_html(findings: list[dict]) -> str:
    total = len(findings)
    severity = Counter(f.get("Severity", {}).get("Label", "UNKNOWN") for f in findings)
    compliance = Counter(
        f.get("Compliance", {}).get("status", "UNKNOWN") for f in findings
    )
    regions = Counter(f.get("Region", "UNKNOWN") for f in findings)

    attack_surface = Counter()
    tactics = Counter()
    resources = Counter()
    for f in findings:
        for surface in f.get("ThreatModel", {}).get("attack_surface", []) or []:
            attack_surface[surface] += 1
        mitre = f.get("ThreatModel", {}).get("MITRE_ATTACK", {})
        for tactic in mitre.get("tactics", []) or []:
            tactics[tactic] += 1
        for resource in f.get("Resources", []) or []:
            resources[resource.get("Type", "AwsResource")] += 1

    scores = []
    for f in findings:
        risk = f.get("ThreatModel", {}).get("risk_score")
        if isinstance(risk, (int, float)):
            scores.append(risk)

    top_findings = sorted(
        findings,
        key=lambda f: f.get("ThreatModel", {}).get("risk_score") or 0,
        reverse=True,
    )[:4]

    dominant_region, dominant_region_total = regions.most_common(1)[0]
    dominant_surface, dominant_surface_total = attack_surface.most_common(1)[0]
    dominant_tactic, dominant_tactic_total = tactics.most_common(1)[0]

    insight_cards = [
        f"{severity.get('CRITICAL', 0)} critical + {severity.get('HIGH', 0)} high "
        f"issues drive {percent(severity.get('CRITICAL', 0) + severity.get('HIGH', 0), total):.1f}% "
        "of total risk-weighted alerts.",
        f"{dominant_region} hosts {percent(dominant_region_total, total):.1f}% of findings, "
        "revealing a heavy geographic concentration.",
        f"{dominant_surface} is the most attacked surface "
        f"({dominant_surface_total} findings) with MITRE {dominant_tactic} "
        f"tactics surfacing {percent(dominant_tactic_total, total):.1f}% of the time.",
        f"Average modeled risk score is {sum(scores)/len(scores):.1f}/100 "
        f"across {len(scores)} findings, with {max(scores):.0f} as the ceiling.",
    ]

    def render_counter_rows(counter: Counter, limit: int = 5) -> str:
        rows = []
        for name, count in counter.most_common(limit):
            rows.append(
                f"<li><span>{escape(name)}</span>"
                f"<strong>{count} ({percent(count, total):.1f}%)</strong></li>"
            )
        if not rows:
            rows.append("<li><span>No data</span><strong>0</strong></li>")
        return "\n".join(rows)

    def render_top_findings() -> str:
        cards = []
        for f in top_findings:
            risk = f.get("ThreatModel", {}).get("risk_score", 0)
            cards.append(
                f"""
                <article class="finding-card">
                    <div class="chip chip-{escape(f.get('Severity', {}).get('Label', 'LOW').lower())}">
                        {escape(f.get('Severity', {}).get('Label', 'LOW'))} • Risk {risk}
                    </div>
                    <h3>{escape(f.get('Title', 'Untitled Finding'))}</h3>
                    <p>{escape(f.get('Description', 'No description available'))}</p>
                    <ul class="finding-meta">
                        <li><strong>Region:</strong> {escape(f.get('Region', 'N/A'))}</li>
                        <li><strong>Resource:</strong> {escape(f.get('Resources', [{}])[0].get('Type', 'AwsResource'))}</li>
                        <li><strong>Generator:</strong> {escape(f.get('GeneratorId', 'Unknown'))}</li>
                    </ul>
                    <div class="attack-pill">
                        Attack Surface: {escape(', '.join(f.get('ThreatModel', {}).get('attack_surface', []) or ['Not Modeled']))}
                    </div>
                </article>
                """
            )
        return "\n".join(cards)

    def render_issue_diagram(finding: dict) -> str:
        attack_surface = ", ".join(
            finding.get("ThreatModel", {}).get("attack_surface", [])
            or ["General Surface"]
        )
        mitre = ", ".join(
            finding.get("ThreatModel", {}).get("MITRE_ATTACK", {}).get("tactics", [])
            or ["Unmapped Tactic"]
        )
        resources = finding.get("Resources", []) or [{}]
        resource_type = resources[0].get("Type", "AwsResource")
        resource_id = truncate(resources[0].get("Id", "Unknown"))
        description = finding.get("Description", "No description provided.")

        nodes = [
            ("Resource", f"{resource_type}\n{resource_id}"),
            ("Attack Surface", attack_surface),
            ("MITRE Tactics", mitre),
            ("Potential Impact", truncate(description, DIAGRAM_MAX_IMPACT)),
        ]
        node_width = 190
        node_height = 110
        gap = 40
        padding = 20
        svg_width = padding * 2 + len(nodes) * node_width + (len(nodes) - 1) * gap
        svg_height = node_height + padding * 2

        rect_colors = ["#e0f2ff", "#fff1db", "#ede4ff", "#ffe3ee"]

        def format_node_text(content: str) -> str:
            lines = wrap_text(content, line_len=24)
            line_elements = []
            for idx, line in enumerate(lines[:4]):
                y = 70 + idx * 16
                line_elements.append(
                    f'<text x="{{x_center}}" y="{y}" text-anchor="middle" font-size="12" fill="#444">{escape(line)}</text>'
                )
            return "\n".join(line_elements)

        svg_parts = [
            f'<svg class="issue-svg" viewBox="0 0 {svg_width} {svg_height}" role="img" aria-label="Threat flow diagram">'
            "<defs>"
            '<marker id="arrowhead" markerWidth="8" markerHeight="6" refX="6" refY="3" orient="auto">'
            '<polygon points="0 0, 8 3, 0 6" fill="#9aa0c7" />'
            "</marker>"
            "</defs>"
        ]

        for idx, (title, content) in enumerate(nodes):
            x = padding + idx * (node_width + gap)
            y = padding
            bg = rect_colors[idx % len(rect_colors)]
            x_center = x + node_width / 2
            node_svg = [
                f'<rect x="{x}" y="{y}" width="{node_width}" height="{node_height}" rx="18" fill="{bg}" stroke="#cfd3f7" />',
                f'<text x="{x_center}" y="{y + 30}" text-anchor="middle" font-size="13" font-weight="600" fill="#1f2247">{escape(title)}</text>',
                format_node_text(content).replace("{x_center}", str(x_center)),
            ]
            svg_parts.extend(node_svg)
            if idx < len(nodes) - 1:
                arrow_x_start = x + node_width
                arrow_x_end = arrow_x_start + gap
                arrow_y = y + node_height / 2
                svg_parts.append(
                    f'<line x1="{arrow_x_start}" y1="{arrow_y}" x2="{arrow_x_end}" y2="{arrow_y}" '
                    'stroke="#9aa0c7" stroke-width="2" marker-end="url(#arrowhead)" />'
                )

        svg_parts.append("</svg>")
        return "\n".join(svg_parts)

    def render_issue_breakdowns() -> str:
        blocks = []
        for idx, finding in enumerate(findings, 1):
            severity_label = finding.get("Severity", {}).get("Label", "UNKNOWN")
            risk = finding.get("ThreatModel", {}).get("risk_score", "N/A")
            compliance_status = finding.get("Compliance", {}).get("status", "UNKNOWN")
            summary_title = f"#{idx} · {finding.get('Title', 'Untitled Finding')}"
            description = finding.get("Description", "No description provided.")
            blocks.append(
                f"""
                <details class="issue">
                    <summary>
                        <span>{escape(summary_title)}</span>
                        <span class="issue-meta">
                            <span class="chip chip-{escape(severity_label.lower())}">{escape(severity_label)}</span>
                            <span class="mini-pill">Risk {escape(str(risk))}</span>
                        </span>
                    </summary>
                    <div class="issue-body">
                        <p>{escape(description)}</p>
                        <div class="issue-diagram">
                            {render_issue_diagram(finding)}
                        </div>
                        <ul class="issue-insights">
                            <li><strong>Region:</strong> {escape(finding.get('Region', 'N/A'))}</li>
                            <li><strong>Compliance:</strong> {escape(compliance_status)}</li>
                            <li><strong>Generator:</strong> {escape(finding.get('GeneratorId', 'Unknown'))}</li>
                        </ul>
                    </div>
                </details>
                """
            )
        return "\n".join(blocks)

    now = datetime.now(timezone.utc).strftime("%d %b %Y %H:%M UTC")

    # Prepare chart payloads
    severity_items = list(severity.items())
    severity_labels = [name for name, _ in severity_items]
    severity_counts = [count for _, count in severity_items]
    top_surfaces = attack_surface.most_common(5)
    surface_labels = [name for name, _ in top_surfaces]
    surface_counts = [count for _, count in top_surfaces]
    top_tactics = tactics.most_common(5)
    tactic_labels = [name for name, _ in top_tactics]
    tactic_counts = [count for _, count in top_tactics]

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>AWS CSPM Security Findings Analysis</title>
    <style>
        :root {{
            --purple: #6b4eff;
            --pink: #ff6db3;
            --card-bg: #fff;
            --chip-critical: #ff4d4f;
            --chip-high: #fa8c16;
            --chip-medium: #faad14;
            --chip-low: #52c41a;
        }}
        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            margin: 0;
            background: #f5f6fb;
            color: #1f2247;
        }}
        .hero {{
            background: linear-gradient(135deg, var(--purple), var(--pink));
            color: white;
            padding: 56px 64px 72px;
            border-bottom-left-radius: 36px;
            border-bottom-right-radius: 36px;
            box-shadow: 0 16px 40px rgba(86, 70, 255, 0.25);
        }}
        .hero h1 {{
            margin: 0 0 12px;
            font-size: 40px;
        }}
        .hero p {{
            margin: 0;
            font-size: 18px;
            opacity: 0.9;
        }}
        main {{
            margin: -60px auto 64px;
            max-width: 1100px;
            padding: 0 24px;
        }}
        .alert {{
            background: #fff6f0;
            border-left: 6px solid #ff9f43;
            padding: 24px;
            border-radius: 24px;
            margin-bottom: 28px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.05);
        }}
        .alert h2 {{
            margin: 0 0 8px;
            font-size: 20px;
            color: #c96b00;
        }}
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));
            gap: 16px;
            margin-bottom: 32px;
        }}
        .card {{
            background: var(--card-bg);
            border-radius: 24px;
            padding: 24px;
            box-shadow: 0 15px 40px rgba(31,34,71,0.08);
        }}
        .card h3 {{
            margin-top: 0;
            font-size: 18px;
        }}
        .card strong {{
            font-size: 28px;
            display: block;
            margin-top: 8px;
        }}
        .two-column {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(310px, 1fr));
            gap: 24px;
            margin-bottom: 32px;
        }}
        .problem, .solution {{
            background: white;
            border-radius: 24px;
            padding: 28px;
            box-shadow: 0 14px 36px rgba(0,0,0,0.07);
        }}
        .problem h3, .solution h3 {{
            margin-top: 0;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        .problem h3::before {{
            content: "✖";
            color: #f5222d;
        }}
        .solution h3::before {{
            content: "✔";
            color: #52c41a;
        }}
        ul.details {{
            list-style: none;
            padding-left: 0;
        }}
        ul.details li {{
            margin-bottom: 10px;
            padding-left: 18px;
            position: relative;
        }}
        ul.details li::before {{
            content: '•';
            color: var(--purple);
            position: absolute;
            left: 0;
        }}
        section {{
            margin-bottom: 36px;
        }}
        .section-subtitle {{
            margin-top: -8px;
            color: #5a5d7c;
            font-size: 14px;
            margin-bottom: 16px;
        }}
        section h2 {{
            margin-bottom: 12px;
            font-size: 22px;
            color: #1b1e3d;
        }}
        .charts {{
            background: white;
            border-radius: 24px;
            padding: 28px;
            box-shadow: 0 14px 36px rgba(0,0,0,0.07);
        }}
        .chart-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 24px;
        }}
        .chart-card {{
            background: #f8f9ff;
            border-radius: 18px;
            padding: 16px;
        }}
        .chart-card h3 {{
            margin-top: 0;
            font-size: 16px;
        }}
        .list-card ul {{
            list-style: none;
            padding: 0;
            margin: 0;
        }}
        .list-card li {{
            display: flex;
            justify-content: space-between;
            padding: 12px 0;
            border-bottom: 1px dashed #eceef7;
        }}
        .insights {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 16px;
        }}
        .insights .card {{
            border-left: 5px solid var(--purple);
        }}
        .finding-card {{
            background: #ffffff;
            border-radius: 20px;
            padding: 20px;
            box-shadow: 0 12px 30px rgba(0,0,0,0.08);
            margin-bottom: 18px;
        }}
        .chip {{
            display: inline-block;
            padding: 6px 12px;
            border-radius: 999px;
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            color: white;
            margin-bottom: 12px;
        }}
        .chip-critical {{ background: var(--chip-critical); }}
        .chip-high {{ background: var(--chip-high); }}
        .chip-medium {{ background: var(--chip-medium); }}
        .chip-low {{ background: var(--chip-low); }}
        .finding-card h3 {{
            margin-top: 0;
            margin-bottom: 10px;
        }}
        .finding-meta {{
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
            list-style: none;
            padding-left: 0;
            margin: 12px 0;
            font-size: 14px;
            color: #4b4f68;
        }}
        .attack-pill {{
            display: inline-block;
            background: #eef0ff;
            color: var(--purple);
            padding: 8px 14px;
            border-radius: 999px;
            font-weight: 600;
            font-size: 12px;
        }}
        .issue-stack {{
            display: flex;
            flex-direction: column;
            gap: 14px;
            max-height: 70vh;
            overflow-y: auto;
            padding-right: 8px;
        }}
        .issue {{
            border-radius: 18px;
            background: white;
            box-shadow: 0 8px 24px rgba(0,0,0,0.07);
            padding: 0 18px;
        }}
        .issue summary {{
            cursor: pointer;
            display: flex;
            justify-content: space-between;
            align-items: center;
            list-style: none;
            padding: 18px 0;
            font-weight: 600;
        }}
        .issue summary::-webkit-details-marker {{
            display: none;
        }}
        .issue-meta {{
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        .mini-pill {{
            background: #eef0ff;
            color: #4b4f68;
            padding: 4px 10px;
            border-radius: 999px;
            font-size: 12px;
            font-weight: 600;
        }}
        .issue-body {{
            border-top: 1px dashed #eceef7;
            padding: 14px 0 20px;
            font-size: 14px;
            color: #4b4f68;
        }}
        .issue-diagram {{
            margin: 18px 0;
            overflow-x: auto;
        }}
        .issue-svg {{
            width: 100%;
            max-width: 960px;
            height: auto;
            display: block;
            margin: 0 auto;
        }}
        .issue-insights {{
            list-style: none;
            padding-left: 0;
            display: flex;
            flex-wrap: wrap;
            gap: 18px;
            font-size: 13px;
            margin: 0;
        }}
        footer {{
            text-align: center;
            font-size: 12px;
            color: #7a7e9d;
            padding-bottom: 48px;
        }}
    </style>
</head>
<body>
    <header class="hero">
        <h1>AWS Security Findings Observatory</h1>
        <p>Generated {now} from {total} findings sourced from Security Hub, GuardDuty, and adjacent services.</p>
    </header>
    <main>
        <section class="alert">
            <h2>Situation Snapshot · Elevated Risk</h2>
            <p><strong>Issue:</strong> Concentration of CRITICAL/HIGH misconfigurations across AI/ML workloads, IAM surfaces, and east coast regions.</p>
            <p><strong>Impact:</strong> Broad blast radius for initial access attempts, key management weaknesses, and exposed data planes that can accelerate credential theft and ransomware scenarios.</p>
        </section>
        <div class="grid">
            <div class="card">
                <h3>Total Findings</h3>
                <strong>{total}</strong>
                <p>{severity.get('CRITICAL', 0)} Critical · {severity.get('HIGH', 0)} High · {severity.get('MEDIUM', 0)} Medium · {severity.get('LOW', 0)} Low</p>
            </div>
            <div class="card">
                <h3>Non-compliant Controls</h3>
                <strong>{compliance.get('NON_COMPLIANT', 0)}</strong>
                <p>{percent(compliance.get('NON_COMPLIANT', 0), total):.1f}% of all findings are confirmed gaps.</p>
            </div>
            <div class="card">
                <h3>Regional Hotspot</h3>
                <strong>{escape(dominant_region)}</strong>
                <p>{dominant_region_total} findings need regional prioritization.</p>
            </div>
            <div class="card">
                <h3>Avg. Risk Score</h3>
                <strong>{sum(scores)/len(scores):.1f}</strong>
                <p>Scale 0-100 based on embedded threat modeling metadata.</p>
            </div>
        </div>

        <div class="two-column">
            <div class="problem">
                <h3>Current Exposure</h3>
                <ul class="details">
                    <li>{severity.get('CRITICAL', 0)} critical controls unresolved — focus on perimeter and data plane guardrails.</li>
                    <li>{attack_surface.get('AI/ML Services', 0)} findings tied to AI/ML services show model endpoints and pipelines as prime targets.</li>
                    <li>{tactics.get('Initial Access', 0)} MITRE Initial Access patterns highlight open attack paths for adversaries.</li>
                </ul>
            </div>
            <div class="solution">
                <h3>Recommended Motion</h3>
                <ul class="details">
                    <li>Enforce guardrails for AI/ML and KMS integrations; require private endpoints plus CMK rotation.</li>
                    <li>Accelerate remediation of unrestricted network policies (RDP/SSH) and public data stores.</li>
                    <li>Expand detective coverage in {escape(dominant_region)} with automated evidence collection.</li>
                </ul>
            </div>
        </div>

        <section class="insights">
            {"".join(f'<div class="card">{escape(text)}</div>' for text in insight_cards)}
        </section>

        <section>
            <h2>Interactive Metrics</h2>
            <div class="charts">
                <div class="chart-grid">
                    <div class="chart-card">
                        <h3>Severity Distribution</h3>
                        <canvas id="severityChart" height="220"></canvas>
                    </div>
                    <div class="chart-card">
                        <h3>Top Attack Surfaces</h3>
                        <canvas id="surfaceChart" height="220"></canvas>
                    </div>
                    <div class="chart-card">
                        <h3>MITRE Tactics</h3>
                        <canvas id="tacticChart" height="220"></canvas>
                    </div>
                </div>
            </div>
        </section>

        <section>
            <h2>Threat Landscape Signals</h2>
            <div class="grid">
                <div class="card list-card">
                    <h3>Top Attack Surfaces</h3>
                    <ul>{render_counter_rows(attack_surface)}</ul>
                </div>
                <div class="card list-card">
                    <h3>MITRE ATT&CK Tactics</h3>
                    <ul>{render_counter_rows(tactics)}</ul>
                </div>
                <div class="card list-card">
                    <h3>Resource Types</h3>
                    <ul>{render_counter_rows(resources)}</ul>
                </div>
            </div>
        </section>

        <section>
            <h2>Highest-Risk Findings</h2>
            {render_top_findings()}
        </section>

        <section>
            <h2>Issue-by-Issue Deep Dive</h2>
            <p class="section-subtitle">Expand each card to view a narrative plus visual chain for every finding in the dataset.</p>
            <div class="issue-stack">
                {render_issue_breakdowns()}
            </div>
        </section>
    </main>
    <footer>
        AWS CSPM Dashboard · Generated automatically from security_findings_all.json
    </footer>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script>
        const severityCtx = document.getElementById('severityChart').getContext('2d');
        new Chart(severityCtx, {{
            type: 'doughnut',
            data: {{
                labels: {json.dumps(severity_labels)},
                datasets: [{{
                    data: {json.dumps(severity_counts)},
                    backgroundColor: ['#ff4d4f', '#fa8c16', '#faad14', '#52c41a', '#8c8c8c'],
                    borderWidth: 0
                }}]
            }},
            options: {{
                plugins: {{
                    legend: {{
                        position: 'bottom'
                    }}
                }}
            }}
        }});

        const surfaceCtx = document.getElementById('surfaceChart').getContext('2d');
        new Chart(surfaceCtx, {{
            type: 'bar',
            data: {{
                labels: {json.dumps(surface_labels)},
                datasets: [{{
                    label: 'Findings',
                    data: {json.dumps(surface_counts)},
                    backgroundColor: '#6b4eff',
                    borderRadius: 8
                }}]
            }},
            options: {{
                plugins: {{ legend: {{ display: false }} }},
                scales: {{
                    y: {{
                        beginAtZero: true,
                        ticks: {{ precision: 0 }}
                    }}
                }}
            }}
        }});

        const tacticCtx = document.getElementById('tacticChart').getContext('2d');
        new Chart(tacticCtx, {{
            type: 'radar',
            data: {{
                labels: {json.dumps(tactic_labels)},
                datasets: [{{
                    label: 'Findings',
                    data: {json.dumps(tactic_counts)},
                    backgroundColor: 'rgba(255,164,81,0.3)',
                    borderColor: '#ffa451',
                    pointBackgroundColor: '#ffa451'
                }}]
            }},
            options: {{
                scales: {{
                    r: {{
                        beginAtZero: true,
                        ticks: {{
                            stepSize: 5
                        }}
                    }}
                }}
            }}
        }});
    </script>
</body>
</html>"""
    return html


def main() -> None:
    findings = load_findings()
    html = build_html(findings)
    OUTPUT_PATH.write_text(html, encoding="utf-8")
    print(f"Wrote {OUTPUT_PATH} with {len(findings)} findings.")


if __name__ == "__main__":
    main()
