import os
import re

file_path = "d:/devsecops/devsecops_portfolio/app/templates/index.html"
with open(file_path, "r", encoding="utf-8") as f:
    text = f.read()

# 1. Strip the old bad selectors we don't need from CSS. 
# It's safer to just APPEND the final styles with !important which will overwrite cleanly.
new_css = """
/* =========================================
   THE APPLE-GRADE LIQUID GLASS (FINAL)
   ========================================= */

.card, .waf-container, #packet-sniffer {
    background: rgba(10, 15, 25, 0.35) !important;
    backdrop-filter: blur(40px) saturate(250%) !important;
    -webkit-backdrop-filter: blur(40px) saturate(250%) !important;
    border-radius: 20px !important;
    position: relative !important;
    overflow: hidden !important; 
    padding: 1.5rem !important;
    display: flex !important;
    flex-direction: column !important;
    border: 1px solid rgba(255, 255, 255, 0.05) !important;
    border-top: 1px solid rgba(0, 229, 255, 0.3) !important; 
    box-shadow: 
        inset 0 1px 2px rgba(255, 255, 255, 0.2),
        inset 0 -1px 2px rgba(0, 0, 0, 0.5),
        0 25px 50px -15px rgba(0, 0, 0, 0.99) !important;
    color: #f8fafc !important;
}

.card::before, .waf-container::before, #packet-sniffer::before {
    content: ''; 
    position: absolute !important; 
    top: -50%; left: -50%; width: 200%; height: 200%;
    background: 
        radial-gradient(circle at 30% 70%, rgba(0, 229, 255, 0.15) 0%, transparent 40%),
        radial-gradient(circle at 70% 30%, rgba(255, 51, 102, 0.15) 0%, transparent 40%);
    filter: blur(30px) !important;
    animation: liquid-spin 20s linear infinite !important;
    z-index: 0 !important;
    pointer-events: none !important;
    mix-blend-mode: color-dodge !important;
}

@keyframes liquid-spin {
    100% { transform: rotate(360deg); }
}

.card > *, .waf-container > *, #packet-sniffer > * {
    position: relative !important;
    z-index: 10 !important;
}

#threat-log-container, #traffic-stream {
    overflow-y: auto !important;
}
#threat-log-container::-webkit-scrollbar, #traffic-stream::-webkit-scrollbar {
    width: 4px;
}
#threat-log-container::-webkit-scrollbar-thumb, #traffic-stream::-webkit-scrollbar-thumb {
    background: rgba(0, 229, 255, 0.3); border-radius: 4px;
}

#main-dashboard {
   justify-content: space-between !important; 
   padding: 2.5rem !important;
}
.left-column {
    width: 380px !important; 
    gap: 1.25rem !important; 
    mask-image: none !important; -webkit-mask-image: none !important; 
    padding-bottom: 0 !important;
    overflow: visible !important;
}
.right-column {
    width: 520px !important;
    height: calc(100vh - 5rem) !important;
    display: flex !important;
    flex-direction: column !important;
}

/* Typography Replicas */
.card-title {
    font-size: 1.1rem !important; font-weight: 500 !important; letter-spacing: 1px !important;
    text-transform: uppercase; color: #fff !important;
    text-shadow: 0 0 10px rgba(255,255,255,0.4) !important; margin-bottom: 5px;
}
.mockup-sub {
    font-size: 0.70rem; color: #a0aec0; line-height: 1.6; font-family: 'Inter', sans-serif;
    text-shadow: none;
}

/* Rings Layout */
.rings-wrapper { display: flex; justify-content: space-between; align-items: center; margin-top: 15px; }
.ring-container { position: relative; width: 65px; height: 90px; display: flex; flex-direction: column; align-items: center; }
.circ-svg { width: 65px; height: 65px; transform: rotate(-90deg); overflow: visible; }
.circ-bg { fill: none; stroke: rgba(255, 255, 255, 0.08); stroke-width: 6; }
.circ-fill { fill: none; stroke-width: 6; stroke-linecap: round; transition: stroke-dasharray 0.5s ease; }
.circ-fill.cyan { stroke: #00e5ff; filter: drop-shadow(0 0 6px rgba(0,229,255,0.8)); }
.circ-fill.pink { stroke: #ff3366; filter: drop-shadow(0 0 6px rgba(255,51,102,0.8)); }
.ring-text { position: absolute; top: 25px; font-size: 0.75rem; font-family: var(--font-mono); font-weight: bold; width: 100%; text-align: center; color: #fff; }
.ring-label { font-size: 0.5rem; color: #a0aec0; text-transform: uppercase; margin-top: 5px; text-align: center; font-weight: bold;}

/* Center Glass Panel */
.center-area {
    position: absolute;
    top: 55%; left: 50%;
    transform: translate(-50%, -50%);
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1.5rem;
    pointer-events: none; /* Let clicks pass to canvas if needed */
    z-index: 50;
}
.glass-hologram {
    background: rgba(20, 25, 35, 0.45);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-top: 1px solid rgba(0, 229, 255, 0.3);
    border-radius: 12px;
    padding: 3rem 4.5rem;
    text-align: center;
    font-size: 1.8rem;
    font-weight: 500;
    color: #fff;
    letter-spacing: 3px;
    line-height: 1.6;
    box-shadow: 0 40px 80px rgba(0,0,0,0.8), inset 0 0 20px rgba(0,229,255,0.05);
    text-shadow: 0 0 15px rgba(0, 229, 255, 0.8);
    pointer-events: auto;
}
.mac-dock {
    display: flex; gap: 18px;
    background: rgba(10, 15, 25, 0.5);
    backdrop-filter: blur(15px);
    padding: 12px 24px;
    border-radius: 30px;
    border: 1px solid rgba(255,255,255,0.08);
    pointer-events: auto;
}
.dock-dot { width: 16px; height: 16px; border-radius: 50%; box-shadow: 0 0 10px rgba(0,0,0,0.5); }
.dock-pills { display: flex; gap: 15px; pointer-events: auto; }
.mac-pill {
    width: 45px; height: 45px; border-radius: 50%;
    background: rgba(20, 25, 30, 0.6);
    border: 1px solid rgba(255,255,255,0.1);
    display: flex; justify-content: center; align-items: center;
    color: #a0aec0; font-size: 1.2rem;
    cursor: pointer;
    box-shadow: 0 5px 15px rgba(0,0,0,0.3);
}
.mac-pill.blue { background: rgba(0, 50, 150, 0.4); border-color: #00e5ff; color: #00e5ff; }

/* Right Column Table Grid */
.net-grid-header {
    display: flex; gap: 15px;
    font-size: 0.65rem; color: #a0aec0; letter-spacing: 1px;
    border-bottom: 1px solid rgba(255,255,255,0.1);
    padding-bottom: 10px; margin-bottom: 12px; margin-top: 15px;
}
.net-grid-row {
    display: flex; gap: 15px;
    font-size: 0.75rem; color: #00e5ff; font-family: var(--font-mono);
    margin-bottom: 6px; align-items: center;
    animation: cyber-log-entry 0.35s cubic-bezier(0.1, 0.8, 0.2, 1) forwards;
}
.net-method { width: 12%; font-weight: bold; }
.net-path { flex: 1; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; color: #e2e8f0; }
.net-ip { width: 25%; color: #94a3b8; }
.net-status { width: 10%; text-align: right; }
"""

