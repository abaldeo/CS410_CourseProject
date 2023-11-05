import cssText from "data-text:../styles.module.css"
import { useState, useEffect } from "react"
import { ChatBox } from "../chatbox"
import type { PlasmoCSConfig, PlasmoGetInlineAnchor, PlasmoGetOverlayAnchor } from "plasmo"
import Pic from "../chat-icon.png"
import createCache from '@emotion/cache'
import { CacheProvider } from '@emotion/react';

// chrome.commands.onCommand.addListener()

const styleElement = document.createElement("style")

const styleCache = createCache({
    key: "plasmo-mui-cache",
    prepend: true,
    container: styleElement
})

export const getStyle = () => styleElement



export const config: PlasmoCSConfig = {
    matches: ["https://www.coursera.org/*"]
}

export const getInlineAnchor: PlasmoGetInlineAnchor = () =>
    // document.querySelectorAll('div[aria-label="Video Player"]')[0]
    document.querySelectorAll('button[id="downloads-dropdown-btn"]')[0]

// export const getStyle = () => {
//     const style = document.createElement("style")
//     style.textContent = cssText
//     return style
// }

const CustomButton = () => {
    const [openChatbox, setOpenChatbox] = useState(false)
    
    return (
        <CacheProvider value={styleCache}>
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
                {openChatbox ? <ChatBox closePopup={() => setOpenChatbox(false)}/> : null}
            </div>
        </CacheProvider>
    )
}

export default CustomButton
