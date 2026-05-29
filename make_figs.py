# -*- coding: utf-8 -*-
"""Generate matplotlib figures for 分析化学 重心 chapter upgrades.
All figures saved to img/ with prefix 'fxy_' to avoid clashing with existing PPT crops.
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import matplotlib.font_manager as fm

# CJK font
for cand in ["Microsoft YaHei", "SimHei", "SimSun"]:
    if any(f.name == cand for f in fm.fontManager.ttflist):
        plt.rcParams["font.sans-serif"] = [cand]
        break
plt.rcParams["axes.unicode_minus"] = False

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "img")
os.makedirs(OUT, exist_ok=True)

PRI = "#1a5276"
ACC = "#c0392b"
BLUE = "#2980b9"
GREEN = "#27ae60"
ORANGE = "#e67e22"
GREY = "#7f8c8d"


def save(fig, name):
    p = os.path.join(OUT, name)
    fig.savefig(p, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("saved", p)


# ============================================================
# FIG 1: pH 公式选择判别地图 (一元弱酸) —— FXY 头号弱点 ch5-1b
# ============================================================
def fig_ph_decision():
    fig, ax = plt.subplots(figsize=(8.6, 6.4))
    ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.axis("off")

    def box(x, y, w, h, text, fc, ec=PRI, fs=10.5, tc="#222"):
        b = FancyBboxPatch((x - w/2, y - h/2), w, h,
                           boxstyle="round,pad=0.08,rounding_size=0.12",
                           fc=fc, ec=ec, lw=1.6)
        ax.add_patch(b)
        ax.text(x, y, text, ha="center", va="center", fontsize=fs, color=tc, wrap=True)

    def arrow(x1, y1, x2, y2, label="", color=GREY, lx=0, ly=0):
        a = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>",
                            mutation_scale=16, lw=1.6, color=color)
        ax.add_patch(a)
        if label:
            ax.text((x1+x2)/2 + lx, (y1+y2)/2 + ly, label, ha="center",
                    va="center", fontsize=9.5, color=color, fontweight="bold",
                    bbox=dict(boxstyle="round,pad=0.18", fc="white", ec="none"))

    ax.text(5, 9.55, "一元弱酸 pH 公式选择判别地图", ha="center",
            fontsize=14, fontweight="bold", color=PRI)
    ax.text(5, 9.05, "口诀：20Kw 管水，500 管自己（先算两个数再选式）",
            ha="center", fontsize=10, color=ACC)

    # gate 1
    box(5, 8.0, 5.4, 0.95, "闸门①  $cK_a \\geq 20K_w$ ?\n(能否忽略水的电离)", "#eaf2fb", BLUE, 11)
    # gate 2 (yes path)
    box(2.6, 5.7, 4.0, 0.95, "闸门②  $c/K_a \\geq 500$ ?\n(能否忽略酸自身解离)", "#eaf2fb", BLUE, 10.5)
    arrow(3.6, 7.52, 2.9, 6.2, "满足 OK", GREEN, lx=-0.5)
    #极弱酸 (gate1 no)
    box(8.0, 5.7, 3.0, 1.5, "极弱酸式\n$[H^+]=\\sqrt{cK_a+K_w}$\n(酸太弱/太稀)", "#fef5e7", ORANGE, 10)
    arrow(6.3, 7.52, 7.6, 6.5, "不满足 X", ACC, lx=0.55)

    # leaves under gate2
    box(1.2, 3.0, 2.4, 1.5, "最简式\n$[H^+]=\\sqrt{cK_a}$\n两条都满足 ★", "#e9f7ef", GREEN, 10)
    arrow(2.0, 5.22, 1.4, 3.8, "满足 OK", GREEN, lx=-0.45)
    box(4.4, 3.0, 3.1, 1.6, "近似式 (一元二次)\n$[H^+]=\\dfrac{-K_a+\\sqrt{K_a^2+4cK_a}}{2}$\n(酸略强/略稀)", "#fef5e7", ORANGE, 9.3)
    arrow(3.3, 5.22, 4.2, 3.85, "不满足 X", ACC, lx=0.55)

    # bottom note
    ax.text(5, 1.15,
            "弱碱：整套照搬，把 $H^+\\to OH^-$、$K_a\\to K_b$，最后 $pH=14-pOH$\n"
            "多元酸：若 $K_{a1}/K_{a2}\\geq10^4$ 当一元弱酸，$K_a$ 取 $K_{a1}$",
            ha="center", fontsize=10, color="#444",
            bbox=dict(boxstyle="round,pad=0.4", fc="#f9f7f2", ec="#e0d8c8"))
    save(fig, "fxy_ph_decision_map.png")


# ============================================================
# FIG 2: 两套判别式对比 (可行性 vs 公式选择) —— ch5-1b
# ============================================================
def fig_two_criteria():
    fig, ax = plt.subplots(figsize=(8.8, 4.3))
    ax.set_xlim(0, 10); ax.set_ylim(0, 6); ax.axis("off")
    ax.text(5, 5.6, "两套判别式：别再混了（FXY 卡了 5 次的根源）",
            ha="center", fontsize=13.5, fontweight="bold", color=ACC)

    # left card: 可行性
    l = FancyBboxPatch((0.3, 0.5), 4.5, 4.3, boxstyle="round,pad=0.1,rounding_size=0.15",
                       fc="#fdecea", ec=ACC, lw=2)
    ax.add_patch(l)
    ax.text(2.55, 4.35, "判别式①  能不能滴", ha="center", fontsize=12.5,
            fontweight="bold", color=ACC)
    ax.text(2.55, 3.55, "问题：这个酸/碱\n能否被准确滴定？", ha="center", fontsize=10.5, color="#333")
    ax.text(2.55, 2.55, "$cK_a \\geq 10^{-8}$\n多元分步 $K_{a1}/K_{a2}\\geq10^4$",
            ha="center", fontsize=11, color="#222")
    ax.text(2.55, 1.25, "本质：化学反应\n完全度判据", ha="center", fontsize=10,
            color=GREY, style="italic")

    # right card: 公式选择
    r = FancyBboxPatch((5.2, 0.5), 4.5, 4.3, boxstyle="round,pad=0.1,rounding_size=0.15",
                       fc="#eaf2fb", ec=BLUE, lw=2)
    ax.add_patch(r)
    ax.text(7.45, 4.35, "判别式②  用哪个式子算", ha="center", fontsize=12.5,
            fontweight="bold", color=BLUE)
    ax.text(7.45, 3.55, "问题：算 pH 用\n最简式还是近似式？", ha="center", fontsize=10.5, color="#333")
    ax.text(7.45, 2.55, "$cK_a$ vs $20K_w$ (忽略水?)\n$c/K_a$ vs 500 (忽略解离?)",
            ha="center", fontsize=10.5, color="#222")
    ax.text(7.45, 1.25, "本质：数学近似\n误差判据 (<5%)", ha="center", fontsize=10,
            color=GREY, style="italic")

    ax.text(5, 0.15, "一个问『滴不滴得动』，一个问『算 pH 能不能偷懒』——数值阈值完全不相干",
            ha="center", fontsize=9.5, color="#555")
    save(fig, "fxy_two_criteria.png")


# ============================================================
# FIG 3: t 分布 vs 正态分布 (不同自由度) —— ch3-2
# ============================================================
def fig_t_dist():
    from math import gamma, pi, sqrt
    def t_pdf(x, f):
        c = gamma((f+1)/2) / (sqrt(f*pi) * gamma(f/2))
        return c * (1 + x*x/f) ** (-(f+1)/2)
    x = np.linspace(-5, 5, 600)
    fig, ax = plt.subplots(figsize=(7.6, 4.6))
    ax.plot(x, np.exp(-x**2/2)/np.sqrt(2*np.pi), color="black", lw=2.4,
            label="正态分布 N(0,1)  ($f\\to\\infty$)")
    for f, col in [(2, ACC), (5, ORANGE), (10, BLUE)]:
        ax.plot(x, [t_pdf(xi, f) for xi in x], color=col, lw=1.9,
                label=f"t 分布  f={f} (n={f+1})")
    ax.axvline(0, color=GREY, lw=0.8, ls=":")
    ax.set_xlabel("t", fontsize=11)
    ax.set_ylabel("概率密度", fontsize=11)
    ax.set_title("t 分布：自由度 f 越小，两尾越『肥』(小样本更不确定)",
                 fontsize=12, color=PRI, fontweight="bold")
    ax.legend(fontsize=9.5, loc="upper right")
    ax.set_ylim(0, 0.42)
    ax.annotate("f 越小，尾巴越肥\n→ 临界 t 越大\n→ 置信区间越宽",
                xy=(2.6, t_pdf(2.6, 2)), xytext=(3.0, 0.27),
                fontsize=9.5, color=ACC,
                arrowprops=dict(arrowstyle="->", color=ACC))
    ax.grid(alpha=0.25)
    save(fig, "fxy_t_distribution.png")


# ============================================================
# FIG 4: 误差统计大题 5 步流程 —— ch3-2
# ============================================================
def fig_stat_flow():
    fig, ax = plt.subplots(figsize=(9.2, 3.0))
    ax.set_xlim(0, 10); ax.set_ylim(0, 3); ax.axis("off")
    steps = [
        ("①\n算 $\\bar{x}$、$s$", "#eaf2fb"),
        ("②\nQ/Grubbs\n剔可疑值", "#fef5e7"),
        ("③\n剔除后\n重算 $\\bar{x},s,n,f$", "#fdecea"),
        ("④\n95% 置信区间\n$\\mu=\\bar{x}\\pm\\frac{t s}{\\sqrt{n}}$", "#eaf2fb"),
        ("⑤\nt 检验\n判系统误差", "#e9f7ef"),
    ]
    n = len(steps)
    w = 1.62; gap = (10 - n*w) / (n+1)
    for i, (txt, fc) in enumerate(steps):
        x = gap + i*(w+gap)
        ec = ACC if i == 2 else PRI
        lw = 2.4 if i == 2 else 1.6
        b = FancyBboxPatch((x, 0.9), w, 1.3, boxstyle="round,pad=0.06,rounding_size=0.1",
                           fc=fc, ec=ec, lw=lw)
        ax.add_patch(b)
        ax.text(x+w/2, 1.55, txt, ha="center", va="center", fontsize=10, color="#222")
        if i < n-1:
            a = FancyArrowPatch((x+w, 1.55), (x+w+gap, 1.55), arrowstyle="-|>",
                                mutation_scale=15, lw=1.8, color=GREY)
            ax.add_patch(a)
    ax.text(5, 2.65, "误差统计大题：固定 5 步，背成肌肉记忆", ha="center",
            fontsize=13, fontweight="bold", color=PRI)
    ax.text(gap + 2*(w+gap) + w/2, 0.45, "★最易漏：剔除后必须重算", ha="center",
            fontsize=9.2, color=ACC, fontweight="bold")
    save(fig, "fxy_stat_5steps.png")


# ============================================================
# FIG 5: 林邦终点误差 Et 6 步分步流程 —— ch6
# ============================================================
def fig_et_steps():
    fig, ax = plt.subplots(figsize=(8.4, 6.0))
    ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.axis("off")
    ax.text(5, 9.55, "配位滴定终点误差 $E_t$：6 步分步书写法", ha="center",
            fontsize=13.5, fontweight="bold", color=PRI)
    ax.text(5, 9.05, "$E_t=\\dfrac{10^{\\Delta pM'}-10^{-\\Delta pM'}}{\\sqrt{c_{sp,M}\\,K'_{MY}}}\\times100\\%,"
            "\\quad \\Delta pM'=pM'_{ep}-pM'_{sp}$",
            ha="center", fontsize=11.5, color=ACC)
    steps = [
        ("① 求 $c_{sp,M}$", "计量点稀释后浓度\n$c_{sp}=c_0/2$ (等浓等体积)", "#fdecea"),
        ("② 求 $\\lg K'_{MY}$", "$\\lg K_{MY}-\\lg\\alpha_{Y(H)}-\\lg\\alpha_{M}$\n(条件常数，带撇)", "#eaf2fb"),
        ("③ 求 $pM'_{sp}$", "$pM'_{sp}=\\frac{1}{2}(\\lg K'_{MY}+pc_{sp})$", "#eaf2fb"),
        ("④ 求 $pM'_{ep}$", "$pM'_{ep}=\\lg K'_{MIn}$\n(由金属指示剂定)", "#fef5e7"),
        ("⑤ 求 $\\Delta pM'$", "$\\Delta pM'=pM'_{ep}-pM'_{sp}$\n(符号别反!)", "#fdecea"),
        ("⑥ 代入 $E_t$ 公式", "分母用 $\\sqrt{c_{sp}K'_{MY}}$\n得百分数误差", "#e9f7ef"),
    ]
    y = 8.0
    for i, (head, body, fc) in enumerate(steps):
        ec = ACC if i in (0, 4) else PRI
        b = FancyBboxPatch((1.0, y-0.55), 8.0, 1.0,
                           boxstyle="round,pad=0.06,rounding_size=0.1",
                           fc=fc, ec=ec, lw=1.7)
        ax.add_patch(b)
        ax.text(2.5, y, head, ha="center", va="center", fontsize=11.5,
                fontweight="bold", color=PRI)
        ax.text(6.4, y, body, ha="center", va="center", fontsize=9.8, color="#222")
        if i < len(steps)-1:
            a = FancyArrowPatch((5, y-0.55), (5, y-0.95), arrowstyle="-|>",
                                mutation_scale=13, lw=1.6, color=GREY)
            ax.add_patch(a)
        y -= 1.27
    save(fig, "fxy_et_6steps.png")


# ============================================================
# FIG 6: 条件稳定常数 lgK' 削减条形图 —— ch6
# ============================================================
def fig_condK_bar():
    # 2022 真题 Bi/Pb：lgK_BiY=27.9, pH=1 时 lgα_Y(H)=18.3 -> lgK'=9.6
    fig, ax = plt.subplots(figsize=(7.6, 4.4))
    labels = ["理论\n$\\lg K_{BiY}$", "被酸效应削\n$-\\lg\\alpha_{Y(H)}$", "条件常数\n$\\lg K'_{BiY}$"]
    base = 27.9
    cut = 18.3
    final = round(base - cut, 2)
    # waterfall
    ax.bar(0, base, color=BLUE, width=0.55)
    ax.text(0, base+0.5, f"{base}", ha="center", fontsize=11, fontweight="bold")
    ax.bar(1, cut, bottom=final, color=ACC, width=0.55)
    ax.text(1, base+0.5, f"$-{cut}$", ha="center", fontsize=11, fontweight="bold", color=ACC)
    ax.bar(2, final, color=GREEN, width=0.55)
    ax.text(2, final+0.5, f"{final}", ha="center", fontsize=11, fontweight="bold", color=GREEN)
    ax.axhline(final, color=GREEN, ls=":", lw=1, alpha=0.6)
    ax.set_xticks([0, 1, 2]); ax.set_xticklabels(labels, fontsize=10)
    ax.set_ylabel("$\\lg K$", fontsize=11)
    ax.set_ylim(0, 31)
    ax.set_title("条件稳定常数 = 理论战斗力 − 副反应削弱\n(2022 真题 Bi/EDTA，pH=1)",
                 fontsize=11.5, color=PRI, fontweight="bold")
    ax.annotate("$\\lg(c_{sp}K')=9.6-2.0=7.6\\geq6$\n→ 仍能准确滴定 OK",
                xy=(2, final), xytext=(0.4, 13.5), fontsize=10, color=GREEN,
                arrowprops=dict(arrowstyle="->", color=GREEN))
    ax.grid(axis="y", alpha=0.25)
    save(fig, "fxy_condK_waterfall.png")


# ============================================================
# FIG 7: 弱酸滴定曲线 (含半当量点/计量点标注) —— ch6/ch5 复用题型B
# ============================================================
def fig_weak_acid_curve():
    # 0.1000 NaOH 滴 0.1000 HA, pKa=4.87 (2022 真题三-4)
    pKa = 4.87; Ka = 10**(-pKa); c = 0.1000; V0 = 20.00; Kw = 1e-14
    Vs = np.linspace(0.01, 39.5, 500)
    pH = []
    for V in Vs:
        n_HA0 = c*V0/1000.0
        n_OH = c*V/1000.0
        Vtot = (V0+V)/1000.0
        if V < V0 - 1e-6:
            n_A = n_OH; n_HAr = n_HA0 - n_OH
            ca = n_HAr/Vtot; cb = n_A/Vtot
            if n_A < 1e-9:
                H = np.sqrt(Ka*ca)
            else:
                H = Ka*ca/cb
            pH.append(-np.log10(H))
        elif abs(V - V0) < 1e-6:
            cA = n_HA0/Vtot; Kb = Kw/Ka
            OH = np.sqrt(Kb*cA); pH.append(14+np.log10(OH))
        else:
            cOHex = (n_OH - n_HA0)/Vtot
            pH.append(14+np.log10(cOHex))
    fig, ax = plt.subplots(figsize=(7.6, 4.8))
    ax.plot(Vs, pH, color=PRI, lw=2.4)
    # half-equivalence
    ax.plot(10, pKa, "o", color=ORANGE, ms=8)
    ax.annotate(f"半当量点 (50%)\n$pH=pK_a={pKa}$", xy=(10, pKa), xytext=(2, 6.8),
                fontsize=9.5, color=ORANGE,
                arrowprops=dict(arrowstyle="->", color=ORANGE))
    # equivalence
    ax.plot(20, 8.78, "o", color=ACC, ms=9)
    ax.annotate("计量点\nV=20.00 mL, pH=8.78\n(偏碱侧→选酚酞)", xy=(20, 8.78),
                xytext=(22, 5.2), fontsize=9.5, color=ACC,
                arrowprops=dict(arrowstyle="->", color=ACC))
    ax.axhspan(7.7, 10.0, xmin=0.46, xmax=0.56, color=ACC, alpha=0.12)
    ax.axvline(20, color=GREY, ls=":", lw=1)
    ax.set_xlabel("加入 NaOH 体积 V / mL", fontsize=11)
    ax.set_ylabel("pH", fontsize=11)
    ax.set_title("强碱滴定一元弱酸曲线 (2022 真题三-4, $pK_a$=4.87)",
                 fontsize=11.5, color=PRI, fontweight="bold")
    ax.set_ylim(2, 12); ax.grid(alpha=0.25)
    save(fig, "fxy_weak_acid_curve.png")


if __name__ == "__main__":
    fig_ph_decision()
    fig_two_criteria()
    fig_t_dist()
    fig_stat_flow()
    fig_et_steps()
    fig_condK_bar()
    fig_weak_acid_curve()
    print("ALL DONE")
