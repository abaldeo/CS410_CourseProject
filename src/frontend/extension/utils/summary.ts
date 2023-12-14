
import {BACKEND_URL} from './index'

export const fetchSummary = async (course_Name: string, video_Name: string) => {
    if (!(course_Name.length > 0) || !(video_Name.length > 0)) {
        throw new Error('Course name or video name was not provided');
    }
    const request = new Request(BACKEND_URL + 'summarization/fetchSummary?courseName=' + course_Name + '&videoName=' + video_Name + '.en.txt', {
        method: 'GET'
      });
    const response = await fetch(request);
    if (response.status === 500) {
        throw new Error('Internal server error');
    }
    const data = await response.json();
    console.log(data)
    if (data.msg != "Not Found") {
        console.log("Fetch")
        return data
    }
    else {
        console.log("Generate")
        const formData = new FormData();
        // formData.append('userId', 0)
        formData.append('courseName', course_Name)
        formData.append('videoName', video_Name + '.en.txt')
        formData.append('s3_path', 's3://coursebuddy/' + course_Name + '/transcripts/' + video_Name + '.en.txt')
        for (let pair of formData.entries()) {
            console.log(pair[0]+ ', ' + pair[1]);
        }
        console.log(course_Name)
        console.log(video_Name)
        const request = new Request(BACKEND_URL + 'summarization/generateSummary', {
            method: 'POST',
            body: formData,
          });
        const response = await fetch(request);
        if (response.status === 500) {
            throw new Error('Internal server error');
        }
        const data = await response.json();
        console.log(data)
        return data;
    }
}

// export const generateSummary = async (course_Name: string, video_Name: string) => {
//     if (!(course_Name.length > 0) || !(video_Name.length > 0)) {
//         throw new Error('Course name or video name was not provided');
//     }
//     const formData = new FormData();
//     formData.append('userId', '0')
//     formData.append('courseName', course_Name)
//     formData.append('videoName', video_Name)
//     formData.append('s3_path', 's3://coursebuddy/' + course_Name + '/transcripts/' + video_Name + '.txt')
//     const request = new Request(BACKEND_URL + 'summarization/generateSummary', {
//         method: 'POST',
//         body: formData,
//       });
//     const response = await fetch(request);
//     if (response.status === 500) {
//         throw new Error('Internal server error');
//     }
//     const data = await response.json();
//     console.log(data)
//     return data;
// }