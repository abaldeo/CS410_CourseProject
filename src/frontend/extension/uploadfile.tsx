import React, { useState, type FormEvent, useEffect } from 'react';
import * as style from "./styles.module.css"
import { BACKEND_URL } from '../src/config';

export const FileUpload = ({closePopupUpload}) => {

    const [transcriptText, setTranscriptText] = useState('What is philosophy?');
    const [data, setData] = useState('');
    const [isLoading, setIsLoading] = useState(true);
    const [isSubmit, setIsSubmit] = useState(false);
    const [error, setError] = useState(null);
    const [videoName, setVideoName] = useState<string>("")
    const [courseName, setCourseName] = useState<string>("")

    useEffect(() => { setCourseName(location.href.split('/')[4].replace('-', '')), setVideoName(location.href.split('/')[7]) }, [])

    async function fetchWithAuth(body) {
        try {
          const myHeaders = new Headers();
          const token = localStorage.getItem('token');
          myHeaders.append('Authorization', `Bearer ${token}`);
          myHeaders.append('Content-Type', 'application/json');
    
          const res = await fetch(`${BACKEND_URL}/bot/chat`, {
              method: 'POST',
              headers: myHeaders,
              body: body
            });
          const resData = await res.json();
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
        event.preventDefault();
        const ext = event.target.files[0].name.split('.').pop();
        if (['.pdf', '.ppt', '.pptx'].includes(ext)) {
          const formData = new FormData();
          formData.append("userName", "");
          formData.append("videoName", videoName);
          formData.append("courseName", courseName);
          formData.append("slideFile", event.target.files[0]); 
          fetchWithAuth(formData);
        }
        else {
          const fileReader = new FileReader();
          fileReader.readAsText(event.target.files[0]);
          fileReader.onload = e => {
            const textAsString = fileReader.result;
            setTranscriptText(textAsString);
          };
          fetchWithAuth(JSON.stringify({
              userName: "",
              videoName: videoName,
              courseName: courseName,
              transcriptText: transcriptText
          }));
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
                <input type="file" accept=".txt,.pdf, .ppt, .pptx" multiple={true} className={style.input}/>
                <button className={style.button} type="submit">Submit</button>
            </form>
        </div>
    )
}