text = text.replace("</style>", new_css + "\n    </style>")

# 2. Rebuild the left-column
new_left = """
        <div class="left-column">
            
            <!-- Target element for magnetic effect (injectat dinamic) -->
            <div class="card">
                <div class="card-title">BBMLAB Sec Ops</div>
                <div class="mockup-sub">
                    Security: BBMLAB<br>
                    Operation 25.00.0.610T<br>
                    Powerered 21 hoss
                </div>
            </div>

            <div class="card">
                <div style="display: flex; justify-content: space-between;">
                    <div class="card-title">CPU/WAF</div>
                    <div class="card-title" style="color: #a0aec0 !important; text-shadow: none !important;">WAF</div>
                </div>
                <div class="rings-wrapper">
                    <!-- Ring 1 (CPU mapped to Cyanfal) -->
                    <div class="ring-container">
                        <svg viewBox="0 0 100 100" class="circ-svg"><path class="circ-bg" d="M50 5 a 45 45 0 0 1 0 90 a 45 45 0 0 1 0 -90"/><path class="circ-fill cyan" id="svg-cyanfal" stroke-dasharray="0, 300" d="M50 5 a 45 45 0 0 1 0 90 a 45 45 0 0 1 0 -90"/></svg>
                        <div class="ring-text" id="cpu-percent">53%</div>
                        <div class="ring-label">Cyanfal</div>
                    </div>
                    <!-- Ring 2 (CPPO) -->
                    <div class="ring-container">
                        <svg viewBox="0 0 100 100" class="circ-svg"><path class="circ-bg" d="M50 5 a 45 45 0 0 1 0 90 a 45 45 0 0 1 0 -90"/><path class="circ-fill pink" id="svg-cppo" stroke-dasharray="0, 300" d="M50 5 a 45 45 0 0 1 0 90 a 45 45 0 0 1 0 -90"/></svg>
                        <div class="ring-text" id="ram-percent">3%</div>
                        <div class="ring-label">CPPO</div>
                    </div>
                    <!-- Ring 3 (Data/soote) -->
                    <div class="ring-container">
                        <svg viewBox="0 0 100 100" class="circ-svg"><path class="circ-bg" d="M50 5 a 45 45 0 0 1 0 90 a 45 45 0 0 1 0 -90"/><path class="circ-fill cyan" id="svg-datasoote" stroke-dasharray="0, 300" d="M50 5 a 45 45 0 0 1 0 90 a 45 45 0 0 1 0 -90"/></svg>
                        <div class="ring-text" id="disk-percent">43%</div>
                        <div class="ring-label">Data/soote</div>
                    </div>
                    <!-- Ring 4 (ANNG) -->
                    <div class="ring-container">
                        <svg viewBox="0 0 100 100" class="circ-svg"><path class="circ-bg" d="M50 5 a 45 45 0 0 1 0 90 a 45 45 0 0 1 0 -90"/><path class="circ-fill cyan" id="svg-anng" stroke-dasharray="0, 300" d="M50 5 a 45 45 0 0 1 0 90 a 45 45 0 0 1 0 -90"/></svg>
                        <div class="ring-text" id="net-sent">45%</div>
                        <div class="ring-label">ANNG</div>
                    </div>
                </div>
            </div>

            <div class="card">
                <div class="card-title">LIVE THREAT INTELLIGENCE</div>
                <div id="threat-log-container" style="max-height: 160px; font-family: var(--font-mono); font-size: 0.65rem; color: #a0aec0;"></div>
                <!-- Aceste field-uri ascunse sunt ca sa nu crape JS-ul existent de metrics updater -->
                <div style="display:none;"><span id="count-blocked">0</span><span id="count-warnings">0</span><span id="count-banned">0</span></div>
            </div>

            <div class="card" id="card-chaos">
                <div class="card-title">CHAOS ENGINEERING</div>
                <div class="mockup-sub" style="margin-bottom: 20px; text-transform: uppercase;">
                    THE CHAOS ENGINEERING AMITAS TO EMRTIATE VERIATE THE FAILURE AND TUIR NODE FAILURE.
                </div>
                <!-- Span invizibil pt status status -->
                <span id="chaos-status" style="display:none;"></span>
                <button id="btn-chaos" style="width: auto; padding: 0.7rem 1.2rem !important; font-size: 0.75rem; border: 1px solid rgba(0, 229, 255, 0.4) !important; background: rgba(0,229,255,0.1) !important; color: #00e5ff !important; margin: 0; align-self: flex-start; text-shadow:none;">INITIATE NODE FAILURE</button>
            </div>

        </div>

        <!-- CENTER HOLOGRAPHIC AREA -->
        <div class="center-area" id="center-hologram" style="opacity:0;">
            <div class="glass-hologram">
                BBM LAB<br>
                // SYSTEM ONLINE //<br>
                SEC OPS CENTER...
            </div>
            <div class="mac-dock">
                <div class="dock-dot" style="background:#ff3b30"></div>
                <div class="dock-dot" style="background:#ffcc00"></div>
                <div class="dock-dot" style="background:#28cd41"></div>
                <div class="dock-dot" style="background:#00e5ff"></div>
                <div class="dock-dot" style="background:#ffffff"></div>
            </div>
            <div class="dock-pills">
                <div class="mac-pill">⠿</div>
                <div class="mac-pill blue">∿</div>
                <div class="mac-pill">T</div>
            </div>
        </div>
"""

