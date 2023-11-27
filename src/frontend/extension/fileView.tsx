import { useState, useEffect } from "react"
import * as style from "./styles.module.css"
import {fetchTranscriptList} from "../src/utils/fileUploading"
import {List, ListItem} from '@mui/material'


const sendMessage = async (video) => {
    const response = await chrome.runtime.sendMessage({from: "fileView", courseName: "cs410", videoName: video })
}

export const FileView = ({closeFileView}) => {
    const [list, setList] = useState([])
    fetchTranscriptList().then(res => {
        setList(res)
    })
    // for (let i = 0; i < list.length; i++) {
    //     list[i] = list[i].slice(30);
    // }
    const arrayDataItems = list.map((transcript) => <ListItem sx={{cursor: "pointer"}} onClick={() => {
        setTimeout(() => {
            sendMessage(transcript.slice(33))
        }, 1000)
        chrome.windows.create({
            url: "./tabs/summary.html",
            type: "popup",
            height: 500,
            width: 500
          })
        sendMessage(transcript.slice(33))
    }}>{transcript.slice(30)}</ListItem>)
    return (
        <div
        style={{
          display: "flex",
          flexDirection: "column",
          backgroundColor: "#0288d1"
        }}>
            <List>{arrayDataItems}</List>
            
        </div>
    )
}