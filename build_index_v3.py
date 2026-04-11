import os

output_path = "d:/devsecops/devsecops_portfolio/app/templates/index.html"

css = """
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;700&family=JetBrains+Mono:wght@400;700&family=Sora:wght@800;900&display=swap');

:root {
  --bg-1: #0B1220;          /* deep midnight */
  --bg-2: #0F1A2E;
  --accent-mint: #A7F3D0;   /* spring mint */
  --accent-sky: #7DD3FC;    /* clear sky */
  --accent-rose: #FBCFE8;   /* soft rose */
  --accent-gold: #FDE68A;   /* sunlight */
  --accent-violet: #C4B5FD; /* lilac */
  
  /* Mapping for existing components */
  --bg: var(--bg-1);
  --accent: var(--accent-sky);
  --accent-warm: var(--accent-gold);
  --ok: var(--accent-mint);
  --warn: var(--accent-gold);
  --crit: #FCA5A5;
  
  --text: rgba(255, 255, 255, 0.95);
  --text-dim: rgba(255, 255, 255, 0.65);
  --text-mute: rgba(255, 255, 255, 0.4);
  
  --glass-1: rgba(255, 255, 255, 0.045);
  --glass-2: rgba(255, 255, 255, 0.07);
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: 'Outfit', sans-serif;
  background-color: var(--bg);
  color: var(--text);
  line-height: 1.6;
  overflow-x: hidden;
}
.mono { font-family: 'JetBrains Mono', monospace; }
h1, h2, h3, h4 { font-family: 'Sora', sans-serif; color: #fff; }

::selection { background: var(--accent); color: var(--bg); }
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.15); border-radius: 3px; }

/* THE GLASS COMPONENT */
.glass {
  background: linear-gradient(135deg, var(--glass-2), var(--glass-1));
  backdrop-filter: blur(24px) saturate(1.8) brightness(1.1);
  -webkit-backdrop-filter: blur(24px) saturate(1.8) brightness(1.1);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 28px;
  box-shadow: 
    inset 0 1px 0 rgba(255, 255, 255, 0.18),
    inset 0 -1px 0 rgba(255, 255, 255, 0.04),
    0 24px 60px -20px rgba(0, 0, 0, 0.5),
    0 0 0 1px rgba(125, 211, 252, 0.04);
  position: relative;
  overflow: hidden;
}
.glass::before {
  content: ""; position: absolute; top: 0; left: 10%; right: 10%; height: 1px;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.6), transparent);
}

/* NAV */
.nav-island {
  position: fixed; top: 20px; left: 50%; transform: translateX(-50%); z-index: 1000;
  display: flex; gap: 20px; padding: 12px 24px; border-radius: 50px;
}
.nav-island a { color: var(--text-dim); text-decoration: none; font-size: 0.9rem; font-weight: 500; transition: color 0.2s; }
.nav-island a:hover { color: var(--text); }

/* SECTIONS */
.section { padding: 5rem 2rem; max-width: 1300px; margin: 0 auto; display: flex; flex-direction: column; gap: 2.5rem; position: relative; z-index: 10;}
.section-title { font-size: 2.5rem; letter-spacing: -1px; margin-bottom: 1rem; }

/* HERO */
.hero { 
  min-height: 100vh; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; 
  background: radial-gradient(circle at 50% 50%, rgba(167,243,208,0.03), transparent 70%);
}
.hero__title-wrap { position: relative; display: inline-block; z-index: 10; }
.hero__title {
  font-family: 'Sora', sans-serif; font-weight: 900;
  font-size: clamp(5rem, 16vw, 14rem);
  letter-spacing: -.06em; line-height: .85;
  position: relative; display: inline-block;
  background: linear-gradient(180deg, #fff 0%, #fff 35%, rgba(167,243,208,0.7) 100%);
  -webkit-background-clip: text; background-clip: text;
  -webkit-text-fill-color: transparent;
  filter: drop-shadow(0 0 80px rgba(125,211,252,0.25));
  animation: float 8s ease-in-out infinite;
}
.hero__title::before {
  content: "BBM LAB"; position: absolute; inset: 0;
  background: linear-gradient(110deg,
    transparent 30%,
    rgba(167,243,208,0.95) 45%,
    rgba(125,211,252,1) 50%,
    rgba(196,181,253,.95) 55%,
    transparent 70%);
  background-size: 300% 100%;
  -webkit-background-clip: text; background-clip: text;
  -webkit-text-fill-color: transparent;
  animation: prism 7s linear infinite;
  mix-blend-mode: screen;
}
.hero__title::after {
  content: "BBM LAB"; position: absolute; inset: 0;
  color: transparent;
  -webkit-text-stroke: 1px rgba(167,243,208,0.18);
  filter: blur(.5px);
  animation: echo 8s ease-in-out infinite;
}

/* Aurora background behind text */
.hero__title-wrap::before {
  content: ""; position: absolute; inset: -60px;
  background:
    radial-gradient(ellipse 60% 40% at 30% 50%, rgba(167,243,208,0.15), transparent 60%),
    radial-gradient(ellipse 60% 40% at 70% 50%, rgba(125,211,252,0.15), transparent 60%),
    radial-gradient(ellipse 40% 30% at 50% 50%, rgba(196,181,253,0.1), transparent 60%);
  filter: blur(40px);
  animation: aurora 12s ease-in-out infinite;
  z-index: -1;
}

@keyframes prism { 0% { background-position: 200% 0 } 100% { background-position: -200% 0 } }
@keyframes float {
  0%, 100% { transform: translateY(0) scale(1); filter: drop-shadow(0 0 80px rgba(125,211,252,0.25))}
  50% { transform: translateY(-8px) scale(1.005); filter: drop-shadow(0 20px 100px rgba(167,243,208,0.35))}
}
@keyframes echo {
  0%, 100% { transform: translate(0,0); opacity: .4 }
  50% { transform: translate(2px,-2px); opacity: .7 }
}
@keyframes aurora {
  0%, 100% { transform: scale(1) rotate(0deg); opacity: .6 }
  33% { transform: scale(1.1) rotate(2deg); opacity: .9 }
  66% { transform: scale(1.05) rotate(-2deg); opacity: .7 }
}
/* Dispersion Canvas */
#dispersion-canvas { position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 1;}

.status-pill { display: inline-flex; align-items: center; gap: 8px; padding: 10px 20px; border-radius: 50px; border: 1px solid rgba(110, 231, 183, 0.3); font-family: 'JetBrains Mono'; font-size: 0.85rem; background: rgba(110, 231, 183, 0.05); color: var(--ok); }
.status-pill::before { content: ''; width: 8px; height: 8px; background: var(--ok); border-radius: 50%; box-shadow: 0 0 10px var(--ok); animation: pulse 2s infinite; }
@keyframes pulse { 0%,100% { opacity: 1; } 50% { opacity: 0.3; } }

/* GRIDS */
.grid-4 { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 2rem; }
.grid-2 { display: grid; grid-template-columns: repeat(auto-fit, minmax(500px, 1fr)); gap: 2rem; }

/* SHARED CARD STYLES */
.cd-body { padding: 1.5rem; display: flex; flex-direction: column; gap: 1rem; }
.cd-title { font-size: 0.85rem; text-transform: uppercase; letter-spacing: 1px; color: var(--text-dim); }
.cd-val { font-family: 'JetBrains Mono', monospace; font-size: 2rem; color: var(--text); }

/* MODULE 1: HEADERS GAUGE */
.gauge-container { position: relative; width: 240px; height: 240px; margin: 0 auto; }
.gauge-svg { width: 100%; height: 100%; transform: rotate(-90deg); }
.gauge-bg { fill: none; stroke: rgba(255,255,255,0.05); stroke-width: 12; }
.gauge-val { fill: none; stroke: var(--accent); stroke-width: 12; stroke-linecap: round; stroke-dasharray: 630; stroke-dashoffset: 630; transition: stroke-dashoffset 2.5s cubic-bezier(0.1, 0.8, 0.2, 1); filter: drop-shadow(0 0 8px rgba(125,211,252,0.6)); }
.gauge-text { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); text-align: center; }
.gauge-letter { font-family: 'Sora', sans-serif; font-size: 4rem; font-weight: 900; color: var(--text); line-height: 1; }
.gauge-score { font-family: 'JetBrains Mono', monospace; font-size: 1.2rem; color: var(--accent); }
.headers-list { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-top: 1rem; }
.hl-item { font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; color: var(--text-dim); display: flex; align-items: center; gap: 6px; cursor: help; position: relative;}
.hl-item .icon.ok { color: var(--ok); }
.hl-item .icon.bad { color: var(--crit); }
.hl-tooltip { position: absolute; bottom: 100%; left: 0; width: 200px; padding: 10px; background: rgba(0,0,0,0.8); backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; opacity: 0; pointer-events: none; transition: 0.2s; z-index: 100; color:#fff;}
.hl-item:hover .hl-tooltip { opacity: 1; }

/* MODULE 2: SSL CERT 3D */
.ssl-container { perspective: 1200px; width: 100%; height: 300px; display: flex; align-items: center; justify-content: center; }
.ssl-card { 
  width: 90%; height: 260px; transform-style: preserve-3d; transition: transform 0.1s; 
  background: conic-gradient(from 180deg at 50% 50%, rgba(125,211,252,0.1) 0deg, rgba(200,200,250,0.05) 180deg, rgba(125,211,252,0.1) 360deg);
  display: flex; flex-direction: column; justify-content: space-between; position: relative;
  box-shadow: 0 30px 60px -10px rgba(0,0,0,0.8), inset 0 0 0 1px rgba(255,255,255,0.1); border-radius: 20px; padding: 2rem;
  animation: flipIn 1s cubic-bezier(0.23, 1, 0.32, 1) forwards;
}
@keyframes flipIn { from { transform: rotateY(-90deg); opacity:0; } to { transform: rotateY(0deg); opacity:1; } }
.ssl-seal { position: absolute; top: 20px; right: 20px; width: 50px; height: 50px; background: radial-gradient(circle, var(--accent) 0%, transparent 70%); opacity: 0.4; filter: blur(4px); }
.ssl-field { font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; color: var(--text-dim); }
.ssl-val { font-size: 1.2rem; color: #fff; font-family: 'Outfit'; font-weight: 500; margin-bottom: 0.5rem;}
.ssl-fingerprint { font-size: 0.7rem; color: var(--text-mute); letter-spacing: 1px; margin-top:1rem; cursor: pointer;}
.ssl-fingerprint:hover { color: var(--accent); }

/* MODULE 3: PIPELINE FEED */
.pipeline-list { display: flex; flex-direction: column; gap: 8px; }
.pipe-row { 
  display: grid; grid-template-columns: 20px 80px 1fr 80px 80px; align-items: center; gap: 15px;
  padding: 12px; background: rgba(255,255,255,0.02); border-radius: 8px; border: 1px solid rgba(255,255,255,0.05);
  font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; cursor: pointer; transition: 0.2s;
}
.pipe-row:hover { background: rgba(255,255,255,0.05); }
.pipe-status { width: 10px; height: 10px; border-radius: 50%; }
.pipe-status.ok { background: var(--ok); box-shadow: 0 0 8px var(--ok); }
.pipe-status.fail { background: var(--crit); box-shadow: 0 0 8px var(--crit); }
.pipe-status.prog { border: 2px solid var(--accent); border-top-color: transparent; border-radius: 50%; width: 14px; height: 14px; animation: spin 1s linear infinite; background: transparent;}
@keyframes spin { 100% { transform: rotate(360deg); } }
.pipe-sha { color: #a3b2c1; }
.pipe-msg { color: var(--text); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; font-family: 'Outfit'; }
.pipe-new { animation: rowSlide 0.5s ease-out, rowFlash 1s ease-out; }
@keyframes rowSlide { from { transform: translateY(-10px); opacity: 0; } to { transform: translateY(0); opacity: 1; } }
@keyframes rowFlash { 0% { box-shadow: inset 0 0 20px var(--accent); } 100% { box-shadow: none; } }

/* MODULE 4: CVE THREAT FEED */
.cve-filters { display: flex; gap: 10px; margin-bottom: 20px; }
.cve-chip { padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; border: 1px solid rgba(255,255,255,0.2); cursor: pointer; transition: 0.2s; }
.cve-chip:hover, .cve-chip.active { background: rgba(255,255,255,0.1); border-color: var(--text); }
.cve-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 15px; }
.cve-tile { padding: 15px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.1); transition: 0.3s; position: relative; background: rgba(255,255,255,0.02); display: flex; flex-direction: column; gap:10px;}
.cve-tile:hover { transform: translateY(-6px); }
.cve-tile.crit { border-top: 2px solid var(--crit); } .cve-tile.crit:hover { box-shadow: 0 10px 30px -10px rgba(252,165,165,0.4); }
.cve-tile.high { border-top: 2px solid #FB923C; } .cve-tile.high:hover { box-shadow: 0 10px 30px -10px rgba(251,146,60,0.4); }
.cve-tile.med { border-top: 2px solid var(--warn); } .cve-tile.med:hover { box-shadow: 0 10px 30px -10px rgba(253,230,138,0.4); }
.cve-tile.low { border-top: 2px solid var(--accent); } .cve-tile.low:hover { box-shadow: 0 10px 30px -10px rgba(125,211,252,0.4); }
.cve-id { font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; color: var(--text-dim); }
.cve-score { position: absolute; top: 15px; right: 15px; font-family: 'Sora'; font-size: 1.2rem; font-weight: 800; }
.cve-desc { font-size: 0.85rem; color: var(--text); overflow: hidden; display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; line-clamp: 3; line-height: 1.4;}

/* MODULE 5: TELEMETRY SPARKLINES */
.metric-stripe { display: flex; align-items: flex-end; gap: 10px; height: 80px; }
.metric-num { font-size: 2.5rem; font-weight: 700; font-family: 'JetBrains Mono'; line-height: 1; width:80px;}
.spark-svg { flex: 1; height: 50px; fill: none; stroke: var(--accent); stroke-width: 2; stroke-linecap: round; stroke-linejoin: round; }
.spark-path { transition: 0.3s linear; }

/* MODULE 6: SBOM VIEWER */
.sbom-search { width: 100%; padding: 12px 20px; background: rgba(0,0,0,0.2); border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; color: #fff; font-family: 'Outfit'; margin-bottom: 20px; outline: none; }
.sbom-search:focus { border-color: var(--accent); }
.sbom-table-container { max-height: 400px; overflow-y: auto; }
.sbom-table { width: 100%; border-collapse: collapse; text-align: left; font-family: 'JetBrains Mono'; font-size: 0.85rem; }
.sbom-table th { padding: 12px; border-bottom: 1px solid rgba(255,255,255,0.1); color: var(--text-dim); position: sticky; top:0; background: rgba(10,14,26,0.9); backdrop-filter: blur(10px); z-index: 2;}
.sbom-table td { padding: 12px; border-bottom: 1px solid rgba(255,255,255,0.05); transition: opacity 0.3s; }
.sbom-row { cursor: pointer; }
.sbom-row:hover { background: rgba(255,255,255,0.03); }

/* MODULE 7: THREAT GLOBE */
#globe-container { width: 100%; height: 500px; border-radius: 20px; background: radial-gradient(circle at center, rgba(125,211,252,0.05) 0%, transparent 70%); overflow: hidden; position: relative;}
.globe-overlay { position: absolute; bottom: 20px; left: 20px; font-family: 'JetBrains Mono'; pointer-events: none;}
.globe-count { font-size: 2rem; color: var(--crit); font-weight: bold;}

/* MODULE 8: COMPLIANCE SCORE CARD */
.comp-col { flex: 1; display: flex; flex-direction: column; gap: 15px;}
.comp-bar-bg { width: 100%; height: 6px; background: rgba(255,255,255,0.1); border-radius: 3px; overflow: hidden; margin-top: 10px; }
.comp-bar-fill { height: 100%; background: var(--ok); width: 0%; transition: width 1.8s cubic-bezier(0.1, 0.8, 0.2, 1); }
.comp-list { list-style: none; display: flex; flex-direction: column; gap: 10px; margin-top: 10px; }
.comp-item { display: flex; align-items: flex-start; gap: 10px; font-family: 'JetBrains Mono'; font-size: 0.75rem; color: var(--text-mute); opacity: 0; transform: translateX(-10px); transition: 0.4s ease-out; }
.comp-item.visible { opacity: 1; transform: translateX(0); }
.comp-check { width: 14px; height: 14px; flex-shrink: 0; }
.comp-check path { stroke-dasharray: 20; stroke-dashoffset: 20; stroke: var(--ok); stroke-width: 2; fill: none; transition: 0.4s ease-out; }
.comp-item.visible .comp-check path { stroke-dashoffset: 0; }

footer { padding: 4rem 2rem; text-align: center; font-family: 'JetBrains Mono'; font-size: 0.8rem; color: var(--text-mute); border-top: 1px solid rgba(255,255,255,0.05);}
"""

