import { React,useCallback, useRef, useState } from "react";
import { Form, Input, Button, Row, Col, Card, message, Image } from "antd";
import { UserOutlined, LockOutlined } from "@ant-design/icons";
import "./css/index.css";
import { Link, useHistory } from 'react-router-dom'
import axiosInstance from './../../common/axios'
import { useDispatch, useSelector } from "react-redux";
import axios from "axios";
import mainLogo from'./../../images/face_logo.png';
import Webcam from "react-webcam";
import {
  CameraOutlined
} from '@ant-design/icons';

const Login = () => {
  let history = useHistory();
  const dispatch = useDispatch();
  const webcamRef = useRef(null);
  const [imgSrc, setImgSrc] = useState(null);
  const key = 'loading';

  const capture = useCallback(() => {
    const imageSrc = webcamRef.current.getScreenshot();
    setImgSrc(imageSrc);
  }, [webcamRef, setImgSrc]);

  const onFinish = (values) => {
    message.loading({ content: 'Loading...', key });
    axios.post('http://localhost:5000/api/users/login', { //TODO: before prod change this link
      username: values.username,
      password: values.password,
      photo: imgSrc
    }).then(response => {
      message.success({ content: 'Loaded!', key });
      axiosInstance.defaults.headers['Authorization'] = response.data.message;
      localStorage.setItem('token', response.data.message);
      localStorage.setItem("isLogged", true)
      dispatch({ type: "SET_LOGIN", payload: true })
      history.push("/edit-profile");
    }).catch(err => {
      message.error(err.response.data.message)
    });


  };

  return (
    <Row className="login-row" justify={"space-around"} align={'middle'}>
      <h3 className="login-logo">Foauth</h3>
      <Col className="login-col" col={12}>
        <Card title="Welcome back !" style={{ width: "40rem" }}>
          <Form
            name="normal_login"
            className="login-form"
            initialValues={{ remember: true }}
            onFinish={onFinish}
          >
            <Form.Item
              name="username"
              rules={[
                { required: true, message: "Please input your Username!" },
              ]}
            >
              <Input
                prefix={<UserOutlined className="site-form-item-icon" />}
                placeholder="Username"
              />
            </Form.Item>
            <Form.Item
              name="password"
              rules={[
                { required: true, message: "Please input your Password!" },
              ]}
            >
              <Input.Password
                prefix={<LockOutlined className="site-form-item-icon" />}
                type="password"
                placeholder="Password"
              />
            </Form.Item>
              <Webcam
                  audio={false}
                  ref={webcamRef}
                  screenshotFormat="image/jpeg"
                  style={{width:'90%', margin:'0 auto'}}
                />
            <Button type="primary" onClick={capture} shape="circle" icon={<CameraOutlined />} />
            {imgSrc && <Image
              width={200}
              src={imgSrc}
            />}
            <Form.Item>
              <Button
                type="primary"
                htmlType="submit"
                className="login-form-button"
              >
                Log in
              </Button>
              <Link to="/registration">&nbsp;Or register now</Link>
            </Form.Item>
          </Form>
        </Card>
      </Col>
      <Col col={12}>
        <img  src={mainLogo} alt="Logo" style={{width:'25vw'}}/>
      </Col>
    </Row>
  );
};

export default Login;
