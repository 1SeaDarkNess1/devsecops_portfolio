
            /* ═══════════════════════════════════════════════════════════
               §JS-3  THREAT VISUALIZATION ENGINE
               Network graph showing threats blocked
               ═══════════════════════════════════════════════════════════ */
            const tCanvas = document.getElementById('threat-canvas');
            if (tCanvas) {
                const tCtx = tCanvas.getContext('2d');
                let tNodes = [];
                let tParticles = [];
                
                function initThreatMap() {
                    tCanvas.width = tCanvas.parentElement.clientWidth;
                    tCanvas.height = 400;
                    tNodes = [];
                    // Generate map nodes
                    for (let i = 0; i < 15; i++) {
                        tNodes.push({
                            x: Math.random() * tCanvas.width,
                            y: Math.random() * tCanvas.height,
                            r: Math.random() * 3 + 2,
                            type: Math.random() > 0.8 ? 'target' : 'relay'
                        });
                    }
                }
                
                window.addEventListener('resize', initThreatMap);
                initThreatMap();

                function spawnThreatParticle() {
                    const origin = tNodes[Math.floor(Math.random() * tNodes.length)];
                    const target = tNodes[Math.floor(Math.random() * tNodes.length)];
                    const type = Math.random() > 0.7 ? 'threat' : 'normal';
                    
                    tParticles.push({
                        x: origin.x, y: origin.y,
                        startX: origin.x, startY: origin.y,
                        targetX: target.x, targetY: target.y,
                        progress: 0,
                        speed: Math.random() * 0.01 + 0.005,
                        type: type,
                        color: type === 'threat' ? '#ff6b6b' : '#00f5d4'
                    });
                }

                setInterval(spawnThreatParticle, 800);

                function animateThreats() {
                    tCtx.fillStyle = 'rgba(10, 10, 18, 0.2)';
                    tCtx.fillRect(0, 0, tCanvas.width, tCanvas.height);

                    // Draw connections
                    tCtx.strokeStyle = 'rgba(255, 255, 255, 0.05)';
                    tCtx.lineWidth = 1;
                    tNodes.forEach(n1 => {
                        tNodes.forEach(n2 => {
                            const dist = Math.hypot(n1.x - n2.x, n1.y - n2.y);
                            if (dist < 150) {
                                tCtx.beginPath();
                                tCtx.moveTo(n1.x, n1.y);
                                tCtx.lineTo(n2.x, n2.y);
                                tCtx.stroke();
                            }
                        });
                    });

                    // Draw Nodes
                    tNodes.forEach(n => {
                        tCtx.beginPath();
                        tCtx.arc(n.x, n.y, n.r, 0, Math.PI * 2);
                        tCtx.fillStyle = n.type === 'target' ? '#00e5ff' : '#00f5d4';
                        tCtx.globalAlpha = 0.5;
                        tCtx.fill();
                        tCtx.globalAlpha = 1.0;
                    });

                    // Draw Particles
                    for (let i = tParticles.length - 1; i >= 0; i--) {
                        let p = tParticles[i];
                        p.progress += p.speed;
                        
                        if (p.progress >= 1) {
                            if (p.type === 'threat') {
                                // Blocked effect
                                tCtx.beginPath();
                                tCtx.arc(p.targetX, p.targetY, 15, 0, Math.PI * 2);
                                tCtx.strokeStyle = '#ff6b6b';
                                tCtx.stroke();
                            }
                            tParticles.splice(i, 1);
                            continue;
                        }

                        p.x = p.startX + (p.targetX - p.startX) * p.progress;
                        p.y = p.startY + (p.targetY - p.startY) * p.progress;

                        tCtx.beginPath();
                        tCtx.arc(p.x, p.y, 3, 0, Math.PI * 2);
                        tCtx.fillStyle = p.color;
                        tCtx.shadowBlur = 10;
                        tCtx.shadowColor = p.color;
                        tCtx.fill();
                        tCtx.shadowBlur = 0;
                    }

                    requestAnimationFrame(animateThreats);
                }
                animateThreats();
            }

            /* ═══════════════════════════════════════════════════════════
               §JS-4  SCROLL REVEAL & PIPELINE ANIMATION
               ═══════════════════════════════════════════════════════════ */
            const revealElements = document.querySelectorAll('.reveal');
            
            const revealObserver = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('visible');
                    }
                });
            }, { threshold: 0.1, rootMargin: "0px 0px -50px 0px" });

            revealElements.forEach(el => revealObserver.observe(el));

            // Pipeline Stages Sequential Reveal
            const pipelineObserver = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const stages = document.querySelectorAll('.pipeline-stage');
                        stages.forEach((stage, idx) => {
                            setTimeout(() => {
                                stage.classList.add('visible');
                                setTimeout(() => stage.classList.add('active'), 600);
                            }, stage.dataset.delay || (idx * 150));
                        });
                        pipelineObserver.disconnect();
                    }
                });
            }, { threshold: 0.5 });
            
            const pipelineTrack = document.getElementById('pipeline-track');
            if (pipelineTrack) pipelineObserver.observe(pipelineTrack);

            /* ═══════════════════════════════════════════════════════════
               §JS-5  DASHBOARD METRICS & TERMINAL
               ═══════════════════════════════════════════════════════════ */
            const termBody = document.getElementById('terminal-body');
            const termLines = [
                "[SYSTEM] Booting secure environment...",
                "[GIT] Webhook received. Event: deployment.",
                "[GITLEAKS] Scanning repository for secrets... <span class='success'>CLEAN</span>.",
                "[SEMGREP] SAST analyzing source code... <span class='success'>PASS</span>.",
                "[DOCKER] Building container image bbm-sec-ui:v4.2.1...",
                "[TRIVY] Scanning image layers... <span class='success'>0 CRITICAL</span>.",
                "[DEPLOY] Pushing to Oracle Cloud Container Engine...",
                "[SYSTEM] Deployment completed in 12.4s.",
                "<span class='prompt'>bbm@prod ~$</span> monitoring mode engaged. Waiting for telemetry..."
            ];

            let termIdx = 0;
            function typeTerminal() {
                if (!termBody || termIdx >= termLines.length) return;
                
                const line = document.createElement('div');
                line.className = 'terminal-line';
                line.innerHTML = termLines[termIdx];
                termBody.appendChild(line);
                
                termIdx++;
                setTimeout(typeTerminal, Math.random() * 400 + 200);
            }

            const termObserver = new IntersectionObserver((entries) => {
                if (entries[0].isIntersecting) {
                    typeTerminal();
                    termObserver.disconnect();
                }
            }, { threshold: 0.5 });
            
            if (termBody) termObserver.observe(document.getElementById('terminal'));

            // Simulated real-time metrics update
            function updateMetrics() {
                const cpuMetric = document.getElementById('cpu-metric');
                const ramMetric = document.getElementById('ram-metric');
                if (cpuMetric) cpuMetric.innerText = Math.floor(Math.random() * 15 + 5) + '%';
                if (ramMetric) ramMetric.innerText = (Math.random() * 2 + 8).toFixed(1) + ' GB';
            }
            setInterval(updateMetrics, 2000);

            // Refraction light effect on glass cards
            const glassCards = document.querySelectorAll('.liquid-glass');
            glassCards.forEach(card => {
                const light = document.createElement('div');
                light.className = 'refraction-light';
                card.appendChild(light);

                card.addEventListener('mousemove', (e) => {
                    const rect = card.getBoundingClientRect();
                    const x = e.clientX - rect.left;
                    const y = e.clientY - rect.top;
                    light.style.left = `${x}px`;
                    light.style.top = `${y}px`;
                    light.style.opacity = '1';
                });

                card.addEventListener('mouseleave', () => {
                    light.style.opacity = '0';
                });
            });

            // Smooth scrolling and Navbar active state
            const sections = document.querySelectorAll("section");
            const navLinks = document.querySelectorAll(".nav-link");

            window.addEventListener("scroll", () => {
                let current = "";
                sections.forEach((section) => {
                    const sectionTop = section.offsetTop;
                    const sectionHeight = section.clientHeight;
                    if (scrollY >= sectionTop - sectionHeight / 3) {
                        current = section.getAttribute("id");
                    }
                });

                navLinks.forEach((a) => {
                    a.classList.remove("active");
                    if (a.getAttribute("href").includes(current)) {
                        a.classList.add("active");
                    }
                });
            });

        })();