# Extract the left-column using string match (from <div class="left-column"> to <div class="right-column">)
left_col_start = text.find('<div class="left-column">')
right_col_start = text.find('<div class="right-column">')

if left_col_start != -1 and right_col_start != -1:
    text = text[:left_col_start] + new_left + text[right_col_start:]


# 3. Rebuild the right-column
new_right = """<div class="right-column">
            <div id="packet-sniffer" style="height: 100% !important;">
                <div class="card-title" style="margin-bottom: 0;">NETWORK PACKET STREAM</div>
                <div class="net-grid-header">
                    <div class="net-method">METHOD</div>
                    <div class="net-path">PATH</div>
                    <div class="net-ip">IP</div>
                    <div class="net-status">STATUS</div>
                </div>
                <div id="traffic-stream" style="justify-content: flex-start; mask-image: none; -webkit-mask-image: none; height: 100% !important;"></div>
            </div>
        </div>"""

# Replace right-column
text = re.sub(r'<div class="right-column">.*?</div>\s+</div>\s+<script>', new_right + '\n    </div>\n\n    <script>', text, flags=re.DOTALL)


# 4. Modify JavaScript traffic insertion logic
js_old = """const pre = document.createElement('div');
                pre.className = 'network-log-row';
                
                const methodSpan = document.createElement('span');
                methodSpan.style.color = getMethodColor(log.method);
                methodSpan.style.fontWeight = 'bold';
                methodSpan.textContent = `[${log.method}]`;

                const pathSpan = document.createElement('span');
                pathSpan.style.color = '#fff';
                pathSpan.style.marginLeft = '8px';
                pathSpan.textContent = log.path;

                const statusSpan = document.createElement('span');
                statusSpan.style.color = log.status_code >= 400 ? 'var(--crimson)' : 'var(--neon-green)';
                statusSpan.style.marginLeft = 'auto';
                statusSpan.style.fontWeight = 'bold';
                statusSpan.textContent = log.status_code;

                const ipSpan = document.createElement('span');
                ipSpan.style.color = 'var(--text-secondary)';
                ipSpan.style.marginLeft = '12px';
                ipSpan.style.fontSize = '0.7em';
                ipSpan.textContent = log.ip;

                pre.appendChild(methodSpan);
                pre.appendChild(pathSpan);
                pre.appendChild(ipSpan);
                pre.appendChild(statusSpan);

                stream.appendChild(pre);"""

