// Bridges the user's popupButton clickEvent and the actual extension workflow
document
	.getElementById(startButtonID)
	.addEventListener(clickEvent, async () => {
		const statusBox = document.getElementById(statusID);
		let [tab] = await chrome.tabs.query({
			active: true,
			currentWindow: true,
		});

		if (tab.url.includes(instagramURL)) {
			// Updates the UI to show the extraction is in progress
			statusBox.innerText = extractingDataLog;
			statusBox.style.color = extractingDataColor;

			// Sends a message to the content script (check_unfollowers.js)
			chrome.tabs.sendMessage(tab.id, { action: startExtEvent });
		} else {
			alert(openInstagramAlert);
		}
	});
