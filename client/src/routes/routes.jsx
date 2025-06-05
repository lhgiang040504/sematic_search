import { Routes, Route } from "react-router-dom";

import ChatbotManagement from "../pages/ChatbotManagement";

function AppRouter() {
  return (
    <Routes>
      <Route path="/chatbot-management" element={<ChatbotManagement />} />
    </Routes>
  );
}

export default AppRouter;