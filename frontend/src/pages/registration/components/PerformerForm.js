import { Form, Input, InputNumber, Checkbox, Button, Select, message } from "antd";
import axiosInstance from "../../../common/axios";
import { useHistory } from 'react-router-dom'
import { formItemLayout, tailFormItemLayout, prefixSelector } from './layout'
import { useEffect, useState } from "react";

const { Option } = Select;

const PerformerForm = (props) => {
    var options = {
        enableHighAccuracy: true,
        timeout: 5000,
        maximumAge: 0
    };
    const [crd, setCrd] = useState()
    const [form] = Form.useForm();
    const history = useHistory()
    useEffect(() => { navigator.geolocation.getCurrentPosition((v) => setCrd(v.coords), (r) => console.log(r), options); }, [])



    const onFinish = (values) => {

        axiosInstance.post('users/registration/performer', {
            username: values.username,
            password: values.password,
            phone_number: values.phone,
            email: values.email,
            avg_price_per_hour: values.avg_price_per_hour,
            performer_specialization_id: values.performer_specialization_id,
            latitude: crd.latitude,
            longitude: crd.longitude,
        }).then(res => {
            message.success("User created, please login")
            history.push('/login')
        }).catch(err => {
            var keys = Object.keys(err.response.data);
            const errors = []
            keys.forEach(function (key) {
                errors.push(err.response.data[key])
            });
            message.error(errors.map(item => <span style={{ color: 'red' }}>{item[0]}<br /></span>))
        })
    };

    return (
        <Form
            {...formItemLayout}
            form={form}
            name="register"
            onFinish={onFinish}
            initialValues={{
                prefix: "38",
            }}
            scrollToFirstError
        >
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

            <Form.Item
                name="confirm"
                label="Confirm Password"
                dependencies={["password"]}
                hasFeedback
                rules={[
                    {
                        required: true,
                        message: "Please confirm your password!",
                    },
                    ({ getFieldValue }) => ({
                        validator(_, value) {
                            if (!value || getFieldValue("password") === value) {
                                return Promise.resolve();
                            }

                            return Promise.reject(
                                new Error(
                                    "The two passwords that you entered do not match!"
                                )
                            );
                        },
                    }),
                ]}
            >
                <Input.Password />
            </Form.Item>

            <Form.Item
                name="username"
                label="Username"
                tooltip="What do you want others to call you?"
                rules={[
                    {
                        required: true,
                        message: "Please input your nickname!",
                        whitespace: true,
                    },
                ]}
            >
                <Input />
            </Form.Item>

            <Form.Item
                name="phone"
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
                name="avg_price_per_hour"
                label="Price per hour"
                rules={[
                    {
                        required: true,
                        message: "Please input your price!",
                    },
                ]}
            >
                <InputNumber
                    defaultValue={0}
                    formatter={value => `₴ ${value}`.replace(/\B(?=(\d{3})+(?!\d))/g, ',')}
                    // parser={value => value.replace(/\$\s?|(,*)/g, '')}
                    style={{
                        width: "100%",
                    }}
                />
            </Form.Item>
            <Form.Item
                name="performer_specialization_id"
                label="Spezialization"
                rules={[
                    {
                        required: true,
                        message: 'Please select specialization!',
                    },
                ]}
            >
                <Select placeholder="select your specialization">
                    {props.specs.map(item => <Option value={item.performer_specialization}>{item.performer_specialization}</Option>)}
                </Select>
            </Form.Item>

            <Form.Item
                name="agreement"
                valuePropName="checked"
                rules={[
                    {
                        validator: (_, value) =>
                            value
                                ? Promise.resolve()
                                : Promise.reject(new Error("Should accept agreement")),
                    },
                ]}
                {...tailFormItemLayout}
            >
                <Checkbox>
                    I have read the <a href="">agreement</a>
                </Checkbox>
            </Form.Item>
            <Form.Item {...tailFormItemLayout}>
                <Button type="primary" htmlType="submit">
                    Register
                </Button>
            </Form.Item>
        </Form>
    )
}

export default PerformerForm;