var greeting = "hola, ";
const para = document.createElement("div");
para.className = "overlay"

const text = document.createElement("p");
text.innerText = "bob";
text.id = "InnerText"

para.appendChild(text);

const element = document.getElementsByTagName("body")[0];
element.appendChild(para);

function changeText(text) {
    document.getElementById("InnerText").textContent = text
}

chrome.runtime.onMessage.addListener(
    function (request, sender, sendResponse) {
        console.log(sender.tab ?
            "from a content script:" + sender.tab.url :
            "from the extension");
        changeText(request.text)
    }
);