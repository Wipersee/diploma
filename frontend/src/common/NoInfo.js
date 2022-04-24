import emptyLogo from'./../images/empty.png';
import { Col, Row } from 'antd';

const NoInfo = () => {
    return <Row justify='center'>
    <Col span={24} style={{textAlign:'center'}}>
      <img  src={emptyLogo} alt="Logo" style={{width:'25vw'}}/>
    </Col>
    <h2>No info found yet</h2>
  </Row>
}

export default NoInfo;