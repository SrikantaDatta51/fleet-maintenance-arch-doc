#!/usr/bin/env python3
"""
Healthy Fleet Maintenance & Tenant-Safe Node Lifecycle
Architecture Design Document Generator

Generates a professional Word document (.docx) with rendered diagrams,
formatted tables with black borders, and enterprise-grade styling.

Author: Distinguished Engineer, AI Compute Platform
"""

import os
from datetime import datetime
from docx import Document
from docx.shared import Inches, Pt, Cm, RGBColor, Emu
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.section import WD_ORIENT
from docx.oxml.ns import qn, nsdecls
from docx.oxml import parse_xml

# =============================================================================
# Configuration
# =============================================================================
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DIAGRAMS_DIR = os.path.join(SCRIPT_DIR, "diagrams")
OUTPUT_FILE = os.path.join(SCRIPT_DIR, "Healthy_Fleet_Maintenance_Architecture_Design.docx")

# Colors
DARK_BLUE = RGBColor(0x1B, 0x3A, 0x5C)
MEDIUM_BLUE = RGBColor(0x2C, 0x5F, 0x8A)
ACCENT_BLUE = RGBColor(0x35, 0x72, 0xA5)
DARK_GRAY = RGBColor(0x33, 0x33, 0x33)
MEDIUM_GRAY = RGBColor(0x66, 0x66, 0x66)
LIGHT_GRAY = RGBColor(0xF2, 0xF2, 0xF2)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
BLACK = RGBColor(0x00, 0x00, 0x00)
HEADER_BG = RGBColor(0x1B, 0x3A, 0x5C)
ROW_ALT_BG = RGBColor(0xE8, 0xF0, 0xF8)

# =============================================================================
# Utility Functions
# =============================================================================

def set_cell_border(cell, **kwargs):
    """Set cell borders. Usage: set_cell_border(cell, top={"sz": 12, "val": "single", "color": "000000"})"""
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcBorders = parse_xml(f'<w:tcBorders {nsdecls("w")}></w:tcBorders>')
    for edge in ("start", "top", "end", "bottom", "insideH", "insideV"):
        if edge in kwargs:
            element = parse_xml(
                f'<w:{edge} {nsdecls("w")} w:val="{kwargs[edge]["val"]}" '
                f'w:sz="{kwargs[edge]["sz"]}" w:space="0" '
                f'w:color="{kwargs[edge]["color"]}"/>'
            )
            tcBorders.append(element)
    tcPr.append(tcBorders)


def set_cell_shading(cell, color_hex):
    """Set cell background color."""
    shading = parse_xml(
        f'<w:shd {nsdecls("w")} w:fill="{color_hex}" w:val="clear"/>'
    )
    cell._tc.get_or_add_tcPr().append(shading)


def apply_table_borders(table):
    """Apply black borders to the entire table."""
    tbl = table._tbl
    tblPr = tbl.tblPr if tbl.tblPr is not None else parse_xml(f'<w:tblPr {nsdecls("w")}></w:tblPr>')
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'  <w:top w:val="single" w:sz="6" w:space="0" w:color="000000"/>'
        f'  <w:start w:val="single" w:sz="6" w:space="0" w:color="000000"/>'
        f'  <w:bottom w:val="single" w:sz="6" w:space="0" w:color="000000"/>'
        f'  <w:end w:val="single" w:sz="6" w:space="0" w:color="000000"/>'
        f'  <w:insideH w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
        f'  <w:insideV w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)
    if tbl.tblPr is None:
        tbl.append(tblPr)


def style_header_row(row, font_size=9):
    """Style a table header row with dark blue background and white text."""
    for cell in row.cells:
        set_cell_shading(cell, "1B3A5C")
        for paragraph in cell.paragraphs:
            paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for run in paragraph.runs:
                run.font.color.rgb = WHITE
                run.font.bold = True
                run.font.size = Pt(font_size)
                run.font.name = "Calibri"


def style_data_row(row, index, font_size=8.5):
    """Style a data row with alternating colors."""
    bg = "E8F0F8" if index % 2 == 0 else "FFFFFF"
    for cell in row.cells:
        set_cell_shading(cell, bg)
        for paragraph in cell.paragraphs:
            for run in paragraph.runs:
                run.font.size = Pt(font_size)
                run.font.name = "Calibri"
                run.font.color.rgb = DARK_GRAY


def add_styled_heading(doc, text, level=1):
    """Add a styled heading."""
    heading = doc.add_heading(text, level=level)
    for run in heading.runs:
        run.font.color.rgb = DARK_BLUE
        run.font.name = "Calibri"
    return heading


def add_body_text(doc, text, bold=False, italic=False, font_size=10.5):
    """Add styled body text."""
    para = doc.add_paragraph()
    run = para.add_run(text)
    run.font.name = "Calibri"
    run.font.size = Pt(font_size)
    run.font.color.rgb = DARK_GRAY
    run.bold = bold
    run.italic = italic
    para.paragraph_format.space_after = Pt(6)
    para.paragraph_format.space_before = Pt(3)
    return para


def add_bullet(doc, text, level=0, bold_prefix="", font_size=10):
    """Add a styled bullet point."""
    para = doc.add_paragraph(style='List Bullet')
    if bold_prefix:
        run_bold = para.add_run(bold_prefix)
        run_bold.bold = True
        run_bold.font.name = "Calibri"
        run_bold.font.size = Pt(font_size)
        run_bold.font.color.rgb = DARK_GRAY
    run = para.add_run(text)
    run.font.name = "Calibri"
    run.font.size = Pt(font_size)
    run.font.color.rgb = DARK_GRAY
    para.paragraph_format.left_indent = Inches(0.25 + level * 0.25)
    return para


