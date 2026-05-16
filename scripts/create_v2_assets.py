from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "v2"
OUT.mkdir(parents=True, exist_ok=True)

FONT_REG = "/System/Library/Fonts/Hiragino Sans GB.ttc"
FONT_BOLD = "/System/Library/Fonts/STHeiti Medium.ttc"


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REG, size=size)


def rounded(draw: ImageDraw.ImageDraw, box, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def multiline(draw: ImageDraw.ImageDraw, xy, text, fnt, fill, spacing=8):
    draw.multiline_text(xy, text, font=fnt, fill=fill, spacing=spacing)


def save(img: Image.Image, name: str):
    img.save(OUT / name, "PNG", optimize=True)


def codex_os():
    img = Image.new("RGB", (1600, 900), "#0f172a")
    d = ImageDraw.Draw(img)
    d.rectangle((0, 0, 1600, 900), fill="#0f172a")
    d.ellipse((1050, -260, 1880, 570), fill="#172554")
    d.ellipse((-260, 520, 540, 1210), fill="#0e7490")

    d.text((90, 80), "Codex Operating System", font=font(66, True), fill="#f8fafc")
    d.text((94, 160), "把模型能力变成可持续复利的工程系统", font=font(34), fill="#cbd5e1")

    center = (560, 345, 1040, 595)
    rounded(d, center, 42, "#f8fafc", "#dbeafe", 4)
    d.text((665, 405), "Codex / GPT", font=font(54, True), fill="#0f172a")
    d.text((645, 480), "Reasoning + Tools + Context", font=font(26), fill="#334155")

    cards = [
        ((90, 270, 390, 390), "AGENTS.md", "长期规则\n项目约束"),
        ((90, 480, 390, 600), "Skills", "按需加载\n复用流程"),
        ((1210, 270, 1510, 390), "MCP", "结构化工具\n外部系统"),
        ((1210, 480, 1510, 600), "Hooks / Rules", "确定性护栏\n权限边界"),
        ((420, 700, 720, 820), "Subagents", "并行探索\n专门角色"),
        ((880, 700, 1180, 820), "Verification", "测试证据\n风险闭环"),
    ]
    for box, title, desc in cards:
        rounded(d, box, 26, "#111827", "#38bdf8", 3)
        d.text((box[0] + 28, box[1] + 24), title, font=font(30, True), fill="#e0f2fe")
        d.text((box[0] + 28, box[1] + 66), desc, font=font(24), fill="#cbd5e1", spacing=4)

    d.text((90, 830), "Top 1% 的差异不是 prompt 更长，而是上下文、流程、验证、记忆被系统化。", font=font(28), fill="#d1fae5")
    save(img, "codex-operating-system.png")


def surface_map():
    img = Image.new("RGB", (1600, 950), "#f8fafc")
    d = ImageDraw.Draw(img)
    d.rectangle((0, 0, 1600, 950), fill="#f8fafc")
    d.text((90, 70), "Codex Surface Map", font=font(58, True), fill="#0f172a")
    d.text((94, 142), "不同入口服务不同任务，不要把所有任务都塞进一个聊天窗口。", font=font(30), fill="#475569")

    headers = ["Surface", "最佳场景", "成熟用法"]
    xs = [90, 410, 930]
    widths = [280, 470, 580]
    y = 230
    row_h = 86
    for i, h in enumerate(headers):
        rounded(d, (xs[i], y, xs[i] + widths[i], y + 64), 16, "#0f172a")
        d.text((xs[i] + 20, y + 16), h, font=font(28, True), fill="#f8fafc")
    rows = [
        ("App", "多项目、多线程、review pane", "用作日常控制台和任务总览"),
        ("CLI", "本地工程、日志、JSONL、自动化", "接入 shell、CI、脚本和 schema 输出"),
        ("IDE", "打开文件上下文、局部修改", "边看边改，适合小范围高频协作"),
        ("Cloud", "后台 issue、PR、CI 修复", "把明确任务交给远程工程师"),
        ("GitHub", "PR review、@codex fix", "把 Codex 嵌入团队研发流程"),
        ("Mobile", "跟进长任务、批准动作", "离开电脑也能接管后台任务"),
    ]
    y += 82
    for idx, row in enumerate(rows):
        fill = "#ffffff" if idx % 2 == 0 else "#eef6ff"
        for i, txt in enumerate(row):
            d.rounded_rectangle((xs[i], y, xs[i] + widths[i], y + row_h - 10), radius=14, fill=fill, outline="#cbd5e1", width=2)
            d.text((xs[i] + 20, y + 22), txt, font=font(25, i == 0), fill="#0f172a")
        y += row_h

    d.text((90, 860), "原则: 能用 CLI 确定性解决的，不一定上 MCP；需要长期复用的，沉淀为 skill。", font=font(27), fill="#0f766e")
    save(img, "surface-map.png")


def workflow_loop():
    img = Image.new("RGB", (1600, 850), "#fff7ed")
    d = ImageDraw.Draw(img)
    d.text((90, 70), "Codex Delivery Loop", font=font(58, True), fill="#111827")
    d.text((94, 142), "每个任务都按 Explore -> Plan -> Implement -> Review -> Verify -> Capture 形成闭环。", font=font(30), fill="#475569")
    steps = [
        ("Explore", "只读探索\n真实调用链"),
        ("Plan", "拆阶段\n定义风险"),
        ("Implement", "最小改动\nTDD 优先"),
        ("Review", "owner-level\n找真实问题"),
        ("Verify", "测试证据\n可复现结果"),
        ("Capture", "沉淀 skill\n更新规则"),
    ]
    x0, y0 = 90, 330
    w, h, gap = 210, 180, 38
    colors = ["#0ea5e9", "#2563eb", "#7c3aed", "#db2777", "#ea580c", "#059669"]
    for i, (title, desc) in enumerate(steps):
        x = x0 + i * (w + gap)
        rounded(d, (x, y0, x + w, y0 + h), 28, colors[i])
        d.text((x + 26, y0 + 30), title, font=font(30, True), fill="#ffffff")
        d.text((x + 26, y0 + 82), desc, font=font(25), fill="#f8fafc", spacing=7)
        if i < len(steps) - 1:
            d.line((x + w + 8, y0 + h // 2, x + w + gap - 8, y0 + h // 2), fill="#334155", width=5)
            d.polygon([(x + w + gap - 8, y0 + h // 2), (x + w + gap - 26, y0 + h // 2 - 12), (x + w + gap - 26, y0 + h // 2 + 12)], fill="#334155")
    rounded(d, (170, 650, 1430, 755), 28, "#ffffff", "#fed7aa", 3)
    d.text((220, 684), "Done Definition: 代码可运行、测试有证据、diff 可 review、剩余风险说清楚。", font=font(32, True), fill="#9a3412")
    save(img, "delivery-loop.png")


def roadmap():
    img = Image.new("RGB", (1600, 850), "#ecfeff")
    d = ImageDraw.Draw(img)
    d.text((90, 70), "90-Day Operator Roadmap", font=font(58, True), fill="#0f172a")
    d.text((94, 142), "从会用 Codex，到能把 Codex 讲给别人听。", font=font(30), fill="#475569")
    phases = [
        ("Days 1-7", "基础能力", "App / CLI / IDE\nPrompt + 验证"),
        ("Week 2", "配置能力", "AGENTS.md\nconfig + rules"),
        ("Weeks 3-4", "工作流能力", "TDD / Review\nDomain skills"),
        ("Month 2", "编排能力", "Subagents\nWorktrees + MCP"),
        ("Month 3", "专家能力", "Evals\n课程与团队 playbook"),
    ]
    x, y = 110, 300
    for i, (time, title, desc) in enumerate(phases):
        x1 = x + i * 292
        rounded(d, (x1, y, x1 + 248, y + 310), 30, "#ffffff", "#67e8f9", 4)
        d.ellipse((x1 + 82, y - 48, x1 + 166, y + 36), fill="#0891b2")
        d.text((x1 + 110, y - 32), str(i + 1), font=font(42, True), fill="#ffffff", anchor="mm")
        d.text((x1 + 28, y + 58), time, font=font(25, True), fill="#155e75")
        d.text((x1 + 28, y + 112), title, font=font(34, True), fill="#0f172a")
        d.text((x1 + 28, y + 178), desc, font=font(25), fill="#334155", spacing=8)
    d.text((110, 715), "验收标准: 你不仅能完成任务，还能解释失败、改造流程、沉淀成可复用资产。", font=font(31, True), fill="#0f766e")
    save(img, "ninety-day-roadmap.png")


if __name__ == "__main__":
    codex_os()
    surface_map()
    workflow_loop()
    roadmap()
    print(f"wrote {OUT}")
