import { useState, useEffect } from "react"
import * as style from "./styles.module.css"
import {fetchTranscriptList} from "./utils/fileUploading"
import {List, ListItem} from '@mui/material'


const sendMessage = async (video) => {
    const response = await chrome.runtime.sendMessage({from: "fileView", courseName: "cs410", videoName: video })
}

export const FileView = ({closeFileView}) => {
    const [list, setList] = useState([])
    fetchTranscriptList().then(res => {
        var cleanArray = []
        for (let i = 0; i < res.length; i++) {
            if (res[i].type == "transcripts") {
                if (res[i].course != "cs410") {
                    console.log(res[i].file)
                    cleanArray.push(res[i].file)
                }
                else {
                    cleanArray.push(res[i].file.split('_')[1])
                }
            }
        }
        setList(cleanArray)
    })
    const arrayDataItems = list.map((transcript) => <ListItem sx={{cursor: "pointer", color: "#FFFFFF"}} onClick={() => {
        setTimeout(() => {
            sendMessage(transcript)
        }, 1000)
        chrome.windows.create({
            url: "./tabs/summary.html",
            type: "popup",
            height: 500,
            width: 500
          })
        sendMessage(transcript)
    }}>{(transcript)}</ListItem>)
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