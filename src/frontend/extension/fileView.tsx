import { useState, useEffect } from "react"
import * as style from "./styles.module.css"
import {fetchTranscriptList} from "../src/utils/fileUploading"
import {List, ListItem} from '@mui/material'


function showlist() {
    let list = []
    fetchTranscriptList().then(res => {
        list = res
    })
  }

export const FileView = ({closeFileView}) => {
    const [list, setList] = useState([])
    fetchTranscriptList().then(res => {
        setList(res)
    })
    for (let i = 0; i < list.length; i++) {
        list[i] = list[i].slice(30);
    }
    const arrayDataItems = list.map((transcript) => <ListItem>{transcript}</ListItem>)
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