import { Route, Redirect } from "react-router";
import { useDispatch, useSelector } from "react-redux";
import rootReducer from "../store/reducers/rootReducer";
import store from './../store/store'

export function PrivateRoute({ component: Component, ...rest }) {
  const { login } = useSelector((state) => state.loginReducer);
  return (
    <Route
      {...rest}
      render={(props) => {
        return login ? (
          <Component {...props} />
        ) : (
          <Redirect to="/login" />
        );
      }}
    />
  );
}


export function whichRole(role) {
  return role === 'CUST' ? "Customer" : "Performer";
}


export function handleLogout() {
  //need to write logic of logout 
}