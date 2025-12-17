#!/usr/bin/env node
/**
 * Generate a storyboard-style HTML file for every finding.
 */
const fs = require("fs");

const INPUT = "security_findings_all.json";
const OUTPUT = "security_findings_visual_story.html";

function loadFindings() {
  const raw = JSON.parse(fs.readFileSync(INPUT, "utf8"));
  return raw.flatMap((event) => event?.detail?.findings ?? []);
}

function escapeHTML(str = "") {
  return str
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

function truncate(text = "", limit = 80) {
  if (text.length <= limit) return text;
  return `${text.slice(0, limit - 3)}...`;
}

function titleCase(value = "") {
  if (!value) return "";
  return value
    .split(/[\s_-]+/)
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1).toLowerCase())
    .join(" ");
}

function severityClass(label = "") {
  const normalized = label.toUpperCase();
  if (normalized === "CRITICAL") return "sev-critical";
  if (normalized === "HIGH") return "sev-high";
  if (normalized === "MEDIUM") return "sev-medium";
  return "sev-low";
}

function formatDate(value) {
  if (!value) return "Unknown";
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return value;
  return date.toLocaleString("en-US", {
    dateStyle: "medium",
    timeStyle: "short",
  });
}

function simplifyServiceName(resourceType = "", generatorId = "", types = []) {
  const serviceCandidates = [];
  if (resourceType) {
    serviceCandidates.push(resourceType.replace(/^Aws/i, ""));
  }
  if (generatorId) {
    const segment = generatorId.split("/")[0];
    serviceCandidates.push(segment.replace(/^aws[-:]?/i, ""));
  }
  if (types.length) {
    serviceCandidates.push(types[0].split("/")[0]);
  }
  const candidate =
    serviceCandidates.find((item) => item && item.length > 0) || "Cloud";
  const label = titleCase(
    candidate.replace(/([a-z])([A-Z])/g, "$1 $2").replace(/[_-]/g, " ")
  ).trim();
  const slug =
    label.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "") ||
    "cloud";
  return { label, slug };
}

function groupService(service) {
  const slug = service.slug;
  const label = service.label;
  const normalized = slug.toLowerCase();
  if (normalized.includes("bedrock")) {
    return { slug: "bedrock", label: "Amazon Bedrock" };
  }
  if (normalized.includes("sage-maker") || normalized.includes("sagemaker")) {
    return { slug: "sagemaker", label: "Amazon SageMaker" };
  }
  if (normalized.startsWith("iam")) {
    return { slug: "iam", label: "AWS Identity & Access Management" };
  }
  return service;
}

function deriveCloudZone(region = "") {
  if (!region || region.toLowerCase() === "global") return "global";
  const prefix = region.split("-")[0].toLowerCase();
  const map = {
    us: "north-america",
    ca: "north-america",
    eu: "europe",
    ap: "asia-pacific",
    sa: "south-america",
    me: "middle-east",
    af: "africa",
  };
  return map[prefix] || "global";
}

function detectAiMl(finding) {
  const tm = finding?.ThreatModel ?? {};
  const attackSurface = tm?.attack_surface ?? [];
  const resource = finding?.Resources?.[0] ?? {};
  const description = finding?.Description ?? "";
  const candidates = [
    attackSurface.join(" "),
    resource?.Type ?? "",
    finding?.GeneratorId ?? "",
    (finding?.Types ?? []).join(" "),
    description,
  ]
    .join(" ")
    .toLowerCase();
  return /\b(ai|ml|machine learning|bedrock|sagemaker|model|genai)\b/.test(
    candidates
  );
}

function detectRegulations(finding) {
  const text = [
    finding?.Description ?? "",
    finding?.GeneratorId ?? "",
    (finding?.Types ?? []).join(" "),
  ]
    .join(" ")
    .toLowerCase();
  const regulations = [];
  if (text.includes("hipaa")) regulations.push("HIPAA");
  if (text.includes("gdpr")) regulations.push("GDPR");
  if (text.includes("pci")) regulations.push("PCI");
  return regulations;
}

