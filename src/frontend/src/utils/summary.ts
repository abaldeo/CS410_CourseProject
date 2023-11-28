import {jwtDecode} from 'jwt-decode';
import {BACKEND_URL} from '../config/index'

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
    return data;
}