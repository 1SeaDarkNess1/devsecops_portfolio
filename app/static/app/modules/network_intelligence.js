/**
 * Holographic 3D Network Intelligence Module
 * Canvas WebGL/2D Flow Simulation + Grid Overlay
 */

export const initNetworkFlow = (bus) => {
    const canvas = document.getElementById('flow-node-canvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d', { alpha: false });
    
    let w, h;
    const resize = () => {
        const rect = canvas.parentElement.getBoundingClientRect();
        w = rect.width;
        h = rect.height;
        canvas.width = w * window.devicePixelRatio;
        canvas.height = h * window.devicePixelRatio;
        ctx.scale(window.devicePixelRatio, window.devicePixelRatio);
    };
    window.addEventListener('resize', resize);
    resize();
    
    // 3D Flow Nodes
    class FlowNode {
        constructor() {
            this.reset();
        }
        reset() {
            // Spawn far away (z = deep)
            this.x = (Math.random() - 0.5) * w * 2;
            this.y = (Math.random() - 0.5) * h * 2;
            this.z = Math.random() * 1000 + 500;
            this.speed = Math.random() * 2 + 1;
            // Map threat color
            const isThreat = Math.random() < 0.15;
            if(isThreat) {
                this.color = `rgba(255, 0, 51, 1)`; // Red
                // Tell the matrix we spotted an anomaly
                if(Math.random() < 0.05) bus.emit('network_threat_spotted', {});
            } else if(Math.random() < 0.3) {
                this.color = `rgba(179, 136, 255, 1)`; // Purple
            } else {
                this.color = `rgba(0, 229, 255, 1)`; // Cyan
            }
        }
        update() {
            this.z -= this.speed * 10;
            if (this.z <= 0) {
                this.reset();
                this.z = 1500;
            }
        }
        draw() {
            const fov = 300;
            const x3d = this.x * (fov / this.z) + w / 2;
            const y3d = this.y * (fov / this.z) + h / 2;
            const size = Math.max((1500 - this.z) / 400, 0.5);
            
            ctx.fillStyle = this.color;
            ctx.beginPath();
            ctx.arc(x3d, y3d, size, 0, Math.PI * 2);
            ctx.fill();
            
            // Draw a trailing line backwards to give speed feeling
            const prevZ = this.z + this.speed * 20;
            const x3dOld = this.x * (fov / prevZ) + w / 2;
            const y3dOld = this.y * (fov / prevZ) + h / 2;
            ctx.strokeStyle = this.color.replace(', 1)', ', 0.3)');
            ctx.lineWidth = size / 2;
            ctx.beginPath();
            ctx.moveTo(x3dOld, y3dOld);
            ctx.lineTo(x3d, y3d);
            ctx.stroke();
        }
    }

    const nodes = Array.from({length: 150}, () => new FlowNode());
    
    // Animation Loop
    const animate = () => {
        // Dark trail effect for the background
        ctx.fillStyle = 'rgba(5, 7, 15, 0.3)';
        ctx.fillRect(0, 0, w, h);
        
        nodes.forEach(n => {
            n.update();
            n.draw();
        });
        requestAnimationFrame(animate);
    };
    animate();

    // ----------------------------------------------------
    // The Iron Grid Overlay (Contextual Logic)
    // ----------------------------------------------------
    const streamGrid = document.getElementById('network-log-grid');
    const endpoints = ['/api/auth_token', '/core/vault', '/dashboard/api', '/bin/sh', '/wp-admin'];
    const ips = ['192.168.1.100', '10.5.0.32', '172.16.0.4', '185.33.220.1', '104.128.5.5'];
    
    const simulateArrival = () => {
        const row = document.createElement('div');
        row.className = 'log-row';
        
        const path = endpoints[Math.floor(Math.random() * endpoints.length)];
        const ip = ips[Math.floor(Math.random() * ips.length)];
        const latency = Math.floor(Math.random() * 80) + 5;
        
        let method = 'GET'; let mClass = 'get';
        if(path.includes('/auth') || path.includes('/vault')) { method = 'POST'; mClass = 'post'; }
        if(path.includes('/wp-admin') || path.includes('/bin')) { method = 'DROP'; mClass = 'drop'; bus.emit('network_threat_spotted',{}); }
        
        row.innerHTML = `
            <span class="log-method ${mClass}">${method}</span>
            <span class="log-path">${path}</span>
            <span class="log-ip">${ip}</span>
            <span class="log-lat">${latency}ms</span>
        `;
        streamGrid.appendChild(row);
        
        // Auto scroll & trim
        streamGrid.scrollTop = streamGrid.scrollHeight;
        if(streamGrid.children.length > 20) {
            streamGrid.removeChild(streamGrid.firstChild);
        }
        
        setTimeout(simulateArrival, Math.random() * 1500 + 400);
    };
    
    setTimeout(simulateArrival, 1000);
};
