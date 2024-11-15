document.addEventListener("DOMContentLoaded", function() {
  const chatForm = document.getElementById("chat-form");
  const messageInput = document.getElementById("message-input");
  const chatBox = document.getElementById("chat-box");

  // Scroll chat box to the bottom
  function scrollToBottom() {
    chatBox.scrollTop = chatBox.scrollHeight;
  }

  // Append a message to the chat box
  function appendMessage(username, profilePic, content, timestamp, isCurrentUser = false) {
    const messageDiv = document.createElement("div");
    messageDiv.className = "flex items-start space-x-4 " + (isCurrentUser ? "justify-end" : "");

    // Profile picture
    if (!isCurrentUser) {
      const img = document.createElement("img");
      img.src = profilePic;
      img.alt = "User Avatar";
      img.className = "w-10 h-10 rounded-full";
      messageDiv.appendChild(img);
    }

    // Message content
    const messageContent = document.createElement("div");
    messageContent.className = isCurrentUser ? "text-right" : "";

    const userLabel = document.createElement("p");
    userLabel.className = "text-sm font-semibold text-gray-200";
    userLabel.textContent = username;
    messageContent.appendChild(userLabel);

    const messageBubble = document.createElement("div");
    messageBubble.className = (isCurrentUser ? "bg-blue-600" : "bg-gray-700") + " text-gray-200 rounded-lg p-3 max-w-xs";
    messageBubble.innerHTML = `<p>${content}</p>`;
    messageContent.appendChild(messageBubble);

    const timeLabel = document.createElement("p");
    timeLabel.className = "text-xs text-gray-400 mt-1";
    timeLabel.textContent = timestamp;
    messageContent.appendChild(timeLabel);

    messageDiv.appendChild(messageContent);

    // Current user's profile picture
    if (isCurrentUser) {
      const img = document.createElement("img");
      img.src = profilePic;
      img.alt = "User Avatar";
      img.className = "w-10 h-10 rounded-full";
      messageDiv.appendChild(img);
    }

    chatBox.appendChild(messageDiv);
    scrollToBottom();
  }

  // Handle form submission
  chatForm.addEventListener("submit", function(event) {
    event.preventDefault();
    const message = messageInput.value.trim();
    if (message === "") return;

    fetch("{% url 'send_message' recipient.id %}", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": "{{ csrf_token }}"
      },
      body: JSON.stringify({ content: message })
    })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        appendMessage("{{ request.user.username }}", "{{ request.user.profile.profile_pic.url }}", message, "Just now", true);
        messageInput.value = "";
      } else {
        alert("Failed to send message.");
      }
    })
    .catch(error => {
      console.error("Error sending message:", error);
    });
  });
  
  scrollToBottom();  // Scroll to the bottom initially
});

document.addEventListener("DOMContentLoaded", function() {
    const chatBox = document.getElementById("chat-box");

    // Scroll chat box to the bottom
    function scrollToBottom() {
    chatBox.scrollTop = chatBox.scrollHeight;
    }

    // Append a message to the chat box
    function appendMessage(username, profilePic, content, timestamp, isCurrentUser = false) {
    const messageDiv = document.createElement("div");
    messageDiv.className = "flex items-start space-x-4 " + (isCurrentUser ? "justify-end" : "");

    // Profile picture
    if (!isCurrentUser) {
        const img = document.createElement("img");
        img.src = profilePic;
        img.alt = "User Avatar";
        img.className = "w-10 h-10 rounded-full";
        messageDiv.appendChild(img);
    }

    // Message content
    const messageContent = document.createElement("div");
    messageContent.className = isCurrentUser ? "text-right" : "";

    const userLabel = document.createElement("p");
    userLabel.className = "text-sm font-semibold text-gray-200";
    userLabel.textContent = username;
    messageContent.appendChild(userLabel);

    const messageBubble = document.createElement("div");
    messageBubble.className = (isCurrentUser ? "bg-blue-600" : "bg-gray-700") + " text-gray-200 rounded-lg p-3 max-w-xs";
    messageBubble.innerHTML = `<p>${content}</p>`;
    messageContent.appendChild(messageBubble);

    const timeLabel = document.createElement("p");
    timeLabel.className = "text-xs text-gray-400 mt-1";
    timeLabel.textContent = timestamp;
    messageContent.appendChild(timeLabel);

    messageDiv.appendChild(messageContent);

    // Current user's profile picture
    if (isCurrentUser) {
        const img = document.createElement("img");
        img.src = profilePic;
        img.alt = "User Avatar";
        img.className = "w-10 h-10 rounded-full";
        messageDiv.appendChild(img);
    }

    chatBox.appendChild(messageDiv);
    }

    // Fetch messages from server
    function fetchMessages() {
    fetch("{% url 'fetch_messages' recipient.id %}")
        .then(response => response.json())
        .then(data => {
        if (data.success) {
            chatBox.innerHTML = ""; // Clear current messages
            data.messages.forEach(message => {
            const isCurrentUser = message.sender === "{{ request.user.username }}";
            appendMessage(
                message.sender,
                message.sender_profile_pic,
                message.content,
                message.timestamp,
                isCurrentUser
            );
            });
            scrollToBottom(); // Scroll to the latest message
        }
        })
        .catch(error => console.error("Error fetching messages:", error));
    }

    // Periodically fetch new messages every second
    setInterval(fetchMessages, 1000);

    // Scroll to bottom initially
    scrollToBottom();
});