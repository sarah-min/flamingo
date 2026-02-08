chrome.contextMenus.onClicked.addListener(example);

/*
"word" => the word
"usage" => the kind of owrd it is 
"definition" => basic definition of the word
"is_dialect" => whether or not the word is part of the dialetc
*/

function example(info) {
    chrome.storage.local.set({"word": info.word});
    //chrome.storage.lcoal.set({"use": info.usage});
    //chrome.storage.local.set({"def": info.definition});
    //chrome.storage.local.set({"dialect": info.is_dialect});
}

chrome.runtime.onInstalled.addListener(async () => {
    var word = chrome.contextMenus.create({
        id: "selection",
        title: "Search '%s' with Flamingo",
        contexts: ["selection"]
    });
});