function deriveThreatCategory(finding) {
  const text = [
    finding?.Description ?? "",
    finding?.GeneratorId ?? "",
    (finding?.Types ?? []).join(" "),
    (finding?.ThreatModel?.attack_surface ?? []).join(" "),
    (finding?.ThreatModel?.MITRE_ATTACK?.tactics ?? []).join(" "),
  ]
    .join(" ")
    .toLowerCase();
  const rules = [
    {
      slug: "data-exfiltration",
      label: "Data Exfiltration",
      match: /exfil|data leak|pii|data layer|exposure|public bucket/,
      synopsis: "Sensitive data or secrets can be staged or leaked.",
    },
    {
      slug: "credential-abuse",
      label: "Credential Abuse",
      match: /credential|access key|iam|privilege|secret/,
      synopsis: "Identity or privilege misuse enables elevated access.",
    },
    {
      slug: "network-exposure",
      label: "Network Exposure",
      match: /security group|network|rdp|ssh|port|firewall/,
      synopsis: "Exposed network paths allow intrusion or lateral movement.",
    },
    {
      slug: "ai-ml-integrity",
      label: "AI / ML Integrity",
      match: /sagemaker|bedrock|model|ai|ml|training/,
      synopsis: "AI model pipelines or guardrails are at risk of tamper.",
    },
    {
      slug: "visibility-gap",
      label: "Visibility Gap",
      match: /logging|cloudtrail|detective|guardduty|monitor/,
      synopsis: "Telemetry gaps hinder detection and response.",
    },
  ];
  const matched =
    rules.find((rule) => rule.match.test(text)) || ({
      slug: "misconfiguration",
      label: "Cloud Misconfiguration",
      synopsis: "Baseline misconfiguration weakens security posture.",
    });
  return matched;
}

function buildMetaCard(label, value, detail = "") {
  return `<div class="meta-card">
  <span>${escapeHTML(label)}</span>
  <strong>${escapeHTML(value)}</strong>
  <small>${escapeHTML(detail)}</small>
</div>`;
}

function buildList(items) {
  if (!items.length) {
    return "<li>No data provided.</li>";
  }
  return items
    .map((item) => `<li>${escapeHTML(item)}</li>`)
    .join("\n");
}

