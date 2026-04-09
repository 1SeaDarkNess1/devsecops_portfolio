/**
 * TacIntel Summer SaaS Edition - Application Logic
 * BBM Particle Engine & Bento Dashboard Interactivity
 */

class TacIntelSystem {
    constructor() {
        this.initParticleEngine();
        this.initMetrics();
        this.initThreatLiveFeed();
        this.initChaosEngine();
        this.initAITerminal();
    }

    /* ═══════════════════════════════════════════════
       THE BBM PARTICLE ENGINE (LIGHT THEME)
    ═══════════════════════════════════════════════ */
    initParticleEngine() {
        const canvas = document.getElementById('bbm-canvas');
        if (!canvas) return;
        
        const ctx = canvas.getContext('2d', { willReadFrequently: true });
        let w, h;
        let particles = [];
        
        // Mouse Repulsion State
        const mouse = { x: null, y: null, radius: 100 };

        canvas.addEventListener('mousemove', (e) => {
            const rect = canvas.getBoundingClientRect();
            mouse.x = e.clientX - rect.left;
            mouse.y = e.clientY - rect.top;
        });
        
        canvas.addEventListener('mouseleave', () => {
            mouse.x = null;
            mouse.y = null;
        });

        // ---------------- Particle Class ----------------
        class Particle {
            constructor(x, y) {
                this.x = Math.random() * w; 
                this.y = Math.random() * h;
                this.baseX = x; 
                this.baseY = y;
                this.size = 2.5; 
                this.density = (Math.random() * 20) + 1; 
                
                this.vx = 0;
                this.vy = 0;
                
                // Light Theme Physics Config
                this.friction = 0.85; 
                this.ease = 0.05; 
                
                // Summer SaaS Theme Colors
                const colors = ['#1e293b', '#0f172a', '#65a30d', '#84cc16', '#0ea5e9'];
                this.color = colors[Math.floor(Math.random() * colors.length)];
            }

            draw() {
                ctx.fillStyle = this.color;
                ctx.beginPath();
                ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
                ctx.closePath();
                ctx.fill();
            }

            update() {
                // 1. Mouse Repulsion Force
                if (mouse.x != null && mouse.y != null) {
                    const dx = mouse.x - this.x;
                    const dy = mouse.y - this.y;
                    const distance = Math.sqrt(dx * dx + dy * dy);
                    
                    if (distance < mouse.radius) {
                        const forceDirectionX = dx / distance;
                        const forceDirectionY = dy / distance;
                        // Max distance check
                        const force = (mouse.radius - distance) / mouse.radius; 
                        const directionX = forceDirectionX * force * this.density;
                        const directionY = forceDirectionY * force * this.density;
                        
                        this.vx -= directionX;
                        this.vy -= directionY;
                    }
                }

                // 2. Spring Force (Pull back to base with ease)
                const dxBase = this.baseX - this.x;
                const dyBase = this.baseY - this.y;
                this.vx += dxBase * this.ease;
                this.vy += dyBase * this.ease;

                // 3. Apply Friction
                this.vx *= this.friction;
                this.vy *= this.friction;

                // 4. Move
                this.x += this.vx;
                this.y += this.vy;
            }
        }

        // ---------------- Scanner ----------------
        const initTextMap = () => {
            particles = [];
            w = canvas.parentElement.clientWidth;
            h = canvas.parentElement.clientHeight;
            canvas.width = w;
            canvas.height = h;

            // Draw solid text
            ctx.fillStyle = "black"; // Must be dark to read alpha correctly
            const fontSize = Math.min(w / 3.5, 120); // 120px default as requested
            ctx.font = `900 ${fontSize}px 'Inter', sans-serif`;
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            
            ctx.fillText("BBM", w / 2, h / 2);

            // Scan pixels
            const textCoordinates = ctx.getImageData(0, 0, w, h);
            ctx.clearRect(0, 0, w, h); // Clear the solid text

            const step = 4; // Higher density for crisp looks

            for (let y = 0; y < h; y += step) {
                for (let x = 0; x < w; x += step) {
                    const index = (y * w + x) * 4 + 3;
                    if (textCoordinates.data[index] > 128) {
                        particles.push(new Particle(x, y));
                    }
                }
            }
        };

        const animate = () => {
            ctx.clearRect(0, 0, w, h);
            for (let i=0; i<particles.length; i++) {
                particles[i].update();
                particles[i].draw();
            }
            requestAnimationFrame(animate);
        };

        initTextMap();
        animate();

        window.addEventListener('resize', () => {
            clearTimeout(canvas.resizeTimer);
            canvas.resizeTimer = setTimeout(initTextMap, 200);
        });
    }

