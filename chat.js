const backendURL = "https://sibia-chatbot.onrender.com/chat";


function toggleChat() {
  const chat = document.getElementById('chat-box');
  chat.style.display = (chat.style.display === 'none') ? 'block' : 'none';
}

async function sendChat() {
  const input = document.getElementById('chat-input');
  const msg = input.value.trim();
  if (!msg) return;
  const log = document.getElementById('chat-log');
  log.innerHTML += `<div class="user-msg">${msg}</div>`;
  input.value = '';
  const res = await fetch(backendURL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message: msg })
  });
  const data = await res.json();
  log.innerHTML += `<div class="bot-msg">${data.reply}</div>`;
  log.scrollTop = log.scrollHeight;
}