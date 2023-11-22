import { useState, useEffect } from "react"
import * as style from "./styles.module.css"
import { FileUpload } from "./uploadfile"
import React from 'react'
// import {ChatBox} from "./tabs/chatbox"
import ReactDOM from 'react-dom'
import { Box, TextField, Typography, Button, Container, Grid, MenuItem, Menu} from '@mui/material'
import SettingsIcon from '@mui/icons-material/Settings'
import LogoutIcon from '@mui/icons-material/Logout'
import { login, isAuthenticated } from "../src/utils/auth"
import {logout} from "../src/utils/auth"
import {fetchSummary} from "../src/utils/summary"

// const [isLoggedIn, setIsLoggedIn] = useState(false)
// chrome.runtime.onMessage.addListener(
//   function(request, sender, sendResponse) {
//     console.log(sender.tab ?
//                 "from a content script:" + sender.tab.url :
//                 "from the extension");
//     if (request.greeting === "hello")
//       chrome.windows.create({
//         url: "./tabs/summary.html",
//         type: "popup",
//         height: 500,
//         width: 500
//       })
//   }
// );

// const getBullets = async (course, video) => {
//   await fetchSummary(course, video).then(res => {
//     return res
//   })
// }

// let summaryString = ""
// chrome.runtime.onMessage.addListener(
//   function(request, sender, sendResponse) {
//     console.log(request.url_string);
//     if (request.cn != "")
//       fetchSummary(request.cn, request.vn).then(res => {
//         sendResponse({bullets: res})
//     })
//   }
// );


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
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          width: "300px" 
        }}
      >
        <Typography component="h1" variant="h5">
          CourseBuddy
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
            sx={{ mt: 3, mb: 0, borderRadius: 0, borderBottom: 1 }}
          >
            Sign In
          </Button>
          <Button
            fullWidth
            variant="contained"
            sx={{ mt: 0, mb: 2, borderRadius: 0, borderTop: 1 }}
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
    const response = await chrome.tabs.sendMessage(tab.id, {url_string: tab.url});
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
    console.log(currentUrl.split('/')[4].replace('-', ''))
    return (
      <div className={style.div}>
        <Box sx={{display: "flex", justifyContent: "space-between"}}>
          <Button onClick={() => {
            logout()
            window.close()
          }}>
            <LogoutIcon/>
          </Button>
          <Button>
            <SettingsIcon/>
          </Button>
        </Box>
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

