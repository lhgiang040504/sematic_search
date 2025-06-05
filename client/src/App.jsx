import { AppBar, Toolbar, Typography, Box, Button } from "@mui/material";
import { BrowserRouter as Router, Link } from "react-router-dom";
import AppRouter from "./routes/routes";
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

function App() {
  return (
    <Router>
      <Box sx={{ flexGrow: 1, height: "100vh" }}>
        {/* Header */}
        <AppBar position="static">
          <Toolbar>
            <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
              My Application
            </Typography>
            <Button color="inherit" component={Link} to="/chatbot-management">
              Assistant
            </Button>
          </Toolbar>
        </AppBar>

        {/* Content */}
        <Box sx={{ padding: 2, height: "calc(100vh - 64px)" }}>
          <AppRouter />
        </Box>

        <ToastContainer
          position="top-right"
          autoClose={1000}
          hideProgressBar={false}
          newestOnTop={false}
          closeOnClick
          rtl={false}
          pauseOnFocusLoss
          draggable
          pauseOnHover
        />
      </Box>
    </Router>
  );
}

export default App;