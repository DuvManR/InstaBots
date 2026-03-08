/**
 * Automated Instagram Extractor
 * 1. Extracts Followers
 * 2. Extracts Following
 * 3. Compares lists and saves "Non-Follow-Backs" & "Remove-From-Ok-List"
 */

// Downloads the content extracted about current list and saves it as a TXT file
function downloadFile(content, filename) {
	const blob = new Blob([content], { type: textPlain });
	const url = URL.createObjectURL(blob);
	const a = document.createElement(aElement);
	a.href = url;
	a.download = filename;
	document.body.appendChild(a);
	a.click();
	document.body.removeChild(a);
}

// Handles the closing process of a list after finishing the extraction part
async function closeList() {
	const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
	const closeBtn = document
		.querySelector(closeQuerySelector)
		?.closest(buttonElement);
	if (closeBtn) {
		closeBtn.click();
		await sleep(1000);
	}
}

// Handles the extraction process for a single list (Followers/Following)
async function extractCurrentList(scrollSelector, filename) {
	const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
	const scrollable = document.querySelector(scrollSelector);
	if (!scrollable) return [];

	console.log(`Scrolling and capturing ${filename}...`);
	let allNames = new Set(); // Uses a Set to automatically handle duplicates
	let lastHeight = 0;
	let sameHeightCount = 0;

	// The XPath that extracts the users in list
	const xpath = usersXPATH;

	while (sameHeightCount < 5) {
		// Grabs names currently visible in the DOM
		const result = document.evaluate(
			xpath,
			document,
			null,
			XPathResult.ORDERED_NODE_SNAPSHOT_TYPE,
			null
		);
		for (let i = 0; i < result.snapshotLength; i++) {
			allNames.add(result.snapshotItem(i).innerText.trim());
		}

		// Scrolls down
		scrollable.scrollTop += 1000;
		await sleep(1200); // Gives it time to load new rows

		// Checks if we've reached the absolute end
		let currentHeight = scrollable.scrollHeight;
		if (currentHeight === lastHeight) sameHeightCount++;
		else sameHeightCount = 0;
		lastHeight = currentHeight;

		console.log(`Currently captured: ${allNames.size} users...`);
	}

	const finalNames = [...allNames].filter((n) => n.length > 0);
	downloadFile(finalNames.join("\n"), filename);
	return finalNames;
}

// Compares the gathered lists and generates the final reports
function runExtractionComparison(followers, following) {
	// Ensures the items in the lists are written in the same format
	const lowerFollowing = following.map((u) => u.toLowerCase().trim());
	const lowerFollowers = followers.map((u) => u.toLowerCase().trim());
	const lowerOkList = ok_list.map((u) => u.toLowerCase().trim());

	// Compares lists and checks which users appear in following but not in followers
	console.log(unfollowersLog);
	// Filters out people you follow who don't follow you back
	const notFollowingBack = following.filter(
		(user) =>
			!lowerFollowers.includes(user.toLowerCase().trim()) &&
			!lowerOkList.includes(user.toLowerCase().trim())
	);
	downloadFile(notFollowingBack.join("\n"), notFollowingBackFile);

	// Checks which users should be removed from OK LIST
	console.log(removeFromOkListLog);
	// Filters out people that used to be in OK LIST but should be removed now as they do not appear in following list anymore
	const removeFromOkList = ok_list.filter(
		(user) => !lowerFollowing.includes(user.toLowerCase().trim())
	);
	downloadFile(removeFromOkList.join("\n"), removeFromOkListFile);

	console.log(`Extraction Complete!
    - Followers: ${followers.length}
    - Following: ${following.length}
    - Not Following Back: ${notFollowingBack.length}
    - Remove From OK LIST: ${removeFromOkList.length}`);
}

// Handles the extraction process
async function startExtraction() {
	const editProfileBtn = document.querySelector(editProfileQuerySelector);
	const followersLink = document.querySelector(followersQuerySelector);
	const followingLink = document.querySelector(followingQuerySelector);

	if (!editProfileBtn || !followersLink || !followingLink) {
		alert(notOnProfilePageAlert);
		console.error(notOnProfilePageLog);
		return;
	}
	console.log(onProfilePageLog);

	const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

	// Extracts Followers
	console.log(followersLog);
	document.querySelector(followersQuerySelector).click();
	await sleep(3000);
	const followers = await extractCurrentList(
		scrollBarQuerySelector,
		followersFile
	);
	await closeList();

	// Extracts Following
	console.log(followingLog);
	document.querySelector(followingQuerySelector).click();
	await sleep(3000);
	const following = await extractCurrentList(
		scrollBarQuerySelector,
		followingFile
	);
	await closeList();

	// Run comparison logic
	runExtractionComparison(followers, following);
}

// Initiates the extraction process once the user clicks the popupButton
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
	if (request.action === startExtEvent) {
		startExtraction();
	}
});
