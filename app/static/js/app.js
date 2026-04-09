/**
 * Modular Plasma Glass Dashboard Logic
 */

const initDashboard = () => {
    console.log("⚡ Plasma Glass Dashboard Initialized");
    
    // Start sub-modules
    initMetricsPolling();
    initTrafficSimulation();
    initWafAnalyzer();
    initChaosEngine();
};

/**
 * METRICS POLLING
 * Fetches real hardware stats from Flask
 */
const updateMetrics = async () => {
    try {
        const res = await fetch('/api/metrics');
        if (!res.ok) throw new Error('API Error');
        const data = await res.json();
        
        // Update DOM
        const cpuEl = document.getElementById('cpu-val');
        const ramEl = document.getElementById('ram-val');
        const diskEl = document.getElementById('disk-val');
        
        if (cpuEl) cpuEl.textContent = `${data.cpu.percent}%`;
        if (ramEl) ramEl.textContent = `${data.ram.percent}%`;
        if (diskEl) diskEl.textContent = `${data.disk.percent}%`;
        
        // Handle Chaos mode colorization
        const cpuCard = document.getElementById('card-cpu');
        if (cpuCard) {
            const badge = cpuCard.querySelector('.status-badge');
            if (data.cpu.status === 'CRITICAL') {
                badge.textContent = 'CRITICAL';
                badge.className = 'status-badge critical';
            } else {
                badge.textContent = 'NORMAL';
                badge.className = 'status-badge ok';
            }
        }
    } catch (e) {
        console.warn("Failed to update metrics:", e);
    }
};

const initMetricsPolling = () => {
    updateMetrics(); // initial load
    setInterval(updateMetrics, 3000);
};

/**
 * TRAFFIC SIMULATION
 * Generates dummy network traffic & injects it into the Grid
 */
const simulateTraffic = () => {
    const streamContainer = document.getElementById('network-stream');
    if (!streamContainer) return;
    
    const endpoints = ['/api/user/auth', '/wp-admin', '/dashboard/stats', '/config.env', '/health', '/api/payments'];
    const ips = ['192.168.1.105', '10.0.0.42', '172.16.5.99', '45.33.220.1', '104.128.5.5', '159.89.2.222'];
    
    // Generate a single packet
    const generatePacket = () => {
        const path = endpoints[Math.floor(Math.random() * endpoints.length)];
        const ip = ips[Math.floor(Math.random() * ips.length)];
        const latency = Math.floor(Math.random() * 80) + 5;
        
        // Determine status based on path
        let method = 'GET';
        let methodClass = 'get';
        
        if (path === '/wp-admin' || path === '/config.env') {
            method = 'DROP';
            methodClass = 'drop';
        } else if (path.includes('/auth') || path.includes('/payments')) {
            method = 'POST';
            methodClass = 'post';
        }
        
        injectLog(method, methodClass, path, ip, latency);
        
        // Fire next packet at random interval for realism (300ms - 1500ms)
        const nextDelay = Math.random() * 1200 + 300;
        setTimeout(generatePacket, nextDelay);
    };
    
    const injectLog = (method, methodClass, path, ip, lat) => {
        const row = document.createElement('div');
        row.className = 'log-row';
        
        // Note: Matches CSS grid-template-columns: 80px 1fr 140px 80px;
        row.innerHTML = `
            <span class="log-method ${methodClass}">${method}</span>
            <span class="log-path">${path}</span>
            <span class="log-ip">${ip}</span>
            <span class="log-lat">${lat}ms</span>
        `;
        
        streamContainer.appendChild(row);
        
        // Limit to 50 rows in DOM to prevent lag
        if (streamContainer.children.length > 50) {
            streamContainer.removeChild(streamContainer.firstChild);
        }
        
        // Auto-scroll to bottom elegantly
        streamContainer.scrollTop = streamContainer.scrollHeight;
    };
    
    // Start simulation
    generatePacket();
};

const initTrafficSimulation = () => {
    simulateTraffic();
};

/**
 * WAF ANALYZER
 * Sandbox logic
 */
const triggerWafAlert = async () => {
    const input = document.getElementById('waf-input');
    const result = document.getElementById('waf-result');
    if (!input || !result) return;
    
    const payload = input.value.trim();
    if (!payload) return;
    
    // Disable temporarily
    input.disabled = true;
    result.textContent = "[ ANALYZING PAYLOAD... ]";
    result.style.color = "var(--text-muted)";
    
    try {
        const res = await fetch('/api/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ payload })
        });
        const data = await res.json();
        
        if (data.level === 'CRITICAL') {
            result.textContent = `[ BLOCKED ] ${data.type}`;
            result.style.color = "var(--neon-red)";
        } else {
            result.textContent = `[ OK ] Request is clean.`;
            result.style.color = "var(--neon-green)";
        }
    } catch {
        result.textContent = "[ ERROR ] Connection failed.";
        result.style.color = "var(--neon-amber)";
    } finally {
        input.disabled = false;
        input.value = ''; // clear
        input.focus();
    }
};

const initWafAnalyzer = () => {
    const btn = document.getElementById('waf-btn');
    const input = document.getElementById('waf-input');
    
    if (btn) {
        btn.addEventListener('click', triggerWafAlert);
    }
    
    if (input) {
        input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') triggerWafAlert();
        });
    }
};

/**
 * CHAOS ENGINEERING
 */
const initChaosEngine = () => {
    const btn = document.getElementById('chaos-btn');
    if (!btn) return;
    
    btn.addEventListener('click', async () => {
        btn.disabled = true;
        btn.textContent = "INJECTING CHAOS...";
        try {
            await fetch('/api/chaos', { method: 'POST' });
        } catch (e) {
            console.error(e);
        }
        setTimeout(() => {
            btn.textContent = "INITIATE NODE FAILURE";
            btn.disabled = false;
        }, 8000);
    });
};

// Start system when DOM is ready
document.addEventListener('DOMContentLoaded', initDashboard);
