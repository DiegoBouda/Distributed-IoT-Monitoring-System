const socket = new WebSocket("ws://localhost:8000");

let username;
let currentChannel;

const loginSection = document.getElementById("login-section");
const chatSection = document.getElementById("chat-section");
const loginBtn = document.getElementById("join-btn");
const messages = document.getElementById("messages");
const form = document.getElementById("chat-form");
const input = document.getElementById("msg");
const switchBtn = document.getElementById("switch-btn");

socket.addEventListener("open", () => {
  console.log("Connected to server");
});

socket.addEventListener("message", (event) => {
  const data = JSON.parse(event.data);
  if (data.type === "message") {
    displayMessage(`[${data.channel}] ${data.username}: ${data.text}`);
  }
});

socket.addEventListener("close", () => {
  console.log("Disconnected from server");
});

loginBtn.addEventListener("click", () => {
  username = document.getElementById("username").value.trim() || "Anonymous";
  currentChannel = document.getElementById("channel").value.trim() || "general";

  const initMessage = {
    username: username,
    channel: currentChannel
  };
  socket.send(JSON.stringify(initMessage));

  loginSection.style.display = "none";
  chatSection.style.display = "block";
});

form.addEventListener('submit', (event) => {
  event.preventDefault();
  const msg = input.value.trim();
  if (!msg) return;

  const payload = {
    type: "message",
    text: msg
  };
  socket.send(JSON.stringify(payload));
  input.value = '';
});

switchBtn.addEventListener("click", () => {
  const newChannel = document.getElementById("switch-channel").value.trim();
  if (!newChannel || newChannel === currentChannel) return;

  const payload = {
    type: "switch_channel",
    channel: newChannel,
  };
  socket.send(JSON.stringify(payload));
  console.log(`Switched from ${currentChannel} to ${newChannel}`);
  currentChannel = newChannel;

  messages.innerHTML = '';
});

function displayMessage(message) {
  const div = document.createElement('div');
  div.textContent = message;
  messages.appendChild(div);
  messages.scrollTop = messages.scrollHeight; 
}