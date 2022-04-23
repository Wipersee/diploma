import axios from "axios";
import store from './../store/store'

const axiosInstance = axios.create({
    baseURL: 'https://profielp.herokuapp.com/api/', //TODO: rewrite before prod
    headers: {
        'Authorization': "Bearer " + localStorage.getItem('access_token'),
        'Content-Type': 'application/json',
        'accept': 'application/json'
    }
});

axiosInstance.interceptors.response.use(
    response => response,
    error => {
        const originalRequest = error.config;
        if (error.response.status === 401 && error.response.statusText === "Unauthorized" && error.response.data.messages[0].token_type === 'access') {
            const refresh_token = localStorage.getItem('refresh_token');

            return axiosInstance
                .post('/token/refresh/', { refresh: refresh_token })
                .then((response) => {

                    localStorage.setItem('access_token', response.data.access);
                    localStorage.setItem('refresh_token', response.data.refresh);

                    axiosInstance.defaults.headers['Authorization'] = "Bearer " + response.data.access;
                    originalRequest.headers['Authorization'] = "Bearer " + response.data.access;

                    return axiosInstance(originalRequest);
                })
                .catch(err => {
                    localStorage.removeItem('user')
                    localStorage.removeItem('refresh_token')
                    localStorage.removeItem('access_token')
                    localStorage.setItem('isLogged', false)
                    store.dispatch({ type: 'SET_LOGIN', payload: false })
                });
        }
        // else if (error.response.status === 400 && error.response.statusText !== "Bad R") {
        //     localStorage.setItem("isLogged", false)
        // }
        else if (error.response.status === 401 && error.response.statusText === "Unauthorized" && error.response.data.code === "token_not_valid") {
            localStorage.removeItem('user')
            localStorage.removeItem('refresh_token')
            localStorage.removeItem('access_token')
            localStorage.setItem('isLogged', false)
            store.dispatch({ type: 'SET_LOGIN', payload: false })
        }
        return Promise.reject(error);
    }
);

export default axiosInstance;