function articleForFinding(finding, index) {
  const severityLabel = finding?.Severity?.Label ?? "UNKNOWN";
  const compliance = finding?.Compliance?.status ?? "UNKNOWN";
  const region = finding?.Region ?? "Global";
  const createdAt = formatDate(finding?.CreatedAt);
  const resource = finding?.Resources?.[0] ?? {};
  const resourceType = resource?.Type ?? "AwsResource";
  const resourceId = truncate(resource?.Id ?? "Not Provided", 60);
  const tm = finding?.ThreatModel ?? {};
  const attackSurface =
    (tm?.attack_surface && tm.attack_surface.join(", ")) ||
    "General Cloud Surface";
  const mitreTactics =
    (tm?.MITRE_ATTACK?.tactics && tm.MITRE_ATTACK.tactics.join(", ")) ||
    "Unmapped Tactic";
  const stride =
    tm?.STRIDE?.map(({ category, risk }) => `${category} (${risk})`) ?? [];
  const title = finding?.Title ?? `Finding ${index}`;
  const description = finding?.Description ?? "No description provided.";
  const riskScore =
    typeof tm?.risk_score === "number" ? `${tm.risk_score}/100` : "Model N/A";
  const badge =
    finding?.Types?.join(" · ") || finding?.GeneratorId || "AWS Security Hub";
  const typesList = finding?.Types ?? [];
  const serviceInfo = simplifyServiceName(
    resourceType,
    finding?.GeneratorId,
    typesList
  );
  const groupedService = groupService(serviceInfo);
  const cloudZone = deriveCloudZone(region);
  const isAi = detectAiMl(finding);
  const regulations = detectRegulations(finding);
  const threatCategory = deriveThreatCategory(finding);
  const regulationAttr =
    regulations.length > 0
      ? regulations.map((r) => r.toLowerCase()).join(" ")
      : "none";
  const searchable = [
    title,
    description,
    resourceType,
    attackSurface,
    mitreTactics,
    finding?.GeneratorId ?? "",
  ]
    .join(" ")
    .toLowerCase();

  const flowlineItems = [
    { label: "Resource", value: `${resourceType} · ${resourceId}` },
    { label: "Regions", value: region },
    { label: "Attack Surface", value: attackSurface },
    { label: "MITRE", value: mitreTactics },
    { label: "Impact", value: truncate(description, 140) },
  ];

  const stageGrid = [
    {
      icon: "🧩",
      heading: "Generator",
      detail: finding?.GeneratorId ?? "Not provided",
    },
    {
      icon: "🛡️",
      heading: "Compliance",
      detail: compliance,
    },
    {
      icon: "🎯",
      heading: "STRIDE",
      detail: stride.length ? stride.join(", ") : "Not modeled",
    },
    {
      icon: "⚙️",
      heading: "Workflow",
      detail: finding?.Workflow?.status ?? "UNSPECIFIED",
    },
  ];

  const recommendationList = [
    `Prioritize remediation in ${region} to contain blast radius.`,
    `Run playbooks for ${finding?.GeneratorId || "referenced control"} and verify guardrail coverage.`,
    `Investigate resources of type ${resourceType} for misconfiguration drift.`,
    `Ensure telemetry covers attack surface: ${attackSurface}.`,
    regulations.length
      ? `Validate regulatory controls ( ${regulations.join(", ")} ) stay enforced.`
      : "Map finding to applicable regulatory frameworks.",
  ];

  const article = `<article class="issue" id="finding-${index}"
    data-service="${groupedService.slug}"
    data-severity="${severityLabel.toLowerCase()}"
    data-cloud="${cloudZone}"
    data-aiml="${isAi}"
    data-compliance="${(compliance || "UNKNOWN").toLowerCase()}"
    data-regulations="${regulationAttr}"
    data-threat="${threatCategory.slug}"
    data-text="${escapeHTML(searchable)}">
  <div class="badge-row">
    <div class="badge">${escapeHTML(badge)}</div>
    <div class="severity ${severityClass(severityLabel)}">${escapeHTML(
    severityLabel
  )} Severity</div>
  </div>
  <div class="threat-tags">
    <span class="threat-chip threat-${threatCategory.slug}">
      ${escapeHTML(threatCategory.label)}
    </span>
    <span class="threat-chip threat-mitre">MITRE: ${escapeHTML(
      mitreTactics
    )}</span>
    <span class="threat-chip threat-surface">${escapeHTML(
      attackSurface
    )}</span>
  </div>
  <h2>${escapeHTML(title)}</h2>
  <p class="summary">${escapeHTML(description)}</p>
  <div class="meta-grid">
    ${buildMetaCard("Risk Score", riskScore, "Threat-model provided score")}
    ${buildMetaCard("Created", createdAt, region)}
    ${buildMetaCard(
      "Primary Resource",
      resourceType,
      truncate(resourceId, 80)
    )}
    ${buildMetaCard("Service", groupedService.label, truncate(attackSurface, 60))}
    ${buildMetaCard("Threat", threatCategory.label, threatCategory.synopsis)}
  </div>
  <div class="diagram">
    <div class="flow">
      <h3>Threat Flow</h3>
      <ol class="flowline">
        ${flowlineItems
          .map(
            (step) =>
              `<li><strong>${escapeHTML(step.label)}</strong>${escapeHTML(
                step.value
              )}</li>`
          )
          .join("\n")}
      </ol>
      <div class="stage-grid">
        ${stageGrid
          .map(
            (stage) => `<div class="stage">
          <div class="stage-icon">${stage.icon}</div>
          <strong>${escapeHTML(stage.heading)}</strong>
          <span>${escapeHTML(stage.detail)}</span>
        </div>`
          )
          .join("\n")}
      </div>
      <div class="legend">
        <span><i class="risk"></i>Resource</span>
        <span><i class="detect"></i>Region</span>
        <span><i class="mitre"></i>MITRE</span>
        <span><i class="impact"></i>Impact</span>
      </div>
    </div>
    <div class="flow">
      <h3>Response Considerations</h3>
      <ul>
        ${buildList(recommendationList)}
      </ul>
      <div class="highlight-box">
        <h4>Signals & Tags</h4>
        <ul>
          <li>Types: ${escapeHTML(typesList.join(", ") || "Unspecified")}</li>
          <li>Workflow: ${escapeHTML(
            finding?.Workflow?.status ?? "UNSPECIFIED"
          )}</li>
          <li>Account: ${escapeHTML(finding?.AwsAccountId ?? "Unknown")}</li>
          <li>Regulations: ${escapeHTML(
            regulations.join(", ") || "Not referenced"
          )}</li>
          <li>AI/ML Focus: ${isAi ? "Yes" : "General Cloud"}</li>
        </ul>
      </div>
    </div>
  </div>
</article>`;

  return {
    html: article,
    meta: {
      serviceSlug: groupedService.slug,
      serviceLabel: groupedService.label,
      severity: severityLabel,
      compliance,
      cloudZone,
      isAi,
      regulations,
      threatSlug: threatCategory.slug,
      threatLabel: threatCategory.label,
    },
  };
}

