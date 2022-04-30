import { useState } from "react";
import { Modal, Row, Col, Form, Input, message, Button } from "antd";
import axiosInstance from "../../../common/axios";

const ChangePasswordModal = ({ visible, setVisible }) => {
  const [confirmLoading, setConfirmLoading] = useState(false);
  const [form] = Form.useForm();

  const onFinish = (values) => {
    setConfirmLoading(true);
    axiosInstance.put('api/users/password/', {
      password: values.password,
      old_password: values.old_password,
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
        title="Change password form"
        visible={visible}
        confirmLoading={confirmLoading}
        onCancel={handleCancel}
        footer={[
          <>
            <Button
              form="change_password_form"
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
              id={"change_password_form"}
            >
              <Form.Item
                name="old_password"
                label="Old password"
                rules={[
                  {
                    required: true,
                    message: "Please input your password!",
                  },
                ]}
                hasFeedback
              >
                <Input.Password />
              </Form.Item>
              <Form.Item
                name="password"
                label="Password"
                rules={[
                  {
                    required: true,
                    message: "Please input your password!",
                  },
                ]}
                hasFeedback
              >
                <Input.Password />
              </Form.Item>

            </Form>
          </Col>
        </Row>
      </Modal>
    </>
  );
};

export default ChangePasswordModal;

