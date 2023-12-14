import { useState, useEffect } from "react"
import * as style from "./styles.module.css"
import {fetchTranscriptList} from "./utils/fileUploading"
import {List, ListItem} from '@mui/material'


const sendMessage = async (video, course) => {
    const response = await chrome.runtime.sendMessage({from: "fileView", courseName: course, videoName: video })
}

export const FileView = ({closeFileView}) => {
    const [list, setList] = useState([])
    fetchTranscriptList().then(res => {
        var cleanArray = []
        for (let i = 0; i < res.length; i++) {
            if (res[i].type == "transcripts") {
                if (res[i].course != "cs410") {
                    console.log("Success")
                    console.log(res[i])
                    cleanArray.push(res[i])
                }
                else {
                    // cleanArray.push(res[i].file.split('_')[1])
                    if (res[i].file.includes('_')) {
                        res[i].file = res[i].file.split('_')[1]
                        cleanArray.push(res[i])

                    }
                    else {
                        cleanArray.push(res[i])
                    }
                    // cleanArray.push(res[i])
                }
            }
        }
        setList(cleanArray.sort())
        console.log(res.sort())
    })
    const arrayDataItems = list.map((transcript) => <ListItem sx={{cursor: "pointer", color: "#FFFFFF"}} onClick={() => {
        setTimeout(() => {
            sendMessage(transcript.file, transcript.course)
        }, 1000)
        chrome.windows.create({
            url: "./tabs/summary.html",
            type: "popup",
            height: 500,
            width: 500
          })
        sendMessage(transcript.file, transcript.course)
    }}>{(transcript.file)}</ListItem>)
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