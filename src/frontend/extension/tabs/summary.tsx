import { useState, useEffect } from "react"
import React from 'react'
import {fetchSummary} from "../../src/utils/summary"

function showSummary() {

    const [videoName, setVideoName] = useState("")
    const [summary, setSummary] = useState("")

    chrome.runtime.onMessage.addListener(
        function(request, sender, sendResponse) {
          console.log(request.url_string);
          if (request.from === "fileView")
            sendResponse("Received")
            console.log("Received")
            console.log(request.videoName)
            setVideoName(request.videoName.split(".")[0])
        }
    );

    fetchSummary("cs410", videoName).then(res => {
        
        setSummary(res.summary)
        console.log(res.summary)
    })
    
    return(
        <div>
            <p dangerouslySetInnerHTML={{__html: summary}}></p>
        </div>
    )
}
export default showSummary