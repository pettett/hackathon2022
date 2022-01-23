const para = document.createElement("div");
para.className = "overlay";
para.id = "InfoOverlay";
para.onclick = "off()";

playerCont = document.getElementById("player-container")
playerCont.appendChild(para);

const heading = document.createElement("h1");
heading.innerText = "Keyword";
heading.id = "Header";

para.appendChild(heading);

const desc = document.createElement("p");
desc.innerText = "";
desc.id = "desc";

para.appendChild(desc);

/*
const facts = document.createElement("p");
facts.innerText = "Fact 1: Died";
facts.id = "Facts";
facts.style = "font-size: medium";
*/

//para.appendChild(facts);

const element = document.getElementsByTagName("body")[0];
element.appendChild(para);

function changeKeyword(textvar) {
    console.log("hewwo")
	document.getElementById("Header").textContent = textvar;
}

function changeDesc(descrip) {
    console.log(descrip)
	document.getElementById("desc").textContent = descrip;
}

/*function changeFacts(facts) {
	text = getElementById("Facts").textContent;
	text = "";
	for (let fact = 0; fact < facts.length; fact++) {
		text += facts[fact] + "<br>";
	}
}*/

function off() {
	document.getElementById("InfoOverlay").style.display = "none";
}

const interval = setInterval(function () {
	let player = document.getElementsByClassName('video-stream')[0];
	let time = player.currentTime;
	chrome.runtime.sendMessage({
		"timestamp": time
	}, function (response) { });
}, 5000);

/*
	  "type": "pollFact",
	  "data": {
	  "url": window.location.href,
	  "timestamp": time
*/

chrome.runtime.onMessage.addListener(
	function (request, sender, sendResponse) {
		console.log(request);
		switch (request.type) {
			case "facts":
                if(request.data != null){
                    request.data = JSON.parse(request.data)
                    changeKeyword(request.data.keyword)
				    changeDesc(request.data.description)
				    //changeFacts(request.data.facts)
                }
				break;
		}
	}
);