def add_diagram(doc, image_path, caption, width=Inches(6.0)):
    """Add a diagram with caption."""
    para = doc.add_paragraph()
    para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = para.add_run()
    if os.path.exists(image_path):
        run.add_picture(image_path, width=width)
    else:
        run.add_text(f"[Diagram: {caption} — image not found]")

    # Caption
    caption_para = doc.add_paragraph()
    caption_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    caption_run = caption_para.add_run(caption)
    caption_run.font.name = "Calibri"
    caption_run.font.size = Pt(9)
    caption_run.font.color.rgb = MEDIUM_GRAY
    caption_run.italic = True
    caption_para.paragraph_format.space_after = Pt(12)
    return para


def add_page_break(doc):
    """Add a page break."""
    doc.add_page_break()


def create_table_with_data(doc, headers, rows, col_widths=None):
    """Create a professionally styled table."""
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER

    # Header row
    for i, header in enumerate(headers):
        cell = table.rows[0].cells[i]
        cell.text = ""
        para = cell.paragraphs[0]
        run = para.add_run(header)
        run.bold = True
        run.font.name = "Calibri"

    style_header_row(table.rows[0])

    # Data rows
    for row_idx, row_data in enumerate(rows):
        for col_idx, value in enumerate(row_data):
            cell = table.rows[row_idx + 1].cells[col_idx]
            cell.text = ""
            para = cell.paragraphs[0]
            run = para.add_run(str(value))
            run.font.name = "Calibri"
        style_data_row(table.rows[row_idx + 1], row_idx)

    apply_table_borders(table)

    # Column widths
    if col_widths:
        for row in table.rows:
            for idx, width in enumerate(col_widths):
                row.cells[idx].width = Inches(width)

    doc.add_paragraph()  # spacing
    return table


# =============================================================================
# Document Sections
# =============================================================================

