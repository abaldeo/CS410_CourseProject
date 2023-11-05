import type { PlasmoCSConfig, PlasmoGetInlineAnchor } from "plasmo"
import cssText from "data-text:../styles.module.css"

import * as style from "../styles.module.css"

export const config: PlasmoCSConfig = {
    matches: ["https://www.coursera.org/learn*"],
}

export const getInlineAnchor: PlasmoGetInlineAnchor = () =>
    document.querySelectorAll('div[aria-label="Video Player"]')[0]

export const getShadowHostID = () => "summary-button"

export const getStyle = () => {
    const style = document.createElement("style")
    style.textContent = cssText
    return style
}

const Summary = () => {
    return (
        <div>
            <button
                className={style.button}
                value = "Generate Summary"> Generate Summary
            </button>
        </div>
    )
}

export default Summary