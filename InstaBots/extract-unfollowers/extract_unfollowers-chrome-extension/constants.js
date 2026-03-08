// HTML Elements
const aElement = "a";
const buttonElement = "button";

// HTML IDs
const startButtonID = "startButton";
const statusID = "status";

// HTML Events
const clickEvent = "click";
const startExtEvent = "START_EXTRACTION";

// CSS
const extractingDataColor = "#bc1888";

// URLs
const instagramURL = "instagram.com";

// Alerts
const openInstagramAlert = "Please open Instagram first!";
const notOnProfilePageAlert =
	"Hold on! You need to be on YOUR profile page for the extension to work.";

// Logs
const notOnProfilePageLog = "Extraction aborted: Not on profile page.";
const onProfilePageLog = "Profile page verified. Starting extraction...";
const extractingDataLog = "Extracting data...";
const followersLog = "Opening Followers...";
const followingLog = "Opening Following...";
const unfollowersLog = "Calculating unfollowers...";
const removeFromOkListLog =
	"Checks which users should be removed from OK LIST...";

// XPATHs
const usersXPATH =
	"//a[@role='link']//span[@dir='auto' and @class='_ap3a _aaco _aacw _aacx _aad7 _aade']";

// Query Selectors
const editProfileQuerySelector = 'header section a[href*="/accounts/edit/"]';
const closeQuerySelector =
	'button.portal-close, button [aria-label="סגור/סגרי"]';
const scrollBarQuerySelector =
	".x6nl9eh.x1a5l9x9.x7vuprf.x1mg3h75.x1lliihq.x1iyjqo2";
const followersQuerySelector = 'a[href*="/followers/"]';
const followingQuerySelector = 'a[href*="/following/"]';

// File Constants
const followersFile = "followers.txt";
const followingFile = "following.txt";
const notFollowingBackFile = "not_following_back.txt";
const removeFromOkListFile = "remove_from_ok_list.txt";
const textPlain = "text/plain"; // File type

// OK LIST
const ok_list = [
	"gmhikaru",
	"magnus_carlsen",
	"redbull",
	"wwwchesscom",
	"olympics",
	"nasa",
	"m_phelps00",
	"yarin_csw",
	"calisthenics.israel",
	"yosephhaddad",
	"yarin_calisthenics",
	"ian.barseagle",
	"ilay_bar__",
	"liavbrodash",
	"hristov_sw",
	"andry_strong",
	"niv_bekerman",
	"germanyasha",
	"tomer_tal.cali",
	"yairdrory",
	"ram_zardav",
	"niv_rabi_",
	"eliya_bonen",
	"chrisheria",
	"itay_barashi_",
	"achya_ben_harush",
	"ohad.the.nomad",
	"snuba_diving_center",
	"med_student_notes",
	"asrag_med",
	"medbarilan",
	"remember_ofek_rousso",
	"remember_liav_aloush",
	"remember_itaymartsiano",
	"remember_netta_epstein",
	"remember_ido_binenshtock",
	"cyberdefense_alumni",
	"drpickle.phd",
	"science",
	"remember_amir_fisher",
];
