import {useState, useEffect} from 'react';
import axiosInstance from "../../../common/axios";
import {Row, Table, Button, message} from "antd"
import NoInfo from '../../../common/NoInfo';
import moment from 'moment';

const GrantAccess = () => {

    const [access, setAccess] = useState()

    const revokeAccess = (id) => {
      axiosInstance.post("api/clients/grant-access/" + id).then(response => {
        message.success(response.data.message);
      }).catch(err =>  message.success(err.data.message))
    }

    const columns = [
        { 
            title: 'Client name', 
            render: (record) => record.client_name,
            fixed:'left'
        },
        { 
            title: 'Client URI', 
            render: (record) => record.client_uri
        },
        { 
            title: 'Scope', 
            render: (record) => record.scope
        },
        { 
          title: 'Expires in', 
          render: (record) => moment(record.issued_at, 'X').add(record.expires_in, 'seconds').format('lll')
      },
      { 
        title: 'Issued at', 
        render: (record) => moment(record.issued_at, 'X').format('lll')
    },
        {
          title: 'Revoke',
          key: 'revoke',
          render: (text, record) => (
            <Button type="link" danger onClick={() => {revokeAccess(record.id)}}> Revoke </Button>
          ),
        },
      ];

    useEffect(() => {
        axiosInstance.get("api/clients/grant-access").then(response => {
          setAccess(response.data.access)
          }).catch(err => console.log(err))
    }, [])

    return <>
    <Row>
        <h1>You granting access</h1>
    </Row>
    {access ?
    <Table columns={columns} dataSource={access} rowKey="uid"/> : 
    <NoInfo/>
    }
  </>
};

export default GrantAccess;