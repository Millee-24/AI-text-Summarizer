// Initialize Lucide icons
lucide.createIcons();

// Elements
const tabBtns = document.querySelectorAll('.tab-btn');
const tabContents = document.querySelectorAll('.tab-content');
const personaCards = document.querySelectorAll('.persona-card');
const summarizeBtn = document.getElementById('summarize-btn');
const errorMessage = document.getElementById('error-message');

const emptyState = document.getElementById('empty-state');
const loadingState = document.getElementById('loading-state');
const resultsContent = document.getElementById('results-content');
const progressBar = document.getElementById('progress-bar');
const loadingText = document.getElementById('loading-text');

let activeTab = 'text';
let activePersona = 'Researcher';

// Tab Switching
tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        tabBtns.forEach(b => b.classList.remove('active'));
        tabContents.forEach(c => c.classList.remove('active'));
        
        btn.classList.add('active');
        activeTab = btn.getAttribute('data-tab');
        document.getElementById(`tab-${activeTab}`).classList.add('active');
    });
});

// Persona Selection
personaCards.forEach(card => {
    card.addEventListener('click', () => {
        personaCards.forEach(c => c.classList.remove('active'));
        card.classList.add('active');
        activePersona = card.getAttribute('data-persona');
    });
});

// Summarize Action
summarizeBtn.addEventListener('click', async () => {
    // Hide errors
    errorMessage.classList.add('hidden');
    
    // Get Input
    let content = '';
    if (activeTab === 'text') {
        content = document.getElementById('text-input').value;
    } else {
        content = document.getElementById('url-input').value;
    }

    if (!content.trim()) {
        showError('Please provide some content first.');
        return;
    }

    const language = document.getElementById('language-select').value;

    // UI State: Loading
    emptyState.classList.add('hidden');
    resultsContent.classList.add('hidden');
    loadingState.classList.remove('hidden');
    
    // Fake Progress Animation
    let progress = 0;
    progressBar.style.width = '0%';
    const texts = ["Analyzing context...", "Extracting keywords...", "Adapting persona...", "Finalizing..."];
    let textIndex = 0;
    
    const progressInterval = setInterval(() => {
        if(progress < 90) progress += Math.random() * 15;
        progressBar.style.width = `${Math.min(progress, 90)}%`;
        
        if (progress > (textIndex + 1) * 25 && textIndex < texts.length - 1) {
            textIndex++;
            loadingText.innerText = texts[textIndex];
        }
    }, 500);

    // API Request
    try {
        const response = await fetch('http://localhost:5000/api/summarize', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                type: activeTab,
                content: content,
                persona: activePersona,
                language: language
            })
        });

        const data = await response.json();
        clearInterval(progressInterval);
        progressBar.style.width = '100%';

        if (!response.ok || !data.success) {
            throw new Error(data.error || 'Failed to summarize.');
        }

        setTimeout(() => {
            renderResults(data, language);
        }, 500); // Wait for 100% bar animation

    } catch (err) {
        clearInterval(progressInterval);
        loadingState.classList.add('hidden');
        emptyState.classList.remove('hidden');
        showError(err.message);
    }
});

function renderResults(data, language) {
    loadingState.classList.add('hidden');
    resultsContent.classList.remove('hidden');

    // Stats
    document.getElementById('stats-container').innerHTML = `
        <div class="stat-card">
            <div class="stat-num">${data.original_words}</div>
            <div class="stat-lbl">Original words</div>
        </div>
        <div class="stat-card">
            <div class="stat-num blue">${data.lexrank_words}</div>
            <div class="stat-lbl">LexRank</div>
        </div>
        <div class="stat-card">
            <div class="stat-num green">${data.persona_words}</div>
            <div class="stat-lbl">${activePersona}</div>
        </div>
        <div class="stat-card">
            <div class="stat-num amber">${data.words_removed}</div>
            <div class="stat-lbl">Removed</div>
        </div>
        <div class="stat-card">
            <div class="stat-num green">${data.compression}</div>
            <div class="stat-lbl">Compression</div>
        </div>
    `;

    // Summary
    document.getElementById('summary-content').innerHTML = data.highlighted_summary;

    // Translation
    const translationCard = document.getElementById('translation-card');
    if (data.translated_summary) {
        translationCard.classList.remove('hidden');
        document.getElementById('translation-content').innerHTML = data.translated_summary;
    } else {
        translationCard.classList.add('hidden');
    }

    // Keywords
    const kwContainer = document.getElementById('keywords-container');
    kwContainer.innerHTML = '';
    data.keywords.forEach(kw => {
        const span = document.createElement('span');
        span.className = 'kw-chip';
        span.innerText = kw;
        kwContainer.appendChild(span);
    });

    lucide.createIcons();
    
    // Re-trigger animation by removing and re-adding classes
    resultsContent.querySelectorAll('.fade-in-up').forEach(el => {
        el.style.animation = 'none';
        el.offsetHeight; /* trigger reflow */
        el.style.animation = null; 
    });
}

function showError(msg) {
    errorMessage.innerText = msg;
    errorMessage.classList.remove('hidden');
}

async function copyToClipboard(elementId) {
    const el = document.getElementById(elementId);
    if (!el) return;
    
    // Remove mark tags for plain text copying
    const text = el.innerText;
    try {
        await navigator.clipboard.writeText(text);
        // Minimal visual feedback could go here
    } catch (err) {
        console.error('Failed to copy', err);
    }
}
