chrome.contextMenus.onClicked.addListener(example);

/*
"word" => the word
"usage" => the kind of owrd it is 
"definition" => basic definition of the word
"is_dialect" => whether or not the word is part of the dialetc
*/
//var LOCALHOST = "http://45.63.77.179:8000";
LOCALHOST = "http://127.0.0.1:8000";
let word = "default";
let sentence = "This is the default sentence";

function example(info) {
    chrome.storage.local.set({"word": info.word});
    //chrome.storage.lcoal.set({"use": info.usage});
    //chrome.storage.local.set({"def": info.definition});
    //chrome.storage.local.set({"dialect": info.is_dialect});
}

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
