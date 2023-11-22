import { useState, useEffect } from "react"
import React from 'react'

function showSummary() {
    const [currentUrl, setCurrentUrl] = useState<string>("")
    const [videoName, setVideoName] = useState<string>("")
    const [courseName, setCourseName] = useState<string>("")
    
    const getCurrentUrl = async () => {
        const [tab] = await chrome.tabs.query({active: true, currentWindow: true})
        setCurrentUrl(tab.url)
    }
    
    function getCourseName() {
        setCourseName(currentUrl.split('/')[4].replace('-', ''))
    }

    function getVideoName() {
        setVideoName(currentUrl.split('/')[7])
    }

    function handleSuccess() {
        console.log(fetchSummary(courseName, videoName))
    }

    function handleFailure() {
        alert("Failed to fetch summary")
    }
    
    const handleSubmit = async (e) => {
        e.preventDefault()
        fetchSummary(courseName, videoName).then(handleSuccess, handleFailure)
    }
    useEffect(() => {
        getCurrentUrl()
      }, [currentUrl])
    useEffect(() => {
        getCourseName(),
        getVideoName()
      }, [courseName, videoName])
    
    return(
        <div>
            <button>Hi</button>
        </div>
    )
}
export default showSummary