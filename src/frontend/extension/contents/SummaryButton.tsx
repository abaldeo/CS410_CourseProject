import type { PlasmoCSConfig, PlasmoGetInlineAnchor } from "plasmo"
import cssText from "data-text:../styles.module.css"
import {fetchSummary} from "../utils/summary"
import { useState, useEffect } from "react"

import * as style from "../styles.module.css"

export const config: PlasmoCSConfig = {
    matches: ["https://www.coursera.org/learn*"],
}

export const getInlineAnchor: PlasmoGetInlineAnchor = () =>
    document.querySelectorAll('button[id="save-note-button"]')[0]

export const getShadowHostID = () => "summary-button"

export const getStyle = () => {
    const style = document.createElement("style")
    style.textContent = cssText
    return style
}

const Summary = () => {
    const [videoName, setVideoName] = useState<string>("")
    const [courseName, setCourseName] = useState<string>("")
    const [summaryVisible, setSummaryVisible] = useState<boolean>(false)
    
    
    const handleSubmit = async (e) => {
        e.preventDefault()
        if (summaryVisible == false) {
            const response = await chrome.runtime.sendMessage({from: "summaryButton", cn: courseName, vn: videoName});
            // console.log(response.bullets.summary)
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
    
    return (
        <div>
            <button
                className={style.button}
                value = "Generate Summary"
                onClick={handleSubmit}
                > Generate Summary
            </button>
        </div>
    )
}

export default Summary