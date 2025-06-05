import axios from "../axios";

class ChatbotAPI {
  /**
   * Sends a message payload to the chatbot and retrieves a response.
   * @param {Object} options - The request payload containing the chat history.
   * @returns {Promise<Object>} The chatbot's response.
   */
  postChatbotResponse = async (options = {}) => {
    try {
      const response = await axios.post("/api/chat", options);
      return response;
    } catch (error) {
      console.error("Error in postChatbotResponse:", error);
      throw error;
    }
  };
}

const ApiChatbot = new ChatbotAPI();
export default ApiChatbot;