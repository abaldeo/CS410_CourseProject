import { useState, useEffect } from "react"
import * as style from "./styles.module.css"
import { FileUpload } from "./uploadfile"
import React from 'react'
import {ChatBox} from "./chatbox"
import ReactDOM from 'react-dom'
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
  
  if (currentUrl.includes("coursera.org/learn")) {
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
          onClick={() => openUpload ? setOpenUpload(false) : setOpenUpload(true)}
          value="Upload File">Upload File
        </button>
        {openUpload ? <FileUpload closePopupUpload={() => setOpenUpload(false)}/> : null}
        <button
          className={style.button}
          onClick={() => openChatbox ? setOpenChatbox(false) : setOpenChatbox(true)}
          value="Chat Box">Ask a Question
        </button>
        {openChatbox ? <ChatBox closePopup={() => setOpenChatbox(false)}/> : null}
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
          backgroundColor: "#36454F",
          width: "250px",
          borderRadius: "5px"
        }}>
        <h2 className={style.h2}>
          Please navigate to Coursera to use this extension.
        </h2>
      </div>
    )
  }
}

export default IndexPopup

