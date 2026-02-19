#!/usr/bin/env python3
"""Generate architecture diagrams using Pillow when image generation service is unavailable."""

from PIL import Image, ImageDraw, ImageFont
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DIAGRAMS_DIR = os.path.join(SCRIPT_DIR, "diagrams")

# Try to get a good font
def get_font(size, bold=False):
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    for fp in paths:
        if os.path.exists(fp):
            return ImageFont.truetype(fp, size)
    return ImageFont.load_default()

def draw_rounded_rect(draw, bbox, radius, fill, outline=None, width=2):
    x0, y0, x1, y1 = bbox
    draw.rounded_rectangle(bbox, radius=radius, fill=fill, outline=outline, width=width)

def draw_text_wrapped(draw, text, x, y, max_width, font, fill="white", line_spacing=4):
    """Draw text with word wrapping."""
    words = text.split()
    lines = []
    current_line = ""
    for word in words:
        test = f"{current_line} {word}".strip()
        bbox = draw.textbbox((0, 0), test, font=font)
        if bbox[2] - bbox[0] > max_width and current_line:
            lines.append(current_line)
            current_line = word
        else:
            current_line = test
    if current_line:
        lines.append(current_line)
    
    cy = y
    for line in lines:
        draw.text((x, cy), line, font=font, fill=fill)
        bbox = draw.textbbox((0, 0), line, font=font)
        cy += (bbox[3] - bbox[1]) + line_spacing
    return cy