def add_cover_page(doc):
    """Create a professional cover page."""
    # Add spacing
    for _ in range(6):
        doc.add_paragraph()

    # Title
    title = doc.add_paragraph()
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = title.add_run("Healthy Fleet Maintenance\n& Tenant-Safe Node Lifecycle")
    run.font.size = Pt(32)
    run.font.color.rgb = DARK_BLUE
    run.font.name = "Calibri"
    run.bold = True

    # Subtitle
    subtitle = doc.add_paragraph()
    subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = subtitle.add_run("Architecture Design Document")
    run.font.size = Pt(18)
    run.font.color.rgb = MEDIUM_BLUE
    run.font.name = "Calibri"

    # Separator line
    sep = doc.add_paragraph()
    sep.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = sep.add_run("━" * 60)
    run.font.color.rgb = ACCENT_BLUE
    run.font.size = Pt(10)

    doc.add_paragraph()

    # Metadata table
    meta_data = [
        ("Document Classification", "Internal — Engineering"),
        ("Version", "1.0"),
        ("Date", datetime.now().strftime("%B %d, %Y")),
        ("Author", "Distinguished Engineer, AI Compute Platform"),
        ("Status", "Final Draft"),
        ("Review Board", "Compute Platform, K8s, OE, Network, DC Infra"),
    ]

    table = doc.add_table(rows=len(meta_data), cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, (key, value) in enumerate(meta_data):
        cell_key = table.rows[i].cells[0]
        cell_val = table.rows[i].cells[1]
        cell_key.text = ""
        cell_val.text = ""

        pk = cell_key.paragraphs[0]
        pk.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        rk = pk.add_run(key)
        rk.bold = True
        rk.font.name = "Calibri"
        rk.font.size = Pt(10)
        rk.font.color.rgb = DARK_BLUE

        pv = cell_val.paragraphs[0]
        rv = pv.add_run(value)
        rv.font.name = "Calibri"
        rv.font.size = Pt(10)
        rv.font.color.rgb = DARK_GRAY

        cell_key.width = Inches(2.5)
        cell_val.width = Inches(4.0)

    apply_table_borders(table)
    add_page_break(doc)


def add_toc_placeholder(doc):
    """Add table of contents."""
    add_styled_heading(doc, "Table of Contents", level=1)
    toc_items = [
        "1.  Executive Summary",
        "2.  Feature Description",
        "3.  Goals & Objectives",
        "4.  Scope Definition",
        "5.  Architecture Design",
        "6.  Infrastructure Callouts",
        "7.  End-to-End Test Plan",
        "8.  Enterprise Promises",
        "9.  Deployment, Observability & Operations",
        "10. Customer Impact",
        "Appendix A: Diagrams Index",
        "Appendix B: Glossary",
    ]
    for item in toc_items:
        p = doc.add_paragraph(item)
        p.paragraph_format.space_after = Pt(4)
        for run in p.runs:
            run.font.name = "Calibri"
            run.font.size = Pt(11)
            run.font.color.rgb = DARK_GRAY

    add_page_break(doc)


def add_executive_summary(doc):
    """Section 1: Executive Summary."""
    add_styled_heading(doc, "1. Executive Summary", level=1)

    add_body_text(doc,
        "This architecture design document defines the Healthy Fleet Maintenance & Tenant-Safe Node Lifecycle "
        "platform feature. It establishes a deterministic, automated state transition model for GPU compute nodes, "
        "ensuring that every node serving a tenant workload meets a codified \"good host\" standard and that node "
        "movement between tenants follows a secure, clean lifecycle."
    )

    add_body_text(doc,
        "The feature addresses four foundational platform challenges:"
    )

    add_bullet(doc, " Sustaining 99.5% fleet availability through a buffer pool model with rapid remediation and "
               "a defined exception path when buffer capacity is constrained.", bold_prefix="Fleet Availability:")
    add_bullet(doc, " Automating node lifecycle management using Node Problem Detector (NPD) and custom controllers "
               "to detect host-level degradation and enforce tenant safety through cordon/taint semantics.", bold_prefix="Lifecycle Automation:")
    add_bullet(doc, " Codifying a certification pipeline below the Kubernetes layer using BCM burn-in and DCGM/DCGMI "
               "diagnostics as the standard SOP, enforced before tenant attachment and after every repair or RMA cycle.", bold_prefix="Node Certification:")
    add_bullet(doc, " Enforcing a fixed state transition for tenant reassignment: "
               "Buffer(healthy) → Tenant X → Buffer(healthy) → Tenant Y, always including re-image, disk wipe, "
               "recertification, and host network reconfiguration.", bold_prefix="Tenant Reassignment:")

    add_body_text(doc,
        "The design philosophy is tenant-first: unhealthy nodes are prevented from serving tenants through consistent "
        "detection and enforcement mechanisms. The operational model starts with a dedicated L1 support squad using "
        "runbooks and daily triage (Phase 1), transitioning to automation-first operations as the platform matures (Phase 2). "
        "Learnings from Incident 5337 (multi-node distributed training failure) are incorporated throughout."
    )

    # Mind map diagram
    add_diagram(doc,
        os.path.join(DIAGRAMS_DIR, "01_mindmap_overview.png"),
        "Figure 1: Healthy Fleet Maintenance — Four-Pillar Problem Space Overview"
    )

    add_page_break(doc)


def add_feature_description(doc):
    """Section 2: Feature Description."""
    add_styled_heading(doc, "2. Feature Description", level=1)

    add_body_text(doc,
        "Healthy Fleet Maintenance & Tenant-Safe Node Lifecycle is a platform feature that ensures GPU compute nodes "
        "are continuously maintained in a tenant-safe, certifiable state and can be moved between tenants via a "
        "deterministic, automated state transition."
    )

    add_styled_heading(doc, "2.1 Problem Statement", level=2)
    add_body_text(doc, "The feature solves four critical platform problems:")

    problems = [
        ("Healthy Fleet Maintenance",
         "Sustain 99.5% availability using a buffer pool model and rapid remediation/return-to-fleet workflows, "
         "including explicit exception handling when buffer is constrained."),
        ("Automated Node Lifecycle",
         "Use NPD + controllers to detect host-level issues and enforce tenant safety through cordon/taint, "
         "with a phased approach from people-driven ops to full automation."),
        ("Automated Node Certification",
         "Enforce BCM burn-in and DCGM/DCGMI diagnostics as the standard SOP below the Kubernetes layer, "
         "required before tenant attachment and after repairs/RMA."),
        ("Automated Tenant Reassignment",
         "Implement a fixed state transition: Buffer(healthy) → Tenant X → Buffer(healthy) → Tenant Y, "
         "always including re-image, disk wipe, recertification, and host network reconfiguration."),
    ]

    for title, desc in problems:
        add_bullet(doc, f" {desc}", bold_prefix=f"{title}:")

    add_styled_heading(doc, "2.2 Design Philosophy", level=2)
    add_body_text(doc,
        "The design is tenant-first: unhealthy nodes are prevented from serving tenants through consistent detection "
        "and enforcement mechanisms. Operationally, the feature is supported by a people + process foundation: "
        "a dedicated L1 support squad operating with runbooks, daily triage, and strict time-to-recover targets, "
        "which transitions to automation-first operations as the platform matures."
    )
    add_body_text(doc,
        "Learnings from Incident 5337 (multi-node job failure) are incorporated to strengthen multi-node readiness "
        "and faster quarantine of repeat offenders."
    )
    add_page_break(doc)


def add_goals_objectives(doc):
    """Section 3: Goals & Objectives."""
    add_styled_heading(doc, "3. Goals & Objectives", level=1)

    add_styled_heading(doc, "3.1 Primary Goals", level=2)

    goals = [
        ("Tenant Safety by Default",
         "No tenant scheduling on nodes that are degraded, suspect, or uncertified."),
        ("99.5% Availability with Buffer Strategy",
         "Maintain enough healthy buffer capacity and a deterministic recovery workflow to sustain availability; "
         "define explicit exception behavior when buffer is insufficient."),
        ("Zero Ambiguity on \"Good Host\"",
         "Codify the minimum host requirements for GPU and multi-node workloads "
         "(GPU + IB/RDMA + Kubernetes node readiness + tenant networking correctness)."),
        ("Two-Phase Execution",
         "Phase 1: people-driven daily ops with a dedicated L1 squad and runbooks; strict 24-hour repair/return targets. "
         "Phase 2: automation-driven enforcement using NPD + controller workflows + BCM/DCGM tooling."),
        ("NPD as a Platform",
         "Enable multiple teams (Compute Platform, K8s, OE, Network) to contribute detectors and tests under a single "
         "framework with standardized outputs (events/conditions/taints) and consistent enforcement semantics."),
    ]

    for i, (title, desc) in enumerate(goals, 1):
        add_bullet(doc, f" {desc}", bold_prefix=f"G{i}. {title}:")

    add_styled_heading(doc, "3.2 Secondary Goals", level=2)

    secondary = [
        "Prevent recurrence of distributed training failures by tightening multi-node prerequisites and correlation across nodes (Incident 5337 learnings).",
        "Reduce manual toil in node moves between tenants by enforcing a single state transition pipeline.",
        "Standardize on evidence capture and routing for hardware faults to accelerate vendor + RMA loops.",
    ]
    for s in secondary:
        add_bullet(doc, s)

    add_page_break(doc)


def add_scope(doc):
    """Section 4: Scope Definition."""
    add_styled_heading(doc, "4. Scope Definition", level=1)

    headers = ["Category", "In Scope", "Out of Scope"]
    rows = [
        ["People / Process Operations",
         "Dedicated L1 squad, runbooks, daily triage, escalation paths, reporting",
         "Owning tenant application ops/runbooks"],
        ["Host Certification\n(pre-tenant & post-fix)",
         "BCM burn-in, DCGM/DCGMI diagnostics, ECC checks, pass/fail tagging, evidence artifacts",
         "Tenant workload-level tests beyond host safety gating"],
        ["Node Lifecycle\nAutomation",
         "Buffer/tenant/quarantine state machine, cordon/taint, deterministic tenant reassignment flow",
         "Auto-reboot/auto-reimage unless explicitly approved"],
        ["Kubernetes Node\nBoundary",
         "Node readiness, kubelet/runtime stability, operator health (GPU/network), enforcement via taints/tolerations",
         "Tenant scheduling policy beyond enforcing \"don't schedule on unhealthy nodes\""],
        ["NVIDIA + K8s\nStack Layers",
         "GPU operator, network operator, IB SR-IOV, Multus, host driver/runtime integration",
         "Higher-layer tenant services and application SLO/SLA"],
        ["Host Networking /\nTenant Network",
         "IB readiness at node boundary; VLAN + routing via node routing agent; dependency contract with Network team",
         "Full network team domain ownership (fabric architecture/operations)"],
        ["Running Tenants\n(host-level impact)",
         "Host safety detection and quarantine while nodes serve tenants",
         "Application debugging, model/training code issues"],
        ["RMA Workflow",
         "Evidence capture, ticket routing, post-RMA recertification gate back to buffer",
         "Physical swap/shipping execution ownership (DC Infra + vendor)"],
    ]

    create_table_with_data(doc, headers, rows, col_widths=[1.8, 2.8, 2.4])
    add_page_break(doc)


def add_architecture_design(doc):
    """Section 5: Architecture Design."""
    add_styled_heading(doc, "5. Architecture Design", level=1)

    # 5.1 Layered View
    add_styled_heading(doc, "5.1 Layered Component View", level=2)
    add_body_text(doc, "The platform manages the following layers from hardware to application boundary:")

    layers = [
        ("Hardware", "GPU, HCA/NIC (InfiniBand), NVMe, BMC, CPU/Memory"),
        ("Host OS", "Kernel, drivers, filesystem, time sync, container runtime"),
        ("NVIDIA Stack", "BCM tooling, DCGM/DCGMI diagnostics"),
        ("Kubernetes Node Layer", "GPU operator, network operator, IB SR-IOV, Multus, NPD"),
        ("Tenant Network", "Node routing agent for VLAN/tenant routing; IB + VLAN dependencies with Network team"),
        ("Controller Layer", "compute-node-manager/controller for lifecycle and tenant assignments"),
    ]

    headers = ["Layer", "Components"]
    create_table_with_data(doc, headers, layers, col_widths=[2.0, 5.0])

    # 5.2 NPD as a Platform
    add_styled_heading(doc, "5.2 NPD as a Platform (Multi-Team Contribution Model)", level=2)
    add_body_text(doc,
        "Node Problem Detector (NPD) serves as the common substrate for node health detection and standardized outputs. "
        "It operates as a platform that multiple teams contribute to, centralizing health detection while preserving "
        "domain ownership of individual detectors."
    )

    add_styled_heading(doc, "Contribution Model", level=3)
    teams = [
        ("Compute Platform", "GPU + IB multi-node readiness detectors, certification gates, evidence capture hooks"),
        ("Kubernetes Team", "kubelet/runtime, node readiness, nodefs/imagefs pressure detectors and enforcement wiring"),
        ("OE Team", "Host OS and hardware-facing detectors (kernel, drivers, DCGM signal interpretation, time sync)"),
        ("Network Team", "Tenant VLAN/IB fabric validation hooks or APIs used by node routing agent checks"),
    ]
    for team, contribution in teams:
        add_bullet(doc, f" {contribution}", bold_prefix=f"{team}:")

    add_styled_heading(doc, "Standardized Outputs", level=3)
    outputs = [
        ("Node Events", "Human-readable audit trail for operational visibility"),
        ("Node Conditions", "Machine-readable state for controller consumption"),
        ("Taints", "Enforcement mechanism: NoSchedule / PreferNoSchedule"),
    ]
    for output_name, desc in outputs:
        add_bullet(doc, f" {desc}", bold_prefix=f"{output_name}:")

    add_diagram(doc,
        os.path.join(DIAGRAMS_DIR, "04_npd_platform.png"),
        "Figure 2: NPD as a Platform — Multi-Team Contribution Model"
    )

    # 5.3 Good Host Definition
    add_styled_heading(doc, "5.3 \"Good Host\" Definition (Tenant-Eligibility Requirements)", level=2)
    add_body_text(doc,
        "A node must satisfy ALL of the following requirements to be considered tenant-eligible. "
        "These requirements constitute the codified \"good host\" standard:"
    )

    add_styled_heading(doc, "GPU Health", level=3)
    gpu_checks = [
        "DCGM/DCGMI diagnostics pass at required level",
        "ECC within thresholds; no critical ECC escalation",
        "No repeating critical XID classes within a defined window (policy-defined)",
        "GPU operator healthy and reporting",
    ]
    for c in gpu_checks:
        add_bullet(doc, c)

    add_styled_heading(doc, "Network + Multi-Node Readiness", level=3)
    net_checks = [
        "IB interface up and stable; link flaps under threshold",
        "IB error counters under thresholds; SR-IOV VFs healthy",
        "Network operator healthy; Multus configuration correct",
        "Node routing agent applied; VLAN/tenant routing validated",
    ]
    for c in net_checks:
        add_bullet(doc, c)

    add_styled_heading(doc, "Node + OS Health", level=3)
    os_checks = [
        "Node Ready; kubelet and runtime stable",
        "Filesystem not read-only; no repeated kernel panic signatures",
        "Storage health not degraded (SMART/media errors, IO errors)",
        "Meets SKU allocatable expectations (including ephemeral constraints if relevant)",
    ]
    for c in os_checks:
        add_bullet(doc, c)

    # Good host table
    headers = ["Category", "Check", "Threshold / Criteria"]
    good_host_table = [
        ["GPU Health", "DCGM/DCGMI diagnostics", "Pass at Level 3 (default)"],
        ["GPU Health", "ECC error rate", "< threshold per 24h window"],
        ["GPU Health", "XID critical events", "No repeating critical XIDs in defined window"],
        ["GPU Health", "GPU operator status", "Healthy, all pods Running"],
        ["Network", "IB link status", "Up, stable, flaps < threshold"],
        ["Network", "IB error counters", "Below vendor-defined thresholds"],
        ["Network", "SR-IOV VFs", "All VFs healthy and available"],
        ["Network", "Multus configuration", "Correct, validated against expected spec"],
        ["Node/OS", "Node readiness", "Ready condition = True"],
        ["Node/OS", "Filesystem", "Not read-only; no panic signatures"],
        ["Node/OS", "Storage (SMART)", "No media errors, IO errors < threshold"],
        ["Node/OS", "Allocatable resources", "Meets SKU expectations"],
    ]
    create_table_with_data(doc, headers, good_host_table, col_widths=[1.5, 2.5, 3.0])

    add_page_break(doc)

    # 5.4 Core Workflow
    add_styled_heading(doc, "5.4 Core Workflow: Detect → Self-Heal → Enforce → Recover", level=2)
    add_body_text(doc,
        "The core operational workflow follows a deterministic path from signal detection to resolution. "
        "Self-heal is allowed only for an explicit allowlist (example: reset IB interface) with bounded retries "
        "and strict time windows. Otherwise, the default action is quarantine."
    )

    add_diagram(doc,
        os.path.join(DIAGRAMS_DIR, "03_workflow_diagram.png"),
        "Figure 3: Detection → Enforcement → Recovery Workflow"
    )

    add_styled_heading(doc, "Workflow Phases", level=3)
    phases = [
        ("Detection", "NPD detectors and custom plugins monitor host signals (GPU, IB, filesystem, kubelet, runtime). "
                      "Detectors produce standardized Node Events, Node Conditions, and taint/cordon recommendations."),
        ("Self-Heal (Conditional)", "For allowlisted conditions only (e.g., IB interface reset), bounded retry with "
                                   "strict time window. Recovery clears transient state; failure escalates to quarantine."),
        ("Enforcement", "Quarantine via cordon + taint (NoSchedule). Scheduling is immediately prevented on the node. "
                       "Alert and ticket routing are triggered."),
        ("Recovery", "Repair/RMA workflow. Post-fix recertification is mandatory (BCM burn-in + DCGM/DCGMI). "
                    "Only a passing recertification returns the node to BUFFER_HEALTHY."),
    ]
    for phase, desc in phases:
        add_bullet(doc, f" {desc}", bold_prefix=f"{phase}:")

    add_page_break(doc)

    # 5.5 State Machine
    add_styled_heading(doc, "5.5 Node Lifecycle & Tenant Reassignment State Model", level=2)
    add_body_text(doc,
        "The node lifecycle is modeled as a finite state machine with five states and deterministic transitions. "
        "Every tenant reassignment must traverse through BUFFER_HEALTHY, ensuring re-image, disk wipe, recertification, "
        "and network reconfiguration occur before a node can serve a new tenant."
    )

    add_diagram(doc,
        os.path.join(DIAGRAMS_DIR, "02_state_machine.png"),
        "Figure 4: Node Lifecycle State Machine"
    )

    # State descriptions table
    headers = ["State", "Description", "Entry Condition", "Exit Condition"]
    states = [
        ["BUFFER_HEALTHY", "Node is healthy, certified, and available for tenant assignment",
         "Initial provisioning OR recertification pass", "Tenant attachment OR blocking signal"],
        ["TENANT_ASSIGNED", "Node is actively serving a tenant workload",
         "Attach tenant label from BUFFER_HEALTHY", "Detach + recertify OR blocking signal"],
        ["QUARANTINED", "Node has a blocking signal; removed from scheduling",
         "Blocking signal from any active state", "Triage initiated → REPAIR_IN_PROGRESS"],
        ["REPAIR_IN_PROGRESS", "Node is undergoing triage, fix, or RMA process",
         "Triage/fix/RMA initiated", "Fix complete → RECERTIFY"],
        ["RECERTIFY", "Node undergoing BCM burn-in + DCGM/DCGMI diagnostics",
         "Repair/fix complete", "Pass → BUFFER_HEALTHY; Fail → QUARANTINED"],
    ]
    create_table_with_data(doc, headers, states, col_widths=[1.5, 2.0, 1.8, 1.7])

    add_page_break(doc)

    # 5.6 Buffer Pool Strategy
    add_styled_heading(doc, "5.6 Buffer Pool Strategy & Fleet Availability Model", level=2)
    add_body_text(doc,
        "The buffer pool strategy is the mechanism by which 99.5% fleet availability is sustained. "
        "The fleet is partitioned into four pools, with strict flow constraints between them."
    )

    add_diagram(doc,
        os.path.join(DIAGRAMS_DIR, "05_buffer_strategy.png"),
        "Figure 5: Buffer Pool Strategy & Fleet Availability Model"
    )

    # Availability modes table
    headers = ["Mode", "Buffer Status", "Operational Behavior"]
    modes = [
        ["Normal Mode", "Buffer ≥ Threshold",
         "Standard operations. Tenant assignment proceeds without restriction. "
         "Buffer replenishment via repair/recertification pipeline."],
        ["Constrained Mode", "Buffer approaching minimum",
         "Heightened alerting. Repair velocity is escalated. "
         "L1 squad reports buffer status in daily triage."],
        ["Exception Mode", "Buffer below minimum",
         "Audited, time-bounded exceptions. Explicit approval required for any "
         "tenant assignment from constrained buffer. All exceptions logged and reviewed."],
    ]
    create_table_with_data(doc, headers, modes, col_widths=[1.5, 2.0, 3.5])

    add_page_break(doc)


def add_infrastructure_callouts(doc):
    """Section 6: Infrastructure Callouts."""
    add_styled_heading(doc, "6. Infrastructure Callouts", level=1)

    add_styled_heading(doc, "6.1 Fleet Operations Foundation (People + Process)", level=2)
    add_body_text(doc, "The operational foundation is a dedicated L1 squad with the following structure:")

    add_bullet(doc, "Runbooks per failure category (GPU, IB, OS, Kubernetes node, disk)", bold_prefix="Runbooks: ")
    add_bullet(doc, "Daily triage cadence and daily fleet health report", bold_prefix="Daily Triage: ")
    add_bullet(doc, "Defined escalation matrix and paging rules", bold_prefix="Escalation: ")

    add_styled_heading(doc, "Operating Targets", level=3)
    headers = ["Issue Category", "Target", "SLA Commitment"]
    targets = [
        ["Non-hardware issues", "Return node to fleet within 24 hours", "L1 squad accountability"],
        ["Hardware issues", "Evidence capture and ticket initiation same day", "RMA path with DC Infra SLA"],
        ["Critical buffer impact", "Immediate escalation and exception mode activation", "Management notification"],
    ]
    create_table_with_data(doc, headers, targets, col_widths=[2.0, 2.5, 2.5])

    add_styled_heading(doc, "6.2 Tooling Stack", level=2)
    tools = [
        ("BCM Burn-in", "Host reprovision/wipe workflows and burn-in phase certification"),
        ("DCGM/DCGMI", "GPU diagnostics as certification gates at configurable diagnostic levels"),
        ("NPD Plugins", "Custom plugins for GPU/IB-specific checks and multi-node readiness validation"),
        ("Node Routing Agent", "VLAN/tenant network configuration (dependency on Network team)"),
        ("Ticket Routing Automation", "Auto-label and auto-route tickets to appropriate teams"),
    ]
    for tool_name, desc in tools:
        add_bullet(doc, f" {desc}", bold_prefix=f"{tool_name}:")

    add_styled_heading(doc, "6.3 Incident 5337 Integration", level=2)
    add_body_text(doc,
        "Multi-node job failure learnings from Incident 5337 drive the following enhancements:"
    )
    i5337 = [
        "Stricter IB readiness thresholds for multi-node workloads",
        "Correlation across node sets participating in a distributed job",
        "Faster quarantine of repeat offenders (nodes with recurring failures)",
        "Buffer-tenant testing includes multi-node smoke checks, not only single-node checks",
    ]
    for item in i5337:
        add_bullet(doc, item)

    add_page_break(doc)


def add_test_plan(doc):
    """Section 7: End-to-End Test Plan."""
    add_styled_heading(doc, "7. End-to-End Test Plan", level=1)

    add_styled_heading(doc, "7.1 Test Layers", level=2)

    headers = ["Test Layer", "What We Validate", "Where It Runs"]
    tests = [
        ["Pre-Tenant Certification",
         "BCM burn-in pass; DCGM diagnostics pass; ECC thresholds; GPU/network operators healthy",
         "Buffer pool / certification pipeline"],
        ["Node Readiness",
         "Node Ready; kubelet/runtime stable; no FS read-only; disk health OK",
         "Continuous + pre-attach gates"],
        ["IB / Multi-Node Readiness",
         "IB link up, stable, counters within threshold; SR-IOV VFs healthy; Multus correct",
         "Continuous + pre-attach gates"],
        ["Tenant Networking",
         "Node routing agent applied; VLAN/tenant routing verified",
         "Pre-attach gates + periodic checks"],
        ["Enforcement",
         "On failure: taint/cordon applied; scheduling prevented; alerts fired",
         "Continuous"],
        ["Recovery",
         "Repair workflow clears faults; recertification required; node returns to buffer",
         "Post-fix"],
    ]
    create_table_with_data(doc, headers, tests, col_widths=[2.0, 3.0, 2.0])

    add_styled_heading(doc, "7.2 Multi-Node Tests (Incident 5337–Specific)", level=2)
    multi_tests = [
        "Synthetic distributed workload smoke test in buffer/default tenant (small scale, consistent repeatability)",
        "Cross-node connectivity/IB health validation for node set",
        "Correlation logic: job failure → suspect node identification → quarantine repeat offenders",
    ]
    for t in multi_tests:
        add_bullet(doc, t)

    add_styled_heading(doc, "7.3 Acceptance Criteria", level=2)
    criteria = [
        "A node cannot enter TENANT_ASSIGNED unless BUFFER_HEALTHY gates pass.",
        "Any blocking signal results in quarantine (cordon + taint) within a defined detection-to-quarantine SLO.",
        "No return-to-buffer without recertification pass (burn-in + DCGM/DCGMI).",
        "Tenant reassignment always follows reimage + disk wipe + recertification + network reconfig.",
    ]
    for i, c in enumerate(criteria, 1):
        add_bullet(doc, f" {c}", bold_prefix=f"AC-{i}:")

    add_page_break(doc)


def add_enterprise_promises(doc):
    """Section 8: Enterprise Promises."""
    add_styled_heading(doc, "8. Enterprise Promises (50,000-Foot View)", level=1)

    add_body_text(doc,
        "The following commitments represent the platform-level guarantees delivered by this feature:"
    )

    headers = ["#", "Promise", "How It Is Delivered"]
    promises = [
        ["1", "Tenant Safety by Default",
         "Unhealthy nodes are removed from scheduling automatically via NPD + taint enforcement."],
        ["2", "Predictable Availability",
         "Healthy buffer strategy plus rapid repair/recertification maintains 99.5% with defined exception handling."],
        ["3", "Deterministic Lifecycle",
         "All node moves between tenants follow the same secure, clean state transition."],
        ["4", "Operational Maturity",
         "Dedicated L1 squad and runbooks initially, transitioning to automation-first operations."],
        ["5", "Platform Extensibility",
         "NPD as a shared platform allows multiple teams to contribute health checks without fragmenting enforcement."],
    ]
    create_table_with_data(doc, headers, promises, col_widths=[0.5, 2.0, 4.5])

    add_page_break(doc)


def add_deployment_observability(doc):
    """Section 9: Deployment, Observability & Operations."""
    add_styled_heading(doc, "9. Deployment, Observability & Ongoing Operations", level=1)

    add_styled_heading(doc, "9.1 Staged Deployment Approach", level=2)

    headers = ["Stage", "Action", "Risk Posture"]
    stages = [
        ["Stage 1", "Deploy NPD baseline + dashboards (observe only)", "No enforcement — validation mode"],
        ["Stage 2", "Enable enforcement in buffer pool only", "Limited blast radius — buffer nodes only"],
        ["Stage 3", "Enforce gating for tenant attachment", "Tenant-impacting — requires rollback plan"],
        ["Stage 4", "Enable automated reassignment workflow", "Full automation — monitoring at max sensitivity"],
    ]
    create_table_with_data(doc, headers, stages, col_widths=[1.0, 3.0, 3.0])

    add_styled_heading(doc, "Feature Flags", level=3)
    flags = [
        "Allowlisted self-heal on/off",
        "Thresholds for XID/ECC/IB counters (configurable per SKU)",
        "Consent-based toleration policy",
    ]
    for f in flags:
        add_bullet(doc, f)

    add_styled_heading(doc, "9.2 Observability & Alerts", level=2)

    add_styled_heading(doc, "Dashboards", level=3)
    dashboards = [
        "Fleet by state: buffer healthy, tenant assigned, quarantined, recertifying",
        "Detection-to-quarantine latency (P50, P95, P99)",
        "Quarantine-to-recovery latency",
        "Certification pass/fail rate",
        "Repeat offender tracking (multi-node correlation)",
        "Buffer sufficiency vs shortage events",
    ]
    for d in dashboards:
        add_bullet(doc, d)

    add_styled_heading(doc, "Alerts", level=3)
    alerts_list = [
        "Blocking taint/cordon applied",
        "Certification failures",
        "Multi-node failure correlation spikes",
        "Consent toleration granted/used/expired",
        "Buffer below threshold (exception mode activated)",
    ]
    for a in alerts_list:
        add_bullet(doc, a)

    add_styled_heading(doc, "9.3 L1 Squad Daily Report Template", level=2)
    headers = ["Report Item", "Content"]
    report = [
        ["Unhealthy Nodes", "Node hostname, fault category, owner, ETA for resolution"],
        ["Returned to Fleet", "Nodes returned to buffer in last 24 hours, cause summary"],
        ["Escalated to Hardware/RMA", "Nodes escalated, evidence package status, vendor ticket #"],
        ["Buffer Health Summary", "Current buffer size, utilization %, any exceptions active"],
    ]
    create_table_with_data(doc, headers, report, col_widths=[2.5, 4.5])

    add_page_break(doc)


def add_customer_impact(doc):
    """Section 10: Customer Impact."""
    add_styled_heading(doc, "10. Customer Impact", level=1)

    add_styled_heading(doc, "10.1 Positive Impact", level=2)
    positives = [
        "Fewer tenant-visible failures caused by bad hosts",
        "Higher multi-node job success rate and fewer intermittent IB-related disruptions (Incident 5337 mitigation)",
        "Faster quarantine of problematic nodes reduces repeat failures",
        "Cleaner tenant isolation due to reimage + disk wipe in reassignment",
    ]
    for p in positives:
        add_bullet(doc, p)

    add_styled_heading(doc, "10.2 Tradeoffs & Exception Handling", level=2)
    tradeoffs = [
        "Stricter gating can temporarily reduce available capacity when buffer is constrained; exception mode must be explicit, audited, and time-bounded.",
        "Conservative remediation (cordon/taint first) increases reliance on repair velocity in Phase 1; Phase 2 automation reduces recovery time and human toil.",
    ]
    for t in tradeoffs:
        add_bullet(doc, t)

    add_page_break(doc)


def add_appendix_diagrams(doc):
    """Appendix A: Diagrams Index."""
    add_styled_heading(doc, "Appendix A: Diagrams Index", level=1)

    headers = ["Figure #", "Title", "Section"]
    diagrams = [
        ["Figure 1", "Healthy Fleet Maintenance — Four-Pillar Problem Space Overview", "Section 1"],
        ["Figure 2", "NPD as a Platform — Multi-Team Contribution Model", "Section 5.2"],
        ["Figure 3", " Detection → Enforcement → Recovery Workflow", "Section 5.4"],
        ["Figure 4", "Node Lifecycle State Machine", "Section 5.5"],
        ["Figure 5", "Buffer Pool Strategy & Fleet Availability Model", "Section 5.6"],
    ]
    create_table_with_data(doc, headers, diagrams, col_widths=[1.2, 4.0, 1.8])

    add_page_break(doc)


def add_appendix_glossary(doc):
    """Appendix B: Glossary."""
    add_styled_heading(doc, "Appendix B: Glossary", level=1)

    headers = ["Term", "Definition"]
    glossary = [
        ["BCM", "Bright Computing Manager — cluster management and provisioning platform"],
        ["DCGM", "NVIDIA Data Center GPU Manager — GPU monitoring and diagnostics"],
        ["DCGMI", "DCGM Interface — CLI tool for running GPU diagnostics"],
        ["ECC", "Error Correcting Code — memory error detection and correction mechanism"],
        ["HCA", "Host Channel Adapter — InfiniBand network interface card"],
        ["IB", "InfiniBand — high-performance, low-latency networking fabric"],
        ["Multus", "Kubernetes CNI plugin enabling multiple network interfaces per pod"],
        ["NPD", "Node Problem Detector — Kubernetes daemon for node health monitoring"],
        ["NVMe", "Non-Volatile Memory Express — storage interface protocol"],
        ["RMA", "Return Merchandise Authorization — hardware replacement process"],
        ["RDMA", "Remote Direct Memory Access — network data transfer technology"],
        ["SR-IOV", "Single Root I/O Virtualization — hardware virtualization for network devices"],
        ["VF", "Virtual Function — SR-IOV virtualized network interface"],
        ["XID", "NVIDIA GPU error identifier code"],
    ]
    create_table_with_data(doc, headers, glossary, col_widths=[1.5, 5.5])


# =============================================================================
# Main
# =============================================================================

def main():
    """Generate the architecture design document."""
    print("=" * 70)
    print("  Generating Architecture Design Document")
    print("=" * 70)

    doc = Document()

    # Page setup
    section = doc.sections[0]
    section.page_width = Inches(8.5)
    section.page_height = Inches(11)
    section.top_margin = Inches(0.8)
    section.bottom_margin = Inches(0.8)
    section.left_margin = Inches(0.9)
    section.right_margin = Inches(0.9)

    # Style defaults
    style = doc.styles['Normal']
    style.font.name = 'Calibri'
    style.font.size = Pt(10.5)
    style.font.color.rgb = DARK_GRAY

    # Heading styles
    for i in range(1, 4):
        heading_style = doc.styles[f'Heading {i}']
        heading_style.font.name = 'Calibri'
        heading_style.font.color.rgb = DARK_BLUE

    print("[1/12] Creating cover page...")
    add_cover_page(doc)

    print("[2/12] Adding table of contents...")
    add_toc_placeholder(doc)

    print("[3/12] Writing executive summary...")
    add_executive_summary(doc)

    print("[4/12] Writing feature description...")
    add_feature_description(doc)

    print("[5/12] Writing goals & objectives...")
    add_goals_objectives(doc)

    print("[6/12] Writing scope definition...")
    add_scope(doc)

    print("[7/12] Writing architecture design...")
    add_architecture_design(doc)

    print("[8/12] Writing infrastructure callouts...")
    add_infrastructure_callouts(doc)

    print("[9/12] Writing test plan...")
    add_test_plan(doc)

    print("[10/12] Writing enterprise promises...")
    add_enterprise_promises(doc)

    print("[11/12] Writing deployment & observability...")
    add_deployment_observability(doc)

    print("[12/12] Writing customer impact & appendices...")
    add_customer_impact(doc)
    add_appendix_diagrams(doc)
    add_appendix_glossary(doc)

    # Save
    doc.save(OUTPUT_FILE)
    print(f"\n✅ Document saved to: {OUTPUT_FILE}")
    print(f"   File size: {os.path.getsize(OUTPUT_FILE) / 1024:.1f} KB")
    print("=" * 70)


if __name__ == "__main__":
    main()
