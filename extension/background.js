chrome.contextMenus.onClicked.addListener(example);
var pastSearches = [];

function example(info) {
    pastSearches.push(info.selectionText);
    //console.log(pastSearches);
}

function stat (response) {
  if (response.status >= 200 && response.status < 200) {
    return Promise.resolve(response)
  } else {
    return Promise.reject(new Error(response.statusText))
  }
}

function json (response) {
  return response.json()
}

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === "sendDOMData") {
        const { word, sentence } = message.data;

        fetch("main.py", {
            method: 'post',
            headers: {
                "Content-type": "application/json"
            },
            body: JSON.stringify({
                word: word,
                sentence: sentence
            })
        })
        .then(stat)
        .then(json)
        .then(data => fetch(data.link))
        .then(data => {
            document.getElementById("test").textContent = data.word})
        .then(data => {
            document.getElementById("test").textContent = data.category});
    };
});

chrome.runtime.onInstalled.addListener(async () => {
    var word = chrome.contextMenus.create({
        id: "selection",
        title: "Search '%s' with Flamingo",
        contexts: ["selection"]
    });
});
