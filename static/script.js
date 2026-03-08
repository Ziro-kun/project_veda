/**
 * Project Veda – Frontend Script
 * Handles: drag-and-drop upload, preview, fetch /analyze, markdown render
 */

const dropZone = document.getElementById("drop-zone");
const fileInput = document.getElementById("file-input");
const previewCont = document.getElementById("preview-container");
const previewImg = document.getElementById("preview-image");
const analyzeBtn = document.getElementById("analyze-btn");
const idleState = document.getElementById("idle-state");
const loadingState = document.getElementById("loading-state");
const resultContent = document.getElementById("result-content");
const errorState = document.getElementById("error-state");
const errorMsg = document.getElementById("error-message");
const resultStatus = document.getElementById("result-status");

let selectedFile = null;

/* ── Drop Zone ─────────────────────────────────────── */
dropZone.addEventListener("click", () => fileInput.click());
dropZone.addEventListener("keydown", (e) => {
  if (e.key === "Enter" || e.key === " ") fileInput.click();
});

dropZone.addEventListener("dragover", (e) => {
  e.preventDefault();
  dropZone.classList.add("drag-over");
});
dropZone.addEventListener("dragleave", () =>
  dropZone.classList.remove("drag-over"),
);
dropZone.addEventListener("drop", (e) => {
  e.preventDefault();
  dropZone.classList.remove("drag-over");
  const file = e.dataTransfer.files[0];
  if (file) handleFile(file);
});

fileInput.addEventListener("change", () => {
  if (fileInput.files[0]) handleFile(fileInput.files[0]);
});

/* ── File Handler ──────────────────────────────────── */
function handleFile(file) {
  if (!file.type.match(/^image\/(jpeg|png|jpg)$/)) {
    showError("JPG, PNG, JPEG 형식의 이미지만 업로드 가능합니다.");
    return;
  }

  selectedFile = file;

  const reader = new FileReader();
  reader.onload = (e) => {
    previewImg.src = e.target.result;
    // Show preview, hide drop zone
    dropZone.classList.add("hidden");
    previewCont.classList.remove("hidden");
    analyzeBtn.classList.remove("hidden");
    // Reset result area
    resetResults();
  };
  reader.readAsDataURL(file);
}

/* ── Analyze ───────────────────────────────────────── */
analyzeBtn.addEventListener("click", async () => {
  if (!selectedFile) return;

  setLoading(true);

  const formData = new FormData();
  formData.append("image", selectedFile);

  try {
    const res = await fetch("/analyze", {
      method: "POST",
      body: formData,
    });

    const data = await res.json();

    if (!res.ok || data.error) {
      showError(data.error || `서버 오류 (${res.status})`);
    } else {
      showResult(data.result);
    }
  } catch (err) {
    showError(`네트워크 오류가 발생했습니다: ${err.message}`);
  } finally {
    setLoading(false);
  }
});

/* ── State Helpers ─────────────────────────────────── */
function setLoading(isLoading) {
  analyzeBtn.disabled = isLoading;
  if (isLoading) {
    idleState.classList.add("hidden");
    loadingState.classList.remove("hidden");
    resultContent.classList.add("hidden");
    errorState.classList.add("hidden");
    resultStatus.textContent = "LINKING...";
    resultStatus.className = "result-status active";
  } else {
    loadingState.classList.add("hidden");
  }
}

function showResult(markdown) {
  resultContent.innerHTML = renderMarkdown(markdown);
  resultContent.classList.remove("hidden");
  idleState.classList.add("hidden");
  errorState.classList.add("hidden");
  resultStatus.textContent = "DATA RECEIVED";
  resultStatus.className = "result-status done";
}

function showError(message) {
  errorMsg.textContent = message;
  errorState.classList.remove("hidden");
  idleState.classList.add("hidden");
  resultContent.classList.add("hidden");
  resultStatus.textContent = "ERROR";
  resultStatus.className = "result-status";
}

function resetResults() {
  idleState.classList.remove("hidden");
  loadingState.classList.add("hidden");
  resultContent.classList.add("hidden");
  errorState.classList.add("hidden");
  resultStatus.textContent = "STANDBY";
  resultStatus.className = "result-status";
}

/* ── Lightweight Markdown Renderer ────────────────── */
function renderMarkdown(text) {
  return (
    text
      // h3 → <h3>
      .replace(/^### (.+)$/gm, "<h3>$1</h3>")
      // h2 → <h2>
      .replace(/^## (.+)$/gm, "<h3>$1</h3>")
      // h1 → <h3>
      .replace(/^# (.+)$/gm, "<h3>$1</h3>")
      // bold
      .replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>")
      // italic
      .replace(/\*(.+?)\*/g, "<em>$1</em>")
      // unordered list items
      .replace(/^- (.+)$/gm, "<li>$1</li>")
      // wrap consecutive <li> in <ul>
      .replace(/(<li>.*<\/li>\n?)+/g, (m) => `<ul>${m}</ul>`)
      // line breaks (non-heading, non-list)
      .replace(/\n(?!<)/g, "<br />")
      // remove extra <br> after block elements
      .replace(/(<\/(h[1-6]|ul|li)>)\s*<br \/>/g, "$1")
  );
}
