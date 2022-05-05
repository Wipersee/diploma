import { useState } from "react";
import { Modal, Row, Col, Form, Input, message, Button } from "antd";
import axiosInstance from "../../../common/axios";

const ClientsModal = ({ visible, setVisible }) => {
  const [confirmLoading, setConfirmLoading] = useState(false);
  const [form] = Form.useForm();

  const onFinish = (values) => {
    setConfirmLoading(true);
    axiosInstance.post('api/clients/', {
      client_name: values.client_name,
      client_uri: values.client_uri,
      scope: values.scope,
      redirect_uri: [values.redirect_uri],
      grant_type: ["authorization_code", "password"],
      response_type: ["code"],
      token_endpoint_auth_method: "client_secret_basic"
    }).then(res => {
      setVisible(false);
      setConfirmLoading(false);
      message.success(res.data.message);
      form.resetFields();
    }).catch((err) => {
      setConfirmLoading(false);
      message.error(err.response.data.message)
    })
  };

  const handleCancel = () => {
    setVisible(false);
    form.resetFields();
  };

  return (
    <>
      <Modal
        title="Create new client"
        visible={visible}
        confirmLoading={confirmLoading}
        onCancel={handleCancel}
        footer={[
          <>
            <Button
              form="create_new_client_form"
              key="submit"
              htmlType="submit"
              type={"primary"}
              loading={confirmLoading}
            >
              Submit
            </Button>
            <Button onClick={handleCancel}>Cancel</Button>
          </>,
        ]}
      >
        <Row>
          <Col col={24} style={{ width: "100%" }}>
            <Form
              form={form}
              name="changePassword"
              onFinish={onFinish}
              scrollToFirstError
              style={{ width: "100%" }}
              id={"create_new_client_form"}
            >
              <Form.Item
                name="client_name"
                label="Client name"
                rules={[
                  {
                    required: true,
                    message: "Please input your client name!",
                  },
                ]}
                hasFeedback
              >
                <Input />
              </Form.Item>
              <Form.Item
                name="client_uri"
                label="Client URI"
                rules={[
                  {
                    required: true,
                    message: "Please input your client URI!",
                  },
                ]}
                hasFeedback
              >
                <Input />
              </Form.Item>

              <Form.Item
                name="scope"
                label="Scope"
                rules={[
                  {
                    required: true,
                    message: "Please input your client scope!",
                  },
                ]}
                hasFeedback
              >
                <Input />
              </Form.Item>

              <Form.Item
                name="redirect_uri"
                label="Redirect URI"
                rules={[
                  {
                    required: true,
                    message: "Please input your client redirect URI!",
                  },
                ]}
                hasFeedback
              >
                <Input />
              </Form.Item>
            </Form>
          </Col>
        </Row>
      </Modal>
    </>
  );
};

export default ClientsModal;

