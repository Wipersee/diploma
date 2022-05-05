import { Line, Pie } from '@ant-design/charts';
import { Row, Col, Card } from 'antd'
import { useState, useEffect } from 'react';
import axiosInstance from "../../../common/axios";

const Dashboard = () => {
  const [data_line, setDataLine] = useState([])
  const [data_pie, setDataPie] = useState([])

  useEffect(() => {
    axiosInstance.get("api/users/unauth-dashboard/").then(response => {
      setDataLine(response.data.line)
      setDataPie(response.data.pie)
      console.log(response.data.pie)
    }).catch(err => console.log(err))
  }, [])
  const config = {
    appendPadding: 10,
    data_pie,
    angleField: 'value',
    colorField: 'type',
    radius: 0.9,
    interactions: [
      {
        type: 'element-active',
      },
    ],
  };
  return (
    <Row gutter={[16, 16]}>
      <Col span={12}>
        <Card title="Unauthorized logins per day">
          <Line
            data={data_line}
            height={500}
            xField="date"
            yField="value"
            point={{ size: 5, shape: 'diamon' }}
            color='blue'
          />
        </Card>
      </Col>

      <Col span={12}>
        <Card title="Unauthorized logins per type" >
          <Pie data={data_pie} angleField="value" colorField='type' />;
        </Card>
      </Col>
    </Row>
  );
};

export default Dashboard;