js_new = """const pre = document.createElement('div');
                pre.className = 'net-grid-row';
                
                const methodSpan = document.createElement('div');
                methodSpan.className = 'net-method';
                methodSpan.textContent = log.method;

                const pathSpan = document.createElement('div');
                pathSpan.className = 'net-path';
                pathSpan.textContent = log.path;

                const ipSpan = document.createElement('div');
                ipSpan.className = 'net-ip';
                ipSpan.textContent = log.ip;

                const statusSpan = document.createElement('div');
                statusSpan.className = 'net-status';
                statusSpan.style.color = log.status_code >= 400 ? 'var(--crimson)' : '#00e5ff';
                statusSpan.textContent = log.status_code >= 400 ? 'ERR' : 'OK';

                pre.appendChild(methodSpan);
                pre.appendChild(pathSpan);
                pre.appendChild(ipSpan);
                pre.appendChild(statusSpan);

                stream.appendChild(pre);"""

text = text.replace(js_old, js_new)


# 5. Modify JS metrics to update SVG rings (stroke-dasharray logic instead of width logic)
js_metrics_old = """document.getElementById('cpu-percent').textContent = data.cpu_percent + '%';
                document.getElementById('cpu-bar').style.width = data.cpu_percent + '%';

                document.getElementById('ram-percent').textContent = data.ram_percent + '%';
                const ramBarClass = data.ram_percent > 80 ? 'warn' : 'ok';
                document.getElementById('ram-bar').className = `progress-fill ${ramBarClass}`;
                document.getElementById('ram-bar').style.width = data.ram_percent + '%';
                document.getElementById('ram-detail').textContent = `${data.ram_gb_used} / ${data.ram_gb_total} GB`;

                document.getElementById('disk-percent').textContent = data.disk_percent + '%';
                const diskBarClass = data.disk_percent > 85 ? 'warn' : 'ok';
                document.getElementById('disk-bar').className = `progress-fill ${diskBarClass}`;
                document.getElementById('disk-bar').style.width = data.disk_percent + '%';
                document.getElementById('disk-detail').textContent = `${data.disk_gb_used} / ${data.disk_gb_total} GB`;

                document.getElementById('net-sent').textContent = data.net_sent_mb + ' MB';
                document.getElementById('net-recv').textContent = data.net_recv_mb + ' MB';
                document.getElementById('uptime').textContent = data.uptime;
                document.getElementById('os').textContent = data.os;"""

