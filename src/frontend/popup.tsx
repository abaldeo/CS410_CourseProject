import { useState, useEffect } from "react"

function IndexPopup() {
  const [currentUrl, setCurrentUrl] = useState<string>("")
  const getCurrentUrl = async () => {
    const [tab] = await chrome.tabs.query({active: true, currentWindow: true})
    setCurrentUrl(tab.url)
  }

  useEffect(() => {
    getCurrentUrl()
  }, [currentUrl])
  
  if (currentUrl.includes("coursera.org")) {
    return (
      <div
        style={{
          display: "flex",
          flexDirection: "row",
          padding: 16
        }}>
        <h2>
          Welcome to CourseBuddy!
        </h2>
        <a href="https://docs.plasmo.com" target="_blank">
          View Docs
        </a>
      </div>
    )
  }
  else {
    return (
      <div
        style={{
          display: "flex",
          flexDirection: "row",
          padding: 16
        }}>
        <h2>
          This extension only works with Coursera!
        </h2>
        <a href="https://docs.plasmo.com" target="_blank">
          View Docs
        </a>
      </div>
    )
  }
}

export default IndexPopup
