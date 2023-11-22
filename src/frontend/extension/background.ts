import {fetchSummary} from "../src/utils/summary"

export {}

chrome.runtime.onMessage.addListener(
    function(request, sender, sendResponse) {
      console.log(request.url_string);
      if (request.cn != "")
        fetchSummary(request.cn, request.vn).then(res => {
          sendResponse({bullets: res})
      })
    }
  );