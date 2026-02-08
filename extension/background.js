chrome.contextMenus.onClicked.addListener(example);
var pastSearches = [];
//var LOCALHOST = "http://45.63.77.179:8000";
LOCALHOST = "http://127.0.0.1:8000";
let word = "default";
let sentence = "This is the default sentence";

function example(info) {
  pastSearches.push(info.selectionText);
  //console.log(pastSearches);
}

function stat(response) {
  console.log(response.status);
  if (response.status >= 200 && response.status < 400) {
    return Promise.resolve(response);
  } else {
    return Promise.reject(new Error(response.statusText));
  }
}

function json(response) {
  return response.json();
}

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  console.log("message received");
  if (message && message.action === "sendDOMData") {
    console.log("sendDOMData", message.data.word, message.data.sentence);
    chrome.storage.local.set(
      {
        curr_word: message.data.word,
        curr_sentence: message.data.sentence,
      },
      () => {
        if (chrome.runtime.lastError) {
          console.warn("storage.set error:", chrome.runtime.lastError);
          sendResponse({
            success: false,
            error: chrome.runtime.lastError.message,
          });
        } else {
          console.log("storage updated");
          sendResponse({ success: true });
        }
      },
    );
    // Return true to indicate we'll call sendResponse asynchronously
    return true;
  } else {
    // nothing to handle synchronously
    return false;
  }
});

chrome.runtime.onInstalled.addListener(async () => {
  console.log("onInstalled");
  var word = chrome.contextMenus.create({
    id: "selection",
    title: "Search '%s' with Flamingo",
    contexts: ["selection"],
  });
});

chrome.contextMenus.onClicked.addListener(async (info, tab) => {
  console.log("clicked");
  const stored = await chrome.storage.local.get(["curr_word", "curr_sentence"]);
  const storedWord = stored.curr_word || "";
  const storedSentence = stored.curr_sentence || "";

  console.log(storedWord, storedSentence);

  await fetch(`${LOCALHOST}/search/`, {
    method: "post",
    headers: {
      "Content-type": "application/json",
    },
    body: JSON.stringify({
      word: storedWord,
      sentence: storedSentence,
    }),
  })
    .then(stat)
    .then(json)
    .then((data) => {
      console.log("return");
      console.log(
        data.word,
        data.usage,
        data.definition,
        data.usage.includes("African-American Vernacular"),
      );

      chrome.storage.local.set(
        {
          word: data.word,
          usage: data.usage,
          definition: data.definition,
          is_dialect: data.usage.includes("African-American Vernacular"),
        },
        () => {
          if (chrome.runtime.lastError) {
            console.warn("storage.set error:", chrome.runtime.lastError);
          } else {
            console.log("storage updated");
          }
        },
      );
      chrome.runtime.sendMessage({
        action: "returnDefinition",
        data: data,
      });
    })
    .catch((err) => {
      console.log(err);
    });
});
