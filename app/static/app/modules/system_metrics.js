/**
 * System Metrics Module (Predictive Logic)
 */

export const initSystemMetrics = (bus) => {
    const elCpu = document.getElementById('met-cpu');
    const elRam = document.getElementById('met-ram');
    const predCpu = document.getElementById('pred-cpu');
    const predRam = document.getElementById('pred-ram');
    
    if(!elCpu) return;

    const fetchMetrics = async () => {
        try {
            const res = await fetch('/api/metrics');
            const data = await res.json();
            
            const cpu = data.cpu.percent;
            const ram = data.ram.percent;
            
            elCpu.textContent = `${cpu.toFixed(1)}%`;
            elRam.textContent = `${ram.toFixed(1)}%`;
            
            // Predictive dummy logic based on current spike
            predCpu.textContent = `${(cpu * 1.15).toFixed(1)}%`;
            predRam.textContent = `${(ram * 1.05).toFixed(1)}%`;
            
            if(data.cpu.status === 'CRITICAL') {
                predCpu.textContent = `99.9%`;
                predCpu.className = 'highlight-red';
            } else {
                predCpu.className = 'highlight-magenta';
            }
        } catch(e) {}
    };

    setInterval(fetchMetrics, 3000);
    fetchMetrics();
};
