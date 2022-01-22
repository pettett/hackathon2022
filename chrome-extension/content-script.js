const para = document.createElement("div");
para.className = "overlay";
para.id = "InfoOverlay";
para.onclick = "off()";

playerCont = document.getElementById("player-container")
playerCont.appendChild(para);

const heading = document.createElement("h1");
heading.innerText = "Nelson Mandela";
heading.id = "Header";

para.appendChild(heading);

const desc = document.createElement("p");
desc.innerText = "What a dude, so swaggy cool dude";
desc.id = "desc";

para.appendChild(desc);

const facts = document.createElement("p");
facts.innerText = "Fact 1: Died";
facts.id = "Facts";
facts.style= "font-size: medium";

para.appendChild(facts);

const element = document.getElementsByTagName("body")[0];
element.appendChild(para);

player = document.getElementById("movie_player");
time = player.getCurrentTime();

function changeKeyword(textvar){
    document.getElementById("Header").textContent = textvar;
}

function changeDesc(descrip) {
    document.getElementById("desc").textContent = descrip;
}

function changeFacts(facts){
    text = getElementById("Facts").textContent;
    text = "";
    for(let fact = 0; fact < facts.length; fact++){
        text += facts[fact] + "<br>";
    }
}

function off() {
    document.getElementById("InfoOverlay").style.display = "none";
}

chrome.runtime.onMessage.addListener(
    function (request, sender, sendResponse) {
        console.log(sender.tab ?
            "from a content script:" + sender.tab.url :
            "from the extension");
        //changeText(request.text)
        
        time = player.getCurrentTime();
    }
);
