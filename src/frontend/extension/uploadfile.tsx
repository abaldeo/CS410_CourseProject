import React, { useState, type FormEvent, useEffect } from 'react';
import * as style from "./styles.module.css"
import { BACKEND_URL } from '../src/config';

export const FileUpload = ({closePopupUpload}) => {

    const [transcriptText, setTranscriptText] = useState('What is philosophy?');
    const [data, setData] = useState('');
    const [isLoading, setIsLoading] = useState(true);
    const [isSubmit, setIsSubmit] = useState(false);
    const [error, setError] = useState(null);
    const [currentUrl, setCurrentUrl] = useState(null);
    const [userName, setUserName] = useState<string>("")
    const [videoName, setVideoName] = useState<string>("")
    const [courseName, setCourseName] = useState<string>("")


    const getCurrentUrl = async () => {
      const [tab] = await chrome.tabs.query({active: true, currentWindow: true})
      setCurrentUrl(tab.url)
    }

    async function fetchWithAuth(body: string | FormData, endpt: string, headerType: string) {
        try {
          const myHeaders = new Headers();
          const token = localStorage.getItem('token');
          myHeaders.append('Authorization', `Bearer ${token}`);
          if (headerType) {
            myHeaders.append('Content-Type', `${headerType}`);
          }
          myHeaders.append('accept', 'application/json');
          myHeaders.append("Access-Control-Allow-Origin", "*");
          const fullUrl = `${BACKEND_URL}file_upload/${endpt}`
          const res = await fetch(fullUrl, {
              method: 'POST',
              headers: myHeaders,
              body: body
            });
          const resData = await res.json();
          console.log(resData)
          setData(resData.message);
        } catch (err: any) {
          setError(err.message);
        } finally {
          setIsLoading(false);
        }
      };
    
    const handleSubmit = (event) => {
        setData('');
        setIsSubmit(true);
        setIsLoading(true);
        setUserName("");
        event.preventDefault();
        getCurrentUrl();
        if (currentUrl) {
          setCourseName(currentUrl.split('/')[4].replace('-', ''))
          setVideoName(currentUrl.split('/')[7])
        }
        else {
          setCourseName("cs410")
          setVideoName("")
        }

        const ext = event.target.fileInput.files[0].name.split('.').pop();
        if (['pdf', 'ppt', 'pptx'].includes(ext)) {
          const formData = new FormData();
          formData.append("slideFile", event.target.fileInput.files[0], event.target.fileInput.files[0].name); 
          fetchWithAuth(formData, `uploadSlide?courseName=cs410&videoName=${videoName}&userName=${userName}`, "");
        }
        else {
          const fileReader = new FileReader();
          fileReader.readAsText(event.target.fileInput.files[0]);
          fileReader.onload = e => {
            const textAsString = fileReader.result;
            setTranscriptText(textAsString);
          };
          fetchWithAuth(JSON.stringify({
              userName: "",
              videoName: videoName,
              courseName: courseName,
              transcriptText: transcriptText
          }), "uploadTranscript", "application/json");
          
        }
        
    };
    
    return (
        <div
        style={{
          display: "flex",
          flexDirection: "column",
          backgroundColor: "#0288d1"
        }}>
            <form onSubmit={handleSubmit}>
                <h1 className={style.h1}>Lecture File Upload</h1>
                <input name="fileInput" type="file" accept=".txt,.pdf, .ppt, .pptx" multiple={true} className={style.input}/>
                <button className={style.button} type="submit">Submit</button>
            </form>
        </div>
    )
}


