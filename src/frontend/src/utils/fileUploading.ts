import {jwtDecode} from 'jwt-decode';

export const fetchTranscriptList = async () => {
    const request = new Request('https://sturdy-zebra-pw79rpqq4g936jp4-8000.app.github.dev/api/v1/file_upload/listTranscripts', {
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