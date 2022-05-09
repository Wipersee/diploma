import { React, useCallback, useRef, useState } from "react";
import { Form, Input, Button, Row, Col, Card, message, Image } from "antd";
import { UserOutlined, LockOutlined } from "@ant-design/icons";
import "./css/index.css";
import { Link, useHistory } from 'react-router-dom'
import axiosInstance from './../../common/axios'
import { useDispatch, useSelector } from "react-redux";
import axios from "axios";
import mainLogo from './../../images/face_logo.png';
import Webcam from "react-webcam";
import {
  VideoCameraOutlined
} from '@ant-design/icons';
import moment from "moment";

const Login = () => {
  let history = useHistory();
  const dispatch = useDispatch();
  const webcamRef = useRef(null);
  const [imgSrc, setImgSrc] = useState(null);
  const [isNextStep, setNexStep] = useState(false)
  const [response, setResponse] = useState()
  const [images, setImages] = useState([])
  const [username, setUsername] = useState('')
  const key = 'loading';
  const key2 = 'loading2'

  const capture = useCallback(() => {
    const imageSrc = webcamRef.current.getScreenshot();
    setImgSrc(imageSrc);
  }, [webcamRef, setImgSrc]);

  const captureVideo = () => {
    var CurrentDate = moment();
    const arr = []
    while (moment() < moment(CurrentDate).add(2, 'seconds')) {
      const imageSrc = webcamRef.current.getScreenshot();
      arr.push(imageSrc)
    }
    setImages(arr)
    message.info({ content: `Captured. Please click Log in button`, key2 });
  }

  const record = () => {
    message.loading({ content: 'Capturing. Follow instructions...', key2 });
    setTimeout(captureVideo(), 1000);
    
  }

  const onLastFinish = () => {
    message.loading({ content: 'Loading...', key });
    console.log(response)
    axios.post(`http://localhost:5000/api/users/login?token=${response.intermidiate_token}`, { //TODO: before prod change this link
      username: username,
      password: '',
      photos: images
    }).then(response => {
      message.info({ content: `Loaded !`, key });
      axiosInstance.defaults.headers['Authorization'] = response.data.message;
      localStorage.setItem('token', response.data.message);
      localStorage.setItem("isLogged", true)
      dispatch({ type: "SET_LOGIN", payload: true })
      history.push("/edit-profile");
    }).catch(err => {
      message.error(err.response.data.message)
    });
  }

  const onFinish = (values) => {
    setUsername(values.username)
    message.loading({ content: 'Loading...', key });
    axios.post('http://localhost:5000/api/users/login', { //TODO: before prod change this link
      username: values.username,
      password: values.password,
      photo: imgSrc
    }).then(response => {
      message.info({ content: `Please ${response.data.verification_method} ${response.data.repeat} time(s)`, key });
      // axiosInstance.defaults.headers['Authorization'] = response.data.message;
      // localStorage.setItem('token', response.data.message);
      // localStorage.setItem("isLogged", true)
      // dispatch({ type: "SET_LOGIN", payload: true })
      // history.push("/edit-profile");
      setResponse(response.data)
      setNexStep(true)
    }).catch(err => {
      message.error(err.response.data.message)
    });


  };

  return (
    <Row className="login-row" justify={"space-around"} align={'middle'}>
      <h3 className="login-logo">Foauth</h3>
      <Col className="login-col" col={12}>
        {isNextStep ? 
        <Card title="Verification for real human" style={{ width: "40rem" }}>
          <Webcam
              audio={false}
              ref={webcamRef}
              screenshotFormat="image/jpeg"
              style={{ width: '100%', margin: '0 auto' }}
            />
            <div style={{ "margin": "2rem auto", "textAlign": "center" }}>
              <Button type="primary" onClick={() => record()} ><VideoCameraOutlined />Start</Button>
            </div>
            <Button
                type="primary"
                htmlType="submit"
                className="login-form-button"
                onClick={() => onLastFinish()}
              >
                Log in
              </Button>
        </Card>
        
        : <Card title="Welcome back !" style={{ width: "40rem" }}>
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
              style={{ width: '100%', margin: '0 auto' }}
            />
            <div style={{ "margin": "2rem auto", "textAlign": "center" }}>
              <Button type="primary" onClick={capture} >Take a picture</Button>
            </div>

            <Form.Item>
              <Button
                type="primary"
                htmlType="submit"
                className="login-form-button"
              >
                Verify
              </Button>
              <Link to="/registration">&nbsp;Or register now</Link>
            </Form.Item>
          </Form>
        </Card> }
      </Col>
      <Col col={12}>
        {imgSrc ? <Image
          width={'25vw'}
          src={imgSrc}
        /> : <img src={mainLogo} alt="Logo" style={{ width: '25vw' }} />}
      </Col>
      
    </Row>
  );
};

export default Login;
