import { useState } from "react";
// import Register from "./components/Register.jsx";
import Login from "./components/Login.jsx";
import VisitorDashboard from "./components/VisitorDashboard.jsx";

const API_URL = "http://127.0.0.1:8001";

function App() {
  const [page, setPage] = useState(
    localStorage.getItem("access_token") ? "dashboard" : "login"
  );

  return (
    <div>
      <h2>Hostel Visitor Register</h2>
      {page === "register" && <Register apiUrl={API_URL} setPage={setPage} />}
      {page === "login" && <Login apiUrl={API_URL} setPage={setPage} />}
      {page === "dashboard" && <VisitorDashboard apiUrl={API_URL} setPage={setPage} />}
    </div>
  );
}

export default App;