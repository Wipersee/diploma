import { combineReducers } from "redux";
import testReducer from "./testReducer";
import loginReducer from './loginReducer'
import userReducer from "./userReducer";

const rootReducer = combineReducers({
  //here would be reducers
  test: testReducer,
  loginReducer: loginReducer,
  userReducer: userReducer,
});

export default rootReducer;
