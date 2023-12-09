import {fetchSummary} from "./utils/summary"

export {}

chrome.runtime.onMessage.addListener(
    function(request, sender, sendResponse) {
      if (request.from === "summaryButton") {
        fetchSummary(request.cn, request.vn).then(res => {
            sendResponse({bullets: res})
            console.log(res.summary)
        })
      }
      return true
    }
);
