import { Comment, Tooltip, Avatar, Divider } from "antd";
import moment from "moment";

const CustomComment = (props) => {
  const { author, avatar, content, datetime } = props;
  return (
    <Comment
      author={<a>Han Solo</a>}
      avatar={
        <Avatar src="https://joeschmoe.io/api/v1/random" alt="Han Solo" />
      }
      content={
        <p>
          We supply a series of design principles, practical patterns and high
          quality design resources (Sketch and Axure), to help people create
          their product prototypes beautifully and efficiently.
        </p>
      }
      datetime={datetime}
    />
  );
};

export default CustomComment;
