import { useState } from "react";
import Register from "./components/Register.jsx";
import Login from "./components/Login.jsx";
import VisitorDashboard from "./components/VisitorDashboard.jsx";

const API_URL = "http://127.0.0.1:8001";

function App() {
  const [tokens, setTokens] = useState(null);   
  return (
    <div>
      <h2>Hostel Visitor Register</h2>

      {!tokens && (
        <div>
          <Register apiUrl={API_URL} />
          <hr />
          <Login apiUrl={API_URL} onLogin={setTokens} />
        </div>
      )}

      {tokens && (
        <VisitorDashboard
          apiUrl={API_URL}
          tokens={tokens}
          setTokens={setTokens}
          onLogout={() => setTokens(null)}
        />
      )}
    </div>
  );
}

export default App;
