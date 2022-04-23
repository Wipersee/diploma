import axiosInstance from './axios'

export const getData = (value) => ({
    type: value
})

export const getDataSuccess = (data, value) => ({
    type: value,
    payload: data,
})

export const getDataFailure = (value) => ({
    type: value
})


export function fetchData(custom_url, action) {
    return async (dispatch) => {
        dispatch(getData(`GET_${action}_DATA`))
        axiosInstance.get(custom_url).then(response => dispatch(getDataSuccess(response.data, `GET_${action}_DATA_SUCCESS`)));
    }
}