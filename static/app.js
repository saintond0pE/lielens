// LieLens — Human-Centric Analysis Logic

document.addEventListener('DOMContentLoaded', () => {
    const textarea = document.getElementById('target-content');
    const charCount = document.getElementById('char-count');
    const analyzeBtn = document.getElementById('analyze-btn');
    const resultsSection = document.getElementById('results-section');
    const loadingOverlay = document.getElementById('loading-overlay');
    const loadingStatus = document.getElementById('loading-status');

    // Character counter
    textarea.addEventListener('input', () => {
        const count = textarea.value.length;
        charCount.textContent = `${count} CHARACTERS`;
        charCount.style.color = count > 0 ? 'var(--neon-cyan)' : 'var(--text-dim)';
    });

    // Simple status messages
    const statusMessages = [
        'REVIEWING CONTENT...',
        'CHECKING FOR PATTERNS...',
        'EVALUATING TACTICS...',
        'GENERATING REPORT...',
    ];

    function cycleStatus() {
        let i = 0;
        return setInterval(() => {
            loadingStatus.textContent = statusMessages[i % statusMessages.length];
            i++;
        }, 1500);
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
        bar.style.width = '0%';
        setTimeout(() => {
            bar.style.width = value + '%';
        }, 100);
    }

    function renderTactics(tactics) {
        const grid = document.getElementById('tactics-grid');
        grid.innerHTML = '';
        tactics.forEach(tactic => {
            const chip = document.createElement('div');
            chip.className = 'tactic-chip';
            chip.textContent = tactic;
            grid.appendChild(chip);
        });
    }

    async function analyzeContent() {
        const content = textarea.value.trim();
        if (!content) return;

        // UI Feedback
        loadingOverlay.classList.remove('hidden');
        analyzeBtn.textContent = 'ANALYZING...';
        analyzeBtn.classList.add('loading');
        const statusInterval = cycleStatus();

        try {
            // Priority 1: Cloud Providers via Puter.js
            let data = null;
            const models = ['gpt-4o', 'claude-3-5-sonnet', 'gpt-4o-mini'];
            const systemPrompt = "Analyze for credibility and manipulation. Return JSON ONLY: {credibility_score: int, manipulation_score: int, tactics_detected: string[], risk_classification: string, reasoning: string, ai_generated_probability: int}";

            for (const model of models) {
                try {
                    const response = await Promise.race([
                        puter.ai.chat(`${systemPrompt}\n\nContent: "${content}"`, { model }),
                        new Promise((_, reject) => setTimeout(() => reject(new Error('TIMEOUT')), 6000))
                    ]);
                    if (response) {
                        let text = response.message.content.trim();
                        if (text.includes('```')) text = text.replace(/```json/g, '').replace(/```/g, '').trim();
                        data = JSON.parse(text);
                        break;
                    }
                } catch (e) { console.warn(`Model ${model} failed, skipping...`); }
            }

            // Priority 2: Local Fallback
            if (!data) {
                const res = await fetch('/api/analyze', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ content })
                });
                const result = await res.json();
                data = result.data;
            }

            // Render Results
            resultsSection.classList.remove('hidden');
            resultsSection.scrollIntoView({ behavior: 'smooth' });

            setTimeout(() => {
                animateScore('credibility-score', 'credibility-bar', data.credibility_score);
                animateScore('manipulation-score', 'manipulation-bar', data.manipulation_score, true);
                animateScore('ai-score', 'ai-bar', data.ai_generated_probability, true);
                
                const badge = document.getElementById('risk-badge');
                badge.textContent = data.risk_classification;
                const color = data.risk_classification === 'LOW' ? '#00ffcc' : (data.risk_classification === 'MEDIUM' ? '#ffcc00' : '#ff3300');
                badge.style.color = color;
                badge.style.borderColor = color;
                
                renderTactics(data.tactics_detected);
                document.getElementById('reasoning-content').textContent = data.reasoning;
            }, 300);

        } catch (error) {
            console.error(error);
            alert('Analysis could not be completed at this time.');
        } finally {
            clearInterval(statusInterval);
            loadingOverlay.classList.add('hidden');
            analyzeBtn.textContent = 'ANALYZE NOW';
            analyzeBtn.classList.remove('loading');
        }
    }

    analyzeBtn.addEventListener('click', analyzeContent);
});
