const API_BASE = 'http://localhost:7000/api';

const statusEl = document.getElementById('status');
const resultsEl = document.getElementById('results');
const textInput = document.getElementById('textInput');
const sendBtn = document.getElementById('sendBtn');
const searchInput = document.getElementById('searchInput');
const searchBtn = document.getElementById('searchBtn');
const micBtn = document.getElementById('micBtn');

async function postJSON(url, payload) {
  const res = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });
  const data = await res.json().catch(() => ({ error: 'Invalid JSON' }));
  return { ok: res.ok, data };
}

async function sendQuery() {
  const text = (textInput.value || '').trim();
  if (!text) return;
  
  statusEl.textContent = 'Thinking...';
  statusEl.style.color = '#ff6b35';
  
  const { ok, data } = await postJSON(`${API_BASE}/chat`, { message: text });
  
  if (ok && data.speaking) {
    statusEl.textContent = 'Speaking...';
    statusEl.style.color = '#00d9ff';
    
    // Animate hologram sync
    document.body.style.animation = 'pulse 0.5s ease-in-out infinite';
    
    // Stop animation after 3 seconds
    setTimeout(() => {
      statusEl.textContent = 'Ready';
      statusEl.style.color = '#00ff88';
      document.body.style.animation = 'none';
    }, 3000);
  } else {
    statusEl.textContent = ok ? 'Ready' : 'Error';
    statusEl.style.color = ok ? '#00ff88' : '#ff4757';
  }
  
  resultsEl.textContent = data.response || data.error || 'No response';
  textInput.value = '';
}

async function doSearch() {
  const query = (searchInput.value || '').trim();
  if (!query) return;
  statusEl.textContent = 'Searching...';
  const { ok, data } = await postJSON(`${API_BASE}/chat`, { message: `search for: ${query}` });
  statusEl.textContent = ok ? 'OK' : 'Error';
  resultsEl.textContent = data.response || data.error || 'No response';
}

sendBtn.addEventListener('click', sendQuery);
searchBtn.addEventListener('click', doSearch);

textInput.addEventListener('keydown', (e) => {
  if (e.key === 'Enter') sendQuery();
});
searchInput.addEventListener('keydown', (e) => {
  if (e.key === 'Enter') doSearch();
});

// Voice input via Web Speech API (browser-side)
let recognition;
if ('webkitSpeechRecognition' in window) {
  recognition = new webkitSpeechRecognition();
  recognition.lang = 'en-US';
  recognition.interimResults = false;
  recognition.maxAlternatives = 1;

  recognition.onresult = (event) => {
    const transcript = event.results[0][0].transcript;
    textInput.value = transcript;
    sendQuery();
  };
  recognition.onerror = () => { statusEl.textContent = 'Mic error'; };
}

micBtn.addEventListener('click', () => {
  if (!recognition) {
    alert('Browser speech recognition not supported.');
    return;
  }
  recognition.start();
});
