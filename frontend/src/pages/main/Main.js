import { Layout, Menu, Breadcrumb, MenuProps } from 'antd';
import {
  PieChartOutlined,
  CameraOutlined,
  LockOutlined,
  SettingOutlined,
  ApiOutlined,
  LogoutOutlined
} from '@ant-design/icons';
import "./css/index.css";
import { useState} from 'react';
import { Switch, Route, Link, Redirect } from "react-router-dom";
import Settings from "./components/Settings"
import Dashboard from "./components/Dashboard"
import Clients from './components/Clients'
import Photos from "./components/Photos"
import Logs from "./components/Logs"
import { useEffect } from 'react'
import axiosInstance from "../../common/axios";
import userReducer from "../../store/reducers/userReducer";
import { useDispatch, useSelector } from "react-redux";
const { Header, Content, Footer, Sider } = Layout;

const Main = ({ match }) => {
  const [collapsed, setCollabsed] = useState(false)
  const [username, setUsername] = useState('')
  const dispatch = useDispatch();
  const keys = {
    "edit-profile": '1',
    "security-logs": '2',
    "load-photos": '3',
    "dashboard": '4',
    "clients": '5'
  }
  const get_active_element = () => {
    var string_url = window.location.href.split('/')
    var element = string_url[string_url.length - 1]
    return keys[element]
  }

  useEffect(() => {
    axiosInstance.get("api/users/").then(response => {
      dispatch({ type: "SET_USER", payload: response.data }); localStorage.setItem('user', JSON.stringify(response.data));
      setUsername(response.data.username)
    }).catch(err => console.log(err))
  }, [])

  const logout = () => {
    axiosInstance.post("api/users/logout/").then(response => {
      localStorage.removeItem('token');
      axiosInstance.defaults.headers['Authorization'] = null;
      localStorage.removeItem("isLogged");
      localStorage.removeItem("user")
      dispatch({ type: 'SET_USER', payload: {} })
      dispatch({ type: "SET_LOGIN", payload: false })
    }).catch(err => console.log(err))
  }

  return (
    <Layout style={{ minHeight: '100vh' }}>
    <Sider collapsible collapsed={collapsed} onCollapse={setCollabsed} className="sider_menu">
      <div className="logo">{collapsed ? 'F' : 'Foauth'}</div>
      <Menu theme="dark" defaultSelectedKeys={[get_active_element()]} mode="inline" > 
        <Menu.Item key="1" icon={<SettingOutlined />}>
          <Link to={`/edit-profile`}>Edit profile</Link>
        </Menu.Item>
        <Menu.Item key="2" icon={<LockOutlined />}>
          <Link to={`/security-logs`}>Security logs</Link>
        </Menu.Item>
        <Menu.Item key="3" icon={<CameraOutlined />}>
          <Link to={`/load-photos`}>Load photos</Link>
        </Menu.Item>
        <Menu.Item key="4" icon={<PieChartOutlined />}>
          <Link to={`/dasboard`}>Dashboard</Link>
        </Menu.Item>
        <Menu.Item key="5" icon={<ApiOutlined />}>
          <Link to={`/clients`}>Clients</Link>
        </Menu.Item>
        <Menu.Item key="10" icon={<LogoutOutlined />} onClick={logout}>
          Logout
        </Menu.Item>
      </Menu>
    </Sider>
    <Layout className="site-layout">
      <Header className="site-layout-background header" style={{ padding: "0 3rem", textAlign: 'right' }}>Logged as: <b>{username}</b></Header>
      <Content style={{ margin: '0 16px' }}>
        <div className="site-layout-background" style={{ padding: 24, minHeight: 360 }}>
        <Switch>
          <Route path={`/edit-profile`}>
            <Settings/>
          </Route>
          <Route path={'/dasboard'}>
            <Dashboard/>
          </Route>
          <Route path={'/clients'}>
            <Clients/>
          </Route>
          <Route path={'/load-photos'}>
            <Photos/>
          </Route>
          <Route path={'/security-logs'}>
            <Logs/>
          </Route>
        </Switch>
        </div>
      </Content>
      <Footer style={{ textAlign: 'center' }}>Foauth ©2022</Footer>
    </Layout>
  </Layout>
  );
};

export default Main;

