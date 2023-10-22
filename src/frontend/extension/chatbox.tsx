import { useState, useEffect } from "react"
import * as style from "./styles.module.css"
import * as style2 from "./chatstyle.module.css"
import Pic from "./send-message.png"

export const ChatBoxPopUp = ({closePopup}) => {
    return (
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            backgroundColor: "lightgreen",
            borderRadius: "5px"
          }}>
          <button className={style.button2} onClick={closePopup}>Close</button>
          <div className={style2.chatbotcontainer}>
            <div className={style2.chatbot}>
                <div className={style2.conversation}>
                    <div className={style2.chatbotmessage}>
                        <p className={style2.chatbottext}>Hi! How are you?</p>
                    </div>
                </div>
                <form className={style2.inputform}>
                    <div className={style2.messagecontainer}>
                        <input className={style2.inputfield} type="text" placeholder="Type your message here"></input>
                        <button className={style2.submitbutton} type="submit">
                            <img className={style2.sendicon} src={Pic} alt=""></img>
                        </button>
                    </div>
                </form>
            </div>
          </div>
        </div>
    )
}