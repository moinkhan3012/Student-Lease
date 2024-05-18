import { useEffect } from "react";
import "../styles/chat-client.css";

const ChatClient = () => {
  var websocket;
  var currentRecipient;
  function getQueryParams() {
    const params = new URLSearchParams(window.location.search);
    const data = params.get("data"); // Assuming the parameter is named 'data'
    console.log(data);
    let data2 = data.replace(/['"]+/g, "");
    document.getElementById("targetUsername").value = data2; // recipient user id
    document.getElementById("username").value = params
      .get("user_id")
      .replace(/['"]+/g, ""); // my user id
    connectWebSocket();
    currentRecipient = document.getElementById("targetUsername").value;
    fetchPastConversations(currentRecipient);
  }
  useEffect(() => {
    getQueryParams();
  }, []);

  function connectWebSocket() {
    var username = document.getElementById("username").value;
    if (!username) {
      alert("Please enter your name.");
      return;
    }
    var wsUri = `wss://pii672v338.execute-api.us-east-1.amazonaws.com/dev?userId=${encodeURIComponent(
      username
    )}`;
    console.log("username", username);
    websocket = new WebSocket(wsUri);

    websocket.onopen = function (event) {
      console.log("Connected");
    };

    websocket.onmessage = function (event) {
      let info = JSON.parse(event.data);
      let msg = info.sender + ": " + info.msg;
      displayMessage(msg, "received");
    };

    websocket.onerror = function (event) {
      console.log("WebSocket Error");
    };

    websocket.onclose = function (event) {
      console.log("Disconnected!");
    };
  }

  function sendMessage() {
    // connectWebSocket();
    var message = document.getElementById("message").value;
    if (websocket && websocket.readyState === WebSocket.OPEN) {
      var username = document.getElementById("username").value;
      var currentRecipient = document.getElementById("targetUsername").value;
      console.log(username);
      console.log(currentRecipient);
      var msg = JSON.stringify({
        action: "sendMessage",
        sender: username,
        target: currentRecipient,
        message: message,
      });
      websocket.send(msg);
      displayMessage("You: " + message, "sent");
    } else {
      alert("WebSocket is not connected.");
    }
  }

  // function checkEnter(event) {
  //   if (event.keyCode === 13) {
  //     // Enter key
  // currentRecipient = document.getElementById("targetUsername").value;
  // fetchPastConversations(currentRecipient);
  //   }
  // }

  // function checkEnterMessage(event) {
  //   if (event.keyCode === 13) {
  //     // Enter key
  //     sendMessage();
  //   }
  // }

  function disconnectWebSocket() {
    if (websocket) {
      websocket.close();
    }
  }
  function get_order(str1, str2) {
    if (str1 > str2) {
      return str2 + "_" + str1;
    } else {
      return str1 + "_" + str2;
    }
  }
  function fetchPastConversations(recipient) {
    // API URL, include the recipient as a query parameter
    var username = document.getElementById("username").value;
    var msg_id = get_order(username, recipient);
    console.log(msg_id);
    var apiUrl = `https://f2pn2qk4t5.execute-api.us-east-1.amazonaws.com/dev-ma/get_msgs?message_id=${encodeURIComponent(
      msg_id
    )}`;

    var headers = {
      "Access-Control-Allow-Origin": "*",
      "Content-Type": "application/json",
    };

    fetch(apiUrl, { headers: headers })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok " + response.statusText);
        }
        return response.json();
      })
      .then((data) => {
        console.log(data);
        let content = JSON.parse(data.body);
        for (let i = 0; i < content.length; i++) {
          displayMessage(
            content[i].msg,
            content[i].sender === recipient ? "received" : "sent"
          );
        }
      })
      .catch((error) => {
        console.error("Error fetching past conversations:", error);
        displayMessage("Failed to load past messages", "received");
      });
  }

  function displayMessage(message, type) {
    var div = document.createElement("div");
    div.textContent = message;
    div.className = "message " + type;
    document.getElementById("messages").appendChild(div);
  }

  return (
    <>
      <h2>Student Lease chat</h2>
      <input
        type='text'
        id='username'
        placeholder='Enter your name'
        required
        hidden
      />
      {/* <button>Connect</button> */}
      {/* <hr /> */}

      <input
        type='text'
        id='targetUsername'
        placeholder="Enter recipient's name"
        onkeypress='checkEnter(event)'
        disabled='disabled'
        hidden
      />
      <input
        type='text'
        id='message'
        placeholder='Enter message'
        onkeypress='checkEnterMessage(event)'
      />
      <button onClick={sendMessage}>Send Message</button>

      {/* <button onClick={disconnectWebSocket}>Disconnect</button> */}

      <div id='messages'></div>
    </>
  );
};

export default ChatClient;
