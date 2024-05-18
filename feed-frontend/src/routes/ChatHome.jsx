import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { getCookieValue } from "../utils";

const ChatHome = () => {
  const [userId, setUserId] = useState("");
  const navigate = useNavigate();

  const fetchChatHistory = () => {
    fetch(
      `https://f2pn2qk4t5.execute-api.us-east-1.amazonaws.com/dev-ma/get_chats?user_id=${userId}`
    )
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        const dataList = document.getElementById("dataList");
        dataList.innerHTML = "";
        console.log(data);
        let content = JSON.parse(data.body);
        for (let i = 0; i < content.length; i++) {
          const listItem = document.createElement("a");
          listItem.textContent = content[i].receiver_id; // Assuming each item has a 'name' property
          listItem.href = `chat-client?data=${encodeURIComponent(
            JSON.stringify(content[i].receiver_id)
          )}&user_id=${getCookieValue("user_id")}`;
          listItem.classList.add("dataItem");
          dataList.appendChild(listItem);
          dataList.appendChild(document.createElement("br"));
        }
      });
  };
  return (
    <div className='container'>
      <h1>API Data Viewer</h1>
      <label htmlFor='userId'>Enter User ID:</label>
      <input
        type='text'
        id='userId'
        name='userId'
        onChange={(e) => setUserId(e.target.value)}
        required
      />
      <button onClick={fetchChatHistory}>Get Data</button>
      <div id='dataList'></div>
    </div>
  );
};

export default ChatHome;
