chrome.contextMenus.onClicked.addListener(example);
var pastSearches = [];

function example(info) {
    pastSearches.push(info.selectionText);
}


chrome.runtime.onInstalled.addListener(async () => {
    chrome.contextMenus.create({
        id: "selection",
        title: "Search '%s' with Flamingo",
        contexts: ["selection"]
    });
});

console.log(pastSearches);