    /* ═══════════════════════════════════════════════
       INTERACTIVITY LOGIC
    ═══════════════════════════════════════════════ */
    
    // 1. Metrics Auto-Update
    initMetrics() {
        this.cpuEl = document.getElementById('cpu-val');
        this.ramEl = document.getElementById('ram-val');
        this.isChaos = false;

        const simulateMetrics = () => {
            if(this.isChaos) return; // Freeze if chaos is running
            
            const cpu = Math.floor(Math.random() * (28 - 12 + 1)) + 12; // 12% to 28%
            const ram = Math.floor(Math.random() * (55 - 40 + 1)) + 40; // 40% to 55%
            
            this.updateMetricsUI(cpu, ram);
        };
        
        setInterval(simulateMetrics, 2000);
        simulateMetrics(); // run once immediately
    }

    updateMetricsUI(cpu, ram) {
        this.cpuEl.textContent = `${cpu}%`;
        this.ramEl.textContent = `${ram}%`;
        
        if (cpu >= 80) {
            this.cpuEl.classList.add('danger');
        } else {
            this.cpuEl.classList.remove('danger');
        }
    }

    // 2. Threat Intel Live Feed
    initThreatLiveFeed() {
        this.logList = document.getElementById('log-list');
        const internalLogs = [
            "[WAF] Blocked SQLi from 192.168.1.12",
            "[CI/CD] Container image scanned: Clean",
            "[SYSTEM] Auto-scaling node cluster",
            "[PROXY] Traffic normalized at Edge",
            "[AUTH] 5 failed logins suppressed"
        ];
        
        setInterval(() => {
            const randomLog = internalLogs[Math.floor(Math.random() * internalLogs.length)];
            this.injectLog(randomLog, 'system');
        }, 4000);
    }

    injectLog(text, type = 'system') {
        const li = document.createElement('li');
        
        // Match regex to extract tag e.g. [WAF]
        const match = text.match(/^(\[[A-Z\/_]+\])\s(.*)/);
        
        if(match) {
            li.innerHTML = `<span class="log-tag">${match[1]}</span> ${match[2]}`;
        } else {
            li.innerHTML = text;
        }

        if(type === 'danger') li.classList.add('log-danger');
        if(type === 'user') li.classList.add('log-user');
        
        this.logList.prepend(li); // Insert at top
        
        // Remove older logs (max 4 visible)
        if(this.logList.children.length > 4) {
            this.logList.removeChild(this.logList.lastChild);
        }
    }

    // 3. Chaos Engine Executer
    initChaosEngine() {
        const btn = document.getElementById('btn-chaos-exec');
        if(!btn) return;

        btn.addEventListener('click', () => {
            if(this.isChaos) return; // Prevent spam
            
            this.isChaos = true;
            btn.textContent = 'EXECUTING...';
            btn.classList.add('active');
            
            // Spike metrics
            this.updateMetricsUI(99, 95);
            
            // Inject critical log
            this.injectLog("[CHAOS] Node failure simulated. Rerouting traffic...", "danger");
            
            // Reset after 5s
            setTimeout(() => {
                this.isChaos = false;
                btn.textContent = 'Execute Failure Scenario';
                btn.classList.remove('active');
                
                // Instantly normalize visuals
                this.injectLog("[SYSTEM] Mitigation successful. Normalizing...", "system");
                this.updateMetricsUI(14, 42); 
            }, 5000);
        });
    }

    // 4. Bottom AI Terminal
    initAITerminal() {
        const input = document.getElementById('terminal-input');
        if(!input) return;

        input.addEventListener('keydown', (e) => {
            if(e.key === 'Enter') {
                const val = input.value.trim();
                if(!val) return;
                
                input.value = '';
                
                // Inject User CMD
                this.injectLog(`[USER_CMD] ${val}`, 'user');
                
                // Delay system response slightly
                setTimeout(() => {
                    this.injectLog("[SYSTEM] Task queued for execution.", "system");
                }, 600);
            }
        });
    }
}

// Boot System
document.addEventListener('DOMContentLoaded', () => {
    new TacIntelSystem();
});
