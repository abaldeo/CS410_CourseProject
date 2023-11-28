import {jwtDecode} from 'jwt-decode';
import {BACKEND_URL} from '../config/index'

export const fetchAnswer = async (question: string) => {
    if (!(question.length > 0)) {
        throw new Error('Question was not provided');
    }
    const request = new Request(BACKEND_URL + 'rag/qa?question=' + question, {
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