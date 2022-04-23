import { React, useState } from "react";
import { Card, Row, Col, Tabs } from "antd";
import "./css/registration.css";
import CustomerFrom from './components/CustomerFrom'
import PerformerForm from './components/PerformerForm'
import axiosInstance from "../../common/axios";
import { useEffect } from "react";

const { TabPane } = Tabs;

const Registration = () => {
  const [specs, setSpecs] = useState([])

  useEffect(() => {
    axiosInstance.get('users/performerSpecializations').then(response => setSpecs(response.data)).catch(err => console.log(err))
  }, [])

  return (
    <Row className="registration-row" justify={"center"}>
      <h3 className="registration-logo">Foauth</h3>
      <Col className="registration-col" col={24}>
        <Card title="Sign up" style={{ width: "45rem" }}>
          <Tabs defaultActiveKey="1">
            <TabPane tab="Customer" key="1">
              <CustomerFrom />
            </TabPane>
            <TabPane tab="Performer" key="2" >
              <PerformerForm specs={specs} />
            </TabPane>
          </Tabs>
        </Card>
      </Col >
    </Row >
  );
};

export default Registration;
