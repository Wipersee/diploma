import { React, useState } from "react";
import { Card, Row, Col, Tabs } from "antd";
import "./css/registration.css";
import RegisterForm from './components/RegisterForm'

const Registration = () => {
  return (
    <Row className="registration-row" justify={"center"}>
      <h3 className="registration-logo">Foauth</h3>
      <Col className="registration-col" col={24}>
        <Card title="Sign up" style={{ width: "45rem" }}>
          <RegisterForm/>
        </Card>
      </Col >
    </Row >
  );
};

export default Registration;
