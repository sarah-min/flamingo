const word = chrome.storage.local.set("word");
/*const usage = chrome.storage.lcoal.set("use");
const definition = chrome.storage.local.set("def");
const is_dialect = chrome.storage.local.set("dialect");*/

document.addEventListener('DOMContentLoaded', () => {
    /*
    if(is_dialect) {

    } else {

    }
    */

    const container = document.querySelector('.current-word');

    const conWord = document.createElement('h1');
    conWord.textContent = "word";
    conWord.className = 'word';
    container.appendChild(conWord);

    /*const conUse = document.createElement('p');
    conUse.textContent = usage;
    conUse.className = 'usage';
    container.appendChild(conUse);

    const conDef = document.createElement('p');
    conDef.textContent = definition;
    conDef.className = 'def';
    container.appendChild(conDef);*/
});