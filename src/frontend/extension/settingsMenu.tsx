import { useState, useEffect } from "react"
import * as style from "./styles.module.css"
import { logout } from "../src/utils/auth"


export const SettingsMenu = ({closeSettings}) => {
    return (
        <div
        style={{
          display: "flex",
          flexDirection: "column",
          backgroundColor: "#0288d1"
        }}>
            <button className={style.button} onClick={() => {
                logout()
                window.close()
                }}>Logout
            </button>
        </div>
    )
}