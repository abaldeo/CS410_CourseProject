import type { PlasmoCSConfig, PlasmoGetInlineAnchor } from "plasmo"
import cssText from "data-text:../styles.module.css"
import {fetchSummary} from "../utils/summary"
import { useState, useEffect } from "react"

import * as style from "../styles.module.css"

export const config: PlasmoCSConfig = {
    matches: ["https://www.coursera.org/learn*"],
}

export const getInlineAnchor: PlasmoGetInlineAnchor = () =>
    // document.querySelectorAll('button[aria-label="Notes, opens notes panel"]')[0]
    document.querySelectorAll('button[id="save-note-button"]')[0]

export const getShadowHostID = () => "summary-button"

export const getStyle = () => {
    const style = document.createElement("style")
    style.textContent = cssText
    return style
}

const Summary = () => {
    const [currentUrl, setCurrentUrl] = useState<string>("")
    const [videoName, setVideoName] = useState<string>("")
    const [courseName, setCourseName] = useState<string>("")
    const [summaryVisible, setSummaryVisible] = useState<boolean>(false)
    
    // chrome.runtime.onMessage.addListener(
    //     function(request, sender, sendResponse) {
    //       console.log(request.url_string);
    //       if (request.url_string != "")
    //         setCurrentUrl(request.url_string);
    //         console.log(currentUrl)
    //         sendResponse("Received")
    //         setCourseName(currentUrl.split('/')[4].replace('-', ''))
    //         setVideoName(currentUrl.split('/')[7])
    //     }
    // );
    // const getCurrentUrl = async () => {
    //     // const [tab] = await chrome.tabs.query({active: true, currentWindow: true})
    //     setCurrentUrl(location.href)
    // }
    
    // function getCourseName() {
    //     console.log(location.href.split('/'))
    //     setCourseName(location.href.split('/')[4].replace('-', ''))
    // }

    // function getVideoName() {
    //     setVideoName(location.href.split('/')[7])
    // }

    // function handleSuccess() {
    //     console.log("hello")
    // }

    // function handleFailure() {
    //     // console.log(fetchSummary(courseName, videoName))
    //     alert("Failed to fetch summary")
    // }
    
    const handleSubmit = async (e) => {
        e.preventDefault()
        // setCurrentUrl(location.href)
        // getCourseName()
        // console.log(location.href)
        // getVideoName()
        // console.log(courseName)
        // console.log(videoName)
        if (summaryVisible == false) {
            const response = await chrome.runtime.sendMessage({from: "summaryButton", cn: courseName, vn: videoName});
            console.log(response.bullets.summary)
            const parser = new DOMParser()
            const bulletPoints = parser.parseFromString(response.bullets.summary, "text/html");
            document.getElementById('video-item-title-and-save-note').appendChild(bulletPoints.documentElement)
            setSummaryVisible(true)
        } else {
            var summaryText = document.getElementById('video-item-title-and-save-note').childNodes[2]
            document.getElementById('video-item-title-and-save-note').removeChild(summaryText)
            setSummaryVisible(false)
        }
    }

    useEffect(() => { setCourseName(location.href.split('/')[4].replace('-', '')), setVideoName(location.href.split('/')[7]) }, [])
    // useEffect(() => {
    //     getCurrentUrl(),
    //     getCourseName(),
    //     getVideoName()
    //   }, [currentUrl, courseName, videoName])
    // useEffect(() => {
    //     getCourseName(),
    //     getVideoName()
    //   }, [courseName, videoName])
    
    return (
        <div>
            <button
                className={style.button}
                value = "Generate Summary"
                // onClick={() => {
                //     (async () => {
                //         const response = await chrome.runtime.sendMessage({greeting: "hello", });
                //         // do something with response here, not outside the function
                //         console.log(response);
                //       })();
                //   }}
                onClick={handleSubmit}
                > Generate Summary
            </button>
        </div>
    )
}

export default Summary