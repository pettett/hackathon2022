

async function getTabId(){
    let queryOptions = { active: true, currentWindow: true };
    let tab = await chrome.tabs.query(queryOptions);
    console.log(tab[0]);
    console.log(tab[0])
    return tab[0].id;
}

const socket = new WebSocket('ws://localhost:8765');
console.log("Here");
// Connection opened
socket.addEventListener('open', function (event) {
    socket.send('Hello Server!');
});

// Listen for messages
socket.addEventListener('message', async function (event) {
    console.log('Message from server ', event.data);
    const tabId = await getTabId();
    console.log(tabId)
    // chrome.scripting.executeScript({
    //     target: { tabId: tabId },
    //     function: () => reddenPage(event.data)
    // });
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
        chrome.tabs.sendMessage(tabs[0].id, {text: event.data}, function(response) {
          console.log(response.farewell);
        });
      });
});