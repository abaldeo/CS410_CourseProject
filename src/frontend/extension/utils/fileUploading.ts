
import { BACKEND_URL } from './index';

export const fetchTranscriptList = async () => {
    const request = new Request(BACKEND_URL + 'file_upload/listLectureMaterials?detail=false', {
        method: 'GET'
      });
    const response = await fetch(request);
    if (response.status === 500) {
        throw new Error('Internal server error');
    }
    const data = await response.json();
    // console.log(data)
    return data;
}