js_metrics_new = """// Convert percentage to stroke-dasharray out of 283 (circumference)
                 let pCpu = Math.floor((data.cpu_percent / 100) * 282);
                 let pRam = Math.floor((data.ram_percent / 100) * 282);
                 let pDisk = Math.floor((data.disk_percent / 100) * 282);
                 // Mock a 4th metric based on uptime / arbitrary value just to animate "ANNG"
                 let pAnng = Math.floor((data.cpu_percent * 1.5 + 20) % 100 / 100 * 282);

                 document.getElementById('cpu-percent').textContent = data.cpu_percent + '%';
                 if(document.getElementById('svg-cyanfal')) document.getElementById('svg-cyanfal').style.strokeDasharray = `${pCpu}, 300`;

                 document.getElementById('ram-percent').textContent = data.ram_percent + '%';
                 if(document.getElementById('svg-cppo')) document.getElementById('svg-cppo').style.strokeDasharray = `${pRam}, 300`;

                 document.getElementById('disk-percent').textContent = data.disk_percent + '%';
                 if(document.getElementById('svg-datasoote')) document.getElementById('svg-datasoote').style.strokeDasharray = `${pDisk}, 300`;

                 document.getElementById('net-sent').textContent = ((data.cpu_percent * 1.5 + 20) % 100).toFixed(0) + '%';
                 if(document.getElementById('svg-anng')) document.getElementById('svg-anng').style.strokeDasharray = `${pAnng}, 300`;"""

text = text.replace(js_metrics_old, js_metrics_new)


# Remove boot-text block from HTML
text = re.sub(r'<div>\s*<h1 id="boot-text">BBM LAB // SYSTEM OFFLINE. Scroll to initiate uplink.</h1>\s*</div>', '', text)


# Ensure the GSAP animation turns on Center Hologram
# Search for: .to(".right-column", { x: 0, autoAlpha: 1, duration: 1 }, "<");
gsap_old = '.to(".right-column", { x: 0, autoAlpha: 1, duration: 1 }, "<");'
gsap_new = gsap_old + '\n              .to("#center-hologram", { autoAlpha: 1, duration: 1 }, "<");'
text = text.replace(gsap_old, gsap_new)


with open(file_path, "w", encoding="utf-8") as f:
    f.write(text)
    
print("Replaced content correctly!")
