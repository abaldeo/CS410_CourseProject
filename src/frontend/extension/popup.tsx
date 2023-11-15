import { useState, useEffect } from "react"
import * as style from "./styles.module.css"
import { FileUpload } from "./uploadfile"
import { SettingsMenu } from "./settingsMenu"
import React from 'react'
// import {ChatBox} from "./tabs/chatbox"
import ReactDOM from 'react-dom'
import Pic from "./settings-icon.png"
import { Box, TextField, Typography, Button, Container, Grid } from '@mui/material'
import { login, isAuthenticated } from "../src/utils/auth"

// const [isLoggedIn, setIsLoggedIn] = useState(false)

function Login() {
  // const [isLoggedIn, setIsLoggedIn] = useState(false)
  const [email, setEmail] = useState('')
  const [pwd, setPwd] = useState('')

  if (isAuthenticated()) {
    return(
      <IndexPopup/>
    )
  }

  function handleSuccess() {
    console.log(isAuthenticated())
    window.close()
  }
  function handleFailure() {
    console.log(isAuthenticated())
    alert("Login Failed")
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    login(email, pwd).then(handleSuccess, handleFailure)
    // console.log(isAuthenticated())
  }

  // if (isLoggedIn) {
  //   return(
  //     <IndexPopup/>
  //   )
  // }
  return (
    <Container component="main">
      <Box
        sx={{  
          marginTop: 8,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          width: "300px"
        }}
      >
        <Typography component="h1" variant="h5">
          Sign in
        </Typography>
        <Box component="form" onSubmit={handleSubmit} noValidate sx={{ mt: 1 }}>
          <TextField
            margin="normal"
            required
            fullWidth
            id="email"
            label="Email Address"
            name="email"
            autoComplete="email"
            autoFocus
            onChange={(e) => setEmail(e.target.value)}
            value = {email}
          />
          <TextField
            margin="normal"
            required
            fullWidth
            name="password"
            label="Password"
            type="password"
            id="password"
            autoComplete="current-password"
            onChange={(e) => setPwd(e.target.value)}
            value = {pwd}
          />
          <Button
            type="submit"
            fullWidth
            variant="contained"
            sx={{ mt: 3, mb: 0, borderRadius: 0 }}
          >
            Sign In
          </Button>
          <Button
            fullWidth
            variant="contained"
            sx={{ mt: 0, mb: 2, borderRadius: 0 }}
            onClick={() => {
              chrome.windows.create({
                url: "./tabs/signup.html",
                type: "popup",
                height: 500,
                width: 500
              })
            }}
          >
            Sign Up
          </Button>
        </Box>
        {/* {isLoggedIn && <IndexPopup/>} */}
      </Box>
    </Container>
  );
}

function IndexPopup() {
  const [currentUrl, setCurrentUrl] = useState<string>("")
  const [currentUsername, setCurrentUsername] = useState<string>("")
  const [openChatbox, setOpenChatbox] = useState(false)
  const [openUpload, setOpenUpload] = useState(false)
  const [openSettings, setOpenSettings] = useState(false)

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
        <button className={style.settingsButton} value="settings" onClick={() => openSettings ? setOpenSettings(false) : setOpenSettings(true)}>
            <img className={style.settingsIcon} src={Pic} alt=""></img>
        </button>
        {openSettings ? <SettingsMenu closeSettings={() => setOpenSettings(false)}/> : null}
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
          onClick={() => {
            chrome.windows.create({
              url: "./tabs/chatbox.html",
              type: "popup",
              height: 500,
              width: 500
            })
          }}
          value="Chat Box">Ask a Question
        </button>
        {/* {openChatbox ? <ChatBox closePopup={() => setOpenChatbox(false)}/> : null} */}
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


export default Login

