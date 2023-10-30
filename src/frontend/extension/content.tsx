import cssText from "./styles.module.css"
import { useState, useEffect } from "react"
import { ChatBoxPopUp } from "./chatbox"
import type { PlasmoCSConfig } from "plasmo"
import Pic from "./chat-icon.png"



export const config: PlasmoCSConfig = {
    matches: ["https://www.coursera.org/*"]
  }

export const getStyle = () => {
    const style = document.createElement("style")
    style.textContent = cssText
    return style
  }

const CustomButton = () => {
    const [openChatbox, setOpenChatbox] = useState(false)
    
    return (
        <div>
            <button
                style={{
                    backgroundColor: "transparent",
                    border: "none",
                    textAlign: "right"
                }}
                onClick={() => setOpenChatbox(true)}>
                <img 
                    style={{
                        cursor: "pointer",
                        width: "50px",
                        height: "50px"
                    }}
                    src={Pic}
                    alt=""></img>
            </button>
            {openChatbox ? <ChatBoxPopUp closePopup={() => setOpenChatbox(false)}/> : null}
        </div>
    )
}

export default CustomButton
