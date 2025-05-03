// Global variables
let eventSource = null;
let isGenerating = false;


// DOM Content Loaded
document.addEventListener("DOMContentLoaded", () => {
    setupEventListeners();
});

// Initialize all event listeners
function setupEventListeners() {
    document.getElementById("question").addEventListener("keydown", handleKeyDown);
    document.querySelector(".chat-input .action-button").addEventListener("click", handleActionButton);
    document.getElementById("scroll-to-bottom").addEventListener("click", scrollToBottom);
    
    // Observe chat messages for scroll events
    const chatMessages = document.querySelector(".chat-messages");
    chatMessages.addEventListener("scroll", handleChatScroll);
}

// Update the appendMessage function
function appendMessage(sender, text) {
    const wrapper = document.querySelector(".messages-wrapper") || createMessagesWrapper();
    const messageDiv = document.createElement("div");
    messageDiv.className = `message ${sender}`;
    messageDiv.innerHTML = `<div class="bubble">${text}</div>`;
    wrapper.appendChild(messageDiv);
}

// Create messages wrapper if it doesn't exist
function createMessagesWrapper() {
    const responseDiv = document.getElementById("response");
    const wrapper = document.createElement("div");
    wrapper.className = "messages-wrapper";
    responseDiv.appendChild(wrapper);
    return wrapper;
}

// Handle sending messages
async function sendMessage() {
    const questionInput = document.getElementById("question");
    const question = questionInput.value.trim();
    const wrapper  = document.querySelector(".messages-wrapper");
  
      // 1.1 Append a single user bubble
      wrapper.appendChild(createBubble(
        "user",
        `Files: ${selectedFiles[0].name}, ${selectedFiles[1].name}`
      ));
  
      // 1.2 Append one “Comparing…” bot bubble
      const botDiv = createBubble("bot", "Comparing files…");
      wrapper.appendChild(botDiv);
      scrollToBottom();
  
      // 1.3 POST the two files
      const fd = new FormData();
      fd.append("file1", selectedFiles[0]);
      fd.append("file2", selectedFiles[1]);
  
      try {
        const res  = await fetch("/compare", { method: "POST", body: fd });
        isGenerating = true;
        updateActionButton();
        const json = await res.json();
        const pct  = (json.similarity * 100).toFixed(2);
  
        // 1.4 Overwrite that same bubble with the result
        botDiv.querySelector(".bubble").innerText =
          `File similarity: ${pct}%`;
        isGenerating = false;
        updateActionButton();
      } catch (err) {
        console.error(err);
        botDiv.querySelector(".bubble").innerText =
          "Error comparing files.";
      }
  
      // 1.5 Clear out the file‑chips & array
      selectedFiles = [];
      document.querySelector(".file-list").innerHTML = "";
  
}
  
  // Simple helper to build a message div + bubble
  function createBubble(role, text) {
    const m = document.createElement("div");
    m.className = `message ${role}`;
    m.innerHTML = `<div class="bubble">${text}</div>`;
    return m;
  }
  

// UI Helper Functions
function toggleSidebar() {
    const container = document.querySelector('.container');
    container.classList.toggle('sidebar-open');
    container.classList.toggle('sidebar-closed');
    
    // Force a reflow to ensure smooth animation
    void container.offsetWidth;
}

function updateActionButton() {
    const button = document.querySelector(".chat-input .action-button");
    const input = document.querySelector(".chat-input textarea");
    if (isGenerating) {
        // When generating, show a white square inside the blue circle.
        input.disabled = true;
        button.innerHTML = `
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" 
                 xmlns="http://www.w3.org/2000/svg">
                <rect x="5" y="5" width="13" height="13" fill="white"/>
            </svg>
        `;
        button.style.backgroundColor = "#3b82f6";
    } else {
        // When not generating, show a white upward arrow inside the blue circle.
        input.disabled = false;
        button.innerHTML = `
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" 
                 xmlns="http://www.w3.org/2000/svg">
                <line x1="12" y1="19" x2="12" y2="5" stroke="white" stroke-width="2" stroke-linecap="round"/>
                <polyline points="5 12 12 5 19 12" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
        `;
        button.style.backgroundColor = "#3b82f6";
    }
}

function handleActionButton() {
    isGenerating ? stopGeneration() : sendMessage();
}

function stopGeneration() {
    isGenerating = false;
    updateActionButton();
}

function handleKeyDown(e) {
    if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
}

function scrollToBottom() {
    const chatMessages = document.querySelector(".chat-messages");
    chatMessages.scrollTo({
        top: chatMessages.scrollHeight,
        behavior: "smooth"
    });
}

function isAtBottom() {
    const chatMessages = document.querySelector(".chat-messages");
    return chatMessages.scrollTop + chatMessages.clientHeight >= chatMessages.scrollHeight - 100;
}

function handleChatScroll() {
    const scrollButton = document.getElementById("scroll-to-bottom");
    scrollButton.style.display = isAtBottom() ? "none" : "block";
}


// File–upload preview logic
const fileInput    = document.getElementById("file-input");
const uploadBtn    = document.getElementById("upload-btn");
const fileListDiv  = document.querySelector(".chat-input .file-list");
let selectedFiles  = [];

// 1️⃣ When 📎 is clicked, open the file picker
uploadBtn.addEventListener("click", () => {
  fileInput.click();
});

// 2️⃣ When a file is chosen, show it as a "chip"
fileInput.addEventListener("change", (e) => {
  const file = e.target.files[0];
  if (!file) return;

  // Keep track
  selectedFiles.push(file);

  // Build chip
  const chip = document.createElement("div");
  chip.className = "file-chip";
  chip.textContent = file.name;

  // remove × button
  const removeBtn = document.createElement("span");
  removeBtn.className = "remove-file";
  removeBtn.textContent = "×";
  removeBtn.onclick = () => {
    selectedFiles = selectedFiles.filter(f => f !== file);
    chip.remove();
  };
  chip.appendChild(removeBtn);

  fileListDiv.appendChild(chip);
  fileInput.value = "";  // reset so same file can be re-picked
});

