import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

st.set_page_config(page_title="CricCoach AI", page_icon="🏏", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Rajdhani:wght@400;500;600;700&display=swap');
html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"], .main, section.main, [data-testid="block-container"] {
    background-color: #0a0a0f !important; font-family: 'Rajdhani', sans-serif !important;
}
[data-testid="stAppViewContainer"] {
    background: radial-gradient(ellipse at 20% 0%, rgba(0,112,243,0.25) 0%, transparent 45%), radial-gradient(ellipse at 80% 0%, rgba(220,38,38,0.25) 0%, transparent 45%), linear-gradient(180deg, #0a0a0f 0%, #0d0d1a 100%) !important;
}
[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stSidebar"] { background: linear-gradient(180deg, #0d0d1a 0%, #0a0a14 100%) !important; border-right: 1px solid rgba(0,112,243,0.3) !important; }
[data-testid="stSidebar"] * { color: #e2e8f0 !important; }
[data-testid="stSidebar"] .stSelectbox label, [data-testid="stSidebar"] .stTextInput label, [data-testid="stSidebar"] .stNumberInput label {
    color: #60a5fa !important; font-weight: 600 !important; font-size: 13px !important; text-transform: uppercase !important; letter-spacing: 1px !important;
}
[data-testid="stSidebar"] input { background: rgba(0,112,243,0.08) !important; border: 1px solid rgba(0,112,243,0.3) !important; border-radius: 6px !important; color: #fff !important; }
[data-testid="stMetric"] { background: linear-gradient(135deg, rgba(0,112,243,0.15), rgba(220,38,38,0.1)) !important; border: 1px solid rgba(0,112,243,0.4) !important; border-radius: 10px !important; padding: 12px !important; }
[data-testid="stMetricLabel"] { color: #60a5fa !important; font-size: 12px !important; text-transform: uppercase; letter-spacing: 1px; }
[data-testid="stMetricValue"] { color: #fff !important; font-family: 'Bebas Neue', sans-serif !important; font-size: 2rem !important; }
.ipl-title { font-family: 'Bebas Neue', sans-serif; font-size: clamp(2.5rem, 6vw, 4.5rem); letter-spacing: 4px; background: linear-gradient(90deg, #0070f3, #60a5fa, #dc2626, #f87171); background-size: 300% 100%; -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; animation: shimmer 4s linear infinite; line-height: 1; }
@keyframes shimmer { 0% { background-position: 0% 50%; } 100% { background-position: 300% 50%; } }
.ipl-subtitle { font-family: 'Rajdhani', sans-serif; font-size: 14px; color: #60a5fa !important; letter-spacing: 3px; text-transform: uppercase; margin-top: 4px; }
.sidebar-header { font-family: 'Bebas Neue', sans-serif; font-size: 1.4rem; letter-spacing: 3px; background: linear-gradient(90deg, #0070f3, #60a5fa); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; margin-bottom: 16px; }
.live-dot { display: inline-block; width: 8px; height: 8px; background: #ef4444; border-radius: 50%; margin-right: 6px; animation: pulse 1.2s infinite; }
@keyframes pulse { 0%, 100% { opacity: 1; transform: scale(1); } 50% { opacity: 0.4; transform: scale(1.3); } }
.phase-badge { display: inline-block; padding: 4px 14px; border-radius: 20px; font-family: 'Rajdhani', sans-serif; font-weight: 700; font-size: 13px; letter-spacing: 1px; text-transform: uppercase; }
.phase-power { background: rgba(34,197,94,0.15); border: 1px solid rgba(34,197,94,0.4); color: #22c55e !important; }
.phase-middle { background: rgba(245,158,11,0.15); border: 1px solid rgba(245,158,11,0.4); color: #f59e0b !important; }
.phase-death { background: rgba(239,68,68,0.15); border: 1px solid rgba(239,68,68,0.4); color: #ef4444 !important; }
.stButton > button { background: linear-gradient(135deg, rgba(0,112,243,0.2), rgba(0,112,243,0.05)) !important; border: 1px solid rgba(0,112,243,0.5) !important; color: #60a5fa !important; font-family: 'Rajdhani', sans-serif !important; font-weight: 700 !important; font-size: 14px !important; letter-spacing: 1px !important; text-transform: uppercase !important; border-radius: 8px !important; transition: all 0.2s ease !important; }
.stButton > button:hover { background: linear-gradient(135deg, rgba(0,112,243,0.4), rgba(0,112,243,0.2)) !important; color: #fff !important; }
.stSpinner > div { border-top-color: #0070f3 !important; }
[data-testid="stExpander"] { background: rgba(0,10,30,0.6) !important; border: 1px solid rgba(0,112,243,0.2) !important; border-radius: 10px !important; }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    df = pd.read_csv("data/deliveries.csv")
    df["over"] = df["ball"].apply(lambda x: int(str(x).split(".")[0]))
    df["total_runs"] = df["runs_off_bat"] + df["extras"]
    df["is_wicket"] = df["wicket_type"].notna().astype(int)
    df["is_boundary"] = df["runs_off_bat"].apply(lambda x: 1 if x in [4, 6] else 0)
    df["is_six"] = df["runs_off_bat"].apply(lambda x: 1 if x == 6 else 0)
    df["is_dot"] = df["runs_off_bat"].apply(lambda x: 1 if x == 0 else 0)
    return df

df = load_data()

def get_phase(over):
    if over <= 5:  return "Powerplay", "phase-power"
    if over <= 14: return "Middle Overs", "phase-middle"
    return "Death Overs", "phase-death"

def phase_range(over):
    if over <= 5:  return 0, 5
    if over <= 14: return 6, 14
    return 15, 19

def bowler_stats(bowler_name, ps, pe):
    b = df[(df["bowler"] == bowler_name) & (df["over"] >= ps) & (df["over"] <= pe)]
    if len(b) < 6: return None
    balls = len(b); runs = b["total_runs"].sum()
    return {"balls": balls, "runs": int(runs), "wickets": int(b["is_wicket"].sum()),
            "economy": round((runs / balls) * 6, 2), "dot_pct": round((b["is_dot"].sum() / balls) * 100, 1),
            "boundary_pct": round((b["is_boundary"].sum() / balls) * 100, 1)}

def batter_stats(batter_name, ps, pe):
    b = df[(df["striker"] == batter_name) & (df["over"] >= ps) & (df["over"] <= pe)]
    if len(b) < 6: return None
    balls = len(b); runs = b["runs_off_bat"].sum()
    return {"balls": balls, "runs": int(runs), "strike_rate": round((runs / balls) * 100, 1),
            "boundary_pct": round((b["is_boundary"].sum() / balls) * 100, 1),
            "six_pct": round((b["is_six"].sum() / balls) * 100, 1)}

def generate_strategy(batting_team, bowling_team, current_over, current_score,
                      current_wickets, target, innings, striker, bowler):
    ps, pe = phase_range(current_over)
    phase_name, phase_cls = get_phase(current_over)
    wickets_left = 10 - current_wickets
    over_data = df[(df["over"] >= max(0, current_over-1)) & (df["over"] <= min(19, current_over+1))]
    avg_rpo = round(over_data.groupby(["match_id","innings","over"])["total_runs"].sum().mean(), 1)
    avg_wpo = round(over_data.groupby(["match_id","innings","over"])["is_wicket"].sum().mean(), 2)
    b_stats = bowler_stats(bowler, ps, pe) if bowler else None
    s_stats = batter_stats(striker, ps, pe) if striker else None

    rrr = runs_needed = balls_left = pressure = pressure_cls = None
    if innings == 2:
        balls_left  = (20 - current_over) * 6
        runs_needed = target - current_score
        rrr         = round((runs_needed * 6) / balls_left, 2) if balls_left > 0 else 99
        pressure     = "CRITICAL" if rrr > 12 else "TOUGH" if rrr > 9 else "IN CONTROL"
        pressure_cls = "danger" if rrr > 12 else "warn" if rrr > 9 else "good"

    html = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Rajdhani:wght@600;700&display=swap');
    body {{ background: #0a0a0f; margin: 0; padding: 8px; color: #e2e8f0; font-family: 'Rajdhani', sans-serif; }}
    .sc {{ background: linear-gradient(135deg,#00091f,#0a0020); border: 1px solid rgba(0,112,243,0.35); border-radius:16px; padding:28px 32px; }}
    .sh {{ font-family:'Bebas Neue',sans-serif; font-size:1.3rem; letter-spacing:2px; color:#60a5fa; margin:18px 0 8px; padding-bottom:6px; border-bottom:1px solid rgba(0,112,243,0.2); }}
    .sb {{ background:rgba(0,10,30,0.9); border:1px solid rgba(0,112,243,0.4); border-radius:12px; padding:14px 20px; margin:12px 0; display:grid; grid-template-columns:repeat(3,1fr); gap:16px; text-align:center; }}
    .sn {{ font-family:'Bebas Neue',sans-serif; font-size:3rem; color:#fff; line-height:1; }}
    .sl {{ font-size:11px; color:#60a5fa; text-transform:uppercase; letter-spacing:2px; }}
    .sp {{ display:inline-block; background:rgba(0,112,243,0.15); border:1px solid rgba(0,112,243,0.3); border-radius:20px; padding:3px 12px; font-size:13px; color:#93c5fd; margin:3px 4px 3px 0; font-weight:600; }}
    .ab {{ background:linear-gradient(135deg,rgba(0,112,243,0.2),rgba(220,38,38,0.1)); border:1px solid rgba(0,112,243,0.5); border-radius:12px; padding:16px 20px; margin:10px 0; }}
    .rb {{ background:rgba(220,38,38,0.08); border:1px solid rgba(220,38,38,0.3); border-radius:12px; padding:16px 20px; margin:10px 0; }}
    .good {{ color:#22c55e; }} .warn {{ color:#f59e0b; }} .danger {{ color:#ef4444; }}
    .pb {{ display:inline-block; padding:4px 14px; border-radius:20px; font-weight:700; font-size:13px; letter-spacing:1px; text-transform:uppercase; font-family:'Rajdhani',sans-serif; }}
    .pp {{ background:rgba(34,197,94,0.15); border:1px solid rgba(34,197,94,0.4); color:#22c55e; }}
    .pm {{ background:rgba(245,158,11,0.15); border:1px solid rgba(245,158,11,0.4); color:#f59e0b; }}
    .pd {{ background:rgba(239,68,68,0.15); border:1px solid rgba(239,68,68,0.4); color:#ef4444; }}
    .ld {{ display:inline-block; width:8px; height:8px; background:#ef4444; border-radius:50%; margin-right:6px; animation:pulse 1.2s infinite; }}
    @keyframes pulse {{ 0%,100% {{ opacity:1; }} 50% {{ opacity:0.4; }} }}
    </style>
    <div class="sc">
      <div style="display:flex;align-items:center;gap:12px;margin-bottom:16px;flex-wrap:wrap;">
        <span class="ld"></span>
        <span style="font-family:'Bebas Neue',sans-serif;font-size:1.6rem;color:#fff;letter-spacing:2px;">Strategy Report</span>
        <span class="pb {'pp' if 'Power' in phase_name else 'pm' if 'Middle' in phase_name else 'pd'}">{phase_name}</span>
        {"<span class='pb " + pressure_cls + "'>" + pressure + "</span>" if pressure else ""}
      </div>
      <div class="sh">SITUATION</div>
    """

    if innings == 2:
        rrr_color = '#ef4444' if rrr > 12 else '#f59e0b' if rrr > 9 else '#22c55e'
        html += f'<div class="sb"><div><div class="sn">{runs_needed}</div><div class="sl">Runs Needed</div></div><div><div class="sn" style="color:{rrr_color}">{rrr}</div><div class="sl">Req. Run Rate</div></div><div><div class="sn">{balls_left}</div><div class="sl">Balls Left</div></div></div>'
    else:
        html += f'<div class="sb"><div><div class="sn">{current_score}/{current_wickets}</div><div class="sl">Score</div></div><div><div class="sn">{current_over}</div><div class="sl">Overs</div></div><div><div class="sn">{wickets_left}</div><div class="sl">Wickets Left</div></div></div><p style="color:#94a3b8;font-size:13px;">Avg this phase: <b style="color:#60a5fa">{avg_rpo} runs/over</b> | <b style="color:#f87171">{avg_wpo} wkts/over</b></p>'

    html += f'<div class="sh">BOWLER — {bowler or "Not set"}</div>'
    if b_stats:
        eco_cls = "good" if b_stats["economy"] < 8 else "danger" if b_stats["economy"] > 10 else "warn"
        verdict = "Keep bowling" if b_stats["economy"] < 8 else "Consider change" if b_stats["economy"] > 10 else "Neutral"
        html += f'<span class="sp">Econ: <b class="{eco_cls}">{b_stats["economy"]}</b></span><span class="sp">Wkts: <b style="color:#f87171">{b_stats["wickets"]}</b></span><span class="sp">Dot%: <b style="color:#22c55e">{b_stats["dot_pct"]}%</b></span><span class="sp">Boundary%: <b style="color:#f59e0b">{b_stats["boundary_pct"]}%</b></span><p style="margin-top:8px">{verdict} — {b_stats["balls"]} balls in {phase_name}</p>'
    else:
        html += f'<p style="color:#94a3b8">No data for <b style="color:#fff">{bowler}</b>. Try initials e.g. <b>YS Chahal</b></p>'

    html += f'<div class="sh">STRIKER — {striker or "Not set"}</div>'
    if s_stats:
        sr_cls = "good" if s_stats["strike_rate"] > 150 else "warn" if s_stats["strike_rate"] > 110 else "danger"
        verdict = "Keep on strike" if s_stats["strike_rate"] > 150 else "Rotate if needed" if s_stats["strike_rate"] > 110 else "Look for single"
        html += f'<span class="sp">SR: <b class="{sr_cls}">{s_stats["strike_rate"]}</b></span><span class="sp">Runs: <b style="color:#60a5fa">{s_stats["runs"]}</b>/{s_stats["balls"]} balls</span><span class="sp">Boundary%: <b style="color:#f59e0b">{s_stats["boundary_pct"]}%</b></span><span class="sp">Six%: <b style="color:#a78bfa">{s_stats["six_pct"]}%</b></span><p style="margin-top:8px">{verdict} — {s_stats["balls"]} balls in {phase_name}</p>'
    else:
        html += f'<p style="color:#94a3b8">No data for <b style="color:#fff">{striker}</b>. Try initials e.g. <b>HH Pandya</b></p>'

    html += '<div class="sh">RECOMMENDED ACTION</div><div class="ab">'
    if innings == 2:
        if rrr > 12:
            html += f'<p class="danger"><b>ATTACK NOW</b> — RRR {rrr} needs 2+ boundaries every over.</p><p>Keep {striker} on strike. Target {bowler} for maximums.</p>'
        elif rrr > 9:
            html += f'<p class="warn"><b>CONTROLLED AGGRESSION</b> — RRR {rrr} is gettable. One boundary per over minimum.</p><p>Rotate strike smartly. Build to final 3 overs.</p>'
        else:
            html += f'<p class="good"><b>IN CONTROL</b> — RRR {rrr} is comfortable. Bat deep, preserve wickets.</p>'
    else:
        if current_over <= 5:
            html += '<p><b style="color:#22c55e">POWERPLAY:</b> Target 50–60 runs. Max 1 wicket. Rotate and attack bad balls only.</p>'
        elif current_over <= 14:
            html += '<p><b style="color:#f59e0b">MIDDLE OVERS:</b> Build partnerships. Keep 6+ wickets for death.</p>'
        else:
            html += '<p><b style="color:#ef4444">DEATH OVERS:</b> All out attack. Target 10+ per over.</p>'
    html += '</div>'

    html += '<div class="sh">RISK</div><div class="rb">'
    if innings == 2 and rrr and rrr > 12:
        html += f'<p style="color:#fca5a5">Going reckless risks losing {striker}. Calculated hitting only.</p>'
    elif innings == 2:
        html += '<p style="color:#fca5a5">3 consecutive dots shifts pressure massively. Never allow dot-dot-dot.</p>'
    else:
        html += f'<p style="color:#fca5a5">Historical: {avg_wpo} wickets/over in this phase. 2 quick wickets derails the innings.</p>'
    html += '</div></div>'
    return html


# ── SIDEBAR ──
with st.sidebar:
    st.markdown('<div class="sidebar-header">LIVE MATCH</div>', unsafe_allow_html=True)
    innings         = st.selectbox("Innings", [1, 2], index=1)
    batting_team    = st.text_input("Batting Team", "Mumbai Indians")
    bowling_team    = st.text_input("Bowling Team", "Rajasthan Royals")
    current_score   = st.number_input("Current Score", 0, 300, 142)
    current_wickets = st.number_input("Wickets Lost", 0, 9, 4)
    current_over    = st.number_input("Current Over (0-19)", 0, 19, 16)
    target          = st.number_input("Target", 0, 300, 185)
    striker         = st.text_input("Striker", "HH Pandya")
    bowler          = st.text_input("Current Bowler", "YS Chahal")
    if innings == 2:
        bl = (20 - current_over) * 6
        rn = target - current_score
        rrr_val = round((rn * 6) / bl, 2) if bl > 0 else 99
        c1, c2 = st.columns(2)
        c1.metric("Need", f"{rn}")
        c2.metric("RRR", f"{rrr_val}", delta="High" if rrr_val > 10 else "OK", delta_color="inverse" if rrr_val > 10 else "normal")

# ── MAIN ──
st.markdown("""
<div style="margin-bottom:8px">
  <div class="ipl-title">CRICCOACH AI</div>
  <div class="ipl-subtitle"><span class="live-dot"></span> Data-driven strategy · 243,815 IPL deliveries · 2008–2024</div>
</div>
""", unsafe_allow_html=True)

st.divider()

col1, col2, col3, col4 = st.columns(4)
analyze = False
with col1:
    if st.button("Powerplay Crisis"): analyze = True
with col2:
    if st.button("Last Over Chase"): analyze = True
with col3:
    if st.button("Death Bowling"): analyze = True
with col4:
    if st.button("Analyze Now", type="primary"): analyze = True

st.divider()

if analyze:
    with st.spinner("Scanning 243,815 deliveries..."):
        result = generate_strategy(
            batting_team, bowling_team, current_over,
            current_score, current_wickets, target,
            innings, striker, bowler
        )
    components.html(result, height=1100, scrolling=True)
    with st.expander("Raw historical data sample"):
        sample = df[
            (df["innings"] == innings) &
            (df["over"] >= max(0, current_over-1)) &
            (df["over"] <= min(19, current_over+1))
        ][["season","batting_team","bowling_team","over","striker","bowler","runs_off_bat","wicket_type"]].head(25)
        st.dataframe(sample, use_container_width=True)
else:
    st.markdown("""
    <div style="text-align:center;padding:48px 24px;">
      <div style="font-family:'Bebas Neue',sans-serif;font-size:4rem;color:rgba(255,255,255,0.04);letter-spacing:6px;">CRICCOACH</div>
      <div style="font-family:'Rajdhani',sans-serif;font-size:16px;color:#475569;margin-top:-32px;">
        Set the live match state in the sidebar · Click <b style="color:#60a5fa">Analyze Now</b>
      </div>
      <div style="display:flex;justify-content:center;gap:24px;margin-top:32px;flex-wrap:wrap;">
        <div style="background:rgba(0,112,243,0.08);border:1px solid rgba(0,112,243,0.2);border-radius:12px;padding:16px 24px;text-align:center;">
          <div style="font-family:'Bebas Neue',sans-serif;font-size:2rem;color:#60a5fa;">243K</div>
          <div style="font-size:12px;color:#64748b;text-transform:uppercase;letter-spacing:1px;">Deliveries</div>
        </div>
        <div style="background:rgba(220,38,38,0.08);border:1px solid rgba(220,38,38,0.2);border-radius:12px;padding:16px 24px;text-align:center;">
          <div style="font-family:'Bebas Neue',sans-serif;font-size:2rem;color:#f87171;">16</div>
          <div style="font-size:12px;color:#64748b;text-transform:uppercase;letter-spacing:1px;">IPL Seasons</div>
        </div>
        <div style="background:rgba(168,85,247,0.08);border:1px solid rgba(168,85,247,0.2);border-radius:12px;padding:16px 24px;text-align:center;">
          <div style="font-family:'Bebas Neue',sans-serif;font-size:2rem;color:#a78bfa;">900+</div>
          <div style="font-size:12px;color:#64748b;text-transform:uppercase;letter-spacing:1px;">Matches</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)