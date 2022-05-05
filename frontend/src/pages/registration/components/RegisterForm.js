import { Form, Input, notification, Select, Row, Col, Checkbox, Button, Radio, message } from "antd";
import axiosInstance from "../../../common/axios";
import { useHistory } from 'react-router-dom'
import { formItemLayout, tailFormItemLayout, prefixSelector } from './layout'
import { Link } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";

const RegisterForm = () => {
    const [form] = Form.useForm();
    const history = useHistory()
    const dispatch = useDispatch();

    const args = {
        message: 'End register process',
        description:
            'You need to upload photos on the Load photos page before 2 days pass. If not you will lose your account.',
        duration: 0,
    };


    const onFinish = (values) => {
        axiosInstance.post('api/users/', {
            username: values.username,
            password: values.password,
            email: values.email,
        }).then(response => {
            console.log(response.data)
            message.success("User created, redirecting")
            axiosInstance.defaults.headers['Authorization'] = response.data.message;
            localStorage.setItem('token', response.data.message);
            localStorage.setItem("isLogged", true)
            dispatch({ type: "SET_LOGIN", payload: true })
            notification['warning'](args);
            history.push("/load-photos");
        }).catch(err => {
            message.error(err.response.data.message)
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
                    I have read the <Link to="agreement" target="_blank" rel="noopener noreferrer">Agreement</Link>
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

export default RegisterForm;