import { useState, useEffect } from "react"
import * as style from "./styles.module.css"
import { FileUpload } from "./uploadfile"
import React from 'react'
import ReactDOM from 'react-dom'
import { Box, TextField, Typography, Button, Container, Grid, MenuItem, Menu} from '@mui/material'
import SettingsIcon from '@mui/icons-material/Settings'
import LogoutIcon from '@mui/icons-material/Logout'
import { login, isAuthenticated } from "./utils/auth"
import {logout} from "./utils/auth"
import {fetchSummary} from ".//utils/summary"
import {fetchTranscriptList} from "./utils/fileUploading"
import { FileView} from "./fileView"



function Login() {
  const [email, setEmail] = useState('')
  const [pwd, setPwd] = useState('')

  if (isAuthenticated()) {
    return(
      <IndexPopup/>
    )
  }

  function handleSuccess() {
    window.close()
  }
  function handleFailure() {
    alert("Login Failed")
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    login(email, pwd).then(handleSuccess, handleFailure)
  }

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
      </Box>
    </Container>
  );
}

function IndexPopup() {
  const [currentUrl, setCurrentUrl] = useState<string>("")
  const [openUpload, setOpenUpload] = useState(false)
  const [openFiles, setOpenFiles] = useState(false)
  const [openSettings, setOpenSettings] = useState(false)


  const getCurrentUrl = async () => {
    const [tab] = await chrome.tabs.query({active: true, currentWindow: true})
    setCurrentUrl(tab.url)
  }



  useEffect(() => {
    getCurrentUrl()
  }, [currentUrl])
  
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
          Welcome to CourseBuddy!
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
        <button
          className={style.button}
          onClick={() => {
            openFiles ? setOpenFiles(false) : setOpenFiles(true)
          }}
          value="View Uploaded Files">View Uploaded Files
        </button>
        {openFiles ? <FileView closeFileView={() => setOpenFiles(false)}/> : null}
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

