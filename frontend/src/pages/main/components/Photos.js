import Webcam from "react-webcam";
import { message, Image, Button, Row, Col } from "antd";
import { useState, useRef, useCallback } from "react";
import {
    CameraOutlined,
    DeleteOutlined
} from '@ant-design/icons';
import axiosInstance from "../../../common/axios";

const Photos = () => {
    const [photos, setPhotos] = useState([])
    const webcamRef = useRef(null);
    const updatePhotosArray = (img) => {
        if (photos.length >= 15) {
            message.warning("Max number of photos is 15. Removing 1st photo")
            setPhotos(photos.filter(item => photos.indexOf(item) !== 0));
        }

        setPhotos(old_photos => [...old_photos, img]);
    }

    const deletePhoto = (idx) => {
        setPhotos(photos.filter(item => photos.indexOf(item) !== idx));
    }

    const capture = useCallback(() => {
        const imageSrc = webcamRef.current.getScreenshot();
        updatePhotosArray(imageSrc);
    }, [webcamRef, updatePhotosArray]);
    const key = 'loading';
    const upload = () => {
        message.loading({ content: 'Loading...', key });
        axiosInstance.post('api/users/auth-photos/', {
            photos: photos
        }).then(response => {
            message.success({ content: response.data.message, key });
        }).catch(err => {
            message.error(err.response.data.message)
        });
    }

    return <>
        <Row>
            <h1>Update photos DB</h1>
        </Row>
        <Row>
            <Webcam
                audio={false}
                ref={webcamRef}
                screenshotFormat="image/jpeg"
                style={{ width: '30%', margin: '0 auto' }}
            />
        </Row>
        <Row justify="space-between" style={{ "margin": "2rem 0.5rem" }}>
            <Button type="primary" onClick={capture}>Take a photo</Button>
            <Button type="primary" onClick={upload}>Submit</Button>
        </Row>
        <Row gutter={[16, 16]}>
            {photos.map((item, idx) => <Col span={3}>
                <Button type="danger" onClick={() => deletePhoto(idx)} shape="circle" icon={<DeleteOutlined />} />
                <Image width={150} src={item} />
            </Col>)}
        </Row>
    </>
}

export default Photos;