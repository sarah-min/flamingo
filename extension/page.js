// thank you copilot
document.addEventListener("DOMContentLoaded", () => {
  // keys your extension sets in background.js
  const keys = [
    "word",
    "usage",
    "definition",
    "is_dialect",
    "curr_word",
    "curr_sentence",
  ];

  chrome.storage.local.get(keys, (items) => {
    if (chrome.runtime.lastError) {
      console.warn("storage.get error:", chrome.runtime.lastError);
      return;
    }

    // prefer user-visible keys; fall back to curr_* if present
    const word = items.word || items.curr_word || "";
    const usage = items.usage || "";
    const definition = items.definition || "";

    const setText = (id, txt) => {
      const el = document.getElementById(id);
      if (el) el.textContent = txt;
    };

    setText("word", word);
    setText("usage", usage);
    setText("definition", definition);

    // optional: show dialect flag
    const dialectEl = document.getElementById("is_dialect");
    if (dialectEl) {
      dialectEl.textContent =
        "Cultural vernacular: " + (items.is_dialect ? "Yes" : "No");
      dialectEl.style.color = isDialect ? "red" : "black";
    }
  });
});
