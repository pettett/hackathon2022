const para = document.createElement("div");
para.className = "overlay";
para.id = "InfoOverlay";
para.onclick = "off()";

//playerCont = document.getElementById("player-container")
//playerCont.appendChild(para);

const heading = document.createElement("h1");
heading.id = "Header";

const headinglink = document.createElement("a");
headinglink.id = "HeadingLink"
headinglink.innerText = "Keyword";
heading.appendChild(headinglink)

para.appendChild(heading);

const desc = document.createElement("p");
desc.innerText = "";
desc.id = "myDesc";



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

function changeKeyword(textvar, link) {
	console.log("hewwo")
	const HeadingLinkEl = document.getElementById("HeadingLink");
	HeadingLinkEl.textContent = textvar;
	console.log(link)
	HeadingLinkEl.href = link
}

function changeDesc(descrip) {
	console.log(descrip)
	if (descrip == null) {
		return
	}
	document.getElementById("myDesc").textContent = descrip;
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
		switch (request.type) {
			case "facts": 
				if (request.data != null) {
					console.log(request);
					request.data = JSON.parse(request.data);
					changeKeyword(request.data.keyword, request.data.link);
					changeDesc(request.data.description);
					
					//changeFacts(request.data.facts)
				}
				break;
		}
	}
);