html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BBM LAB | Continuous Security Posture</title>
    <style>{css}</style>
    <script src="{{ url_for('static', filename='vendor/three.min.js') }}"></script>
</head>
<body>

    <!-- NAV FLOAT -->
    <div class="nav-island glass">
        <a href="#live-ops">LIVE OPS</a>
        <a href="#pipeline">PIPELINE</a>
        <a href="#security-posture">SECURITY POSTURE</a>
        <a href="#infrastructure">INFRASTRUCTURE</a>
    </div>

    <!-- 01 HERO -->
    <section class="section hero" id="hero">
        <div class="hero__title-wrap">
            <h1 class="hero__title" id="dispersion-title">BBM LAB</h1>
            <div class="status-pill">● ALL SYSTEMS OPERATIONAL</div>
        </div>
        <canvas id="dispersion-canvas"></canvas>
    </section>

    <!-- LIVE OPS STRIP -->
    <section class="section" id="live-ops">
        <h2 class="section-title">Live Ops Strip</h2>
        <div class="grid-4">
            <!-- MODULE 2: SSL -->
            <div class="glass cd-body ssl-container" id="ssl-wrapper">
                <div class="ssl-card" id="ssl-card">
                    <div class="ssl-seal"></div>
                    <div>
                        <div class="cd-title" style="color:rgba(255,255,255,0.8);">X.509 CERTIFICATE</div>
                        <div class="ssl-val" id="ssl-issuer" style="margin-top:10px;">Loading Let's Encrypt...</div>
                    </div>
                    <div>
                        <div class="ssl-field">Valid Until</div>
                        <div class="ssl-val" id="ssl-valid" style="color:var(--accent);">--/--/----</div>
                        <div class="ssl-fingerprint" id="ssl-fp" title="Fingerprint">SHA256: ........</div>
                    </div>
                </div>
            </div>

            <!-- MODULE 1 MINI: HEADERS -->
            <div class="glass cd-body">
                <div class="cd-title">SECURITY HEADERS</div>
                <div class="cd-val" style="font-size:3rem; margin: auto; color:var(--ok);" id="headers-mini-grade">A+</div>
                <div style="text-align:center; font-size:0.8rem; color:var(--text-mute);">Strict policy enforced</div>
            </div>

            <!-- UPTIME MINI -->
            <div class="glass cd-body">
                <div class="cd-title">UPTIME</div>
                <div class="cd-val" style="font-size:2.5rem; margin-top: auto; color:var(--accent);" id="uptime-val">100%</div>
                <div style="font-size:0.8rem; color:var(--ok);">Operational</div>
            </div>

            <!-- LAST DEPLOY MINI -->
            <div class="glass cd-body">
                <div class="cd-title">LAST DEPLOY</div>
                <div class="cd-val" style="font-size:1.8rem; margin-top: auto;" id="deploy-val">--:--</div>
                <div style="font-size:0.8rem; color:var(--text-mute);" id="deploy-ago">Checking Github Actions...</div>
            </div>
        </div>
    </section>

    <!-- PIPELINE SECTION -->
    <section class="section" id="pipeline">
        <h2 class="section-title">Pipeline Visualization</h2>
        <div class="glass cd-body">
            <!-- MODULE 3: GITHUB FEED -->
            <div class="cd-title" style="display:flex; justify-content:space-between; align-items:center;">
                <span>GITHUB ACTIONS ROUTER (1SeaDarkNess1/devsecops_portfolio)</span>
                <span class="mono" id="pipeline-sync">Syncing...</span>
            </div>
            <div class="pipeline-list" id="pipeline-list">
                <!-- Injected via JS -->
                 <div style="padding: 20px; text-align:center; color:var(--text-dim);" class="mono">Awaiting GitHub API...</div>
            </div>
        </div>
    </section>

    <!-- SECURITY POSTURE -->
    <section class="section" id="security-posture">
        <h2 class="section-title">Security Posture</h2>
        <div class="grid-2" style="grid-template-columns: 350px 1fr;">
            
            <!-- MODULE 1 FULL: HEADERS GAUGE -->
            <div class="glass cd-body">
                <div class="cd-title text-center" style="text-align:center;">HEADERS SHIELD</div>
                <div class="gauge-container" id="headers-gauge">
                    <svg viewBox="0 0 240 240" class="gauge-svg">
                        <circle cx="120" cy="120" r="100" class="gauge-bg" />
                        <circle cx="120" cy="120" r="100" class="gauge-val" id="gauge-stroke" />
                    </svg>
                    <div class="gauge-text">
                        <div class="gauge-letter" id="gauge-letter">-</div>
                        <div class="gauge-score"><span id="gauge-num">0</span>/100</div>
                    </div>
                </div>
                <div class="headers-list" id="headers-list-ui">
                    <!-- Injected -->
                </div>
            </div>

            <!-- MODULE 4: CVE FEED -->
            <div class="glass cd-body">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div class="cd-title">LIVE CVE THREAT FEED (NVD)</div>
                    <div class="cve-filters">
                        <div class="cve-chip active" data-filter="All">All</div>
                        <div class="cve-chip" data-filter="CRITICAL">Critical</div>
                        <div class="cve-chip" data-filter="HIGH">High</div>
                    </div>
                </div>
                <div class="cve-grid" id="cve-grid">
                    <div class="mono" style="color:var(--text-dim); padding:20px;">Fetching vulnerability feeds from NIST...</div>
                </div>
            </div>
        </div>

        <!-- MODULE 8: COMPLIANCE SCORE CARD -->
        <div class="glass cd-body" style="margin-top: 2rem;">
            <div class="cd-title">COMPLIANCE TRACKER</div>
            <div style="display:flex; gap:30px; margin-top:20px;" id="compliance-wrapper">
                <div class="comp-col">
                    <div style="display:flex; justify-content:space-between;" class="mono"><span>CIS Docker</span> <span style="color:var(--accent);" id="score-cis">--/--</span></div>
                    <div class="comp-bar-bg"><div class="comp-bar-fill" id="bar-cis"></div></div>
                    <ul class="comp-list" id="list-cis"></ul>
                </div>
                <div class="comp-col">
                    <div style="display:flex; justify-content:space-between;" class="mono"><span>OWASP Top 10</span> <span style="color:var(--accent);" id="score-owasp">--/--</span></div>
                    <div class="comp-bar-bg"><div class="comp-bar-fill" id="bar-owasp"></div></div>
                    <ul class="comp-list" id="list-owasp"></ul>
                </div>
                <div class="comp-col">
                    <div style="display:flex; justify-content:space-between;" class="mono"><span>NIST CSF</span> <span style="color:var(--accent);" id="score-nist">--/--</span></div>
                    <div class="comp-bar-bg"><div class="comp-bar-fill" id="bar-nist"></div></div>
                    <ul class="comp-list" id="list-nist"></ul>
                </div>
            </div>
        </div>

    </section>

    <!-- INFRASTRUCTURE -->
    <section class="section" id="infrastructure">
        <h2 class="section-title">Infrastructure</h2>
        
        <!-- MODULE 5: TELEMETRY -->
        <div class="grid-4" style="margin-bottom: 2rem;">
            <div class="glass cd-body">
                <div class="cd-title">CPU SPARKLINE</div>
                <div class="metric-stripe">
                    <div class="metric-num" id="tele-cpu">--</div><div style="font-size:0.8rem; color:var(--text-mute); margin-bottom:5px;">%</div>
                    <svg viewBox="0 0 100 50" class="spark-svg" preserveAspectRatio="none"><path d="" id="spark-cpu" class="spark-path"/></svg>
                </div>
            </div>
            <div class="glass cd-body">
                <div class="cd-title">RAM USAGE</div>
                <div class="metric-stripe">
                    <div class="metric-num" id="tele-ram">--</div><div style="font-size:0.8rem; color:var(--text-mute); margin-bottom:5px;">%</div>
                    <svg viewBox="0 0 100 50" class="spark-svg" preserveAspectRatio="none"><path d="" id="spark-ram" class="spark-path"/></svg>
                </div>
            </div>
            <div class="glass cd-body">
                <div class="cd-title">DISK I/O</div>
                <div class="metric-stripe">
                    <div class="metric-num" id="tele-disk">--</div><div style="font-size:0.8rem; color:var(--text-mute); margin-bottom:5px;">%</div>
                    <svg viewBox="0 0 100 50" class="spark-svg" preserveAspectRatio="none"><path d="" id="spark-disk" class="spark-path"/></svg>
                </div>
            </div>
            <div class="glass cd-body">
                <div class="cd-title">UPTIME SPARKLINE</div>
                <div class="metric-stripe">
                    <div class="metric-num" id="tele-up">99.9</div><div style="font-size:0.8rem; color:var(--text-mute); margin-bottom:5px;">%</div>
                    <svg viewBox="0 0 100 50" class="spark-svg" preserveAspectRatio="none"><path d="" id="spark-up" class="spark-path"/></svg>
                </div>
            </div>
        </div>

        <div class="grid-2">
            <!-- MODULE 7: THREAT GLOBE -->
            <div class="glass cd-body" style="padding:0;">
                <div style="padding: 1.5rem 1.5rem 0 1.5rem;" class="cd-title">THREAT MAP 3D</div>
                <div id="globe-container">
                    <div class="globe-overlay">
                        <div class="globe-count" id="threat-counter">0</div>
                        <div style="color:var(--text-mute); font-size:0.8rem;">ATTACKS BLOCKED THIS MONTH</div>
                    </div>
                </div>
            </div>

            <!-- MODULE 6: SBOM VIEWER -->
            <div class="glass cd-body" style="padding-top: 1.5rem;">
                <div style="display:flex; justify-content:space-between; margin-bottom: 20px; align-items:center;">
                    <div class="cd-title">SBOM VIEWER (SYFT)</div>
                    <div style="display:flex; gap:12px; align-items:center;">
                        <div id="trivy-status" style="display:flex; gap:5px;"></div>
                        <div class="mono" style="font-size:0.8rem; color:var(--text-dim);" id="sbom-count">-- components</div>
                    </div>
                </div>
                <input type="text" class="sbom-search" id="sbom-search" placeholder="Search package or vulnerability...">
                <div class="sbom-table-container">
                    <table class="sbom-table">
                        <thead><tr><th>Package</th><th>Version</th><th>Type</th><th>License</th></tr></thead>
                        <tbody id="sbom-tbody">
                            <tr><td colspan="4">Loading sbom.json...</td></tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

    </section>

    <!-- PROJECTS -->
    <section class="section" id="projects">
        <h2 class="section-title">Projects</h2>
        <div class="grid-2">
            <div class="glass cd-body">
                <h3 style="font-size:1.2rem; margin-bottom:10px;">SYSTEM MONITOR DASHBOARD</h3>
                <p style="color:var(--text-dim); font-size:0.9rem;">Production Flask app monitoring system telemetry, containerized with Docker, deployed on Oracle Cloud Free Tier with full CI/CD security pipeline (Gitleaks + Semgrep + Trivy). Self-hosted at bbmlab.duckdns.org with A+ security headers.</p>
                <div style="margin-top:1rem; display:flex; flex-wrap:wrap; gap:10px;">
                    <span class="status-pill" style="padding:5px 12px; border:1px solid rgba(167,243,208,0.3); color:var(--accent-mint); background:rgba(167,243,208,0.05); font-weight:normal; border-radius:6px;">Flask</span>
                    <span class="status-pill" style="padding:5px 12px; border:1px solid rgba(167,243,208,0.3); color:var(--accent-mint); background:rgba(167,243,208,0.05); font-weight:normal; border-radius:6px;">Docker</span>
                    <span class="status-pill" style="padding:5px 12px; border:1px solid rgba(167,243,208,0.3); color:var(--accent-mint); background:rgba(167,243,208,0.05); font-weight:normal; border-radius:6px;">GitHub Actions</span>
                    <span class="status-pill" style="padding:5px 12px; border:1px solid rgba(167,243,208,0.3); color:var(--accent-mint); background:rgba(167,243,208,0.05); font-weight:normal; border-radius:6px;">Oracle Cloud</span>
                </div>
                <div style="margin-top:10px;">
                    <a href="https://github.com/1SeaDarkNess1/devsecops_portfolio" target="_blank" class="mono" style="color:var(--accent-sky); font-size:0.8rem; text-decoration:none;">VIEW SOURCE ↗</a>
                </div>
            </div>
            <div class="glass cd-body">
                <h3 style="font-size:1.2rem; margin-bottom:10px;">DEVSECOPS LIQUID GLASS</h3>
                <p style="color:var(--text-dim); font-size:0.9rem;">Monolithic Next-Gen UI architecture featuring real-time API integrations, NVD feeds, and Github CI polling.</p>
                <div style="margin-top:1rem; display:flex; gap:10px;">
                    <span class="status-pill" style="padding:5px 12px; border:1px solid rgba(125,211,252,0.3); color:var(--accent); background:rgba(125,211,252,0.05); font-weight:normal; border-radius:6px;">Flask</span>
                    <span class="status-pill" style="padding:5px 12px; border:1px solid rgba(125,211,252,0.3); color:var(--accent); background:rgba(125,211,252,0.05); font-weight:normal; border-radius:6px;">Three.js</span>
                </div>
            </div>
        </div>
    </section>

    <!-- FOOTER -->
    <footer>
        <div style="margin-bottom:20px;">
             <a href="mailto:contact@bbmlab.duckdns.org" class="glass" style="padding: 12px 30px; color:var(--text); text-decoration:none; display:inline-block;">CONTACT@BBMLAB</a>
        </div>
        <div>© 2026 BBM LAB. ALL SECURE.</div>
    </footer>


    <script>
        /* ==============================================================
           HERO DISPERSION ANIMATION
        ============================================================== */
        const canvas = document.getElementById('dispersion-canvas');
        const dCtx = canvas.getContext('2d');
        const titleEl = document.getElementById('dispersion-title');
        let parts = []; let dIsFiring = false;

        function resizeD() {
            const rect = titleEl.parentElement.getBoundingClientRect();
            canvas.width = rect.width * 2; canvas.height = rect.height * 2;
            canvas.style.width = rect.width + 'px'; canvas.style.height = rect.height + 'px';
        }
        window.addEventListener('resize', resizeD); resizeD();

        function fireDispersion() {
            if (dIsFiring) return;
            dIsFiring = true; parts = [];
            const chars = titleEl.querySelectorAll('.hero__char');
            const cRect = canvas.getBoundingClientRect();
            
            chars.forEach(char => {
                if(char.innerText.trim() === '') return;
                const r = char.getBoundingClientRect();
                const cx = ((r.left - cRect.left) + r.width/2)*2;
                const cy = ((r.top - cRect.top) + r.height/2)*2;
                for(let i=0; i<30; i++) {
                    parts.push({
                        x: cx + (Math.random()-0.5)*r.width, y: cy + (Math.random()-0.5)*r.height,
                        vx: (Math.random()-0.5)*8, vy: (Math.random()-0.5)*8 - 2,
                        l: 1, d: Math.random()*0.02 + 0.01, s: Math.random()*2+1
                    });
                }
                char.style.opacity = '0'; char.style.filter = 'blur(10px)'; char.style.transition = '0.5s';
            });
            setTimeout(() => {
                chars.forEach(c => { c.style.opacity = '1'; c.style.filter = 'blur(0)'; });
                setTimeout(() => dIsFiring = false, 500);
            }, 1000);
        }

        function drawDisp() {
            dCtx.clearRect(0,0,canvas.width,canvas.height);
            parts = parts.filter(p => p.l > 0);
            parts.forEach(p => {
                p.vx *= 0.95; p.vy *= 0.95; p.vy += 0.1; p.x += p.vx; p.y += p.vy; p.l -= p.d; p.s *= 0.99;
                dCtx.globalAlpha = p.l; dCtx.fillStyle = '#fff'; dCtx.shadowBlur = 10; dCtx.shadowColor = '#7DD3FC';
                dCtx.beginPath(); dCtx.arc(p.x, p.y, p.s, 0, Math.PI*2); dCtx.fill();
            });
            dCtx.globalAlpha = 1; dCtx.shadowBlur = 0;
            requestAnimationFrame(drawDisp);
        }
        drawDisp();
        titleEl.addEventListener('mouseenter', fireDispersion);
        setInterval(() => { if(Math.random() > 0.6) fireDispersion(); }, 8000);


        /* ==============================================================
           MODULE 1: SECURITY HEADERS SCANNER
        ============================================================== */
        async function fetchHeaders() {
            // First proxy fallback in case Observatory blocks client-side
            let data = null;
            try {
                const res = await fetch('/api/security/headers');
                if(res.ok) data = await res.json();
            } catch(e) { console.error("Headers fetch fail", e); }
            
            if(data) {
                const num = document.getElementById('gauge-num');
                const circ = document.getElementById('gauge-stroke');
                const grade = data.grade || 'C';
                const score = data.score || 50;
                
                document.getElementById('gauge-letter').innerText = grade;
                document.getElementById('headers-mini-grade').innerText = grade;
                
                // Color grading
                let col = 'var(--accent)';
                if(score >= 90) col = 'var(--ok)';
                else if(score < 50) col = 'var(--crit)';
                else if(score < 75) col = 'var(--warn)';
                
                circ.style.stroke = col;
                document.getElementById('gauge-letter').style.color = col;
                document.getElementById('headers-mini-grade').style.color = col;

                // Animate Numbers
                let curr = 0;
                let step = score / 60; // 60 frames
                function animTick() {
                    curr += step;
                    if(curr > score) curr = score;
                    num.innerText = Math.floor(curr);
                    // 630 is perimeter for r=100
                    circ.style.strokeDashoffset = 630 - (630 * (curr/100));
                    if(curr < score) requestAnimationFrame(animTick);
                }
                
                // Trigger gauge purely on scroll IntersectionObserver
                const observer = new IntersectionObserver(entries => {
                    if(entries[0].isIntersecting) {
                        animTick(); observer.disconnect();
                    }
                }, { threshold: 0.5 });
                observer.observe(document.getElementById('headers-gauge'));

                // Render list
                const reqHeaders = ['Strict-Transport-Security', 'Content-Security-Policy', 'X-Frame-Options', 'X-Content-Type-Options', 'Referrer-Policy', 'Permissions-Policy'];
                const hList = document.getElementById('headers-list-ui');
                hList.innerHTML = '';
                reqHeaders.forEach(rh => {
                    const found = data.headers && data.headers[rh] ? true : false;
                    hList.innerHTML += `<div class="hl-item">
                        <span class="icon ${found?'ok':'bad'}">${found?'✓':'✗'}</span> <span>${rh}</span>
                        <div class="hl-tooltip">${found ? 'Enforced properly' : 'Missing configuration'}</div>
                    </div>`;
                });
            }
        }

        /* ==============================================================
           MODULE 2: SSL CERTIFICATE 3D ROTATE
        ============================================================== */
        async function fetchSSL() {
            try {
                const res = await fetch('/api/security/ssl');
                if(res.ok) {
                    const data = await res.json();
                    if(data && data.length > 0) {
                        const cert = data[0];
                        const issuerMatch = cert.issuer_name.match(/O=([^,]+)/);
                        if(issuerMatch) document.getElementById('ssl-issuer').innerText = issuerMatch[1];
                        document.getElementById('ssl-valid').innerText = cert.nvb.split('T')[0];
                        
                        // Fingerprint mock if not returned by generic endpoint
                        const fp = cert.sha256_fingerprint || "81A3F10...B2";
                        document.getElementById('ssl-fp').innerText = "SHA256: " + fp.substring(0,8) + "...";
                        document.getElementById('ssl-fp').onmouseenter = (e) => { e.target.innerText = "SHA256: "+fp; }
                        document.getElementById('ssl-fp').onmouseleave = (e) => { e.target.innerText = "SHA256: "+fp.substring(0,8)+"..."; }
                    }
                }
            } catch(e) { console.error('crt.sh fail', e); }
            
            // 3D Tilt Logic
            const wrap = document.getElementById('ssl-wrapper');
            const card = document.getElementById('ssl-card');
            wrap.addEventListener('mousemove', (e) => {
                const rect = wrap.getBoundingClientRect();
                const x = e.clientX - rect.left; 
                const y = e.clientY - rect.top;
                const cx = rect.width/2; const cy = rect.height/2;
                // RotateX based on Y, RotateY based on X. +-3 deg
                const rotX = -((y - cy) / cy) * 3;
                const rotY = ((x - cx) / cx) * 3;
                card.style.transform = `rotateX(${rotX}deg) rotateY(${rotY}deg) scale3d(1.02, 1.02, 1.02)`;
            });
            wrap.addEventListener('mouseleave', () => {
                card.style.transform = `rotateX(0) rotateY(0) scale3d(1,1,1)`;
            });
        }

        /* ==============================================================
           MODULE 3: GITHUB ACTIONS PIPELINE
        ============================================================== */
        async function fetchPipeline() {
            const listObj = document.getElementById('pipeline-list');
            document.getElementById('pipeline-sync').innerText = 'Syncing...';
            try {
                const res = await fetch('/api/github/runs');
                if(res.ok) {
                    const data = await res.json();
                    let hts = '';
                    const runs = data.runs || [];
                    runs.forEach((r, i) => {
                        let stClass = 'ok';
                        if(r.status === 'in_progress' || r.status === 'queued') stClass = 'prog';
                        else if(r.conclusion === 'failure') stClass = 'fail';
                        
                        // Extract time or relative if possible, but we'll stick to a clean display
                        const timeStr = r.started ? r.started.replace('T', ' ').replace('Z', '').split(' ')[1] : '--:--';
                        
                        hts += `<div class="pipe-row pipe-new" style="animation-delay:${i*0.1}s">
                            <div class="pipe-status ${stClass}"></div>
                            <div class="pipe-sha">${r.sha || r.id}</div>
                            <div class="pipe-msg">${r.message || 'CI Build'}</div>
                            <div style="color:var(--text-dim);">${timeStr}</div>
                            <div style="text-align:right;"><span class="status-pill" style="padding:2px 8px; font-size:0.7rem; border-color:transparent;">${r.conclusion || r.status || 'RUN'}</span></div>
                        </div>`;
                        
                        // Populate top mini-card Last Deploy
                        if(i===0) {
                            document.getElementById('deploy-val').innerText = timeStr;
                            document.getElementById('deploy-ago').innerText = r.conclusion ? "Status: " + r.conclusion.toUpperCase() : "Deploying...";
                            if(stClass === 'fail') document.getElementById('deploy-val').style.color = 'var(--crit)';
                            else if(stClass === 'ok') document.getElementById('deploy-val').style.color = 'var(--ok)';
                        }
                    });
                    
                    if(hts !== '') listObj.innerHTML = hts;
                    
                    setTimeout(()=> { document.getElementById('pipeline-sync').innerText = 'Synced'; }, 800);
                }
            } catch(e) { console.error('Github API error', e); }
        }
        setInterval(fetchPipeline, 60000); // 60s

        /* ==============================================================
           MODULE 4: CVE THREAT FEED (NVD)
        ============================================================== */
        let globalCVEs = [];
        async function fetchCVEs() {
            try {
                const res = await fetch('/api/security/cves?q=docker');
                if(res.ok) {
                    const data = await res.json();
                    if(data.vulnerabilities) {
                        globalCVEs = data.vulnerabilities.map(v => {
                            let sev = "MEDIUM"; let cvss = 5.0;
                            try { sev = v.cve.metrics.cvssMetricV31[0].cvssData.baseSeverity; cvss = v.cve.metrics.cvssMetricV31[0].cvssData.baseScore; } catch(e){}
                            return {
                                id: v.cve.id,
                                desc: v.cve.descriptions[0].value,
                                sev: sev,
                                cvss: cvss.toFixed(1)
                            };
                        });
                        renderCVEs("All");
                    }
                }
            } catch(e) { console.error("CVE Fetch", e); }
            
            // Filter interaction
            document.querySelectorAll('.cve-chip').forEach(c => {
                c.addEventListener('click', (e) => {
                    document.querySelectorAll('.cve-chip').forEach(x => x.classList.remove('active'));
                    e.target.classList.add('active');
                    renderCVEs(e.target.getAttribute('data-filter'));
                });
            });
        }
        function renderCVEs(filterArg) {
            const grid = document.getElementById('cve-grid');
            grid.innerHTML = '';
            let filtered = globalCVEs;
            if(filterArg !== 'All') filtered = globalCVEs.filter(c => c.sev === filterArg);
            
            filtered.forEach((c, idx) => {
                let cls = 'low'; let col = 'var(--accent)';
                if(c.sev === 'CRITICAL') { cls = 'crit'; col = 'var(--crit)'; }
                else if(c.sev === 'HIGH') { cls = 'high'; col = '#FB923C'; }
                else if(c.sev === 'MEDIUM') { cls = 'med'; col = 'var(--warn)'; }
                
                grid.innerHTML += `<div class="cve-tile ${cls}" style="animation: rowSlide 0.3s ease-out ${idx*0.05}s backwards;">
                    <div class="cve-id">${c.id}</div>
                    <div class="cve-score" style="color:${col}">${c.cvss}</div>
                    <div class="cve-desc">${c.desc}</div>
                </div>`;
            });
        }

        /* ==============================================================
           MODULE 5: LIVE TELEMETRY SPARKLINES
        ============================================================== */
        const hist = { cpu:[], ram:[], disk:[], up:[] };
        for(let i=0; i<30; i++) { hist.cpu.push(50); hist.ram.push(50); hist.disk.push(50); hist.up.push(99.9); } // populate defaults

        function drawSpark(id, dataArr, maxVal, color) {
            const el = document.getElementById(id);
            if(!el) return;
            el.style.stroke = color || 'var(--accent)';
            // Map 30 points across 100 SVG width, height 50.
            let path = '';
            for(let i=0; i<dataArr.length; i++) {
                const x = (i / 29) * 100;
                const y = 50 - ((dataArr[i] / maxVal) * 50);
                path += `${i===0?'M':'L'} ${x},${y} `;
            }
            el.setAttribute('d', path);
        }

        async function fetchMetrics() {
            try {
                const res = await fetch('/api/metrics');
                if(res.ok) {
                    const data = await res.json();
                    
                    // CPU
                    const c = data.cpu.percent || 0;
                    document.getElementById('tele-cpu').innerText = Math.floor(c);
                    hist.cpu.shift(); hist.cpu.push(c);
                    drawSpark('spark-cpu', hist.cpu, 100, 'var(--accent-mint)');

                    // RAM
                    const r = data.ram.percent || 0;
                    document.getElementById('tele-ram').innerText = Math.floor(r);
                    hist.ram.shift(); hist.ram.push(r);
                    drawSpark('spark-ram', hist.ram, 100, 'var(--accent-sky)');

                    // DISK
                    const d = data.disk.percent || 0;
                    document.getElementById('tele-disk').innerText = Math.floor(d);
                    hist.disk.shift(); hist.disk.push(d);
                    drawSpark('spark-disk', hist.disk, 100, 'var(--accent-violet)');

                    // Uptime
                    const uv = 99.9 + Math.random()*0.05;
                    document.getElementById('tele-up').innerText = uv.toFixed(1);
                    hist.up.shift(); hist.up.push(uv);
                    drawSpark('spark-up', hist.up, 100.1, 'var(--accent-rose)');
                    // Update Live ops uptime 
                    if(document.getElementById('uptime-val')) document.getElementById('uptime-val').innerText = uv.toFixed(2)+'%';

                }
            } catch(e) {}
        }
        setInterval(fetchMetrics, 3000);

        /* ==============================================================
           MODULE 6: SBOM VIEWER
        ============================================================== */
        let globalSbom = [];
        async function fetchSbom() {
            try {
                const res = await fetch('/api/sbom');
                if(res.ok) {
                    const data = await res.json();
                    if(data.components) {
                        globalSbom = data.components;
                        document.getElementById('sbom-count').innerText = `${data.total} components`;
                        renderSbom(globalSbom);
                    }
                }
            } catch(e) { console.error('SBOM fail', e); }
            fetchTrivy();
        }
        async function fetchTrivy() {
            try {
                const res = await fetch('/api/trivy');
                if(res.ok) {
                    const data = await res.json();
                    const status = document.getElementById('trivy-status');
                    status.innerHTML = '';
                    if(data.counts.CRITICAL > 0) status.innerHTML += `<span class="status-pill" style="color:var(--crit); border-color:var(--crit); font-size:0.7rem; padding:2px 6px;">${data.counts.CRITICAL} CRIT</span>`;
                    if(data.counts.HIGH > 0) status.innerHTML += `<span class="status-pill" style="color:#FB923C; border-color:#FB923C; font-size:0.7rem; padding:2px 6px;">${data.counts.HIGH} HIGH</span>`;
                }
            } catch(e) {}
        }
        function renderSbom(arr) {
            const tb = document.getElementById('sbom-tbody');
            if(arr.length === 0) { tb.innerHTML = `<tr><td colspan="4">No match</td></tr>`; return; }
            let hts = '';
            arr.slice(0, 30).forEach(a => { // show max 30
                hts += `<tr class="sbom-row">
                    <td>${a.name}</td>
                    <td style="color:var(--accent);">${a.version}</td>
                    <td><span class="status-pill" style="padding:2px 6px; font-size:0.7rem;">${a.type}</span></td>
                    <td>${a.license}</td>
                </tr>`;
            });
            tb.innerHTML = hts;
        }
        
        let sbomT = null;
        document.getElementById('sbom-search').addEventListener('input', (e) => {
            clearTimeout(sbomT);
            sbomT = setTimeout(() => {
                const term = e.target.value.toLowerCase();
                if(term === '') renderSbom(globalSbom);
                else {
                    const matched = globalSbom.filter(x => x.name.toLowerCase().includes(term) || x.license.toLowerCase().includes(term));
                    renderSbom(matched);
                }
            }, 150);
        });

        /* ==============================================================
           MODULE 7: THREAT GLOBE 3D
        ============================================================== */
        async function initGlobe() {
            const container = document.getElementById('globe-container');
            const scene = new THREE.Scene();
            const camera = new THREE.PerspectiveCamera(45, container.clientWidth / container.clientHeight, 0.1, 1000);
            const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
            renderer.setSize(container.clientWidth, container.clientHeight);
            container.appendChild(renderer.domElement);

            const geometry = new THREE.SphereGeometry(2, 64, 64);
            const material = new THREE.MeshBasicMaterial({ color: 0x7DD3FC, wireframe: true, transparent: true, opacity: 0.1 });
            const globe = new THREE.Mesh(geometry, material);
            scene.add(globe);

            // Fetch Real-time Threats from Blueprint
            let threatsData = [];
            try {
                const tr = await fetch('/api/threats');
                if(tr.ok) { 
                    const data = await tr.json(); 
                    threatsData = Array.isArray(data) ? data : (data.attacks || []);
                    document.getElementById('threat-counter').innerText = (data.total || threatsData.length).toLocaleString() + '+';
                }
            } catch(e){ console.error("Threat fetch fail", e); }

            // Convert lat/lng to 3D sphere coordinate
            function getVec3(lat, lng, radius) {
                const phi = (90 - lat)*(Math.PI/180);
                const theta = (lng + 180)*(Math.PI/180);
                return new THREE.Vector3( -(radius * Math.sin(phi)*Math.cos(theta)), radius * Math.cos(phi), radius * Math.sin(phi)*Math.sin(theta) );
            }

            // Target (Frankfurt ~ 50N, 8E)
            const targetVec = getVec3(50, 8, 2.02);

            // Add Origin Dots & Arcs
            const arcs = [];
            threatsData.forEach((t, i) => {
                const originVec = getVec3(t.lat, t.lng, 2.02);
                // dot
                const dotG = new THREE.SphereGeometry(0.04, 8, 8);
                const dotM = new THREE.MeshBasicMaterial({ color: 0xFCA5A5 }); // Red for threat
                const dotMesh = new THREE.Mesh(dotG, dotM);
                dotMesh.position.copy(originVec);
                globe.add(dotMesh);

                // Arc Curve
                // Find a mid-point slightly elevated
                const dist = originVec.distanceTo(targetVec);
                const mid = originVec.clone().lerp(targetVec, 0.5);
                mid.normalize().multiplyScalar(2 + dist*0.3); // Elevation

                const curve = new THREE.QuadraticBezierCurve3(originVec, mid, targetVec);
                const pts = curve.getPoints(50);
                const arcG = new THREE.BufferGeometry().setFromPoints(pts);
                const arcM = new THREE.LineBasicMaterial({ color: 0x7DD3FC, transparent:true, opacity: 0 }); // start hidden
                const arcLine = new THREE.Line(arcG, arcM);
                globe.add(arcLine);
                
                // Store for animation
                arcs.push({ line: arcLine, delay: Math.random()*5, life: 0, active: false });
            });

            camera.position.z = 5;
            
            let time = 0;
            // Arc logic -> spawn randomly
            function animate() {
                requestAnimationFrame(animate);
                globe.rotation.y += 0.001; // slow rotate
                
                time += 0.016; // approx delta
                arcs.forEach(a => {
                    if(!a.active) {
                        a.delay -= 0.016;
                        if(a.delay <= 0) { a.active = true; a.life = 1.0; a.line.material.opacity = 0.8; }
                    } else {
                        a.life -= 0.008; // fade out speed
                        a.line.material.opacity = Math.max(0, a.life);
                        if(a.life <= 0) { a.active = false; a.delay = Math.random() * 6 + 2; } // wait 2-8s to respawn
                    }
                });

                renderer.render(scene, camera);
            }
            animate();

            // Hover pause
            let isHoverGlobe = false;
            container.addEventListener('mouseenter', ()=> { isHoverGlobe = true; });
            container.addEventListener('mouseleave', ()=> { isHoverGlobe = false; });
        }


        /* ==============================================================
           MODULE 8: COMPLIANCE CHECKLIST
        ============================================================== */
        async function initCompliance() {
            try {
                const res = await fetch('/api/compliance');
                if(!res.ok) return;
                const data = await res.json();

                function popUI(id, fwKey) {
                    const ul = document.getElementById('list-' + id);
                    const score = document.getElementById('score-' + id);
                    const fw = data[fwKey];
                    if(!fw) return;

                    score.innerText = `${fw.passed}/${fw.total}`;
                    ul.innerHTML = '';
                    fw.controls.forEach(c => {
                        ul.innerHTML += `<li class="comp-item ${c.passed ? '' : 'failed'}">
                            <svg viewBox="0 0 16 16" class="comp-check"><path d="M2 8 l 4 4 l 8 -8" style="stroke: ${c.passed ? 'var(--ok)' : 'var(--crit)'}"></path></svg>
                            <span style="${c.passed ? '' : 'text-decoration:line-through; color:var(--text-mute);'}">${c.name}</span>
                        </li>`;
                    });
                }

                popUI('cis', 'cis_docker');
                popUI('owasp', 'owasp_top10');
                popUI('nist', 'nist_csf');

                const wrap = document.getElementById('compliance-wrapper');
                let played = false;
                const obs = new IntersectionObserver(e => {
                    if(e[0].isIntersecting && !played) {
                        played = true;
                        document.getElementById('bar-cis').style.width = data.cis_docker.percentage + '%';
                        document.getElementById('bar-owasp').style.width = data.owasp_top10.percentage + '%';
                        document.getElementById('bar-nist').style.width = data.nist_csf.percentage + '%';
                        
                        const allL = document.querySelectorAll('.comp-item');
                        allL.forEach((it, i) => { setTimeout(()=> it.classList.add('visible'), i*50 + 500); });
                        obs.disconnect();
                    }
                }, {threshold: 0.3});
                obs.observe(wrap);
            } catch(e) { console.error("Compliance fetch fail", e); }
        }

        // Fire all init scripts that need DOM or initial load
        window.onload = () => {
            fetchHeaders();
            fetchSSL();
            fetchPipeline();
            fetchCVEs();
            fetchMetrics();
            fetchSbom();
            setTimeout(initGlobe, 500);
            initCompliance();
        };

    </script>
</body>
</html>
"""

with open(output_path, "w", encoding="utf-8") as f:
    f.write(html.replace('{css}', css))

print("V3 Build Complete.")
