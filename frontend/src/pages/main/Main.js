import { Layout, Menu, Breadcrumb, MenuProps } from 'antd';
import {
  PieChartOutlined,
  CameraOutlined,
  LockOutlined,
  SettingOutlined,
} from '@ant-design/icons';
import "./css/index.css";
import { useState} from 'react';
import { Switch, Route, Link, Redirect } from "react-router-dom";
import Settings from "./components/Settings"
import Dashboard from "./components/Dashboard"
const { Header, Content, Footer, Sider } = Layout;

const Main = ({ match }) => {
  const [collapsed, setCollabsed] = useState(false)

  const keys = {
    "edit-profile": '1',
    "security-logs": '2',
    "load-photos": '3'
  }
  const get_active_element = () => {
    var string_url = window.location.href.split('/')
    var element = string_url[string_url.length - 1]
    return keys[element]
  }
  console.log(get_active_element())
  return (
    <Layout style={{ minHeight: '100vh' }}>
    <Sider collapsible collapsed={collapsed} onCollapse={setCollabsed}>
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
      </Menu>
    </Sider>
    <Layout className="site-layout">
      <Header className="site-layout-background" style={{ padding: 0 }} />
      <Content style={{ margin: '0 16px' }}>
        <div className="site-layout-background" style={{ padding: 24, minHeight: 360 }}>
        <Switch>
          <Route path={`/edit-profile`}>
            <Settings/>
          </Route>
          <Route path={'/dasboard'}>
            <Dashboard/>
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

