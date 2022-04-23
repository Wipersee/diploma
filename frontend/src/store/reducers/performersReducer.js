let initialState = {
    data: [],
    loading: false,
    hasErrors: false,
};

const performersReducer = (state = initialState, action) => {
    switch (action.type) {
        case "GET_PERFORMERS_DATA":
            return { ...state, loading: true };
        case "GET_PERFORMERS_DATA_SUCCESS":
            return { data: action.payload, loading: false, hasErrors: false };
        case "GET_PERFORMERS_DATA_FAILURE":
            return { ...state, loading: false, hasErrors: true };
        default:
            return state;
    }
};

export default performersReducer;
