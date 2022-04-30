import { Form, Input, Image, Select, Row, Col, Button, message } from "antd";
import ImageUpload from "./../../../common/ImageUpload";
import { useState } from "react";
import PasswordModal from "./PasswordModal";
import { useDispatch, useSelector } from "react-redux";
import axiosInstance from "../../../common/axios";
import { url } from "../../../common/url";
const { Option } = Select;

const formItemLayout = {
  labelCol: {
    xs: {
      span: 24,
    },
    sm: {
      span: 8,
    },
  },
  wrapperCol: {
    xs: {
      span: 24,
    },
    sm: {
      span: 16,
    },
  },
};
const tailFormItemLayout = {
  wrapperCol: {
    xs: {
      span: 24,
      offset: 0,
    },
    sm: {
      span: 16,
      offset: 8,
    },
  },
};


const CustomerSettings = () => {
  const data = useSelector((state) => state.userReducer)
  const dispatch = useDispatch()

  const [form] = Form.useForm();
  const [visible, setVisible] = useState(false);
  const onFinish = (values) => {
    axiosInstance.put('/api/users/', {
      first_name: values.first_name,
      last_name: values.last_name,
      email: values.email,
      // phone_number: values.phone_number,
      // address: values.address
    })
      .then(response => {
        dispatch({ type: "SET_USER", payload: { ...response.data, role: data.role, username: data.username, on_site: data.on_site } });
        localStorage.setItem('user', JSON.stringify({ ...response.data, role: data.role, username: data.username, on_site: data.on_site }));
        message.success("Data is update")
      })
      .catch(err => {
        message.error(err.response.data["message"])
      });
  };

  const prefixSelector = (
    <Form.Item name="prefix" noStyle>
      <Select
        style={{
          width: 70,
        }}
      >
        <Option value="38">+38</Option>
      </Select>
    </Form.Item>
  );

  return (
    <>
      <PasswordModal visible={visible} setVisible={setVisible} />
      <Row>
        <h1>Edit profile</h1>
      </Row>
      <Row justify={"space-around"}>
        <Col col={24}>
          <Form
            {...formItemLayout}
            form={form}
            name="settings"
            onFinish={onFinish}
            initialValues={{ ...data, prefix: "38" }}
            scrollToFirstError
            style={{ width: "100%" }}
          >
            <Form.Item
              name="first_name"
              label="First name"
              rules={[
                {
                  whitespace: true,
                },
              ]}
            >
              <Input />
            </Form.Item>
            <Form.Item
              name="last_name"
              label="Last name"
              rules={[
                {
                  whitespace: true,
                },
              ]}
            >
              <Input />
            </Form.Item>

            <Form.Item
              name="email"
              label="E-mail"
              rules={[
                {
                  type: "email",
                  message: "The input is not valid E-mail!",
                },
                {
                  required: true,
                  message: "Please input your E-mail!",
                },
              ]}
            >
              <Input />
            </Form.Item>

            {/* <Form.Item
              name="phone_number"
              label="Phone Number"
              rules={[
                {
                  required: true,
                  message: "Please input your phone number!",
                },
              ]}
            >
              <Input
                addonBefore={prefixSelector}
                style={{
                  width: "100%",
                }}
              />
            </Form.Item>

            <Form.Item
              name="address"
              label="Address"
              rules={[
                {
                  required: true,
                  message: "Please input your address!",
                },
              ]}
            >
              <Input />
            </Form.Item> */}
            <Row justify={"center"}>
              <Col col={12}>
                <Form.Item {...tailFormItemLayout}>
                  <Button type="text" htmlType="submit">
                    Save
                  </Button>
                </Form.Item>
              </Col>
              <Col col={12}>
                <Form.Item {...tailFormItemLayout}>
                  <Button type="link" onClick={() => setVisible(true)}>
                    Change password
                  </Button>
                </Form.Item>
              </Col>
            </Row>
          </Form>
        </Col>
        {/* <Col col={6}>
          <h2>Avatar:</h2>
          <Image
            width={300}
            src={url + data.avatar}
          />
          <div>
            <ImageUpload />
          </div>
        </Col> */}
      </Row>
    </>
  );
};

export default CustomerSettings;
