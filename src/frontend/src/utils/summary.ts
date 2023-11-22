import {jwtDecode} from 'jwt-decode';

export const fetchSummary = async (course_Name: string, video_Name: string) => {
    if (!(course_Name.length > 0) || !(video_Name.length > 0)) {
        throw new Error('Course name or video name was not provided');
    }
    const request = new Request('https://sturdy-zebra-pw79rpqq4g936jp4-8000.app.github.dev/api/v1/summarization/fetchSummary?courseName=' + course_Name + '&videoName=' + video_Name + '.en.txt', {
        method: 'GET'
      });
    const response = await fetch(request);
    if (response.status === 500) {
        throw new Error('Internal server error');
    }
    const data = await response.json();
    console.log(data)
    return data;
}