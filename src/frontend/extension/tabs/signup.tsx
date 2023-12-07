import { useState, useEffect } from "react"
import React from 'react'
import { Box, TextField, Typography, Button, Container, Grid } from '@mui/material';
import { signUp } from "../utils/auth"

function SignUp() {
  const [email, setEmail] = useState('')
  const [pwd, setPwd] = useState('')
  const [confirmPwd, setConfirmPwd] = useState('')

  function onSuccess() {
    window.close()
  }
  function onFailure() {
    alert("Sign Up Error")
  }


  const handleSubmit = async (e) => {
    e.preventDefault()
    signUp(email, pwd, confirmPwd).then(onSuccess, onFailure)
  }

  return (
    <Container component="main">
      <Box
        sx={{  
          marginTop: 8,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          width: "400px"
        }}
      >
        <Typography component="h1" variant="h5">
          Sign Up
        </Typography>
        <Box component="form" noValidate sx={{ mt: 1 }} onSubmit={handleSubmit}>
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
            value={pwd}
          />
          <TextField
            margin="normal"
            required
            fullWidth
            name="confirm password"
            label="Confirm Password"
            type="password"
            id="confirmpassword"
            autoComplete="current-password"
            onChange={(e) => setConfirmPwd(e.target.value)}
            value={confirmPwd}
          />
          <Button
            type="submit"
            fullWidth
            variant="contained"
            sx={{ mt: 3, mb: 0, borderRadius: 0 }}
          >
            Sign Up
          </Button>
        </Box>
      </Box>
    </Container>
  );
  }
export default SignUp