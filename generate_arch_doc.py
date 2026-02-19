#!/usr/bin/env python3
"""
Healthy Fleet Maintenance & Tenant-Safe Node Lifecycle
Architecture Design Document Generator — V2

Compact 15-page version with updated diagrams and content.
"""

import os
from datetime import datetime
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import nsdecls
from docx.oxml import parse_xml

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DIAGRAMS_DIR = os.path.join(SCRIPT_DIR, "diagrams")
OUTPUT_FILE = os.path.join(SCRIPT_DIR, "Healthy_Fleet_Maintenance_Architecture_Design.docx")

DARK_BLUE = RGBColor(0x1B, 0x3A, 0x5C)
MEDIUM_BLUE = RGBColor(0x2C, 0x5F, 0x8A)
ACCENT_BLUE = RGBColor(0x35, 0x72, 0xA5)
DARK_GRAY = RGBColor(0x33, 0x33, 0x33)
MEDIUM_GRAY = RGBColor(0x66, 0x66, 0x66)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)


def apply_table_borders(table):
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


def set_cell_shading(cell, color_hex):
    shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}" w:val="clear"/>')
    cell._tc.get_or_add_tcPr().append(shading)


def style_header_row(row, font_size=8):
    for cell in row.cells:
        set_cell_shading(cell, "1B3A5C")
        for p in cell.paragraphs:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_after = Pt(1)
            p.paragraph_format.space_before = Pt(1)
            for r in p.runs:
                r.font.color.rgb = WHITE
                r.font.bold = True
                r.font.size = Pt(font_size)
                r.font.name = "Calibri"


def style_data_row(row, index, font_size=7.5):
    bg = "E8F0F8" if index % 2 == 0 else "FFFFFF"
    for cell in row.cells:
        set_cell_shading(cell, bg)
        for p in cell.paragraphs:
            p.paragraph_format.space_after = Pt(1)
            p.paragraph_format.space_before = Pt(1)
            for r in p.runs:
                r.font.size = Pt(font_size)
                r.font.name = "Calibri"
                r.font.color.rgb = DARK_GRAY


def h(doc, text, level=1):
    heading = doc.add_heading(text, level=level)
    heading.paragraph_format.space_before = Pt(6)
    heading.paragraph_format.space_after = Pt(3)
    for r in heading.runs:
        r.font.color.rgb = DARK_BLUE
        r.font.name = "Calibri"
    return heading


def p(doc, text, bold=False, italic=False, sz=9):
    para = doc.add_paragraph()
    run = para.add_run(text)
    run.font.name = "Calibri"
    run.font.size = Pt(sz)
    run.font.color.rgb = DARK_GRAY
    run.bold = bold
    run.italic = italic
    para.paragraph_format.space_after = Pt(3)
    para.paragraph_format.space_before = Pt(1)
    return para


def bullet(doc, text, bold_prefix="", sz=8.5):
    para = doc.add_paragraph(style='List Bullet')
    para.paragraph_format.space_after = Pt(1)
    para.paragraph_format.space_before = Pt(1)
    if bold_prefix:
        rb = para.add_run(bold_prefix)
        rb.bold = True
        rb.font.name = "Calibri"
        rb.font.size = Pt(sz)
        rb.font.color.rgb = DARK_GRAY
    r = para.add_run(text)
    r.font.name = "Calibri"
    r.font.size = Pt(sz)
    r.font.color.rgb = DARK_GRAY
    return para


def diagram(doc, image_path, caption, width=Inches(5.5)):
    para = doc.add_paragraph()
    para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    para.paragraph_format.space_before = Pt(4)
    run = para.add_run()
    if os.path.exists(image_path):
        run.add_picture(image_path, width=width)
    cap = doc.add_paragraph()
    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cr = cap.add_run(caption)
    cr.font.name = "Calibri"
    cr.font.size = Pt(8)
    cr.font.color.rgb = MEDIUM_GRAY
    cr.italic = True
    cap.paragraph_format.space_after = Pt(6)


