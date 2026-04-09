/**
 * Predictive Threat Matrix Module
 * ARP (Autonomous Response Protocol) linkages
 */
import { updateThreatState } from '../app.js';

export const initThreatMatrix = (bus) => {
    // Canvas or DOM based 3D representation loop
    const container = document.getElementById('matrix-canvas-container');
    const status = document.getElementById('threat-matrix-status');
    const arpPred = document.getElementById('arp-pred');
    const arpActions = document.getElementById('arp-actions');
    
    if(!container || !status) return;

    let threatLevel = 0; // 0-100
    
    // Listen to network flow events to increase threat probabilty
    bus.on('network_threat_spotted', () => {
        threatLevel += 15;
        evaluateMatrix();
    });
    
    // Master chaos trigger
    bus.on('threat_critical', () => {
        threatLevel = 100;
        evaluateMatrix();
    });

    const evaluateMatrix = () => {
        if(threatLevel < 30) {
            updateThreatState('bento-threat-matrix', 'normal');
            updateThreatState('bento-arp', 'normal');
            status.textContent = "Vectors stable. Predict minimal risk.";
            arpPred.textContent = "LOW";
            arpPred.className = "highlight-cyan";
        } else if(threatLevel < 70) {
            updateThreatState('bento-threat-matrix', 'warning');
            updateThreatState('bento-arp', 'warning');
            status.textContent = "Vector convergence detected. Risk elevating.";
            arpPred.textContent = "MEDIUM";
            arpPred.className = "highlight-magenta";
        } else {
            updateThreatState('bento-threat-matrix', 'critical');
            updateThreatState('bento-arp', 'critical');
            status.textContent = "ACTIVE ATTACK PREDICTED.";
            arpPred.textContent = "CRITICAL";
            arpPred.className = "highlight-red";
            
            // ARP Action population
            if(arpActions.children.length === 0) {
                const li = document.createElement('li');
                li.innerHTML = "Auto-Response: <span class='highlight-cyan'>Throttling Gateway...</span>";
                arpActions.appendChild(li);
            }
        }
        
        // Decay over time
        setTimeout(() => { if(threatLevel > 0) threatLevel -= 5; evaluateMatrix(); }, 5000);
    };
    
    // Initial evaluation
    evaluateMatrix();
};
