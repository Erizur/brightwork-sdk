/**
//@line 15 "$SRCDIR/browser/components/backup/content/archive.js"
*/

const UA = navigator.userAgent;
const isMozBrowser = /Firefox/.test(UA);

document.body.toggleAttribute("is-moz-browser", isMozBrowser);
