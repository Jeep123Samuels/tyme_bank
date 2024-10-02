import axios from 'axios';

const baseUrl = 'http://localhost:5000/';

export const getData = async (uri) => {
    const response = await axios.get(`${baseUrl}${uri}`);
    return response.data;
}

export const postRequest = async (uri, data) => {
    const response = await axios.post(`${baseUrl}${uri}`, data);
    return response.data;
}

export const deleteRequest = async (uri) => {
    const response = await axios.delete(`${baseUrl}${uri}`);
}
