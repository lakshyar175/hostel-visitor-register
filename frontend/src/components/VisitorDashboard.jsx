import { useState, useEffect } from "react";

function VisitorDashboard({ apiUrl, setPage }) {
  const [visitors, setVisitors] = useState(null);
  const [message, setMessage] = useState("");

  function logout() {
    localStorage.clear();
    setPage("login");
  }

  async function loadVisitors() {
    const get = (token) =>
      fetch(apiUrl + "/visitors", { headers: { Authorization: "Bearer " + token } });
    try {
      let res = await get(localStorage.getItem("access_token"));

      if (res.status === 401) {
        // access token expired, get a new one using the refresh token
        const r = await fetch(apiUrl + "/refresh", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ refresh_token: localStorage.getItem("refresh_token") }),
        });
        if (!r.ok) return logout();
        const t = await r.json();
        localStorage.setItem("access_token", t.access_token);
        res = await get(t.access_token);
      }

      const data = await res.json();
      if (res.ok) setVisitors(data);
      else setMessage(data.detail);
    } catch {
      setMessage("Cannot connect to the server");
    }
  }

  useEffect(() => {
    loadVisitors();
  }, []);

  return (
    <div>
      <h3>Visitor Dashboard</h3>
      <button onClick={logout}>Logout</button>
      {message && <p>{message}</p>}
      {visitors && visitors.length === 0 && <p>No visitor records found.</p>}
      {visitors && visitors.length > 0 && (
        <table border="1" cellPadding="6">
          <thead>
            <tr>
              <th>Visitor</th><th>Student</th><th>Room</th><th>Purpose</th><th>Date</th>
            </tr>
          </thead>
          <tbody>
            {visitors.map((v) => (
              <tr key={v.id}>
                <td>{v.visitor_name}</td>
                <td>{v.student_name}</td>
                <td>{v.room_no}</td>
                <td>{v.purpose}</td>
                <td>{v.visit_date}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default VisitorDashboard;