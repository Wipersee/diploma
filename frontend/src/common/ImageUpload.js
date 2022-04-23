import React from "react";
import { Upload, message, Button } from "antd";
import { UploadOutlined } from "@ant-design/icons";
import { useState } from "react";
import axiosInstance from "./axios";
import { useHistory } from "react-router";

const ImageUpload = () => {
  const history = useHistory()

  const [selectedFile, setSelectedFile] = useState(null)
  // On file select (from the pop up)
  const onFileChange = event => {
    // Update the state
    setSelectedFile({ selectedFile: event.target.files[0] });
  };

  // On file upload (click the upload button)
  const onFileUpload = () => {
    if (selectedFile) {
      // Create an object of formData
      const formData = new FormData();

      // Update the formData object
      formData.append(
        "avatar",
        selectedFile.selectedFile,
      )
      // Request made to the backend api
      // Send formData object
      axiosInstance.patch("users/me/avatar", formData, {
        headers: {
          'content-type': 'multipart/form-data'
        }
      }).then(response => message.success("Avatar updated, return to main page and refresh"));
    }
    else {
      message.info("Select file first")
    }
  };

  return (
    <>
      <input type="file" onChange={onFileChange} />
      <br />
      <br />
      <Button type="primary" icon={<UploadOutlined />} size='12' onClick={onFileUpload}>
        Upload
      </Button>
    </>
  );
};

export default ImageUpload;
