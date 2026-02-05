const submitBtn = document.getElementById('submitBtn');
const queryInput = document.getElementById('queryInput');
const resultsContainer = document.getElementById('resultsContainer');
const errorMessage = document.getElementById('errorMessage');

submitBtn.addEventListener('click', submitQuery);
queryInput.addEventListener('keydown', (e) => {
    if (e.ctrlKey && e.key === 'Enter') {
        submitQuery();
    }
});

async function submitQuery() {
    const query = queryInput.value.trim();
    
    if (!query) {
        showError('Please enter a question first');
        return;
    }

    // Reset UI
    errorMessage.style.display = 'none';
    resultsContainer.style.display = 'block';
    submitBtn.disabled = true;
    submitBtn.textContent = 'Loading...';

    // Reset all panes to loading state
    resetPanes();

    try {
        const response = await fetch('/api/query', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'An error occurred');
        }

        const results = await response.json();
        
        // Display results
        displayResult('claude', results.claude);
        displayResult('chatgpt', results.chatgpt);
        displayResult('gemini', results.gemini);

    } catch (error) {
        showError(`Error: ${error.message}`);
        resultsContainer.style.display = 'none';
    } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = 'Compare Responses';
    }
}

function resetPanes() {
    ['claude', 'chatgpt', 'gemini'].forEach(llm => {
        const content = document.getElementById(`${llm}Content`);
        const status = document.getElementById(`${llm}Status`);
        
        content.innerHTML = '<div class="loading-spinner"></div>';
        status.className = 'status-indicator loading';
        status.textContent = '';
    });
}

function displayResult(llm, content) {
    const contentElement = document.getElementById(`${llm}Content`);
    const statusElement = document.getElementById(`${llm}Status`);
    
    if (content.startsWith('Error:')) {
        contentElement.innerHTML = `<div style="color: #d32f2f; font-weight: 500;">${content}</div>`;
        statusElement.className = 'status-indicator error';
    } else {
        contentElement.innerHTML = formatContent(content);
        statusElement.className = 'status-indicator done';
    }
}

function formatContent(text) {
    // Basic markdown-like formatting
    let html = text
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/\n\n+/g, '</p><p>')
        .replace(/\n/g, '<br>');
    
    return `<p>${html}</p>`;
}

function showError(message) {
    errorMessage.textContent = message;
    errorMessage.style.display = 'block';
}
