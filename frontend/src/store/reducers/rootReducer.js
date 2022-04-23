import { combineReducers } from "redux";
import testReducer from "./testReducer";
import loginReducer from './loginReducer'
import userReducer from "./userReducer";
import performersReducer from './performersReducer'

const rootReducer = combineReducers({
  //here would be reducers
  test: testReducer,
  loginReducer: loginReducer,
  userReducer: userReducer,
  performersReducer: performersReducer
});

export default rootReducer;
