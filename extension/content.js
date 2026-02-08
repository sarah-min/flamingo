document.addEventListener("mouseup", async () => {
  console.log("selection");
  // some of the below is genreated with copilot
  const sel = window.getSelection();

  if (!sel || sel.rangeCount === 0) return;

  const anchorNode = sel.anchorNode;
  const anchorOffset = sel.anchorOffset;

  if (!anchorNode || !anchorNode.textContent) return;
  if (anchorNode.nodeType !== Node.TEXT_NODE) return;

  const text = anchorNode.textContent;

  // last '.' before the selection (search up to offset-1)
  const before = text.lastIndexOf(".", Math.max(0, anchorOffset - 1));
  // first '.' after the selection (search from offset)
  const afterIndex = text.indexOf(".", anchorOffset);
  const after = afterIndex === -1 ? text.length : afterIndex;

  // determine sentence start (skip the dot + whitespace)
  let start = before + 1;
  while (start < anchorOffset && /\s/.test(text[start])) start++;

  const sentence = text.substring(start, after).trim();
  const word = sel.toString().trim();
  console.log("stuff", sentence, word);

  const payload = { word, sentence };

  try {
    if (
      chrome &&
      chrome.runtime &&
      typeof chrome.runtime.sendMessage === "function"
    ) {
      chrome.runtime.sendMessage(
        { action: "sendDOMData", data: payload },
        (response) => {
          const err = chrome.runtime.lastError;
          if (err) console.warn("sendMessage error:", err.message);
        },
      );
    }
  } catch (e) {
    console.warn("sendMessage failed:", e);
  }
});

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === "returnDefinition") {
    console.log("return");
    const el = document.getElementById("test");
    if (el) el.textContent = message.data.word;
  }
});
