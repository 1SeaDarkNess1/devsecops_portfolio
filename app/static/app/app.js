/**
 * ROOT MODULE: TacIntel Emergent AI Dashboard
 * Orchestrator for all intelligence modules.
 */

import { initNetworkFlow } from './modules/network_intelligence.js';
import { initThreatMatrix } from './modules/threat_intel.js';
import { initCICD } from './modules/cicd_attestation.js';
import { initChaosEngine } from './modules/chaos_engine.js';
import { initSystemMetrics } from './modules/system_metrics.js';

// Central Event Bus for cross-module communication
export const EventBus = {
    events: {},
    on(event, listener) {
        if (!this.events[event]) this.events[event] = [];
        this.events[event].push(listener);
    },
    emit(event, data) {
        if (this.events[event]) {
            this.events[event].forEach(l => l(data));
        }
    }
};

/**
 * Universal Global Threat State Manager
 * Binds CSS data-threat attributes across the Bento Matrix
 */
export const updateThreatState = (panelId, state) => {
    // state can be: "normal", "warning", "critical"
    const panel = document.getElementById(panelId);
    if (!panel) return;
    
    // Apply state change for CSS liquid glass bindings
    panel.setAttribute('data-threat', state);
    console.log(`[TacIntel] State Shift -> ${panelId} is now ${state.toUpperCase()}`);
};

const bootSequence = () => {
    console.log("████████████████████ 100%");
    console.log("[SYSTEM] Tactical Intelligence Center Online.");
    
    // Initialize Subsystems
    initCICD(EventBus);
    initSystemMetrics(EventBus);
    initChaosEngine(EventBus);
    initThreatMatrix(EventBus);
    initNetworkFlow(EventBus);
    
    // Quick Init Zero-Trust Vault UI Loop
    const vaultTxt = document.getElementById('dlp-rules');
    if (vaultTxt) {
        const rules = [
            "Generated: strict_IAM_policy_v4",
            "Auto-applied: Data masking on SSN payload",
            "Predicting Exfil Path: Port 443 -> Unknown Node",
            "Mitigation: Throttled node bandwidth"
        ];
        let idx = 0;
        setInterval(() => {
            vaultTxt.textContent = `[Vault AI] ${rules[idx]}`;
            idx = (idx + 1) % rules.length;
        }, 3500);
    }
    
    // Quick Init WAF Box
    const wafIn = document.getElementById('waf-ai-input');
    const wafOut = document.getElementById('waf-ai-output');
    if(wafIn && wafOut) {
        wafIn.addEventListener('keydown', (e) => {
            if(e.key === 'Enter') {
                const p = wafIn.value;
                wafIn.value = "";
                wafOut.innerHTML = `Analyzing vector...<br><span class="highlight-cyan">> Model Generated:</span> Blocking rule ID: XR-32 for payload shape. <br><span class="highlight-magenta">[SUCCESS] Auto-deployed to Edge.</span>`;
            }
        });
    }
};

document.addEventListener('DOMContentLoaded', bootSequence);
