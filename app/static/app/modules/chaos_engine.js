/**
 * Chaos Engine Modeller
 */
import { updateThreatState } from '../app.js';

export const initChaosEngine = (bus) => {
    const btnModel = document.getElementById('btn-chaos-model');
    const btnExec = document.getElementById('btn-chaos-execute');
    const impactTxt = document.getElementById('chaos-impact');
    if (!btnModel || !btnExec || !impactTxt) return;

    btnModel.addEventListener('click', () => {
        btnModel.disabled = true;
        impactTxt.innerHTML = "Modeling failure scenario...";
        
        setTimeout(() => {
            impactTxt.innerHTML = "Predicted: <span class='highlight-red'>CPU +85%, Net Delay +200ms</span>. Risk: High.";
            btnExec.classList.remove('hidden'); // allow execution
            updateThreatState('bento-chaos', 'warning');
        }, 1500);
    });

    btnExec.addEventListener('click', async () => {
        btnExec.disabled = true;
        impactTxt.innerHTML = "Executing node failure...";
        updateThreatState('bento-chaos', 'critical');
        bus.emit('threat_critical', {});
        
        try {
            await fetch('/api/chaos', { method: 'POST' });
        } catch(e) {}
        
        setTimeout(() => {
            impactTxt.innerHTML = "Node recovered. State stable.";
            btnExec.classList.add('hidden');
            btnModel.disabled = false;
            updateThreatState('bento-chaos', 'normal');
        }, 8000);
    });
};
