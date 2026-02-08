const selectedWord = window.getSelection();

const anchorNode = selectedWord.anchorNode;
const lengthBefore = selectedWord.anchorOffset;

const text = anchorNode.textContent;

const before = text.substring(0, lengthBefore).lastIndexOf(".");
const after = text.substring(lengthBefore, text.length).indexOf(".");

var sentence = text.substring(before+2, after);

chrome.runtime.sendMessage({
    action: "sendDOMData", 
    data: {
        word: selectedWord.toString(),
        sentence: sentence
    }
});
