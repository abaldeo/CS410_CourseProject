import { useState, useEffect } from "react"
import * as style from "./styles.module.css"


export const FileUpload = ({closePopupUpload}) => {
    return (
        <div
        style={{
          display: "flex",
          flexDirection: "column",
          backgroundColor: "#0288d1",
          borderRadius: "5px"
        }}>
            <button className={style.button} onClick={closePopupUpload}>Close</button>
            <form>
                <h1 className={style.h1}>Lecture File Upload</h1>
                <input type="file" multiple={true} className={style.input}/>
                <button className={style.button} type="submit">Submit</button>
            </form>
        </div>
    )
}