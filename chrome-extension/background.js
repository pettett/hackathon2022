

async function getTabId() {
	let queryOptions = { active: true, currentWindow: true };
	let tab = await chrome.tabs.query(queryOptions);
	console.log(tab[0])
	return tab[0].id;
}

const socket = new WebSocket('ws://localhost:8765');
console.log("Here");
// Connection opened
socket.addEventListener('open', function (event) {
	SendWebSocketMessage('echo', 'Hello Server!');
});

// Listen for messages
socket.addEventListener('message', async function (event) {
	console.log('Message from server ', event.data);
	const tabId = await getTabId();
	chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
		response = JSON.parse(event.data)
		console.log(response)
		console.log(tabs[0].id)
		console.log(response.tabId)
		console.log(parseInt(response.tabId) == tabs[0].id)
		if (parseInt(response.tabId) == tabs[0].id) {
			chrome.tabs.sendMessage(tabs[0].id, JSON.parse(event.data), function (response) {
				console.log(response.text);
			});
		}
	});
});

function SendWebSocketMessage(type, data) {
	socket.send(JSON.stringify({
		"type": type,
		"data": data
	}));
}

function SendNavChange(url) {
	SendWebSocketMessage("navChange", {
		"url": url
	});
}

chrome.runtime.onMessage.addListener(
	function (request, sender, sendResponse) {
		console.log(sender.tab.url)
		console.log("Here")
		SendWebSocketMessage("pollFact", {
			"url": sender.tab.url,
			"timestamp": request.timestamp,
			"tabId": sender.tab.id
		});
	}
);

chrome.tabs.onUpdated.addListener(function
	(tabId, changeInfo, tab) {
	// read changeInfo data and do something with it (like read the url)
	if (changeInfo.url) {
		SendNavChange(changeInfo.url)
	}

}
);

chrome.tabs.onActivated.addListener(function (activeInfo) {
	chrome.tabs.get(tabId = activeInfo.tabId,
		callback = (tab) => {
			console.log(tab)
			SendNavChange(tab.url)
		});
});