def generate_mindmap_v3():
    """Generate the updated 4-pillar mind map."""
    W, H = 2400, 1800
    img = Image.new("RGB", (W, H), "white")
    draw = ImageDraw.Draw(img)
    
    title_font = get_font(36, bold=True)
    heading_font = get_font(22, bold=True)
    phase_font = get_font(18, bold=True)
    item_font = get_font(16)
    center_font = get_font(20, bold=True)
    
    # Title
    draw.text((W//2 - 400, 20), "AI Compute Platform — Fleet Operations Pillars", font=title_font, fill="#1B3A5C")
    
    # Center hub
    cx, cy = W//2, H//2 - 50
    draw_rounded_rect(draw, (cx-140, cy-40, cx+140, cy+40), 15, fill="#1B3A5C", outline="#0D2137", width=3)
    draw.text((cx-120, cy-15), "AI COMPUTE\nPLATFORM", font=center_font, fill="white")
    
    # Colors
    colors = {
        "p1": {"bg": "#2563EB", "border": "#1D4ED8", "phase_bg": "#1E40AF"},
        "p2": {"bg": "#059669", "border": "#047857", "phase_bg": "#065F46"},
        "p3": {"bg": "#7C3AED", "border": "#6D28D9", "phase_bg": "#5B21B6"},
        "p4": {"bg": "#EA580C", "border": "#C2410C", "phase_bg": "#9A3412"},
    }
    
    # Pillar 1 - Healthy Fleet Maintenance (top-left)
    bx, by, bw, bh = 40, 80, 540, 700
    draw_rounded_rect(draw, (bx, by, bx+bw, by+bh), 15, fill=colors["p1"]["bg"], outline=colors["p1"]["border"], width=3)
    # Phase badge
    draw_rounded_rect(draw, (bx+10, by+10, bx+120, by+40), 8, fill=colors["p1"]["phase_bg"])
    draw.text((bx+22, by+14), "PHASE 1", font=phase_font, fill="white")
    draw.text((bx+20, by+50), "Healthy Fleet\nMaintenance", font=heading_font, fill="white")
    
    items_p1 = [
        "• 99.5% SLA Squad (Established)",
        "• SLA Scope & Critical Path",
        "  Components Defined",
        "• Runbooks for All Critical",
        "  Path Components",
        "• Observability & Grafana",
        "  Dashboards",
        "• Q4 GPU Reliability Tasks",
        "  Completed",
        "• RMA Workflows & Vendor",
        "  SLA Tracking",
        "• Capacity Return <24h SOP",
        "• Incident 5337 Multi-Node",
        "  Learnings Integrated",
        "• Automated Daily Executive",
        "  Summary Dashboards",
    ]
    iy = by + 105
    for item in items_p1:
        draw.text((bx+20, iy), item, font=item_font, fill="white")
        iy += 22 if item.startswith("  ") else 28
    
    # Draw connector line from pillar 1 to center
    draw.line([(bx+bw, by+bh//2), (cx-140, cy)], fill="#2563EB", width=3)
    
    # Pillar 2 - Automated Node Lifecycle & Certification (top-right)
    bx2, by2 = W-580, 80
    bw2, bh2 = 540, 560
    draw_rounded_rect(draw, (bx2, by2, bx2+bw2, by2+bh2), 15, fill=colors["p2"]["bg"], outline=colors["p2"]["border"], width=3)
    draw_rounded_rect(draw, (bx2+10, by2+10, bx2+120, by2+40), 8, fill=colors["p2"]["phase_bg"])
    draw.text((bx2+22, by2+14), "PHASE 2", font=phase_font, fill="white")
    draw.text((bx2+20, by2+50), "Automated Node Lifecycle\n& Certification", font=heading_font, fill="white")
    
    items_p2 = [
        "• NPD + Controllers for",
        "  Host-Level Detection",
        "• Cordon/Taint Enforcement",
        "• BCM Burn-in & DCGM L4",
        "  Certification Pipeline",
        "• NCCL / HPL / NVLink / IB",
        "  Validation",
        "• Day Zero & Day Two SOP",
        "  Integration",
        "• Multi-Node Readiness Gates",
    ]
    iy = by2 + 110
    for item in items_p2:
        draw.text((bx2+20, iy), item, font=item_font, fill="white")
        iy += 22 if item.startswith("  ") else 28
    
    draw.line([(bx2, by2+bh2//2), (cx+140, cy)], fill="#059669", width=3)
    
    # Pillar 3 - Automated Image Pipeline (bottom-left)
    bx3, by3 = 40, 850
    bw3, bh3 = 540, 500
    draw_rounded_rect(draw, (bx3, by3, bx3+bw3, by3+bh3), 15, fill=colors["p3"]["bg"], outline=colors["p3"]["border"], width=3)
    draw_rounded_rect(draw, (bx3+10, by3+10, bx3+120, by3+40), 8, fill=colors["p3"]["phase_bg"])
    draw.text((bx3+22, by3+14), "PHASE 2", font=phase_font, fill="white")
    draw.text((bx3+20, by3+50), "Automated Image\nPipeline", font=heading_font, fill="white")
    
    items_p3 = [
        "• Deprecate BCM Image",
        "  Cloning Model",
        "• Packer-Based Pipeline",
        "  (NVIDIA Support)",
        "• GitOps CD Style Deployment",
        "• Cross-AZ / Cross-Region",
        "  Image Replication",
        "• Self-Service Layers",
        "  (Storage, K8s, etc.)",
    ]
    iy = by3 + 110
    for item in items_p3:
        draw.text((bx3+20, iy), item, font=item_font, fill="white")
        iy += 22 if item.startswith("  ") else 28
    
    draw.line([(bx3+bw3, by3+bh3//2-100), (cx-140, cy)], fill="#7C3AED", width=3)
    
    # Pillar 4 - Tenant Reassignment (bottom-right)
    bx4, by4 = W-580, 850
    bw4, bh4 = 540, 500
    draw_rounded_rect(draw, (bx4, by4, bx4+bw4, by4+bh4), 15, fill=colors["p4"]["bg"], outline=colors["p4"]["border"], width=3)
    draw.text((bx4+20, by4+20), "Tenant Reassignment", font=heading_font, fill="white")
    
    items_p4 = [
        "• Internal Tenant A →",
        "  Certified → Tenant X",
        "• Re-image + Disk Wipe on",
        "  Every Transition",
        "• Full Recertification Gate",
        "  (Burn-in + DCGM + NCCL)",
        "• Host Network",
        "  Reconfiguration",
        "• VLAN/Tenant Routing",
        "  Validated",
    ]
    iy = by4 + 65
    for item in items_p4:
        draw.text((bx4+20, iy), item, font=item_font, fill="white")
        iy += 22 if item.startswith("  ") else 28
    
    draw.line([(bx4, by4+bh4//2-100), (cx+140, cy)], fill="#EA580C", width=3)
    
    out = os.path.join(DIAGRAMS_DIR, "01_mindmap_overview.png")
    img.save(out, "PNG")
    print(f"✅ Saved: {out}")


def generate_lifecycle_combined():
    """Generate combined lifecycle + NPD detection diagram."""
    W, H = 2400, 1600
    img = Image.new("RGB", (W, H), "white")
    draw = ImageDraw.Draw(img)
    
    title_font = get_font(32, bold=True)
    heading_font = get_font(20, bold=True)
    label_font = get_font(16, bold=True)
    small_font = get_font(14)
    arrow_font = get_font(13)
    
    # Title
    draw.text((W//2 - 380, 15), "Node Lifecycle with NPD Detection & Enforcement", font=title_font, fill="#1B3A5C")
    
    # ---- TOP SECTION: NPD Detection Flow ----
    draw_rounded_rect(draw, (30, 60, W-30, 310), 10, fill="#F8FAFC", outline="#CBD5E1", width=2)
    draw.text((50, 70), "Detection & Enforcement Layer", font=heading_font, fill="#1B3A5C")
    
    # Host Signals box
    draw_rounded_rect(draw, (60, 110, 260, 290), 10, fill="#6B7280", outline="#4B5563", width=2)
    draw.text((80, 115), "Host Signals", font=label_font, fill="white")
    signals = ["GPU / XID", "InfiniBand", "Filesystem", "Kubelet", "Runtime", "Storage"]
    sy = 145
    for s in signals:
        draw.text((80, sy), f"▸ {s}", font=small_font, fill="white")
        sy += 24
    
    # Arrow
    draw.line([(260, 200), (360, 200)], fill="#4B5563", width=3)
    draw.polygon([(360, 190), (380, 200), (360, 210)], fill="#4B5563")
    
    # NPD box
    draw_rounded_rect(draw, (380, 130, 600, 270), 10, fill="#2563EB", outline="#1D4ED8", width=2)
    draw.text((410, 150), "NPD", font=get_font(28, True), fill="white")
    draw.text((400, 188), "Detectors +", font=small_font, fill="white")
    draw.text((400, 208), "Custom Plugins", font=small_font, fill="white")
    draw.text((400, 238), "Multi-team", font=small_font, fill="#93C5FD")
    
    # NPD outputs
    outputs_x = 680
    for i, (name, color) in enumerate([("Node Events", "#DBEAFE"), ("Conditions", "#D1FAE5"), ("Taints", "#FEE2E2")]):
        oy = 120 + i * 65
        draw.line([(600, 200), (outputs_x, oy+22)], fill="#2563EB", width=2)
        draw_rounded_rect(draw, (outputs_x, oy, outputs_x+160, oy+44), 8, fill=color, outline="#94A3B8", width=1)
        draw.text((outputs_x+10, oy+10), name, font=label_font, fill="#1E293B")
    
    # Arrow to Quarantine decision
    draw.line([(840, 200), (960, 200)], fill="#DC2626", width=3)
    draw.polygon([(960, 190), (980, 200), (960, 210)], fill="#DC2626")
    draw.text((870, 175), "blocking", font=arrow_font, fill="#DC2626")
    draw.text((870, 192), "signal", font=arrow_font, fill="#DC2626")
    
    # Quarantine enforcement box
    draw_rounded_rect(draw, (980, 140, 1230, 260), 10, fill="#DC2626", outline="#B91C1C", width=2)
    draw.text((1010, 155), "QUARANTINE", font=label_font, fill="white")
    draw.text((1000, 182), "Cordon + Taint", font=small_font, fill="white")
    draw.text((1000, 202), "NoSchedule applied", font=small_font, fill="white")
    draw.text((1000, 228), "Self-heal: Out of", font=small_font, fill="#FCA5A5")
    draw.text((1000, 244), "Scope (future)", font=small_font, fill="#FCA5A5")
    
    # Arrows to repair paths
    # Software fix
    draw.line([(1230, 170), (1340, 170)], fill="#EA580C", width=2)
    draw.polygon([(1340, 160), (1360, 170), (1340, 180)], fill="#EA580C")
    draw_rounded_rect(draw, (1360, 135, 1540, 205), 8, fill="#EA580C", outline="#C2410C", width=2)
    draw.text((1380, 148), "REPAIR", font=label_font, fill="white")
    draw.text((1375, 175), "SW/Config fix", font=small_font, fill="white")
    
    # RMA
    draw.line([(1230, 230), (1340, 230)], fill="#B45309", width=2)
    draw.polygon([(1340, 220), (1360, 230), (1340, 240)], fill="#B45309")
    draw_rounded_rect(draw, (1360, 210, 1540, 275), 8, fill="#B45309", outline="#92400E", width=2)
    draw.text((1380, 218), "RMA", font=label_font, fill="white")
    draw.text((1375, 245), "HW fault", font=small_font, fill="white")
    
    # Both → Burn-in
    draw.line([(1540, 170), (1620, 200)], fill="#D97706", width=2)
    draw.line([(1540, 240), (1620, 210)], fill="#D97706", width=2)
    draw.polygon([(1620, 195), (1640, 205), (1620, 215)], fill="#D97706")
    draw_rounded_rect(draw, (1640, 140, 1860, 270), 10, fill="#D97706", outline="#B45309", width=2)
    draw.text((1670, 155), "BURN-IN", font=label_font, fill="white")
    draw.text((1660, 185), "BCM burn-in", font=small_font, fill="white")
    draw.text((1660, 205), "6-24 hours", font=small_font, fill="white")
    draw.text((1660, 225), "gpu_burn + stress", font=small_font, fill="white")
    
    # → Recertify
    draw.line([(1860, 200), (1950, 200)], fill="#7C3AED", width=2)
    draw.polygon([(1950, 190), (1970, 200), (1950, 210)], fill="#7C3AED")
    draw_rounded_rect(draw, (1970, 120, 2200, 285), 10, fill="#7C3AED", outline="#6D28D9", width=2)
    draw.text((2000, 130), "RECERTIFY", font=label_font, fill="white")
    draw.text((1990, 160), "DCGM Level 4", font=small_font, fill="white")
    draw.text((1990, 180), "NCCL (bus+algo BW)", font=small_font, fill="white")
    draw.text((1990, 200), "HPL / HPL-MxP", font=small_font, fill="white")
    draw.text((1990, 220), "NVLink / IB tests", font=small_font, fill="white")
    draw.text((1990, 240), "Storage / System", font=small_font, fill="white")
    draw.text((1990, 260), "K8s dummy job", font=small_font, fill="white")
    
    # Pass/Fail labels
    draw.text((2210, 150), "Pass ↓", font=label_font, fill="#059669")
    draw.text((2210, 260), "Fail →", font=label_font, fill="#DC2626")
    # Fail arrow back to quarantine 
    draw.line([(2200, 275), (2250, 275), (2250, 300), (1100, 300), (1100, 260)], fill="#DC2626", width=2)
    draw.polygon([(1090, 260), (1100, 280), (1110, 260)], fill="#DC2626")
    
    # ---- BOTTOM SECTION: Lifecycle Flow ----
    draw_rounded_rect(draw, (30, 330, W-30, 1580), 10, fill="#F8FAFC", outline="#CBD5E1", width=2)
    draw.text((50, 340), "Node Lifecycle States", font=heading_font, fill="#1B3A5C")
    
    # CERTIFIED
    draw_rounded_rect(draw, (2060, 320, 2330, 420), 15, fill="#065F46", outline="#064E3B", width=3)
    draw.text((2100, 335), "CERTIFIED", font=get_font(24, True), fill="white")
    draw.text((2080, 370), "All tests passed", font=small_font, fill="#6EE7B7")
    draw.text((2080, 390), "Fleet-ready", font=small_font, fill="#6EE7B7")
    
    # Arrow from Recertify pass to CERTIFIED
    draw.line([(2200, 285), (2200, 320)], fill="#065F46", width=3)
    draw.polygon([(2190, 320), (2200, 340), (2210, 320)], fill="#065F46")
    
    # INTERNAL TENANT A (large green)
    draw_rounded_rect(draw, (100, 380, 700, 900), 15, fill="#059669", outline="#047857", width=3)
    draw.text((140, 395), "INTERNAL TENANT A", font=get_font(24, True), fill="white")
    draw.text((120, 435), "Certification Testing Environment", font=heading_font, fill="#D1FAE5")
    
    cert_items = [
        "▸ Layer 1: Hardware pre-flight checks",
        "▸ Layer 2: BCM Burn-in (6-24h, gpu_burn)",
        "▸ Layer 3: DCGM Level 4 (all plugins)",
        "▸ Layer 4: NCCL collectives (bus BW ≥1530 GB/s)",
        "▸ Layer 5: HPL / HPL-MxP (≥70% peak)",
        "▸ Layer 6: NVLink5 + NVSwitch + IB NDR",
        "▸ Layer 7: Storage NVMe + IPMI + System",
        "▸ Layer 8: Multi-node sample job",
        "▸ Layer 9: K8s dummy job (pod + GPU alloc)",
        "",
        "Bus BW + Algo BW must scale",
        "Daily certification runs",
    ]
    cy = 475
    for item in cert_items:
        if item == "":
            cy += 10
            continue
        draw.text((130, cy), item, font=small_font, fill="white")
        cy += 26
    
    # Arrow: CERTIFIED → INTERNAL TENANT A (admit to fleet)
    draw.line([(2060, 400), (700, 400), (700, 500)], fill="#065F46", width=3)
    draw.text((1200, 378), "admit to fleet → certification testing", font=arrow_font, fill="#065F46")
    
    # Arrow: Internal Tenant A → All tests pass
    draw.text((320, 920), "all tests pass ↓", font=label_font, fill="#065F46")
    draw.line([(400, 940), (400, 990)], fill="#065F46", width=3)
    draw.polygon([(390, 990), (400, 1010), (410, 990)], fill="#065F46")
    
    # BUFFER_HEALTHY
    draw_rounded_rect(draw, (200, 1010, 600, 1100), 15, fill="#10B981", outline="#059669", width=3)
    draw.text((250, 1025), "BUFFER_HEALTHY", font=get_font(22, True), fill="white")
    draw.text((250, 1060), "Certified & available", font=small_font, fill="white")
    
    # Arrow: BUFFER → TENANT_ASSIGNED
    draw.line([(600, 1055), (850, 1055)], fill="#2563EB", width=3)
    draw.polygon([(850, 1045), (870, 1055), (850, 1065)], fill="#2563EB")
    draw.text((660, 1030), "attach tenant label", font=arrow_font, fill="#2563EB")
    
    # TENANT_ASSIGNED
    draw_rounded_rect(draw, (870, 1010, 1350, 1100), 15, fill="#2563EB", outline="#1D4ED8", width=3)
    draw.text((920, 1025), "TENANT_ASSIGNED", font=get_font(22, True), fill="white")
    draw.text((920, 1060), "Production workload serving tenant", font=small_font, fill="white")
    
    # Arrow: TENANT → QUARANTINED (blocking signal)
    draw.line([(1350, 1055), (1500, 1055), (1500, 900)], fill="#DC2626", width=3)
    draw.polygon([(1490, 900), (1500, 880), (1510, 900)], fill="#DC2626")
    draw.text((1370, 1025), "blocking", font=arrow_font, fill="#DC2626")
    draw.text((1370, 1042), "signal", font=arrow_font, fill="#DC2626")
    
    # QUARANTINED (bottom)
    draw_rounded_rect(draw, (1350, 790, 1700, 880), 15, fill="#DC2626", outline="#B91C1C", width=3)
    draw.text((1400, 805), "QUARANTINED", font=get_font(22, True), fill="white")
    draw.text((1400, 840), "Blocked, removed from sched", font=small_font, fill="white")
    
    # Connection: top quarantine to bottom quarantine
    draw.text((1270, 310), "↓ triggers lifecycle", font=arrow_font, fill="#DC2626")
    
    # Arrow: TENANT → detach (back to Internal Tenant A)
    draw.line([(1110, 1100), (1110, 1200), (400, 1200), (400, 900)], fill="#059669", width=3)
    draw.polygon([(390, 900), (400, 880), (410, 900)], fill="#059669")
    draw.text((600, 1175), "detach + reimage + disk wipe → recertify", font=arrow_font, fill="#059669")
    
    # Arrow: QUARANTINED → repair paths (pointing up to top section)
    draw.line([(1525, 790), (1525, 500), (1100, 500), (1100, 260)], fill="#EA580C", width=2)
    draw.text((1250, 480), "triage → repair/RMA →", font=arrow_font, fill="#EA580C")
    draw.text((1250, 498), "burn-in → recertify", font=arrow_font, fill="#EA580C")
    
    # Arrow: BUFFER_HEALTHY → QUARANTINED (cert regression)
    draw.line([(400, 1010), (400, 980), (1400, 980), (1400, 880)], fill="#DC2626", width=2)
    draw.text((700, 960), "cert regression / blocking signal", font=arrow_font, fill="#DC2626")
    
    # Legend
    draw_rounded_rect(draw, (1600, 1350, 2350, 1560), 10, fill="white", outline="#CBD5E1", width=1)
    draw.text((1620, 1360), "Legend", font=label_font, fill="#1B3A5C")
    legend_items = [
        ("#059669", "Healthy / Certification"),
        ("#2563EB", "Active Tenant Service"),
        ("#DC2626", "Quarantined / Blocked"),
        ("#D97706", "Burn-in Testing"),
        ("#7C3AED", "Recertification Pipeline"),
        ("#B45309", "RMA / Hardware Repair"),
    ]
    ly = 1390
    for color, label in legend_items:
        draw.rectangle((1630, ly, 1660, ly+18), fill=color)
        draw.text((1670, ly), label, font=small_font, fill="#1E293B")
        ly += 26
    
    out = os.path.join(DIAGRAMS_DIR, "06_lifecycle_combined.png")
    img.save(out, "PNG")
    print(f"✅ Saved: {out}")


if __name__ == "__main__":
    generate_mindmap_v3()
    generate_lifecycle_combined()
