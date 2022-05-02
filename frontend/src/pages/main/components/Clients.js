import {useState, useEffect} from 'react';
import axiosInstance from "../../../common/axios";
import {Row, Table, Button, message} from "antd"
import ClientsModal from './ClientsModal'
import NoInfo from '../../../common/NoInfo';

const Clients = () => {
    const [clients, setClients] = useState()
    const [visible, setVisible] = useState(false)

    const deleteClient = (id) => {
      axiosInstance.delete("api/clients/" + id).then(response => {
        message.success(response.data.message);
      }).catch(err =>  message.success(err.data.message))
    }

    const columns = [
        {
          title: 'Client ID',
          width: 100,
          dataIndex: 'client_id',
          key: 'client_id',
          fixed: 'left',
        },
        {
          title: 'Client secret',
          width: 100,
          dataIndex: 'client_secret',
          key: 'client_secret',
          fixed: 'left',
        },
        { 
            title: 'Client name', 
            render: (record) => record.client_metadata.client_name,
            fixed:'left'
        },
        { 
            title: 'Client URI', 
            render: (record) => record.client_metadata.client_uri
        },
        { 
            title: 'Redirect URI', 
            render: (record) => record.client_metadata.redirect_uris.join(", ")
        },
        { 
            title: 'Scope', 
            render: (record) => record.client_metadata.scope
        },
        { 
            title: 'Grant types', 
            render: (record) => record.client_metadata.grant_types.join(", ")
        },
        {
          title: 'Delete',
          key: 'delete',
          render: (text, record) => (
            <Button type="link" danger onClick={() => {deleteClient(record.id)}}> Delete </Button>
          ),
        },
      ];

    useEffect(() => {
        axiosInstance.get("api/clients/").then(response => {
            setClients(response.data.clients)
          }).catch(err => console.log(err))
    }, [])

    return <>
    <ClientsModal visible={visible} setVisible={setVisible} />
    <Row>
        <h1>Your clients list</h1>
    </Row>
    <Button type="link" onClick={() => setVisible(true)}>
        Create new client
    </Button>
    {clients ?
    <Table columns={columns} dataSource={clients} rowKey="uid"/> : 
    <NoInfo/>
    }
  </>
}

export default Clients;