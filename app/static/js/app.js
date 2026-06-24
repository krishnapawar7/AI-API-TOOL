const summarizeForm = document.getElementById("summarize-form");
const translateForm = document.getElementById("translate-form");
const emailForm = document.getElementById("email-form");
const themeToggle = document.getElementById("theme-toggle");
const historyList = document.getElementById("history-list");

const summarizeResult = document.getElementById("summarize-result");
const translateResult = document.getElementById("translate-result");
const emailResult = document.getElementById("email-result");

const MAX_HISTORY = 6;

function updateTheme(theme) {
  document.documentElement.classList.toggle("theme-light", theme === "light");
  themeToggle.textContent = theme === "light" ? "Dark" : "Light";
  localStorage.setItem("theme", theme);
}

function loadTheme() {
  const saved = localStorage.getItem("theme") || "dark";
  updateTheme(saved);
}

function addHistory(entry) {
  const item = document.createElement("div");
  item.className = "history-entry";

  item.innerHTML = `
    <div class="history-entry__top">
      <div>
        <div class="history-entry__endpoint">${entry.label}</div>
        <div>${entry.status}</div>
      </div>
      <div>${entry.timestamp}</div>
    </div>
    <pre>${entry.message}</pre>
  `;

  historyList.prepend(item);
  if (historyList.children.length > MAX_HISTORY) {
    historyList.removeChild(historyList.lastChild);
  }
}

function formatPayload(payload) {
  return Object.entries(payload)
    .map(([key, value]) => `${key}: ${value}`)
    .join(" | ");
}

async function submitForm(event, endpoint, fields, outputElement, label) {
  event.preventDefault();

  const payload = fields.reduce((data, field) => {
    const input = event.target.elements[field];
    if (!input) return data;
    const value = input.value?.trim();
    if (value !== undefined) {
      data[field] = value;
    }
    return data;
  }, {});

  if (payload.recipient_name === "") {
    delete payload.recipient_name;
  }

  const payloadText = formatPayload(payload);
  outputElement.querySelector(".output-card__body").textContent = "Loading...";

  try {
    const response = await fetch(endpoint, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    const data = await response.json();
    let message = "";
    let status = response.ok ? "Success" : "Error";

    if (!response.ok) {
      message = data.detail
        ? data.detail.map(item => `${item.loc.join(".")}: ${item.msg}`).join("\n")
        : data.message || JSON.stringify(data, null, 2);
      outputElement.querySelector(".output-card__body").textContent = `Error:\n${message}`;
    } else {
      if (endpoint.includes("summarize")) {
        message = data.summary;
        outputElement.querySelector(".output-card__body").textContent = message;
      } else if (endpoint.includes("translate")) {
        message = data.translated_text;
        outputElement.querySelector(".output-card__body").textContent = message;
      } else if (endpoint.includes("generate-email")) {
        message = `Subject: ${data.subject}\n\n${data.body}`;
        outputElement.querySelector(".output-card__body").textContent = message;
      }
    }

    addHistory({
      label,
      status,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      message: `${payloadText}\n\n${status === 'Success' ? message : 'Error details: ' + message}`,
    });
  } catch (error) {
    const message = error.message || "Unknown error";
    outputElement.querySelector(".output-card__body").textContent = `Request failed: ${message}`;
    addHistory({
      label,
      status: "Error",
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      message: `Request failed: ${message}`,
    });
  }
}

summarizeForm.addEventListener("submit", event =>
  submitForm(event, "/summarize", ["text", "max_words"], summarizeResult, "Summarize")
);

translateForm.addEventListener("submit", event =>
  submitForm(event, "/translate", ["text", "target_language"], translateResult, "Translate")
);

emailForm.addEventListener("submit", event =>
  submitForm(event, "/generate-email", ["purpose", "tone", "recipient_name"], emailResult, "Generate Email")
);

themeToggle.addEventListener("click", () => {
  updateTheme(document.documentElement.classList.contains("theme-light") ? "dark" : "light");
});

loadTheme();