def table(doc, headers, rows, col_widths=None, hdr_sz=7.5, data_sz=7):
    t = doc.add_table(rows=1 + len(rows), cols=len(headers))
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, hdr in enumerate(headers):
        c = t.rows[0].cells[i]
        c.text = ""
        pr = c.paragraphs[0]
        r = pr.add_run(hdr)
        r.bold = True
        r.font.name = "Calibri"
    style_header_row(t.rows[0], hdr_sz)
    for ri, rd in enumerate(rows):
        for ci, v in enumerate(rd):
            c = t.rows[ri + 1].cells[ci]
            c.text = ""
            pr = c.paragraphs[0]
            r = pr.add_run(str(v))
            r.font.name = "Calibri"
        style_data_row(t.rows[ri + 1], ri, data_sz)
    apply_table_borders(t)
    if col_widths:
        for row in t.rows:
            for idx, w in enumerate(col_widths):
                row.cells[idx].width = Inches(w)
    sp = doc.add_paragraph()
    sp.paragraph_format.space_after = Pt(2)
    return t


def main():
    print("Generating V2 Architecture Document (compact 15-page)...")
    doc = Document()

    # Page setup — 0.5" margins
    sec = doc.sections[0]
    sec.page_width = Inches(8.5)
    sec.page_height = Inches(11)
    sec.top_margin = Inches(0.5)
    sec.bottom_margin = Inches(0.5)
    sec.left_margin = Inches(0.5)
    sec.right_margin = Inches(0.5)

    style = doc.styles['Normal']
    style.font.name = 'Calibri'
    style.font.size = Pt(9)
    style.font.color.rgb = DARK_GRAY
    style.paragraph_format.space_after = Pt(3)
    style.paragraph_format.space_before = Pt(1)

    for i in range(1, 4):
        hs = doc.styles[f'Heading {i}']
        hs.font.name = 'Calibri'
        hs.font.color.rgb = DARK_BLUE
        hs.paragraph_format.space_before = Pt(6)
        hs.paragraph_format.space_after = Pt(3)

    # =========================================================================
    # COVER PAGE
    # =========================================================================
    for _ in range(4):
        doc.add_paragraph()

    t = doc.add_paragraph()
    t.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = t.add_run("Healthy Fleet Maintenance\n& Tenant-Safe Node Lifecycle")
    r.font.size = Pt(28)
    r.font.color.rgb = DARK_BLUE
    r.font.name = "Calibri"
    r.bold = True

    st = doc.add_paragraph()
    st.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = st.add_run("Architecture Design Document")
    r.font.size = Pt(16)
    r.font.color.rgb = MEDIUM_BLUE
    r.font.name = "Calibri"

    sep = doc.add_paragraph()
    sep.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = sep.add_run("━" * 70)
    r.font.color.rgb = ACCENT_BLUE
    r.font.size = Pt(9)

    meta = [
        ("Classification", "Internal — Engineering"),
        ("Version", "2.0"),
        ("Date", datetime.now().strftime("%B %d, %Y")),
        ("Author", "Distinguished Engineer, AI Compute Platform"),
        ("Status", "Final Draft"),
        ("Review Board", "Compute Platform · K8s · OE · Storage · Network · DC Infra"),
    ]
    mt = doc.add_table(rows=len(meta), cols=2)
    mt.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, (k, v) in enumerate(meta):
        ck = mt.rows[i].cells[0]
        cv = mt.rows[i].cells[1]
        ck.text = ""
        cv.text = ""
        pk = ck.paragraphs[0]
        pk.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        rk = pk.add_run(k)
        rk.bold = True
        rk.font.name = "Calibri"
        rk.font.size = Pt(9)
        rk.font.color.rgb = DARK_BLUE
        pv = cv.paragraphs[0]
        rv = pv.add_run(v)
        rv.font.name = "Calibri"
        rv.font.size = Pt(9)
        rv.font.color.rgb = DARK_GRAY
        ck.width = Inches(2.0)
        cv.width = Inches(4.5)
    apply_table_borders(mt)
    doc.add_page_break()

    # =========================================================================
    # TABLE OF CONTENTS
    # =========================================================================
    h(doc, "Table of Contents", 1)
    toc = [
        "1.  Executive Summary",
        "2.  Goals & Objectives",
        "3.  Scope Definition",
        "4.  Architecture Design",
        "5.  \"Good Host\" Certification Standard",
        "6.  Infrastructure & Operations",
        "7.  End-to-End Test Plan",
        "8.  Enterprise Promises",
        "9.  Deployment, Observability & Operations",
        "10. Customer Impact",
        "Appendix A: Glossary",
    ]
    for item in toc:
        tp = doc.add_paragraph(item)
        tp.paragraph_format.space_after = Pt(2)
        for r in tp.runs:
            r.font.name = "Calibri"
            r.font.size = Pt(9)
            r.font.color.rgb = DARK_GRAY
    doc.add_page_break()

    # =========================================================================
    # 1. EXECUTIVE SUMMARY
    # =========================================================================
    h(doc, "1. Executive Summary", 1)
    p(doc, "This document defines the Healthy Fleet Maintenance & Tenant-Safe Node Lifecycle platform feature. "
           "It establishes a deterministic, automated state transition model for GPU compute nodes, ensuring every node "
           "serving a tenant meets a codified \"good host\" standard and that node transitions follow a secure lifecycle.")

    p(doc, "The feature addresses four foundational platform challenges:")
    bullet(doc, " Sustain 99.5% availability using an internal tenant certification model and rapid remediation workflows.", bold_prefix="Fleet Availability:")
    bullet(doc, " Automate lifecycle using NPD + controllers for host-level detection and enforcement via cordon/taint.", bold_prefix="Lifecycle Automation:")
    bullet(doc, " Codify certification below K8s: BCM burn-in, DCGM L4, NCCL collectives, HPL benchmarks, multi-node jobs.", bold_prefix="Node Certification:")
    bullet(doc, " Fixed state transition: Internal Tenant A → Certified → Production Tenant X → reimage + wipe + recertify.", bold_prefix="Tenant Reassignment:")

    p(doc, "Design is tenant-first: unhealthy nodes never serve production tenants. Incident 5337 (multi-node training failure) "
           "learnings are incorporated throughout. Self-heal is explicitly out of scope for the initial phase.")

    diagram(doc, os.path.join(DIAGRAMS_DIR, "01_mindmap_overview.png"),
            "Figure 1: Healthy Fleet Maintenance — Four-Pillar Problem Space Overview")

    # =========================================================================
    # 2. GOALS & OBJECTIVES
    # =========================================================================
    h(doc, "2. Goals & Objectives", 1)
    h(doc, "2.1 Primary Goals", 2)
    bullet(doc, " No scheduling on degraded, suspect, or uncertified nodes.", bold_prefix="G1 — Tenant Safety by Default:")
    bullet(doc, " Deterministic recovery via internal tenant certification model; defined exception handling.", bold_prefix="G2 — 99.5% Availability:")
    bullet(doc, " Codified minimum host requirements: GPU + IB/RDMA + K8s readiness + tenant networking + NCCL/HPL benchmarks.", bold_prefix="G3 — Zero Ambiguity on \"Good Host\":")
    bullet(doc, " Phase 1: people-driven L1 squad with runbooks. Phase 2: automation-driven NPD + controller enforcement.", bold_prefix="G4 — Two-Phase Execution:")
    bullet(doc, " Multi-team detector contribution under NPD with standardized event/condition/taint outputs.", bold_prefix="G5 — NPD as a Platform:")

    h(doc, "2.2 Secondary Goals", 2)
    bullet(doc, "Prevent recurrence of distributed training failures (Incident 5337): stricter IB thresholds, node-set correlation.")
    bullet(doc, "Reduce manual toil in tenant reassignment via single state transition pipeline.")
    bullet(doc, "Standardize evidence capture for hardware faults to accelerate vendor + RMA loops.")

    # =========================================================================
    # 3. SCOPE
    # =========================================================================
    h(doc, "3. Scope Definition", 1)
    table(doc,
        ["Category", "In Scope", "Out of Scope"],
        [
            ["People / Process", "L1 squad, runbooks, daily triage, escalation", "Tenant application ops"],
            ["Host Certification", "BCM burn-in, DCGM L4, NCCL, HPL, ECC, pass/fail tagging", "Tenant workload tests beyond host gating"],
            ["Node Lifecycle", "State machine, cordon/taint, deterministic reassignment", "Auto-reboot/reimage (future phase)"],
            ["Self-Heal", "Out of scope for Phase 1", "Automated self-remediation"],
            ["K8s Node Boundary", "Node readiness, kubelet, operators, taints/tolerations", "Tenant scheduling policy"],
            ["NVIDIA + K8s Stack", "GPU op, network op, IB SR-IOV, Multus, DCGM", "Tenant services, application SLO/SLA"],
            ["Host / Tenant Network", "IB readiness, VLAN routing, node routing agent", "Fabric architecture (Network team)"],
            ["Storage", "Weka/VAST probes, NVMe health, storage operator readiness", "Storage backend ops"],
            ["RMA Workflow", "Evidence capture, ticket routing, post-RMA recertification", "Physical swap (DC Infra + vendor)"],
        ],
        col_widths=[1.5, 2.8, 2.7]
    )

    # =========================================================================
    # 4. ARCHITECTURE DESIGN
    # =========================================================================
    h(doc, "4. Architecture Design", 1)

    h(doc, "4.1 Layered Component View", 2)
    table(doc,
        ["Layer", "Components"],
        [
            ["Hardware", "GPU (B200), HCA/NIC (IB NDR 400G), NVMe, BMC, NVLink5/NVSwitch, CPU/Memory"],
            ["Host OS", "Kernel, drivers, filesystem, time sync, container runtime"],
            ["NVIDIA Stack", "BCM, DCGM/DCGMI, gpu_burn, nccl-tests, nvbandwidth, HPL"],
            ["K8s Node Layer", "GPU operator, network operator, IB SR-IOV, Multus, NPD, CNI (Tigera/Calico)"],
            ["Storage Layer", "Weka/VAST probes, NVMe health monitoring, storage operator"],
            ["Tenant Network", "Node routing agent for VLAN/tenant routing; IB + VLAN dependencies"],
            ["Controller Layer", "compute-node-manager/controller for lifecycle and tenant assignments"],
        ],
        col_widths=[1.5, 5.5]
    )

    h(doc, "4.2 NPD as a Platform (Multi-Team Contribution Model)", 2)
    p(doc, "NPD is the common substrate for node health detection. Five teams contribute domain-specific detectors:")

    diagram(doc, os.path.join(DIAGRAMS_DIR, "04_npd_platform.png"),
            "Figure 2: NPD as a Platform — Multi-Team Contribution Model")

    h(doc, "Team Responsibilities & Asks", 3)
    table(doc,
        ["Team", "Owns / Contributes", "Ask from Team"],
        [
            ["Compute Platform", "Host-side IB & tenant VLAN; GPU/Network Operators; IB SR-IOV/VFs; DCGM; GPU health & XID detection; host-level checks",
             "Owns NPD framework, detector development, certification pipeline, state machine controller"],
            ["Kubernetes", "Kubelet/runtime; node readiness; CNI (Tigera/Calico); nodefs/imagefs pressure",
             "CNI health probes, node readiness signal fidelity, taint/toleration policy enforcement"],
            ["Storage", "Weka probes; VAST probes",
             "Storage health probe integration into NPD, read/write latency signals, capacity alerts"],
            ["OE", "NPD integration support; logs, events, metrics across all AZs",
             "Log/metric pipeline reliability, NPD deployment across AZs, monitoring infra"],
            ["Network / App Network", "Ingress probes for inference workloads",
             "Ingress health signals, endpoint readiness probes, latency thresholds for inference"],
        ],
        col_widths=[1.3, 2.8, 2.9]
    )

    h(doc, "4.3 Detection → Enforcement → Recovery Workflow", 2)
    p(doc, "Core workflow: signal detection → quarantine → repair/RMA → recertify. Self-heal is explicitly out of scope for Phase 1.")

    diagram(doc, os.path.join(DIAGRAMS_DIR, "03_workflow_diagram.png"),
            "Figure 3: Detection → Enforcement → Recovery Workflow (Self-Heal: Out of Scope)")
    doc.add_page_break()

    h(doc, "4.4 Node Lifecycle State Machine", 2)
    p(doc, "The lifecycle has 8 states with deterministic transitions. States include explicit RMA, BURN_IN, and CERTIFIED "
           "phases aligned with the GPU Node Certification SOP (SOP-GPU-CERT-001).")

    diagram(doc, os.path.join(DIAGRAMS_DIR, "02_state_machine.png"),
            "Figure 4: Node Lifecycle State Machine (8 States)")

    table(doc,
        ["State", "Description", "Entry", "Exit"],
        [
            ["BUFFER_HEALTHY", "Healthy, certified, available", "Initial provision OR certified", "Tenant attach OR blocking signal"],
            ["TENANT_ASSIGNED", "Actively serving tenant", "Attach label from buffer", "Detach+recertify OR blocking signal"],
            ["QUARANTINED", "Blocked; removed from scheduling", "Blocking signal", "→ REPAIR or → RMA"],
            ["REPAIR_IN_PROGRESS", "Software/config fix underway", "Triage: software/config issue", "Fix complete → BURN_IN"],
            ["RMA", "Hardware replacement in progress", "Hardware fault confirmed", "Component replaced → BURN_IN"],
            ["BURN_IN", "BCM burn-in (6–24h, gpu_burn, stress)", "Post-repair or post-RMA", "Pass → RECERTIFY; Fail → QUARANTINED"],
            ["RECERTIFY", "DCGM L4 + NCCL + HPL + multi-node", "Burn-in pass", "Pass → CERTIFIED; Fail → QUARANTINED"],
            ["CERTIFIED", "All tests passed; fleet-ready", "Recertification pass", "→ BUFFER_HEALTHY (admit to fleet)"],
        ],
        col_widths=[1.3, 2.0, 1.8, 1.9]
    )

    h(doc, "4.5 Internal Tenant Certification & Fleet Lifecycle", 2)
    p(doc, "Key design: no spare buffer nodes. Instead, nodes are assigned to \"Internal Tenant A\" for continuous "
           "certification testing. This model uses the same lifecycle for all node transitions. Layer-by-layer certification "
           "validates bus bandwidth and algorithm bandwidth scaling, including multi-node NCCL jobs per Incident 5337 retrospective.")

    diagram(doc, os.path.join(DIAGRAMS_DIR, "05_buffer_strategy.png"),
            "Figure 5: Internal Tenant Certification & Fleet Lifecycle Model")

    # =========================================================================
    # 5. GOOD HOST CERTIFICATION
    # =========================================================================
    h(doc, "5. \"Good Host\" Certification Standard", 1)
    p(doc, "A node must pass ALL layers before being tenant-eligible. Aligned with SOP-GPU-CERT-001 v1.1 (NVIDIA B200).")

    h(doc, "5.1 Certification Layers", 2)
    table(doc,
        ["Layer", "Test", "Tool", "B200 Pass Criteria"],
        [
            ["L1: Hardware", "Pre-flight (8× B200, ECC, FW, IB ports)", "nvidia-smi, dcgmi, ibstat, nvsm", "All checks green"],
            ["L2: Burn-In", "GPU stress 6–24h, 100% util, zero errors", "gpu_burn + BCM burn-in", "0 XID, 0 DBE, temp ≤70°C"],
            ["L3: DCGM L4", "All plugins: HW, SM stress, memtest, EUD", "dcgmi diag -r 4", "ALL plugins PASS (~90 min)"],
            ["L4: NCCL", "all_reduce, all_gather, reduce_scatter, broadcast", "nccl-tests (8 GPUs)", "BusBW ≥ 1530 GB/s (85% NVLink5)"],
            ["L4: NCCL Multi-Node", "Cross-node all_reduce via IB", "mpirun + nccl-tests", "≥ 85% per-port IB line rate"],
            ["L5: HPL/HPL-MxP", "Peak FP64 and mixed-precision FLOPS", "HPL (NGC container)", "≥ 70% theoretical peak"],
            ["L6: NVLink/Network", "NVLink5 status, IB BW, GPUDirect RDMA", "nvbandwidth, ibtools", "D2D ≥90% of 1.8 TB/s"],
            ["L7: Storage/System", "NVMe SMART, fio, memtester, PSU", "nvme, fio, stress-ng, ipmitool", "Zero errors, spare ≥80%"],
            ["L8: K8s Job", "Dummy K8s job: pod scheduling, GPU alloc", "kubectl + sample workload", "Job completes, GPU visible"],
        ],
        col_widths=[1.3, 2.0, 1.8, 1.9]
    )

    h(doc, "5.2 Day Two Continuous Monitoring", 2)
    table(doc,
        ["Severity", "Trigger", "Action"],
        [
            ["P1 — Immediate Quarantine", "DBE, row remap fail, XID 48/63/64/79/94/95, GPU off bus", "Cordon + taint, alert, ticket"],
            ["P2 — Investigate 4h", "SBE > 0, retired pages nearing limit, NVLink CRC", "Investigate, trend analysis"],
            ["P3 — Weekly Review", "PCIe replay, NVMe spare < 80%, IB error counters", "Track; weekly triage review"],
        ],
        col_widths=[1.8, 3.0, 2.2]
    )

    h(doc, "5.3 Periodic Re-Validation Schedule", 2)
    table(doc,
        ["Frequency", "Test", "Duration"],
        [
            ["Weekly", "dcgmi diag -r 1 (quick health)", "~2 min"],
            ["Monthly", "dcgmi diag -r 3 (medium diag)", "~15 min"],
            ["Quarterly", "dcgmi diag -r 4 + NCCL collectives", "~100 min"],
            ["Annually", "Full burn-in + HPL + 24h soak", "~8 hrs"],
        ],
        col_widths=[1.5, 3.0, 2.5]
    )

    # =========================================================================
    # 6. INFRASTRUCTURE & OPERATIONS
    # =========================================================================
    h(doc, "6. Infrastructure & Operations", 1)

    h(doc, "6.1 L1 Squad & Operating Targets", 2)
    table(doc,
        ["Issue Category", "Target", "SLA"],
        [
            ["Non-hardware", "Return node to fleet ≤24h", "L1 squad accountability"],
            ["Hardware / RMA", "Evidence capture + ticket same day", "DC Infra SLA for physical swap"],
            ["Critical (buffer impact)", "Immediate escalation", "Management notification, exception mode"],
        ],
        col_widths=[1.8, 2.7, 2.5]
    )

    h(doc, "6.2 RMA Lifecycle", 2)
    p(doc, "Fault (BCM Alert) → Quarantine → Triage & collect diagnostics → RMA submission → Component replaced "
           "→ BURN_IN (12h minimum) → RECERTIFY (DCGM L4 + NCCL + HPL) → 24h soak → CERTIFIED → Fleet re-admission.")
    p(doc, "Required RMA data: nvidia-bug-report.sh, dcgmi diag -r 4, nvsm show health, ipmitool sel, dmesg, "
           "fieldiag.log, GPU serial/part#, nvfwupd show_version.", sz=8)

    h(doc, "6.3 Incident 5337 Integration", 2)
    bullet(doc, "Stricter IB readiness thresholds for multi-node distributed training workloads")
    bullet(doc, "Correlation logic across node sets: job failure → suspect node identification → quarantine repeat offenders")
    bullet(doc, "Certification includes multi-node smoke checks: NCCL cross-node + sample distributed job")
    bullet(doc, "Bus bandwidth AND algorithm bandwidth must scale; validated via nccl-tests and HPL multi-node")

    # =========================================================================
    # 7. TEST PLAN
    # =========================================================================
    h(doc, "7. End-to-End Test Plan", 1)
    table(doc,
        ["Test Layer", "What We Validate", "Where It Runs"],
        [
            ["Pre-Tenant Cert", "BCM burn-in, DCGM L4, NCCL, HPL, NVLink, IB, NVMe", "Internal Tenant A"],
            ["Node Readiness", "Node Ready, kubelet/runtime stable, FS not RO, disk OK", "Continuous + pre-attach"],
            ["IB / Multi-Node", "IB up, stable, counters OK; SR-IOV VFs; cross-node NCCL", "Continuous + pre-attach"],
            ["Tenant Networking", "Node routing agent, VLAN/tenant routing verified", "Pre-attach + periodic"],
            ["Storage", "Weka/VAST probes healthy, NVMe SMART OK", "Continuous"],
            ["K8s Dummy Job", "Pod scheduling, GPU allocation, job completion", "Internal Tenant A"],
            ["Enforcement", "Taint/cordon applied on failure; scheduling prevented", "Continuous"],
            ["Recovery", "Repair → burn-in → recertify → fleet re-admission", "Post-fix"],
        ],
        col_widths=[1.5, 3.0, 2.5]
    )

    h(doc, "Acceptance Criteria", 2)
    bullet(doc, " Node cannot enter TENANT_ASSIGNED unless all certification layers pass.", bold_prefix="AC-1:")
    bullet(doc, " Blocking signal → quarantine (cordon+taint) within defined detection-to-quarantine SLO.", bold_prefix="AC-2:")
    bullet(doc, " No return-to-fleet without full recertification (burn-in + DCGM L4 + NCCL + HPL).", bold_prefix="AC-3:")
    bullet(doc, " Tenant reassignment always follows: reimage → disk wipe → recertification → network reconfig.", bold_prefix="AC-4:")
    bullet(doc, " Multi-node NCCL bus BW ≥ 1530 GB/s and algo BW must scale for distributed workload eligibility.", bold_prefix="AC-5:")

    # =========================================================================
    # 8. ENTERPRISE PROMISES
    # =========================================================================
    h(doc, "8. Enterprise Promises", 1)
    table(doc,
        ["#", "Promise", "Delivered By"],
        [
            ["1", "Tenant Safety by Default", "NPD + taint enforcement; unhealthy nodes never serve tenants"],
            ["2", "Predictable Availability", "Internal tenant certification + rapid repair/recertification pipeline"],
            ["3", "Deterministic Lifecycle", "Fixed state machine: all transitions follow secure, clean path"],
            ["4", "Operational Maturity", "L1 squad + runbooks (Phase 1) → automation-first (Phase 2)"],
            ["5", "Platform Extensibility", "NPD as shared platform; 5 teams contribute detectors independently"],
        ],
        col_widths=[0.4, 2.0, 4.6]
    )

    # =========================================================================
    # 9. DEPLOYMENT & OBSERVABILITY
    # =========================================================================
    h(doc, "9. Deployment, Observability & Operations", 1)

    h(doc, "9.1 Staged Rollout", 2)
    table(doc,
        ["Stage", "Action", "Risk"],
        [
            ["1", "Deploy NPD baseline + dashboards (observe only)", "No enforcement — validation"],
            ["2", "Enable enforcement in Internal Tenant A only", "Limited blast radius"],
            ["3", "Enforce gating for production tenant attachment", "Tenant-impacting; rollback plan"],
            ["4", "Enable automated reassignment workflow", "Full automation; max monitoring"],
        ],
        col_widths=[0.5, 3.5, 3.0]
    )

    h(doc, "9.2 Dashboards & Alerts", 2)
    p(doc, "Dashboards:", bold=True, sz=8.5)
    bullet(doc, "Fleet by state: Internal Tenant A, tenant assigned, quarantined, burn-in, recertifying, certified")
    bullet(doc, "Detection-to-quarantine latency (P50/P95/P99) · Quarantine-to-recovery latency")
    bullet(doc, "Certification pass/fail rate · Repeat offender tracking · NCCL/HPL benchmark trends")

    p(doc, "Alerts:", bold=True, sz=8.5)
    bullet(doc, "Blocking taint/cordon applied · Certification failures · Multi-node correlation spikes")
    bullet(doc, "Consent toleration granted/used/expired · Buffer below threshold (exception mode)")

    h(doc, "9.3 L1 Daily Report", 2)
    table(doc,
        ["Item", "Content"],
        [
            ["Unhealthy Nodes", "Hostname, fault category, owner, ETA"],
            ["Returned to Fleet", "Nodes returned in last 24h, cause summary"],
            ["Escalated (RMA)", "Nodes escalated, evidence status, vendor ticket #"],
            ["Fleet Health", "Internal Tenant A utilization, certification pipeline throughput"],
        ],
        col_widths=[2.0, 5.0]
    )

    # =========================================================================
    # 10. CUSTOMER IMPACT
    # =========================================================================
    h(doc, "10. Customer Impact", 1)
    h(doc, "Positive Impact", 2)
    bullet(doc, "Fewer tenant-visible failures from bad hosts; higher multi-node job success rate (5337 mitigation)")
    bullet(doc, "Faster quarantine reduces repeat failures; cleaner tenant isolation via reimage + disk wipe")
    bullet(doc, "Layer-by-layer certification ensures bus BW and algo BW scale before production exposure")

    h(doc, "Tradeoffs", 2)
    bullet(doc, "Stricter gating may temporarily reduce capacity; exception mode is audited and time-bounded")
    bullet(doc, "Conservative remediation (quarantine-first, no self-heal) increases reliance on repair velocity in Phase 1")

    doc.add_page_break()

    # =========================================================================
    # APPENDIX: GLOSSARY
    # =========================================================================
    h(doc, "Appendix A: Glossary", 1)
    table(doc,
        ["Term", "Definition"],
        [
            ["BCM", "NVIDIA Base Command Manager — cluster management and provisioning"],
            ["DCGM/DCGMI", "NVIDIA Data Center GPU Manager / Interface — GPU diagnostics"],
            ["ECC/DBE/SBE", "Error Correcting Code / Double-Bit Error / Single-Bit Error"],
            ["HPL/HPL-MxP", "High Performance Linpack — FP64 and mixed-precision benchmark"],
            ["IB / NDR", "InfiniBand / Next Data Rate (400 Gb/s) — HPC networking"],
            ["NCCL", "NVIDIA Collective Communications Library — GPU collective operations"],
            ["NPD", "Node Problem Detector — K8s node health daemon"],
            ["NVLink5", "NVIDIA GPU interconnect (1.8 TB/s per GPU on B200)"],
            ["RMA", "Return Merchandise Authorization — hardware replacement"],
            ["SR-IOV / VF", "Single Root I/O Virtualization / Virtual Function"],
            ["XID", "NVIDIA GPU error identifier code"],
        ],
        col_widths=[1.5, 5.5]
    )

    # Save
    doc.save(OUTPUT_FILE)
    fsize = os.path.getsize(OUTPUT_FILE)
    print(f"\n✅ Saved: {OUTPUT_FILE}")
    print(f"   Size: {fsize/1024:.1f} KB")


if __name__ == "__main__":
    main()
