// LieLens — Forensic Engine Logic

document.addEventListener('DOMContentLoaded', () => {
    const textarea = document.getElementById('target-content');
    const charCount = document.getElementById('char-count');
    const analyzeBtn = document.getElementById('analyze-btn');
    const resultsSection = document.getElementById('results-section');
    const loadingOverlay = document.getElementById('loading-overlay');
    const loadingStatus = document.getElementById('loading-status');
    
    // Instrument Panel Metrics
    const stateVal = document.getElementById('state-val');
    const latencyVal = document.getElementById('latency-val');

    // Character counter
    textarea.addEventListener('input', () => {
        const count = textarea.value.length;
        charCount.textContent = `${count} CHARS DETECTED`;
        if (count > 0) {
            charCount.style.color = 'var(--neon-cyan)';
        } else {
            charCount.style.color = 'var(--text-dim)';
        }
    });

    // Loading status messages
    const statusMessages = [
        'ACQUIRING TARGET DATA...',
        'PARSING LINGUISTIC PATTERNS...',
        'CROSS-REFERENCING SCAM DATABASE...',
        'DETECTING MANIPULATION VECTORS...',
        'EVALUATING CREDIBILITY MARKERS...',
        'ANALYZING EMOTIONAL PRESSURE TACTICS...',
        'COMPUTING RISK CLASSIFICATION...',
        'GENERATING FORENSIC REPORT...',
    ];

    function cycleStatus() {
        let i = 0;
        return setInterval(() => {
            loadingStatus.textContent = statusMessages[i % statusMessages.length];
            i++;
        }, 1200);
    }

    function getScoreColor(score, invert = false) {
        if (invert) {
            if (score > 60) return '#ff3300';
            if (score > 30) return '#ffcc00';
            return '#00ffcc';
        }
        if (score > 70) return '#00ffcc';
        if (score > 40) return '#ffcc00';
        return '#ff3300';
    }

    function animateScore(elementId, barId, value, invert = false) {
        const el = document.getElementById(elementId);
        const bar = document.getElementById(barId);
        if (!el || !bar) return;
        
        const color = getScoreColor(value, invert);
        el.style.color = color;
        el.textContent = value + '%';
        
        bar.style.background = color;
        bar.style.boxShadow = `0 0 8px ${color}`;
        setTimeout(() => {
            bar.style.width = value + '%';
        }, 100);
    }

    function renderTactics(tactics) {
        const grid = document.getElementById('tactics-grid');
        grid.innerHTML = '';
        const dangerWords = ['scam', 'fake', 'urgent', 'pressure', 'exploit', 'deceptive', 'manipulation'];
        
        tactics.forEach(tactic => {
            const chip = document.createElement('div');
            chip.className = 'tactic-chip';
            const isDanger = dangerWords.some(w => tactic.toLowerCase().includes(w));
            if (isDanger) chip.classList.add('danger');
            chip.textContent = tactic;
            grid.appendChild(chip);
        });
    }

    function renderReasoning(text) {
        document.getElementById('reasoning-content').textContent = text;
    }

    function setRiskBadge(level) {
        const badge = document.getElementById('risk-badge');
        badge.textContent = level;
        const colors = { 'LOW': '#00ffcc', 'MEDIUM': '#ffcc00', 'HIGH': '#ff3300', 'CRITICAL': '#ff3300' };
        const color = colors[level] || '#ff3300';
        badge.style.borderColor = color;
        badge.style.color = color;
        badge.style.boxShadow = `4px 4px 0px ${color}`;
        if (level === 'CRITICAL') {
            badge.style.background = '#ff3300';
            badge.style.color = '#0a0a0a';
        }
    }

    async function analyzeContent() {
        const content = textarea.value.trim();
        if (!content) {
            textarea.style.borderColor = 'var(--neon-red)';
            setTimeout(() => textarea.style.borderColor = '', 1500);
            return;
        }

        const startTime = Date.now();
        
        // Update Instrument Panel
        stateVal.textContent = 'ANALYZING...';
        stateVal.style.color = 'var(--neon-red)';
        stateVal.style.animation = 'blink-text 0.5s step-end infinite';

        // Show loading
        loadingOverlay.classList.remove('hidden');
        analyzeBtn.textContent = '⏳ DISSECTING...';
        analyzeBtn.classList.add('loading');
        
        const statusInterval = cycleStatus();

        try {
            const systemPrompt = `Analyze the content for credibility and manipulation. Return ONLY JSON: { "credibility_score": int, "manipulation_score": int, "tactics_detected": [], "risk_classification": "LOW"|"MEDIUM"|"HIGH"|"CRITICAL", "reasoning": "string", "ai_generated_probability": int }`;

            const modelsToTry = ['gpt-4o', 'claude-3-5-sonnet', 'gpt-4o-mini', 'x-ai/grok-4-1-fast'];
            let response = null;

            // FUNCTION WITH TIMEOUT
            const fetchWithTimeout = (model, prompt) => {
                return Promise.race([
                    puter.ai.chat(prompt, { model: model }),
                    new Promise((_, reject) => setTimeout(() => reject(new Error('TIMEOUT')), 5000))
                ]);
            };

            for (const model of modelsToTry) {
                try {
                    console.log(`LIELENS: Target Acquisition via ${model}...`);
                    const combinedPrompt = `${systemPrompt}\n\nANALYZE CONTENT: """${content}"""`;
                    response = await fetchWithTimeout(model, combinedPrompt);
                    if (response) break;
                } catch (err) { 
                    console.warn(`LIELENS: ${model} ${err.message === 'TIMEOUT' ? 'TIMED OUT' : 'FAILED'}. Skipping...`);
                }
            }

            let data;
            if (response) {
                let cleanText = response.message.content.trim();
                if (cleanText.includes('```')) cleanText = cleanText.replace(/```json/g, '').replace(/```/g, '').trim();
                data = JSON.parse(cleanText);
            } else {
                const localResponse = await fetch('/api/analyze', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ content }),
                });
                const result = await localResponse.json();
                if (result.status === 'error') throw new Error(result.message);
                data = result.data;
            }

            // Calculate Latency
            const duration = Date.now() - startTime;
            latencyVal.textContent = `${duration}ms`;
            latencyVal.style.color = duration < 2000 ? 'var(--neon-cyan)' : 'var(--neon-red)';

            // Reset UI
            resultsSection.classList.remove('hidden');
            resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });

            setTimeout(() => {
                animateScore('credibility-score', 'credibility-bar', data.credibility_score, false);
                animateScore('manipulation-score', 'manipulation-bar', data.manipulation_score, true);
                animateScore('ai-score', 'ai-bar', data.ai_generated_probability, true);
                setRiskBadge(data.risk_classification);
                renderTactics(data.tactics_detected);
                renderReasoning(data.reasoning);
            }, 300);

        } catch (error) {
            alert('SYSTEM FAILURE: ' + error.message);
        } finally {
            clearInterval(statusInterval);
            loadingOverlay.classList.add('hidden');
            analyzeBtn.textContent = 'INITIATE DISSECTION';
            analyzeBtn.classList.remove('loading');
            
            stateVal.textContent = 'READY';
            stateVal.style.color = 'var(--neon-cyan)';
            stateVal.style.animation = 'none';
        }
    }

    analyzeBtn.addEventListener('click', analyzeContent);
});
