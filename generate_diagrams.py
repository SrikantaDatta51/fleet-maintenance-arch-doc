#!/usr/bin/env python3
"""Generate polished architecture diagrams using Pillow with professional styling."""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os, math

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DIAGRAMS_DIR = os.path.join(SCRIPT_DIR, "diagrams")
os.makedirs(DIAGRAMS_DIR, exist_ok=True)

def get_font(size, bold=False):
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    for fp in paths:
        if os.path.exists(fp):
            return ImageFont.truetype(fp, size)
    return ImageFont.load_default()

# ── Color helpers ──
def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def darken(rgb, factor=0.7):
    return tuple(int(c * factor) for c in rgb)

def lighten(rgb, factor=1.3):
    return tuple(min(255, int(c * factor)) for c in rgb)

# ── Drawing primitives with shadow + gradient ──
def draw_shadow_rect(img, bbox, radius, shadow_offset=6, blur=8):
    """Draw a soft shadow behind a rounded rectangle."""
    x0, y0, x1, y1 = bbox
    shadow = Image.new("RGBA", img.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rounded_rectangle(
        (x0 + shadow_offset, y0 + shadow_offset, x1 + shadow_offset, y1 + shadow_offset),
        radius=radius, fill=(0, 0, 0, 60)
    )
    shadow = shadow.filter(ImageFilter.GaussianBlur(blur))
    img.paste(Image.alpha_composite(Image.new("RGBA", img.size, (0,0,0,0)), shadow), (0, 0), shadow)

def draw_gradient_rect(draw, img, bbox, radius, color_top, color_bottom, outline=None, width=2):
    """Draw a rounded rectangle with vertical gradient fill."""
    x0, y0, x1, y1 = [int(v) for v in bbox]
    # Create gradient
    for y in range(y0, y1):
        ratio = (y - y0) / max(1, (y1 - y0))
        r = int(color_top[0] + (color_bottom[0] - color_top[0]) * ratio)
        g = int(color_top[1] + (color_bottom[1] - color_top[1]) * ratio)
        b = int(color_top[2] + (color_bottom[2] - color_top[2]) * ratio)
        draw.line([(x0 + radius, y), (x1 - radius, y)], fill=(r, g, b))
    # Draw rounded rect outline on top
    draw.rounded_rectangle(bbox, radius=radius, fill=None, outline=outline or darken(color_top), width=width)
    # Fill the corners properly with the main shape
    mask = Image.new("L", img.size, 0)
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle(bbox, radius=radius, fill=255)
    # We'll just use solid fill for cleanliness
    draw.rounded_rectangle(bbox, radius=radius, fill=None, outline=outline or darken(color_top, 0.6), width=width)

def draw_pill(draw, bbox, fill, outline=None):
    """Draw a pill/capsule shape."""
    x0, y0, x1, y1 = bbox
    r = (y1 - y0) // 2
    draw.rounded_rectangle(bbox, radius=r, fill=fill, outline=outline, width=1)

def draw_diamond(draw, cx, cy, size, fill, outline):
    pts = [(cx, cy - size), (cx + size, cy), (cx, cy + size), (cx - size, cy)]
    draw.polygon(pts, fill=fill, outline=outline)

def draw_arrow(draw, start, end, color, width=3, head_size=12):
    """Draw an arrow line with arrowhead."""
    draw.line([start, end], fill=color, width=width)
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    length = math.sqrt(dx*dx + dy*dy)
    if length == 0:
        return
    udx, udy = dx/length, dy/length
    px, py = -udy, udx
    tip = end
    left = (tip[0] - head_size*udx + head_size*0.4*px, tip[1] - head_size*udy + head_size*0.4*py)
    right = (tip[0] - head_size*udx - head_size*0.4*px, tip[1] - head_size*udy - head_size*0.4*py)
    draw.polygon([tip, left, right], fill=color)

def text_center(draw, text, cx, cy, font, fill="white"):
    bb = draw.textbbox((0, 0), text, font=font)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    draw.text((cx - tw//2, cy - th//2), text, font=font, fill=fill)

def draw_icon_circle(draw, cx, cy, r, bg_color, symbol, font):
    """Draw a small circular icon with a symbol character."""
    draw.ellipse((cx-r, cy-r, cx+r, cy+r), fill=bg_color, outline=darken(bg_color), width=2)
    text_center(draw, symbol, cx, cy, font, fill="white")


# =============================================================================
# DIAGRAM 1: Four-Pillar Mind Map (V1-quality restoration)
# =============================================================================
def generate_mindmap():
    W, H = 2400, 1800
    img = Image.new("RGBA", (W, H), (250, 250, 252, 255))
    draw = ImageDraw.Draw(img)

    title_font = get_font(38, bold=True)
    heading_font = get_font(24, bold=True)
    phase_font = get_font(16, bold=True)
    item_font = get_font(17)
    icon_font = get_font(16, bold=True)
    center_font = get_font(22, bold=True)
    sub_font = get_font(16)

    # Title
    text_center(draw, "AI Compute Platform — Fleet Operations Pillars", W//2, 40, title_font, fill="#1B3A5C")

    # ── Center Hub ──
    cx, cy = W//2, H//2 - 20
    draw_shadow_rect(img, (cx-160, cy-55, cx+160, cy+55), 20, shadow_offset=8, blur=10)
    draw = ImageDraw.Draw(img)  # refresh draw after paste
    draw.rounded_rectangle((cx-160, cy-55, cx+160, cy+55), radius=20, fill="#1B3A5C", outline="#0D2137", width=3)
    text_center(draw, "CORE FLEET &", cx, cy-18, center_font, fill="white")
    text_center(draw, "LIFECYCLE HUB", cx, cy+15, center_font, fill="white")

    # ── Pillar configs ──
    pillars = [
        {
            "title": "Healthy Fleet\nMaintenance",
            "phase": "PHASE 1",
            "color": "#2563EB", "dark": "#1D4ED8", "badge": "#1E40AF",
            "pos": (50, 85, 590, 780),
            "items": [
                ("✓", "99.5% Availability Target"),
                ("⚙", "Buffer Pool Model"),
                ("⚡", "Rapid Remediation"),
                ("↺", "Return-to-Fleet Workflows"),
                ("!", "Exception Handling"),
                ("◉", "Observability & Dashboards"),
                ("◉", "Incident 5337 Learnings"),
                ("◉", "Daily Executive Reports"),
            ],
        },
        {
            "title": "Automated Node Lifecycle\n& Certification",
            "phase": "PHASE 2",
            "color": "#059669", "dark": "#047857", "badge": "#065F46",
            "pos": (W-590, 85, W-50, 680),
            "items": [
                ("⊕", "NPD + Controllers"),
                ("⊙", "Host Issue Detection"),
                ("⛔", "Cordon/Taint Enforcement"),
                ("⚙", "BCM Burn-in & DCGM L4"),
                ("⚡", "NCCL / HPL Validation"),
                ("⊞", "Multi-Node Readiness Gates"),
            ],
        },
        {
            "title": "Automated Image\nPipeline",
            "phase": "PHASE 2",
            "color": "#7C3AED", "dark": "#6D28D9", "badge": "#5B21B6",
            "pos": (50, 870, 590, 1440),
            "items": [
                ("⬡", "Packer-Based Pipeline"),
                ("⊛", "GitOps CD Deployment"),
                ("⇋", "Cross-AZ Replication"),
                ("◧", "Self-Service Layers"),
                ("⊞", "Image Versioning & Catalog"),
                ("⚙", "BCM Integration"),
            ],
        },
        {
            "title": "Tenant\nReassignment",
            "phase": "",
            "color": "#EA580C", "dark": "#C2410C", "badge": "#9A3412",
            "pos": (W-590, 870, W-50, 1440),
            "items": [
                ("⇄", "Buffer→Tenant X→Buffer→Y"),
                ("◉", "Re-image + Disk Wipe"),
                ("✓", "Full Recertification Gate"),
                ("⚙", "Network Reconfiguration"),
                ("⊞", "VLAN/Tenant Routing"),
            ],
        },
    ]

    for p in pillars:
        x0, y0, x1, y1 = p["pos"]
        bg = hex_to_rgb(p["color"])
        dk = hex_to_rgb(p["dark"])

        # Shadow
        draw_shadow_rect(img, (x0, y0, x1, y1), 18, shadow_offset=7, blur=9)
        draw = ImageDraw.Draw(img)

        # Main box with gradient effect
        draw.rounded_rectangle((x0, y0, x1, y1), radius=18, fill=p["color"], outline=p["dark"], width=3)
        # Lighter top band for gradient feel
        draw.rounded_rectangle((x0+2, y0+2, x1-2, y0+60), radius=16, fill=lighten(bg, 1.15))

        # Phase badge
        if p["phase"]:
            bw = 110
            draw_pill(draw, (x0+15, y0+12, x0+15+bw, y0+38), fill=p["badge"], outline=dk)
            text_center(draw, p["phase"], x0+15+bw//2, y0+25, phase_font, fill="white")

        # Title
        ty = y0 + 50 if p["phase"] else y0 + 20
        for i, line in enumerate(p["title"].split("\n")):
            draw.text((x0+25, ty + i*30), line, font=heading_font, fill="white")

        # Items with icon circles
        iy = ty + len(p["title"].split("\n")) * 30 + 20
        for icon, text in p["items"]:
            # Icon circle
            icon_r = 14
            icx = x0 + 40
            icy = iy + 2
            draw.ellipse((icx-icon_r, icy-icon_r, icx+icon_r, icy+icon_r),
                         fill=lighten(bg, 1.3), outline="white", width=1)
            text_center(draw, icon, icx, icy-1, icon_font, fill="white")
            # Text
            draw.text((icx + icon_r + 10, iy - 10), text, font=item_font, fill="white")
            iy += 38

        # Connector arrow to center
        mx, my = (x0+x1)//2, (y0+y1)//2
        # Find edge point toward center
        if x1 < cx:  # left pillars
            ex, ey = x1, my
            tx, ty2 = cx-160, cy
        elif x0 > cx:  # right pillars
            ex, ey = x0, my
            tx, ty2 = cx+160, cy
        else:
            ex, ey = mx, y0 if y0 > cy else y1
            tx, ty2 = cx, cy-55 if y0 > cy else cy+55
        draw_arrow(draw, (ex, ey), (tx, ty2), p["color"], width=4, head_size=14)

    # Subtle footer
    draw.text((W//2 - 200, H - 40), "Architecture Design Document v3.0", font=sub_font, fill="#999999")

    out = os.path.join(DIAGRAMS_DIR, "01_mindmap_overview.png")
    img.convert("RGB").save(out, "PNG")
    print(f"✅ Saved: {out}")


# =============================================================================
# DIAGRAM 3: Detection → Enforcement → Recovery Workflow
# =============================================================================
def generate_workflow():
    W, H = 2400, 1500
    img = Image.new("RGBA", (W, H), (250, 250, 252, 255))
    draw = ImageDraw.Draw(img)

    title_font = get_font(36, bold=True)
    box_font = get_font(18, bold=True)
    box_font_sm = get_font(15)
    label_font = get_font(15, bold=True)
    small_font = get_font(13)
    icon_font = get_font(20, bold=True)

    # Title
    text_center(draw, "Detection → Enforcement → Recovery Workflow", W//2, 35, title_font, fill="#1B3A5C")

    # ── Host Signals (left column) ──
    signals = ["GPU", "IB", "FS", "Kubelet", "Runtime"]
    sx, sy_start = 60, 280
    for i, sig in enumerate(signals):
        y = sy_start + i * 55
        draw.rounded_rectangle((sx, y, sx+120, y+40), radius=8, fill="#E5E7EB", outline="#9CA3AF", width=2)
        text_center(draw, sig, sx+60, y+20, box_font, fill="#374151")

    # ── NPD Box ──
    npd_x, npd_y = 250, 350
    draw_shadow_rect(img, (npd_x, npd_y, npd_x+180, npd_y+100), 15, 5, 7)
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle((npd_x, npd_y, npd_x+180, npd_y+100), radius=15, fill="#2563EB", outline="#1D4ED8", width=3)
    text_center(draw, "NPD", npd_x+90, npd_y+30, get_font(22, True), fill="white")
    text_center(draw, "(detectors +", npd_x+90, npd_y+55, small_font, fill="#BFDBFE")
    text_center(draw, "custom plugins)", npd_x+90, npd_y+72, small_font, fill="#BFDBFE")

    # Arrows from signals to NPD
    for i in range(5):
        y = sy_start + i * 55 + 20
        draw_arrow(draw, (sx+120, y), (npd_x, npd_y+50), "#6B7280", 2, 8)

    # ── Three NPD outputs ──
    out_x = 500
    outputs = [
        ("Node Event", "#DBEAFE", "#2563EB", 270),
        ("Node Condition", "#D1FAE5", "#059669", 400),
        ("Taint / Cordon", "#FED7AA", "#EA580C", 530),
    ]
    for label, bg, border, oy in outputs:
        draw_shadow_rect(img, (out_x, oy, out_x+170, oy+50), 10, 4, 5)
        draw = ImageDraw.Draw(img)
        draw.rounded_rectangle((out_x, oy, out_x+170, oy+50), radius=10, fill=bg, outline=border, width=2)
        text_center(draw, label, out_x+85, oy+25, box_font, fill=border)

    # Arrows from NPD to outputs
    for _, _, _, oy in outputs:
        draw_arrow(draw, (npd_x+180, npd_y+50), (out_x, oy+25), "#6B7280", 2, 8)

    # ── Decision Diamond: Allowlisted Self-Heal? ──
    dx, dy = 820, 400
    draw_diamond(draw, dx, dy, 65, "#FEF3C7", "#D97706")
    text_center(draw, "Allowlisted", dx, dy-12, small_font, fill="#92400E")
    text_center(draw, "Self-Heal?", dx, dy+8, small_font, fill="#92400E")

    # Arrow from outputs to diamond
    draw_arrow(draw, (out_x+170, 425), (dx-65, dy), "#6B7280", 2, 8)

    # ── YES path: Attempt Self-Heal ──
    sh_x, sh_y = 720, 570
    draw.text((dx-30, dy+50), "YES", font=label_font, fill="#059669")
    draw_arrow(draw, (dx, dy+65), (sh_x+80, sh_y), "#059669", 3, 10)

    draw_shadow_rect(img, (sh_x, sh_y, sh_x+170, sh_y+70), 12, 4, 6)
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle((sh_x, sh_y, sh_x+170, sh_y+70), radius=12, fill="#EA580C", outline="#C2410C", width=2)
    text_center(draw, "Attempt", sh_x+85, sh_y+20, box_font, fill="white")
    text_center(draw, "Self-Heal", sh_x+85, sh_y+42, box_font_sm, fill="#FED7AA")

    # ── Recovered? diamond ──
    r2x, r2y = 760, 720
    draw_diamond(draw, r2x, r2y, 50, "#FEF3C7", "#D97706")
    text_center(draw, "Recovered?", r2x, r2y, small_font, fill="#92400E")
    draw_arrow(draw, (sh_x+85, sh_y+70), (r2x, r2y-50), "#6B7280", 2, 8)

    # YES → Clear Transient
    ct_x, ct_y = 580, 830
    draw.text((r2x-65, r2y+15), "YES", font=label_font, fill="#059669")
    draw_arrow(draw, (r2x-50, r2y), (ct_x+90, ct_y), "#059669", 3, 10)
    draw_shadow_rect(img, (ct_x, ct_y, ct_x+180, ct_y+65), 12, 4, 6)
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle((ct_x, ct_y, ct_x+180, ct_y+65), radius=12, fill="#059669", outline="#047857", width=2)
    text_center(draw, "Clear Transient", ct_x+90, ct_y+20, box_font, fill="white")
    text_center(draw, "(stay eligible)", ct_x+90, ct_y+42, box_font_sm, fill="#A7F3D0")

    # NO → Quarantine
    q_x, q_y = 900, 830
    draw.text((r2x+35, r2y+15), "NO", font=label_font, fill="#DC2626")
    draw_arrow(draw, (r2x+50, r2y), (q_x+80, q_y), "#DC2626", 3, 10)
    draw_shadow_rect(img, (q_x, q_y, q_x+180, q_y+65), 12, 4, 6)
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle((q_x, q_y, q_x+180, q_y+65), radius=12, fill="#DC2626", outline="#B91C1C", width=2)
    text_center(draw, "Quarantine", q_x+90, q_y+20, box_font, fill="white")
    text_center(draw, "(cordon + taint)", q_x+90, q_y+42, box_font_sm, fill="#FECACA")

    # ── NO path from first diamond → Alert → Repair → Recertify → Return ──
    draw.text((dx+50, dy-35), "NO", font=label_font, fill="#DC2626")

    recovery_chain = [
        ("Alert + Ticket\nRouting", "#FEF3C7", "#D97706", 990, 320),
        ("Repair / RMA", "#FB923C", "#C2410C", 1220, 320),
        ("Recertify\n(BCM + DCGM)", "#7C3AED", "#5B21B6", 1450, 320),
        ("Return to\nBUFFER_HEALTHY", "#059669", "#047857", 1700, 320),
    ]

    # Arrow from diamond NO to first recovery box
    draw_arrow(draw, (dx+65, dy), (recovery_chain[0][3], recovery_chain[0][4]+35), "#DC2626", 3, 10)

    for i, (label, bg, border, bx, by) in enumerate(recovery_chain):
        draw_shadow_rect(img, (bx, by, bx+190, by+75), 12, 4, 6)
        draw = ImageDraw.Draw(img)
        # Use dark fill for colored boxes, light fill for alert
        if i == 0:
            draw.rounded_rectangle((bx, by, bx+190, by+75), radius=12, fill=bg, outline=border, width=2)
            lines = label.split("\n")
            for j, line in enumerate(lines):
                text_center(draw, line, bx+95, by+22+j*22, box_font, fill=border)
        else:
            draw.rounded_rectangle((bx, by, bx+190, by+75), radius=12, fill=bg, outline=border, width=2)
            lines = label.split("\n")
            for j, line in enumerate(lines):
                text_center(draw, line, bx+95, by+22+j*22, box_font, fill="white")

        # Arrow to next
        if i < len(recovery_chain) - 1:
            nx = recovery_chain[i+1][3]
            draw_arrow(draw, (bx+190, by+37), (nx, recovery_chain[i+1][4]+37), "#6B7280", 3, 10)

    # Legend
    lx, ly = 1600, 1050
    draw.text((lx, ly), "Legend", font=get_font(18, True), fill="#1B3A5C")
    legend = [
        ("#2563EB", "Detection"),
        ("#059669", "Healthy / Certified"),
        ("#FEF3C7", "Decision / Alert"),
        ("#EA580C", "Repair / Self-Heal"),
        ("#DC2626", "Quarantine"),
        ("#7C3AED", "Recertification"),
    ]
    for i, (c, t) in enumerate(legend):
        ry = ly + 30 + i * 30
        draw.rounded_rectangle((lx, ry, lx+20, ry+20), radius=4, fill=c, outline=darken(hex_to_rgb(c) if c.startswith("#") else (0,0,0)), width=1)
        draw.text((lx+28, ry), t, font=box_font_sm, fill="#374151")

    out = os.path.join(DIAGRAMS_DIR, "03_workflow_diagram.png")
    img.convert("RGB").save(out, "PNG")
    print(f"✅ Saved: {out}")


# =============================================================================
# DIAGRAM 7: Automated Image Pipeline
# =============================================================================
def generate_image_pipeline():
    W, H = 2400, 1500
    img = Image.new("RGBA", (W, H), (250, 250, 252, 255))
    draw = ImageDraw.Draw(img)

    title_font = get_font(36, bold=True)
    heading_font = get_font(20, bold=True)
    box_font = get_font(17, bold=True)
    item_font = get_font(15)
    label_font = get_font(14, bold=True)
    small_font = get_font(13)

    text_center(draw, "Automated Image Pipeline — Packer-Based GitOps Model", W//2, 35, title_font, fill="#1B3A5C")

    # ── Left: Source Layers ──
    draw.text((80, 90), "Source Layers", font=heading_font, fill="#1B3A5C")
    draw.line([(80, 115), (280, 115)], fill="#1B3A5C", width=2)

    layers = [
        ("Base OS + Drivers", "Compute Platform", "Kernel, NVIDIA Drivers, CUDA,\nContainer Runtime, BCM Agent", "#2563EB", "#1D4ED8"),
        ("DCGM + Diagnostics", "Compute Platform", "DCGM, DCGMI, gpu_burn,\nnccl-tests, nvbandwidth", "#059669", "#047857"),
        ("Storage Agents", "Storage Team", "Weka Client, VAST Agent,\nMount Configuration", "#7C3AED", "#6D28D9"),
        ("K8s Components", "K8s Team", "Kubelet Config, CNI,\nNode Labels/Annotations", "#0891B2", "#0E7490"),
        ("Monitoring", "OE Team", "Log/Metric Agents,\nNPD Config, Alert Rules", "#D97706", "#B45309"),
    ]

    lx = 60
    ly_start = 140
    for i, (title, team, desc, bg, border) in enumerate(layers):
        ly = ly_start + i * 160
        draw_shadow_rect(img, (lx, ly, lx+420, ly+135), 12, 5, 6)
        draw = ImageDraw.Draw(img)
        draw.rounded_rectangle((lx, ly, lx+420, ly+135), radius=12, fill=bg, outline=border, width=2)
        # Header band
        draw.rounded_rectangle((lx+2, ly+2, lx+418, ly+38), radius=10, fill=lighten(hex_to_rgb(bg), 1.2))
        draw.text((lx+15, ly+8), title, font=box_font, fill="white")
        # Team badge
        tb = draw.textbbox((0,0), team, font=small_font)
        tw = tb[2] - tb[0]
        draw_pill(draw, (lx+420-tw-25, ly+8, lx+415, ly+32), fill=darken(hex_to_rgb(bg), 0.7))
        draw.text((lx+420-tw-18, ly+10), team, font=small_font, fill="white")
        # Description
        for j, line in enumerate(desc.split("\n")):
            draw.text((lx+15, ly+48+j*20), line, font=item_font, fill="#E0E7FF")

    # ── Center: Packer Build Pipeline ──
    px, py = 580, 230
    pw, ph = 440, 340
    draw_shadow_rect(img, (px, py, px+pw, py+ph), 18, 8, 10)
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle((px, py, px+pw, py+ph), radius=18, fill="#1B3A5C", outline="#0D2137", width=3)
    # Header
    draw.rounded_rectangle((px+5, py+5, px+pw-5, py+55), radius=14, fill="#2C5F8A")
    text_center(draw, "⚙  Packer Build Pipeline", px+pw//2, py+30, get_font(22, True), fill="white")
    # Items
    packer_items = [
        "HashiCorp Packer + NVIDIA Support",
        "Automated Image Build & Validation",
        "Tests per Layer (unit + integration)",
        "Semantic Versioning (SemVer)",
        "Reproducible & Hermetic Builds",
        "SBOM Generation + Checksums",
    ]
    for i, item in enumerate(packer_items):
        iy = py + 75 + i * 38
        draw.text((px+25, iy), f"▸ {item}", font=item_font, fill="#CBD5E1")

    # ── Git Repository box (below Packer) ──
    gx, gy = 600, 620
    gw, gh = 400, 80
    draw_shadow_rect(img, (gx, gy, gx+gw, gy+gh), 14, 5, 7)
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle((gx, gy, gx+gw, gy+gh), radius=14, fill="#059669", outline="#047857", width=2)
    text_center(draw, "⎇  Git Repository", gx+gw//2, gy+22, box_font, fill="white")
    text_center(draw, "(Source of Truth — CI/CD Trigger on Merge)", gx+gw//2, gy+50, small_font, fill="#A7F3D0")

    # Bidirectional arrow Git ↔ Packer
    draw_arrow(draw, (gx+gw//2 - 30, gy), (px+pw//2 - 30, py+ph), "#059669", 3, 10)
    draw_arrow(draw, (px+pw//2 + 30, py+ph), (gx+gw//2 + 30, gy), "#059669", 3, 10)

    # ── Arrows from source layers to Packer ──
    for i in range(5):
        ly = ly_start + i * 160 + 67
        draw_arrow(draw, (lx+420, ly), (px, py + 50 + i * 55), hex_to_rgb(layers[i][3]), 2, 8)

    # ── Right: Image Catalog ──
    cx2, cy2 = 1120, 170
    cw, ch = 380, 280
    draw_shadow_rect(img, (cx2, cy2, cx2+cw, cy2+ch), 16, 6, 8)
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle((cx2, cy2, cx2+cw, cy2+ch), radius=16, fill="#1E40AF", outline="#1D4ED8", width=2)
    draw.rounded_rectangle((cx2+3, cy2+3, cx2+cw-3, cy2+48), radius=13, fill="#2563EB")
    text_center(draw, "📋  Image Catalog", cx2+cw//2, cy2+25, get_font(20, True), fill="white")

    catalog_items = [
        "Tagged Releases (SemVer)",
        "SBOM + Checksums per Image",
        "Rollback Support",
        "Image Metadata & Provenance",
        "Cross-AZ Distribution Index",
    ]
    for i, item in enumerate(catalog_items):
        draw.text((cx2+20, cy2+60+i*38), f"▸ {item}", font=item_font, fill="#DBEAFE")

    # Arrow from Packer to Catalog
    draw_arrow(draw, (px+pw, py+ph//2 - 50), (cx2, cy2+ch//2), "#2563EB", 3, 12)

    # ── Right: AZ Deployment Targets ──
    azs = [
        ("AZ-1 (Primary)", "#059669", "#047857"),
        ("AZ-2 (Replica)", "#0891B2", "#0E7490"),
        ("AZ-3 (Replica)", "#0891B2", "#0E7490"),
    ]
    az_x = 1580
    for i, (name, bg, border) in enumerate(azs):
        ay = 170 + i * 110
        draw_shadow_rect(img, (az_x, ay, az_x+280, ay+80), 12, 4, 6)
        draw = ImageDraw.Draw(img)
        draw.rounded_rectangle((az_x, ay, az_x+280, ay+80), radius=12, fill=bg, outline=border, width=2)
        text_center(draw, "🏢  " + name, az_x+140, ay+28, box_font, fill="white")
        text_center(draw, "Image deployed + validated", az_x+140, ay+55, small_font, fill="#A7F3D0" if i==0 else "#A5F3FC")
        # Arrow from catalog
        draw_arrow(draw, (cx2+cw, cy2+ch//2 - 30 + i*40), (az_x, ay+40), hex_to_rgb(bg), 2, 8)

    # ── Bottom: BCM Provisioning ──
    bx, by = 1580, 530
    bw, bh = 280, 85
    draw_shadow_rect(img, (bx, by, bx+bw, by+bh), 12, 4, 6)
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle((bx, by, bx+bw, by+bh), radius=12, fill="#EA580C", outline="#C2410C", width=2)
    text_center(draw, "BCM Provisioning", bx+bw//2, by+25, box_font, fill="white")
    text_center(draw, "Image ID tracked in", bx+bw//2, by+48, small_font, fill="#FED7AA")
    text_center(draw, "BCM node record", bx+bw//2, by+65, small_font, fill="#FED7AA")
    draw_arrow(draw, (cx2+cw, cy2+ch - 20), (bx, by+bh//2), "#EA580C", 2, 8)

    # ── Legend ──
    draw.text((80, 980), "Pipeline Flow", font=heading_font, fill="#1B3A5C")
    draw.line([(80, 1005), (250, 1005)], fill="#1B3A5C", width=2)
    flow = [
        "1. Teams contribute layer configs to Git repo",
        "2. CI/CD triggers Packer build on merge",
        "3. Packer builds validated, versioned image",
        "4. Image published to catalog with SBOM",
        "5. Replicated to all target AZs",
        "6. BCM provisions nodes from catalog image",
    ]
    for i, step in enumerate(flow):
        draw.text((80, 1020 + i * 28), step, font=item_font, fill="#374151")

    out = os.path.join(DIAGRAMS_DIR, "07_image_pipeline.png")
    img.convert("RGB").save(out, "PNG")
    print(f"✅ Saved: {out}")


# =============================================================================
# Preserve existing diagram generators
# =============================================================================
def generate_lifecycle_combined():
    """Generate combined lifecycle + NPD detection diagram (unchanged from V3)."""
    # This function preserves the existing 06_lifecycle_combined diagram
    # Content regenerated with matching visual style
    W, H = 2400, 1500
    img = Image.new("RGBA", (W, H), (250, 250, 252, 255))
    draw = ImageDraw.Draw(img)

    title_font = get_font(34, bold=True)
    heading_font = get_font(20, bold=True)
    box_font = get_font(18, bold=True)
    box_sm = get_font(15)
    label_font = get_font(14, bold=True)
    small_font = get_font(13)
    item_font = get_font(15)

    text_center(draw, "Node Lifecycle with NPD Detection & Enforcement", W//2, 35, title_font, fill="#1B3A5C")

    # ── Detection & Enforcement Layer (top) ──
    draw.text((60, 80), "Detection & Enforcement Layer", font=heading_font, fill="#1B3A5C")
    draw.line([(60, 105), (380, 105)], fill="#1B3A5C", width=2)

    # Host Signals
    signals = ["GPU", "IB", "Kubelet", "Runtime", "Storage"]
    draw.text((60, 120), "Host Signals", font=label_font, fill="#6B7280")
    for i, s in enumerate(signals):
        sy = 145 + i * 35
        draw.rounded_rectangle((60, sy, 150, sy+28), radius=6, fill="#E5E7EB", outline="#9CA3AF", width=1)
        text_center(draw, s, 105, sy+14, box_sm, fill="#374151")

    # NPD
    npd_x = 220
    draw_shadow_rect(img, (npd_x, 150, npd_x+160, 300), 12, 4, 6)
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle((npd_x, 150, npd_x+160, 300), radius=12, fill="#2563EB", outline="#1D4ED8", width=2)
    text_center(draw, "NPD", npd_x+80, 190, get_font(22, True), fill="white")
    text_center(draw, "Conditions", npd_x+80, 220, box_sm, fill="#BFDBFE")
    text_center(draw, "Taints", npd_x+80, 245, box_sm, fill="#BFDBFE")
    text_center(draw, "Events", npd_x+80, 270, box_sm, fill="#BFDBFE")

    for i in range(5):
        draw_arrow(draw, (150, 159+i*35), (npd_x, 200+i*20), "#6B7280", 2, 6)

    # Flow boxes top row
    top_states = [
        ("QUARANTINE", "Cordon + Taint\nVerification disabled", "#DC2626", "#B91C1C", 470),
        ("REPAIR", "SW/Config Fix\nHardware Triage", "#FB923C", "#C2410C", 720),
        ("BURN-IN", "BCM burn-in\n6hr+ burn + stress", "#D97706", "#B45309", 970),
        ("RECERTIFY", "DCGM L4, NCCL bus BW\nHPL, NVLink, IB tests", "#7C3AED", "#5B21B6", 1220),
    ]

    for label, desc, bg, border, bx in top_states:
        by = 150
        draw_shadow_rect(img, (bx, by, bx+210, by+100), 12, 4, 6)
        draw = ImageDraw.Draw(img)
        draw.rounded_rectangle((bx, by, bx+210, by+100), radius=12, fill=bg, outline=border, width=2)
        text_center(draw, label, bx+105, by+25, box_font, fill="white")
        for j, line in enumerate(desc.split("\n")):
            text_center(draw, line, bx+105, by+52+j*18, small_font, fill=lighten(hex_to_rgb(bg), 1.6))

    # Arrows between top states
    draw.text((440, 195), "Node Events", font=small_font, fill="#6B7280")
    draw_arrow(draw, (npd_x+160, 225), (470, 200), "#DC2626", 2, 8)
    draw_arrow(draw, (680, 200), (720, 200), "#6B7280", 2, 8)

    # RMA branch
    rma_x, rma_y = 720, 310
    draw_shadow_rect(img, (rma_x, rma_y, rma_x+180, rma_y+60), 10, 4, 5)
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle((rma_x, rma_y, rma_x+180, rma_y+60), radius=10, fill="#EF4444", outline="#DC2626", width=2)
    text_center(draw, "RMA", rma_x+90, rma_y+20, box_font, fill="white")
    text_center(draw, "Hardware Replace", rma_x+90, rma_y+42, small_font, fill="#FECACA")

    draw_arrow(draw, (930, 200), (970, 200), "#6B7280", 2, 8)
    draw_arrow(draw, (825, 250), (825, 310), "#EF4444", 2, 8)
    draw.text((835, 270), "HW fault", font=small_font, fill="#EF4444")
    draw_arrow(draw, (rma_x+180, rma_y+30), (970, 200), "#EF4444", 2, 8)
    draw_arrow(draw, (1180, 200), (1220, 200), "#6B7280", 2, 8)

    # Pass/Fail from RECERTIFY
    draw.text((1440, 175), "Pass ↓", font=label_font, fill="#059669")
    draw.text((1440, 225), "Fail ↗", font=label_font, fill="#DC2626")

    # ── Node Lifecycle States (bottom half) ──
    draw.text((60, 430), "Node Lifecycle States", font=heading_font, fill="#1B3A5C")
    draw.line([(60, 455), (320, 455)], fill="#1B3A5C", width=2)

    # INTERNAL_TENANT_A
    ita_x, ita_y = 60, 480
    draw_shadow_rect(img, (ita_x, ita_y, ita_x+500, ita_y+330), 16, 6, 8)
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle((ita_x, ita_y, ita_x+500, ita_y+330), radius=16, fill="#1E40AF", outline="#1D4ED8", width=3)
    draw.rounded_rectangle((ita_x+5, ita_y+5, ita_x+495, ita_y+55), radius=12, fill="#2563EB")
    text_center(draw, "INTERNAL TENANT A", ita_x+250, ita_y+18, box_font, fill="white")
    text_center(draw, "Certification Testing Environment", ita_x+250, ita_y+40, box_sm, fill="#93C5FD")

    cert_layers = [
        "Layer 1: Hardware pre-flight checks",
        "Layer 2: BCM Burn-in (6h, gpu_burn)",
        "Layer 3: DCGM L4 (all plugins ~90m)",
        "Layer 4: NCCL all_reduce ≥1530 GB/s",
        "Layer 5: HPL / HPL-MxP ≥70% peak",
        "Layer 6: NVLink5 + IB NDR 400G",
        "Layer 7: Storage + System health",
        "Layer 8: Multi-node job validation",
        "Layer 9: K8s dummy job scheduling",
    ]
    for i, layer in enumerate(cert_layers):
        draw.text((ita_x+20, ita_y+70+i*28), f"▸ {layer}", font=item_font, fill="#DBEAFE")

    draw.text((ita_x+20, ita_y+332), "Daily certification runs.", font=small_font, fill="#93C5FD")

    # CERTIFIED
    c_x, c_y = 650, 500
    draw_shadow_rect(img, (c_x, c_y, c_x+200, c_y+80), 12, 5, 7)
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle((c_x, c_y, c_x+200, c_y+80), radius=12, fill="#059669", outline="#047857", width=3)
    text_center(draw, "CERTIFIED", c_x+100, c_y+25, box_font, fill="white")
    text_center(draw, "All tests passed", c_x+100, c_y+50, box_sm, fill="#A7F3D0")

    draw.text((ita_x+510, ita_y+30), "all tests pass ↓", font=label_font, fill="#059669")
    draw_arrow(draw, (ita_x+500, ita_y+50), (c_x, c_y+40), "#059669", 3, 10)

    # Recertify passes → into Tenant A
    draw_arrow(draw, (1430, 210), (c_x+200, c_y+20), "#059669", 2, 8)
    draw.text((1200, 300), "admit to fleet + certification testing", font=small_font, fill="#059669")
    draw_arrow(draw, (c_x, c_y+60), (ita_x+500, ita_y+300), "#2563EB", 2, 8)
    draw.text((c_x-120, c_y+100), "→ re-assigns to\ncertification", font=small_font, fill="#6B7280")

    # QUARANTINED (bottom)
    qb_x, qb_y = 900, 650
    draw_shadow_rect(img, (qb_x, qb_y, qb_x+220, qb_y+80), 12, 4, 6)
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle((qb_x, qb_y, qb_x+220, qb_y+80), radius=12, fill="#DC2626", outline="#B91C1C", width=2)
    text_center(draw, "QUARANTINED", qb_x+110, qb_y+25, box_font, fill="white")
    text_center(draw, "Blocked, removed", qb_x+110, qb_y+52, box_sm, fill="#FECACA")

    # BUFFER_HEALTHY
    bh_x, bh_y = 650, 830
    draw_shadow_rect(img, (bh_x, bh_y, bh_x+220, bh_y+80), 12, 5, 7)
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle((bh_x, bh_y, bh_x+220, bh_y+80), radius=12, fill="#059669", outline="#047857", width=2)
    text_center(draw, "BUFFER_HEALTHY", bh_x+110, bh_y+25, box_font, fill="white")
    text_center(draw, "Certified & available", bh_x+110, bh_y+52, box_sm, fill="#A7F3D0")

    # TENANT_ASSIGNED
    ta_x, ta_y = 1050, 830
    draw_shadow_rect(img, (ta_x, ta_y, ta_x+220, ta_y+80), 12, 5, 7)
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle((ta_x, ta_y, ta_x+220, ta_y+80), radius=12, fill="#2563EB", outline="#1D4ED8", width=2)
    text_center(draw, "TENANT_ASSIGNED", ta_x+110, ta_y+25, box_font, fill="white")
    text_center(draw, "Production workload", ta_x+110, ta_y+52, box_sm, fill="#BFDBFE")

    # Transitions
    draw_arrow(draw, (c_x+100, c_y+80), (bh_x+110, bh_y), "#059669", 2, 8)
    draw.text((c_x-10, c_y+80+20), "admit to fleet", font=small_font, fill="#059669")

    draw_arrow(draw, (bh_x+220, bh_y+40), (ta_x, ta_y+40), "#2563EB", 3, 10)
    draw.text((bh_x+230, bh_y+15), "attach tenant label", font=small_font, fill="#2563EB")

    draw.text((qb_x-30, qb_y-35), "cert regression / blocking signal", font=small_font, fill="#DC2626")
    draw_arrow(draw, (bh_x+220, bh_y+20), (qb_x, qb_y+60), "#DC2626", 2, 8)
    draw_arrow(draw, (ta_x, ta_y+20), (qb_x+220, qb_y+60), "#DC2626", 2, 8)
    draw.text((ta_x-80, ta_y-15), "blocking signal", font=small_font, fill="#DC2626")

    draw_arrow(draw, (ta_x+220, ta_y+40), (ta_x+320, ta_y+40), "#6B7280", 2, 8)
    draw.text((ta_x+330, ta_y+25), "detach → reimage →\ndisk wipe → recertify", font=small_font, fill="#6B7280")

    # Legend
    lx, ly = 1550, 980
    draw.text((lx, ly), "Legend", font=heading_font, fill="#1B3A5C")
    legend = [
        ("#059669", "Healthy / Certification"),
        ("#2563EB", "Active Tenant Service"),
        ("#DC2626", "Quarantined / Blocked"),
        ("#D97706", "Burn-in Testing"),
        ("#7C3AED", "Recertification Pipeline"),
        ("#EF4444", "RMA / Hardware Repair"),
    ]
    for i, (c, t) in enumerate(legend):
        ry = ly + 30 + i * 28
        draw.rounded_rectangle((lx, ry, lx+20, ry+20), radius=4, fill=c, width=0)
        draw.text((lx+28, ry), t, font=item_font, fill="#374151")

    out = os.path.join(DIAGRAMS_DIR, "06_lifecycle_combined.png")
    img.convert("RGB").save(out, "PNG")
    print(f"✅ Saved: {out}")


if __name__ == "__main__":
    generate_mindmap()
    generate_workflow()
    generate_image_pipeline()
    generate_lifecycle_combined()
    print("\n✅ All diagrams generated!")
