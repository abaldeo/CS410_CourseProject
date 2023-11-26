import {fetchSummary} from "../src/utils/summary"

export {}

chrome.runtime.onMessage.addListener(
    function(request, sender, sendResponse) {
      console.log(request.url_string);
      if (request.cn != "") {
        fetchSummary(request.cn, request.vn).then(res => {
          sendResponse({bullets: res})
        })
      }
    }
);
// const getUrl = async () => {
//   const [tab] = await chrome.tabs.query({active: true, currentWindow: true})
//   const response = await chrome.runtime.sendMessage({url_string: tab.url});
//   console.log(tab.url)
// }
// getUrl()
