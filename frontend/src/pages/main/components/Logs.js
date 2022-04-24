import {useState, useEffect} from 'react';
import axiosInstance from "../../../common/axios";
import {Row, Table, Button} from "antd"
import NoInfo from '../../../common/NoInfo';
import moment from 'moment';

const Logs = () => {
    const [unauth_logins, setUnauthLogins] = useState()

    const columns = [
        {
          title: 'Date',
          render: (record) => moment(record.date).format('DD-MMM-YYYY HH:MM:SS'),
          key: 'date',
        },
        {
          title: 'Login type',
          dataIndex: 'type',
          key: 'type',
        },
        { 
            title: 'Max similarity accross your photos', 
            dataIndex: 'similarity',
            key: 'similarity',
        },
      ];

    useEffect(() => {
        axiosInstance.get("/api/users/unauthorized-logins/").then(response => {
            setUnauthLogins(response.data.logins)
          }).catch(err => console.log(err))
    }, [])

    return <>
    <Row>
        <h1>Your security logs</h1>
    </Row>
    {unauth_logins ?
    <Table columns={columns} dataSource={unauth_logins} rowKey="uid"/> : <NoInfo/>}
  </>
}

export default Logs;