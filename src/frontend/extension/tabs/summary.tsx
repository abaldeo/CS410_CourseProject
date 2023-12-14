import { useState, useEffect } from "react"
import React from 'react'
import {fetchSummary} from "../utils/summary"


function showSummary() {

    const [videoName, setVideoName] = useState("")
    const [courseName, setCourseName] = useState("")
    const [summary, setSummary] = useState("<p>Loading...</p>")

    chrome.runtime.onMessage.addListener(
        function(request, sender, sendResponse) {
          console.log(request.url_string);
          if (request.from === "fileView")
            sendResponse("Received")
            console.log("Received")
            console.log(request.videoName)
            console.log(request.courseName)
            setVideoName(request.videoName.split(".")[0])
            setCourseName(request.courseName)

        }
    );

    console.log(courseName)
    console.log(videoName)

    fetchSummary(courseName, videoName).then(res => {
        
        setSummary(res.summary)
        console.log(res)
    })
    
    return(
        <div>
            <p dangerouslySetInnerHTML={{__html: summary}}></p>
        </div>
    )
}
export default showSummary