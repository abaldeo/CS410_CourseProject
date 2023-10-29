import { useState, useEffect } from "react"
import * as style from "./styles.module.css"
import { ChatBoxPopUp } from "./chatbox"
import { FileUpload } from "./uploadfile"
import Pic from "./settings-icon.png"

function IndexPopup() {
  const [currentUrl, setCurrentUrl] = useState<string>("")
  const [currentUsername, setCurrentUsername] = useState<string>("")
  const [openChatbox, setOpenChatbox] = useState(false)
  const [openUpload, setOpenUpload] = useState(false)

  const getCurrentUrl = async () => {
    const [tab] = await chrome.tabs.query({active: true, currentWindow: true})
    setCurrentUrl(tab.url)
  }

  const getCurrentUsername = async () => {
    chrome.identity.getProfileUserInfo(function(info) {
      setCurrentUsername(info.email.substring(0, info.email.indexOf("@")))
      if (info.email.length == 0) {
        setCurrentUsername("Anon")
      }
    })
  }


  useEffect(() => {
    getCurrentUrl(),
    getCurrentUsername()
  }, [currentUrl, currentUsername])
  
  if (currentUrl.includes("coursera.org")) {
    return (
      <div className={style.div}>
        <button className={style.settingsButton} value="settings">
            <img className={style.settingsIcon} src={Pic} alt=""></img>
        </button>
        <h1 className={style.h1}>
          Welcome to CourseBuddy, {currentUsername}!
        </h1>
        <button
          className={style.button}
          value="Generate Summary">Generate Summary
        </button>
        <button
          className={style.button}
          onClick={() => setOpenChatbox(true)}
          value="Chat Box">Ask a Question
        </button>
        {openChatbox ? <ChatBoxPopUp closePopup={() => setOpenChatbox(false)}/> : null}
        <button
          className={style.button}
          onClick={() => setOpenUpload(true)}
          value="Upload File">Upload File
        </button>
        {openUpload ? <FileUpload closePopupUpload={() => setOpenUpload(false)}/> : null}
      </div>
    )
  }
  else {
    return (
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          padding: 16,
          backgroundColor: "lightgreen",
          width: "250px",
          borderRadius: "5px"
        }}>
        <h2 className={style.h2}>
          This extension only works with Coursera!
        </h2>
      </div>
    )
  }
}

export default IndexPopup

