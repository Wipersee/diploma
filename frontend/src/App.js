import {
  BrowserRouter as Router,
  Switch,
  Route,
} from "react-router-dom";
import { PrivateRoute } from "./common/auth";
import Login from "./pages/login/Login";
import Registration from "./pages/registration/Registration";
import Main from "./pages/main/Main";
import "./common/normilize.css";
import 'antd/dist/antd.dark.css';
import License from './pages/registration/components/license'
const App = () => {

  return (
    <Router>
      <Switch>
        <Route path="/login" component={Login} />
        <Route path="/registration" component={Registration} />
        <PrivateRoute path="/" component={Main} />
      </Switch>
    </Router>
  );
};

export default App;
