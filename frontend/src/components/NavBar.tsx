import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../auth/AuthContext";
import { clearToken } from "../api/auth";

export default function Navbar() {
  const { user, setUser } = useAuth();
  const navigate = useNavigate();
  

  const logout = () => {
    clearToken();
    setUser(null);
    navigate("/login");
  };

  return (
    <div
      style={{
        position: "fixed", "top": 0,
        width: "100%",
        padding: "10px 20px",
        background: "#f5f5f5",
        borderBottom: "1px solid #ddd",
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center"
        ,
      }}
    >
      <Link to="/calendar">Calendar</Link>

      {user ? (
        <div>
          <span style={{ marginRight: 10 }}>Hello {user.username}</span>
          <button onClick={logout}>Logout</button>
        </div>
      ) : (
        <Link to="/login">Login</Link>
      )}
    </div>
  );
}

