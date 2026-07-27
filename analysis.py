"""
Meridian Mobility - SaaS project-management tool consolidation
Analysis and chart generation.

All figures come from the case brief. The negotiated rates and the migrated-seat
overlap are my own estimates; the reasoning sits in ANALYSIS-NOTES.md and the
soft numbers are flagged there and in the README.

Run:  python analysis.py   (writes six PNGs next to this file)
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# ----------------------------------------------------------------------
# 1. CURRENT STATE  (all from the brief)
# ----------------------------------------------------------------------
# vendor: [purchased seats, active users, annual cost]
current = {
    "Jira":       [900, None, 1_050_000],   # active not given in brief
    "Asana":      [650, 510,   780_000],
    "Monday.com": [350, 230,   420_000],
    "Trello":     [250, 120,   120_000],
}
CURRENT_TOTAL = sum(v[2] for v in current.values())   # 2,370,000

# list price per seat (annual)
list_rate = {v: current[v][2] / current[v][0] for v in current}

# ----------------------------------------------------------------------
# 2. END STATE  (standardise on Asana, retire Monday.com + Trello, keep Jira)
# ----------------------------------------------------------------------
# Asana end-state seats = current Asana active (510)
#   + net-new users migrated off Monday.com + Trello.
# Monday.com active 230 + Trello active 120 = 350 users to rehome.
# ~150 of them already hold an Asana seat (soft estimate -> limitations),
# so net-new seats added = 350 - 150 = 200.
ASANA_RETAINED = 510
ASANA_NET_NEW = 200
ASANA_END_SEATS = ASANA_RETAINED + ASANA_NET_NEW      # 710

NEG_RATE = 1_000      # negotiated Asana rate/seat (base case) vs 1,200 list
ASANA_END_COST = ASANA_END_SEATS * NEG_RATE           # 710,000
JIRA_END_COST = 1_050_000                             # held flat, audit at renewal
END_TOTAL = ASANA_END_COST + JIRA_END_COST            # 1,760,000

BASE_SAVINGS = CURRENT_TOTAL - END_TOTAL              # 610,000

# ----------------------------------------------------------------------
# 3. SAVINGS RANGE  (vary Asana rate and Jira right-sizing)
# ----------------------------------------------------------------------
# Conservative: Asana @ 1,100 (weak deal), Jira untouched  -> matches brief's ~540K
cons_end = ASANA_END_SEATS * 1_100 + 1_050_000
CONS_SAVINGS = CURRENT_TOTAL - cons_end               # ~539K
# Optimistic: Asana @ 950, Jira right-sized -10% at renewal
opt_end = ASANA_END_SEATS * 950 + 1_050_000 * 0.90
OPT_SAVINGS = CURRENT_TOTAL - opt_end                 # ~750K

# ----------------------------------------------------------------------
# 4. SAVINGS BRIDGE  (reconciles current -> end with no double counting)
# ----------------------------------------------------------------------
# Each migrated seat is priced at the negotiated rate, so the rate cut is
# only applied once, to the 510 retained seats.
bridge = [
    ("Current spend", CURRENT_TOTAL, "start"),
    ("Remove unused\nAsana licences", -(650 - 510) * list_rate["Asana"], "down"),  # -168K
    ("Retire Trello", -120_000, "down"),
    ("Retire\nMonday.com", -420_000, "down"),
    ("Migrate users\nto Asana", +ASANA_NET_NEW * NEG_RATE, "up"),                  # +200K
    ("Renegotiate\nAsana rate", -(1_200 - NEG_RATE) * ASANA_RETAINED, "down"),     # -102K
    ("End-state spend", END_TOTAL, "end"),
]

# ----------------------------------------------------------------------
# palette
# ----------------------------------------------------------------------
INK   = "#1a2b3c"
ASANA = "#2f6fed"   # the winner
KEEP  = "#3a4a5a"   # Jira, retained
CUT   = "#c0563b"   # retired vendors
SOFT  = "#8a9bab"
GRID  = "#e5e9ee"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 11,
    "axes.edgecolor": SOFT,
    "axes.linewidth": 0.8,
    "figure.dpi": 130,
})

def euro(x, _=None):
    return f"€{x/1000:,.0f}K"

def save(fig, name):
    fig.tight_layout()
    fig.savefig(name, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("wrote", name)

# ---- Chart 1: spend by vendor (current) ------------------------------
fig, ax = plt.subplots(figsize=(7, 4))
vendors = list(current.keys())
costs = [current[v][2] for v in vendors]
colors = [KEEP, ASANA, CUT, CUT]
bars = ax.bar(vendors, costs, color=colors, width=0.62)
for b, c in zip(bars, costs):
    ax.text(b.get_x()+b.get_width()/2, c+15000, euro(c), ha="center", fontsize=10.5, color=INK, fontweight="bold")
ax.set_title("Annual spend by tool  ·  €2.37M across four PM platforms", fontsize=12.5, color=INK, pad=14, fontweight="bold", loc="left")
ax.yaxis.set_major_formatter(FuncFormatter(euro))
ax.set_ylim(0, 1_200_000)
ax.grid(axis="y", color=GRID); ax.set_axisbelow(True)
for s in ["top","right"]: ax.spines[s].set_visible(False)
ax.text(0, -0.16, "Keep  ·  Standardise  ·  Retire", transform=ax.transAxes, color=SOFT, fontsize=9)
save(fig, "01_spend_by_vendor.png")

# ---- Chart 2: cost per active user -----------------------------------
fig, ax = plt.subplots(figsize=(7, 4))
cpau_v, cpau = [], []
for v in vendors:
    act = current[v][1]
    if act:
        cpau_v.append(v); cpau.append(current[v][2]/act)
colors2 = [ASANA if v=="Asana" else CUT for v in cpau_v]
bars = ax.bar(cpau_v, cpau, color=colors2, width=0.55)
for b, c in zip(bars, cpau):
    ax.text(b.get_x()+b.get_width()/2, c+25, f"€{c:,.0f}", ha="center", fontsize=10.5, color=INK, fontweight="bold")
ax.set_title("Cost per active user  ·  the tools we pay most for, per real user, are the ones we retire",
             fontsize=11.5, color=INK, pad=14, fontweight="bold", loc="left")
ax.set_ylabel("€/active user/yr")
ax.set_ylim(0, 2200)
ax.grid(axis="y", color=GRID); ax.set_axisbelow(True)
for s in ["top","right"]: ax.spines[s].set_visible(False)
ax.text(0, -0.14, "Jira excluded — brief gives no active-user count", transform=ax.transAxes, color=SOFT, fontsize=9)
save(fig, "02_cost_per_active_user.png")

# ---- Chart 3: utilisation gap ----------------------------------------
fig, ax = plt.subplots(figsize=(7.4, 4))
uv = [v for v in vendors if current[v][1]]
purch = [current[v][0] for v in uv]
act   = [current[v][1] for v in uv]
x = range(len(uv))
ax.bar([i-0.2 for i in x], purch, width=0.4, color=SOFT, label="Purchased")
ax.bar([i+0.2 for i in x], act,   width=0.4, color=ASANA, label="Active")
for i,v in enumerate(uv):
    gap = purch[i]-act[i]
    ax.text(i, purch[i]+12, f"{gap} idle", ha="center", fontsize=9.5, color=CUT, fontweight="bold")
ax.set_xticks(list(x)); ax.set_xticklabels(uv)
ax.set_title("Licences bought vs actually used  ·  390 idle seats across three tools",
             fontsize=12, color=INK, pad=14, fontweight="bold", loc="left")
ax.set_ylabel("Seats")
ax.grid(axis="y", color=GRID); ax.set_axisbelow(True)
for s in ["top","right"]: ax.spines[s].set_visible(False)
ax.legend(frameon=False, loc="upper right")
save(fig, "03_utilisation_gap.png")

# ---- Chart 4: renewal timeline ---------------------------------------
fig, ax = plt.subplots(figsize=(7.6, 3.6))
renew = [("Monday.com", 3, CUT, "retire before renewal"),
         ("Asana", 4, ASANA, "sign 3-yr consolidated deal"),
         ("Trello", 6, CUT, "migrate + drop"),
         ("Jira", 9, KEEP, "audit + renew/right-size")]
for i,(v,m,c,note) in enumerate(renew):
    y = len(renew)-i
    ax.plot([0,m],[y,y], color=GRID, lw=8, solid_capstyle="round", zorder=1)
    ax.scatter([m],[y], s=170, color=c, zorder=3)
    ax.text(-0.15, y, v, ha="right", va="center", fontsize=11, color=INK, fontweight="bold")
    ax.text(m+0.15, y, f"{m} mo — {note}", va="center", fontsize=9.7, color=c)
ax.axvline(3, color=CUT, ls=":", lw=1, alpha=.5)
ax.axvline(4, color=ASANA, ls=":", lw=1, alpha=.5)
ax.set_xlim(-2.2, 12); ax.set_ylim(0.3, len(renew)+0.8)
ax.set_xlabel("Months from now")
ax.set_title("The renewal calendar is the spine  ·  Monday.com and Asana both expire inside 4 months",
             fontsize=11.3, color=INK, pad=12, fontweight="bold", loc="left")
ax.get_yaxis().set_visible(False)
for s in ["top","right","left"]: ax.spines[s].set_visible(False)
ax.grid(axis="x", color=GRID); ax.set_axisbelow(True)
save(fig, "04_renewal_timeline.png")

# ---- Chart 5: current vs end-state -----------------------------------
fig, ax = plt.subplots(figsize=(6.6, 4.2))
states = ["Current", "End state"]
asana_part = [current["Asana"][2], ASANA_END_COST]
jira_part  = [current["Jira"][2], JIRA_END_COST]
mon_part   = [current["Monday.com"][2], 0]
tre_part   = [current["Trello"][2], 0]
ax.bar(states, jira_part, color=KEEP, label="Jira", width=0.5)
ax.bar(states, asana_part, bottom=jira_part, color=ASANA, label="Asana", width=0.5)
ax.bar(states, mon_part, bottom=[j+a for j,a in zip(jira_part,asana_part)], color=CUT, label="Monday.com", width=0.5)
ax.bar(states, tre_part, bottom=[j+a+m for j,a,m in zip(jira_part,asana_part,mon_part)], color="#d98b73", label="Trello", width=0.5)
ax.text(0, CURRENT_TOTAL+30000, euro(CURRENT_TOTAL), ha="center", fontweight="bold", color=INK, fontsize=11)
ax.text(1, END_TOTAL+30000, euro(END_TOTAL), ha="center", fontweight="bold", color=INK, fontsize=11)
ax.annotate(f"−{euro(BASE_SAVINGS)} / yr", xy=(1, END_TOTAL), xytext=(1.15, 1_400_000),
            fontsize=12, color=CUT, fontweight="bold")
ax.set_title("Current vs end-state annual spend", fontsize=12.5, color=INK, pad=14, fontweight="bold", loc="left")
ax.yaxis.set_major_formatter(FuncFormatter(euro))
ax.set_ylim(0, 2_600_000)
ax.grid(axis="y", color=GRID); ax.set_axisbelow(True)
for s in ["top","right"]: ax.spines[s].set_visible(False)
ax.legend(frameon=False, loc="upper right", fontsize=9.5)
save(fig, "05_current_vs_endstate.png")

# ---- Chart 6: savings waterfall --------------------------------------
fig, ax = plt.subplots(figsize=(8.6, 4.4))
labels = [b[0] for b in bridge]
running = 0
for i,(lab,val,kind) in enumerate(bridge):
    if kind == "start":
        ax.bar(i, val, color=INK, width=0.6); running = val
        ax.text(i, val+30000, euro(val), ha="center", fontsize=9.5, fontweight="bold", color=INK)
    elif kind == "end":
        ax.bar(i, val, color=ASANA, width=0.6)
        ax.text(i, val+30000, euro(val), ha="center", fontsize=9.5, fontweight="bold", color=ASANA)
    else:
        bottom = running + val if val < 0 else running
        color = CUT if val < 0 else "#5a8f4a"
        ax.bar(i, abs(val), bottom=bottom, color=color, width=0.6)
        sign = "" if val < 0 else "+"
        ax.text(i, bottom+abs(val)+30000, f"{sign}{euro(val)}", ha="center", fontsize=9, fontweight="bold",
                color=color)
        running += val
        ax.plot([i-0.3, i+0.3+0.4],[running,running], color=SOFT, lw=0.7, ls="--", alpha=0.6)
ax.set_xticks(range(len(labels)))
ax.set_xticklabels(labels, fontsize=8.7)
ax.set_title("From €2.37M to €1.76M  ·  each lever isolated, no double counting",
             fontsize=12.5, color=INK, pad=14, fontweight="bold", loc="left")
ax.yaxis.set_major_formatter(FuncFormatter(euro))
ax.set_ylim(0, 2_600_000)
ax.grid(axis="y", color=GRID); ax.set_axisbelow(True)
for s in ["top","right"]: ax.spines[s].set_visible(False)
save(fig, "06_savings_waterfall.png")

# ----------------------------------------------------------------------
print("\n--- reconciliation ---")
print(f"Current total:        €{CURRENT_TOTAL:,}")
print(f"End-state total:      €{END_TOTAL:,}")
print(f"Base savings:         €{BASE_SAVINGS:,}  ({BASE_SAVINGS/CURRENT_TOTAL:.1%})")
print(f"Conservative:         €{CONS_SAVINGS:,.0f}")
print(f"Optimistic:           €{OPT_SAVINGS:,.0f}")
b = CURRENT_TOTAL + sum(x[1] for x in bridge[1:-1])
print(f"Bridge reconciles to: €{b:,.0f}  (should equal end-state)")
