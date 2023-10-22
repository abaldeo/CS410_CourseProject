import { useState, useEffect } from "react"
import * as style from "./styles.module.css"

export const ChatBoxPopUp = ({closePopup}) => {
    return (
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            padding: 16,
            backgroundColor: "lightgreen",
            borderRadius: "5px"
          }}>
          <button onClick={closePopup}>Close</button>
          <h2 className={style.h2}>
            This extension only works with Coursera!
          </h2>
        </div>
    )
}