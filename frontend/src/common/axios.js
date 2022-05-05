import axios from "axios";
import store from './../store/store'

const axiosInstance = axios.create({
    baseURL: 'http://localhost:5000/', //TODO: rewrite before prod
    headers: {
        'Authorization': localStorage.getItem('token'),
        'Content-Type': 'application/json',
        'accept': 'application/json'
    }
});

export default axiosInstance;