function buildDocument(body, count, filterMeta) {
  const generatedAt = new Date().toLocaleString("en-US", {
    dateStyle: "medium",
    timeStyle: "short",
  });
  const serviceOptions = Array.from(filterMeta.services.entries()).sort((a, b) =>
    a[1].localeCompare(b[1])
  );
  const severityOptions = Array.from(filterMeta.severity)
    .map((value) => value.toUpperCase())
    .sort();
  const complianceOptions = Array.from(filterMeta.compliance)
    .map((value) => value.toUpperCase())
    .sort();
  const cloudOptions = Array.from(filterMeta.cloud).sort();
  const regulationOptions = Array.from(filterMeta.regulations).sort();
  const threatOptions = Array.from(filterMeta.threats.entries()).sort((a, b) =>
    a[1].localeCompare(b[1])
  );
  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>AWS Security Findings · Visual Storyboards</title>
  <style>
    :root {
      --bg: #eef1ff;
      --card: #fff;
      --ink: #1c2040;
      --muted: #6c7095;
      --accent: #7b5bff;
      --accent-2: #ff6db6;
      --border: #dfe2f5;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      font-family: "Inter", "Segoe UI", sans-serif;
      background: var(--bg);
      color: var(--ink);
      padding-bottom: 80px;
    }
    .hero {
      padding: 60px 24px 110px;
      background: radial-gradient(circle at 20% 20%, rgba(255,255,255,0.25), transparent 60%),
                  linear-gradient(135deg, var(--accent), var(--accent-2));
      color: white;
      text-align: center;
      border-bottom-left-radius: 40px;
      border-bottom-right-radius: 40px;
      box-shadow: 0 20px 60px rgba(34, 23, 95, 0.4);
    }
    .hero h1 {
      margin: 0 0 16px;
      font-size: 44px;
    }
    .hero p {
      margin: 0 auto;
      max-width: 780px;
      line-height: 1.7;
      font-size: 18px;
      opacity: 0.95;
    }
    main {
      margin: -90px auto 0;
      padding: 0 24px;
      max-width: 1200px;
    }
    .issue {
      background: var(--card);
      border-radius: 36px;
      padding: 40px;
      box-shadow: 0 25px 80px rgba(24, 27, 70, 0.12);
      margin-bottom: 36px;
      border: 1px solid var(--border);
    }
    .issue[data-aiml="true"] {
      border-image: linear-gradient(120deg, #7b5bff, #2fdaa6) 1;
      border-width: 2px;
    }
    .threat-tags {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      margin-bottom: 12px;
    }
    .threat-chip {
      padding: 6px 14px;
      border-radius: 999px;
      font-size: 12px;
      letter-spacing: 0.5px;
      text-transform: uppercase;
      color: #2f2a4a;
      background: #f4f5ff;
      border: 1px solid rgba(123, 91, 255, 0.18);
      display: inline-flex;
      align-items: center;
      gap: 6px;
    }
    .threat-chip.threat-data-exfiltration { background: rgba(255, 108, 141, 0.15); border-color: rgba(255,108,141,0.5); }
    .threat-chip.threat-credential-abuse { background: rgba(255, 196, 87, 0.2); border-color: rgba(255,196,87,0.5); }
    .threat-chip.threat-network-exposure { background: rgba(106, 206, 255, 0.2); border-color: rgba(106,206,255,0.5); }
    .threat-chip.threat-ai-ml-integrity { background: rgba(127, 147, 255, 0.2); border-color: rgba(127,147,255,0.6); }
    .threat-chip.threat-visibility-gap { background: rgba(164, 173, 255, 0.18); }
    .threat-chip.threat-misconfiguration { background: rgba(160, 237, 201, 0.25); }
    .threat-chip.threat-mitre { background: rgba(127,127,255,0.18); text-transform: none; }
    .threat-chip.threat-surface { background: rgba(255,255,255,0.4); text-transform: none; }
    .badge-row {
      display: flex;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 10px;
      margin-bottom: 16px;
    }
    .badge {
      background: rgba(123, 91, 255, 0.1);
      color: var(--accent);
      padding: 6px 16px;
      border-radius: 999px;
      text-transform: uppercase;
      font-size: 11px;
      font-weight: 700;
      letter-spacing: 1px;
    }
    .severity {
      text-transform: uppercase;
      letter-spacing: 1px;
      font-size: 12px;
      font-weight: 800;
      padding: 6px 20px;
      border-radius: 999px;
      color: white;
      box-shadow: 0 6px 16px rgba(0,0,0,0.12);
    }
    .sev-critical { background: linear-gradient(90deg, #ff4d4f, #ff7b92); }
    .sev-high { background: linear-gradient(90deg, #ff9f43, #ffcc5c); }
    .sev-medium { background: linear-gradient(90deg, #f8c12d, #ffd966); color: #4a3200; }
    .sev-low { background: linear-gradient(90deg, #2fdaa6, #52e2d2); color: #06322a; }
    .issue h2 {
      margin: 0 0 14px;
      font-size: 30px;
    }
    .summary {
      margin: 0 0 24px;
      color: var(--muted);
      line-height: 1.7;
      font-size: 16px;
    }
    .meta-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
      gap: 16px;
      margin-bottom: 28px;
    }
    .meta-card {
      padding: 16px 18px;
      border-radius: 18px;
      background: #f8f9ff;
      border: 1px solid var(--border);
    }
    .meta-card span {
      font-size: 12px;
      letter-spacing: 0.8px;
      text-transform: uppercase;
      color: #8a8fb8;
    }
    .meta-card strong {
      display: block;
      font-size: 24px;
      margin: 6px 0 4px;
    }
    .meta-card small {
      color: var(--muted);
      font-size: 12px;
    }
    .diagram {
      display: flex;
      flex-wrap: wrap;
      gap: 20px;
    }
    .flow {
      flex: 1 1 360px;
      padding: 26px;
      border-radius: 26px;
      background: linear-gradient(145deg, #f9fbff, #eef1ff);
      border: 1px solid var(--border);
      box-shadow: inset 0 0 0 1px rgba(255,255,255,0.3);
    }
    .flow h3 {
      margin-top: 0;
      font-size: 14px;
      text-transform: uppercase;
      letter-spacing: 1.2px;
      color: var(--muted);
    }
    .flowline {
      list-style: none;
      padding-left: 0;
      margin: 0 0 20px;
      position: relative;
    }
    .flowline li {
      padding-left: 36px;
      margin-bottom: 14px;
      position: relative;
      color: var(--muted);
      line-height: 1.4;
    }
    .flowline li strong { color: var(--ink); display: block; }
    .flowline li::before {
      content: '';
      position: absolute;
      left: 12px;
      top: 6px;
      width: 10px;
      height: 10px;
      background: var(--accent);
      border-radius: 50%;
      box-shadow: 0 0 0 4px rgba(123,91,255,0.15);
    }
    .flowline::after {
      content: '';
      position: absolute;
      left: 16px;
      top: 0;
      bottom: 14px;
      width: 2px;
      background: linear-gradient(180deg, rgba(123,91,255,0.3), rgba(123,91,255,0));
    }
    .stage-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
      gap: 14px;
    }
    .stage {
      border-radius: 20px;
      padding: 16px;
      background: white;
      border: 1px solid var(--border);
      min-height: 150px;
      position: relative;
      overflow: hidden;
    }
    .stage-icon {
      width: 38px;
      height: 38px;
      border-radius: 12px;
      background: rgba(123,91,255,0.12);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 18px;
      margin-bottom: 10px;
    }
    .stage strong { display: block; margin-bottom: 6px; }
    .stage span { color: var(--muted); font-size: 13px; line-height: 1.4; }
    .stage::after {
      content: '';
      position: absolute;
      inset: 0;
      border-radius: 20px;
      background: linear-gradient(145deg, rgba(123,91,255,0.05), transparent);
      pointer-events: none;
    }
    .legend {
      display: flex;
      flex-wrap: wrap;
      gap: 12px;
      margin-top: 16px;
      font-size: 12px;
      color: var(--muted);
    }
    .legend span {
      display: inline-flex;
      align-items: center;
      gap: 6px;
    }
    .legend i {
      display: inline-block;
      width: 14px;
      height: 14px;
      border-radius: 4px;
    }
    .legend .risk { background: #ff8c8c; }
    .legend .detect { background: #8cc5ff; }
    .legend .mitre { background: #ffc36c; }
    .legend .impact { background: #9df0d1; }
    .flow ul {
      margin: 0;
      padding-left: 18px;
      color: var(--muted);
    }
    .flow li { margin-bottom: 10px; }
    .highlight-box {
      margin-top: 26px;
      padding: 22px;
      border-radius: 24px;
      background: #fff8ef;
      border-left: 6px solid #ffb97c;
    }
    .highlight-box h4 { margin: 0 0 10px; }
    .highlight-box ul { margin: 0; padding-left: 22px; }
    .highlight-box li { margin-bottom: 8px; }
    .filters-panel {
      background: #ffffff;
      margin-bottom: 32px;
      border-radius: 28px;
      padding: 24px;
      box-shadow: 0 20px 60px rgba(16, 20, 60, 0.12);
      border: 1px solid var(--border);
      display: flex;
      flex-wrap: wrap;
      gap: 18px;
      align-items: flex-end;
    }
    .filter-control {
      flex: 1 1 160px;
      display: flex;
      flex-direction: column;
      gap: 6px;
    }
    .filter-control label {
      font-size: 12px;
      text-transform: uppercase;
      letter-spacing: 1px;
      color: var(--muted);
    }
    .filter-control select,
    .filter-control input[type="text"] {
      border-radius: 999px;
      border: 1px solid var(--border);
      padding: 10px 16px;
      font-size: 14px;
      background: #f7f8ff;
      color: var(--ink);
    }
    .chip-group {
      display: flex;
      gap: 12px;
      flex-wrap: wrap;
    }
    .chip-group label {
      background: #f4f5ff;
      padding: 6px 14px;
      border-radius: 999px;
      font-size: 12px;
      color: var(--muted);
      display: inline-flex;
      align-items: center;
      gap: 6px;
    }
    .results-info {
      flex: 1 1 120px;
      font-size: 14px;
      color: var(--muted);
      text-align: right;
    }
    @media (max-width: 720px) {
      .issue { padding: 28px; }
      .diagram { flex-direction: column; }
      .filters-panel { flex-direction: column; }
      .results-info { text-align: left; }
    }
  </style>
</head>
<body>
  <header class="hero">
    <h1>AWS Security Findings Visual Storyboard</h1>
    <p>
      ${count} AWS Security Hub findings translated into diagram-rich narratives. Generated ${generatedAt}.
      Use the filters below to zero in on services, threat archetypes (Data Exfiltration, Credential Abuse, AI/ML integrity, network exposure), severity bands, geographic clouds, compliance stance, and AI/ML workloads.
    </p>
  </header>
  <main>
    <section class="filters-panel">
      <div class="filter-control filter-control--search">
        <label for="filter-search">Search</label>
        <input type="text" id="filter-search" placeholder="Search findings, resources, MITRE IDs... (use “-term” or “NOT term” to exclude)" />
      </div>
      <div class="filter-control">
        <label for="filter-service">Service / Resource</label>
        <select id="filter-service">
          <option value="all">All Services</option>
          ${serviceOptions
            .map(
              ([slug, label]) =>
                `<option value="${slug}">${escapeHTML(label)}</option>`
            )
            .join("\n")}
        </select>
      </div>
      <div class="filter-control">
        <label for="filter-threat">Threat Profile</label>
        <select id="filter-threat">
          <option value="all">All Threats</option>
          ${threatOptions
            .map(
              ([slug, label]) =>
                `<option value="${slug}">${escapeHTML(label)}</option>`
            )
            .join("\n")}
        </select>
      </div>
      <div class="filter-control">
        <label for="filter-severity">Severity</label>
        <select id="filter-severity">
          <option value="all">All Severities</option>
          ${severityOptions
            .map(
              (value) =>
                `<option value="${value.toLowerCase()}">${escapeHTML(
                  value
                )}</option>`
            )
            .join("\n")}
        </select>
      </div>
      <div class="filter-control">
        <label for="filter-compliance">Compliance State</label>
        <select id="filter-compliance">
          <option value="all">All States</option>
          ${complianceOptions
            .map(
              (value) =>
                `<option value="${value.toLowerCase()}">${escapeHTML(
                  value
                )}</option>`
            )
            .join("\n")}
        </select>
      </div>
      <div class="filter-control">
        <label for="filter-cloud">Cloud Geography</label>
        <select id="filter-cloud">
          <option value="all">All Regions</option>
          ${cloudOptions
            .map(
              (value) =>
                `<option value="${value}">${escapeHTML(
                  titleCase(value.replace("-", " "))
                )}</option>`
            )
            .join("\n")}
        </select>
      </div>
      <div class="filter-control">
        <label>AI / ML</label>
        <div class="chip-group">
          <label><input type="checkbox" id="filter-aiml" /> Focus only</label>
        </div>
      </div>
      <div class="filter-control">
        <label>Regulations</label>
        <div class="chip-group">
          ${regulationOptions
            .map(
              (reg) =>
                `<label><input type="checkbox" value="${reg.toLowerCase()}" class="filter-regulation" /> ${escapeHTML(
                  reg
                )}</label>`
            )
            .join("\n")}
        </div>
      </div>
      <div class="results-info">
        <strong id="result-count">${count}</strong> findings visible
      </div>
    </section>
    ${body}
  </main>
  <script>
    const filters = {
      search: document.getElementById('filter-search'),
      service: document.getElementById('filter-service'),
      severity: document.getElementById('filter-severity'),
      compliance: document.getElementById('filter-compliance'),
      cloud: document.getElementById('filter-cloud'),
      threat: document.getElementById('filter-threat'),
      aiml: document.getElementById('filter-aiml'),
      regulations: Array.from(document.querySelectorAll('.filter-regulation')),
    };
    const issues = Array.from(document.querySelectorAll('.issue'));
    const resultCount = document.getElementById('result-count');

    function applyFilters() {
      const serviceValue = filters.service.value;
      const severityValue = filters.severity.value;
      const complianceValue = filters.compliance.value;
      const cloudValue = filters.cloud.value;
      const searchValue = filters.search.value.trim().toLowerCase();
      const searchTokens = searchValue
        ? searchValue.split(/\s+/).filter(Boolean)
        : [];
      const includeTerms = [];
      const excludeTerms = [];
      for (let i = 0; i < searchTokens.length; i += 1) {
        const token = searchTokens[i];
        if (!token) continue;
        const nextToken = searchTokens[i + 1];
        if (token === "-" || token === "!" || token === "not") {
          if (nextToken) {
            excludeTerms.push(nextToken);
            i += 1;
          }
          continue;
        }
        if (token.startsWith("-") || token.startsWith("!")) {
          const term = token.slice(1);
          if (term) excludeTerms.push(term);
          continue;
        }
        includeTerms.push(token);
      }
      const threatValue = filters.threat.value;
      const aimlOnly = filters.aiml.checked;
      const regulationValues = filters.regulations
        .filter((input) => input.checked)
        .map((input) => input.value);

      let visible = 0;
      issues.forEach((issue) => {
        let show = true;
        if (serviceValue !== 'all' && issue.dataset.service !== serviceValue) {
          show = false;
        }
        if (severityValue !== 'all' && issue.dataset.severity !== severityValue) {
          show = false;
        }
        if (
          complianceValue !== 'all' &&
          issue.dataset.compliance !== complianceValue
        ) {
          show = false;
        }
        if (cloudValue !== 'all' && issue.dataset.cloud !== cloudValue) {
          show = false;
        }
        if (threatValue !== 'all' && issue.dataset.threat !== threatValue) {
          show = false;
        }
        if (aimlOnly && issue.dataset.aiml !== 'true') {
          show = false;
        }
        if (regulationValues.length) {
          const regs = issue.dataset.regulations.split(' ');
          const matchesAll = regulationValues.every((reg) => regs.includes(reg));
          if (!matchesAll) show = false;
        }
        if (includeTerms.length || excludeTerms.length) {
          const haystackSource =
            issue.dataset.text || issue.innerText.toLowerCase() || "";
          const haystack = haystackSource.toLowerCase();
          if (
            includeTerms.length &&
            !includeTerms.every((term) => haystack.includes(term))
          ) {
            show = false;
          }
          if (
            excludeTerms.length &&
            excludeTerms.some((term) => haystack.includes(term))
          ) {
            show = false;
          }
        }
        issue.style.display = show ? '' : 'none';
        if (show) visible += 1;
      });
      resultCount.textContent = visible;
    }

    Object.entries(filters).forEach(([name, control]) => {
      if (Array.isArray(control)) {
        control.forEach((input) => input.addEventListener('change', applyFilters));
      } else if (control && typeof control.addEventListener === 'function') {
        const eventName = name === 'search' ? 'input' : 'change';
        control.addEventListener(eventName, applyFilters);
      }
    });
    applyFilters();
  </script>
</body>
</html>`;
}

function main() {
  const findings = loadFindings();
  const filterMeta = {
    services: new Map(),
    severity: new Set(),
    compliance: new Set(),
    cloud: new Set(),
    regulations: new Set(),
    threats: new Map(),
  };
  const articles = findings
    .map((finding, index) => {
      const { html, meta } = articleForFinding(finding, index);
      filterMeta.services.set(meta.serviceSlug, meta.serviceLabel);
      filterMeta.severity.add(meta.severity.toLowerCase());
      filterMeta.compliance.add((meta.compliance || "UNKNOWN").toLowerCase());
      filterMeta.cloud.add(meta.cloudZone);
      meta.regulations.forEach((reg) => filterMeta.regulations.add(reg));
      filterMeta.threats.set(meta.threatSlug, meta.threatLabel);
      return html;
    })
    .join("\n\n");
  if (filterMeta.regulations.size === 0) {
    ["HIPAA", "GDPR"].forEach((reg) => filterMeta.regulations.add(reg));
  }
  const document = buildDocument(articles, findings.length, filterMeta);
  fs.writeFileSync(OUTPUT, document, "utf8");
  console.log(`Wrote ${OUTPUT} with ${findings.length} findings.`);
}

main();
