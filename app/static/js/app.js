/**
 * TacIntel Particle Architect Engine
 * Pure Canvas Rendering with getImageData & Spring Physics
 */

const initParticleEngine = () => {
    const canvas = document.getElementById('bbm-canvas');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d', { willReadFrequently: true });
    let w, h;
    let particles = [];
    
    // Mouse Interaction State
    const mouse = {
        x: null,
        y: null,
        radius: 120 // Repulsion zone radius
    };

    // Track mouse over canvas
    canvas.addEventListener('mousemove', (e) => {
        const rect = canvas.getBoundingClientRect();
        mouse.x = e.clientX - rect.left;
        mouse.y = e.clientY - rect.top;
    });
    
    // Reset mouse when leaving canvas
    canvas.addEventListener('mouseleave', () => {
        mouse.x = null;
        mouse.y = null;
    });

    /**
     * Particle Class with Spring Physics
     */
    class Particle {
        constructor(x, y) {
            this.x = Math.random() * w; // Start random
            this.y = Math.random() * h;
            this.baseX = x; // Target coordinate
            this.baseY = y;
            this.size = 2.5; // Particle size
            this.density = (Math.random() * 30) + 1; // Weight/Mass variations
            
            // Velocity
            this.vx = 0;
            this.vy = 0;
            
            // Physics Constants
            this.friction = 0.85; // Damping
            this.springFactor = 0.1; // Pull to origin
            
            // Randomize neon blue/cyan colors for depth
            const colors = ['#00e5ff', '#00b3cc', '#004d66', '#ff007f'];
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
                    const maxDistance = mouse.radius;
                    // Force is stronger closer to center
                    const force = (maxDistance - distance) / maxDistance; 
                    const directionX = forceDirectionX * force * this.density;
                    const directionY = forceDirectionY * force * this.density;
                    
                    this.vx -= directionX;
                    this.vy -= directionY;
                }
            }

            // 2. Spring Force (Pull back to origin)
            const dxBase = this.baseX - this.x;
            const dyBase = this.baseY - this.y;
            this.vx += dxBase * this.springFactor;
            this.vy += dyBase * this.springFactor;

            // 3. Apply Friction
            this.vx *= this.friction;
            this.vy *= this.friction;

            // 4. Update Position
            this.x += this.vx;
            this.y += this.vy;
        }
    }

    /**
     * Scan text and convert to particles
     */
    const initTextMap = () => {
        particles = [];
        w = canvas.parentElement.clientWidth;
        h = canvas.parentElement.clientHeight;
        canvas.width = w;
        canvas.height = h;

        // Draw temporary text to scan
        ctx.fillStyle = "white";
        // Calculate font size relative to screen
        const fontSize = Math.min(w / 3, 300);
        ctx.font = `800 ${fontSize}px 'JetBrains Mono', sans-serif`;
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        
        ctx.fillText("BBM", w / 2, h / 2);

        // Scan pixels
        const textCoordinates = ctx.getImageData(0, 0, w, h);
        ctx.clearRect(0, 0, w, h); // Clear the solid text

        // Skip pixels to avoid lag (Resolution step)
        const step = 6; // Check every 6th pixel (Adjust for particle density)

        for (let y = 0; y < h; y += step) {
            for (let x = 0; x < w; x += step) {
                // Determine array index of the alpha channel
                const index = (y * w + x) * 4 + 3;
                
                // If pixel is not transparent (Alpha > 128)
                if (textCoordinates.data[index] > 128) {
                    // Create particle at this coordinate
                    particles.push(new Particle(x, y));
                }
            }
        }
        
        // Connect particles rendering setup
        ctx.lineWidth = 0.5;
    };

    /**
     * Animation Loop
     */
    const animate = () => {
        ctx.clearRect(0, 0, w, h);
        
        particles.forEach(p => {
            p.update();
            p.draw();
        });
        
        // Optional: Draw faint connection lines if particles are close
        // (Turned off by default for performance, enable if needed)
        /*
        for (let i = 0; i < particles.length; i++) {
            for (let j = i; j < particles.length; j++) {
                const dx = particles[i].x - particles[j].x;
                const dy = particles[i].y - particles[j].y;
                const distance = dx * dx + dy * dy;
                
                if (distance < 600) { // Dist squared
                    ctx.strokeStyle = `rgba(0, 229, 255, ${0.1 - distance/6000})`;
                    ctx.beginPath();
                    ctx.moveTo(particles[i].x, particles[i].y);
                    ctx.lineTo(particles[j].x, particles[j].y);
                    ctx.stroke();
                }
            }
        }
        */

        requestAnimationFrame(animate);
    };

    // Bootstrap
    initTextMap();
    animate();

    // Handle Resize
    window.addEventListener('resize', () => {
        // Debounce resize
        clearTimeout(canvas.resizeTimer);
        canvas.resizeTimer = setTimeout(initTextMap, 200);
    });
};

// Start system when DOM is ready
document.addEventListener('DOMContentLoaded', initParticleEngine);
