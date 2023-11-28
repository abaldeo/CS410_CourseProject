import {jwtDecode} from 'jwt-decode';
import { BACKEND_URL } from '../config';

export const fetchTranscriptList = async () => {
    const request = new Request(BACKEND_URL + 'file_upload/listLectureMaterials', {
        method: 'GET'
      });
    const response = await fetch(request);
    if (response.status === 500) {
        throw new Error('Internal server error');
    }
    const data = await response.json();
    return data;
}