import React, { useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { fetchMe, login } from "../api/auth";
import { useAuth } from "../auth/AuthContext";

type LocationState = { from?: { pathname?: string } };

export default function Login() {
  const [username, setUsername] = useState<string>("hans");
  const [password, setPassword] = useState<string>("hans123");
  const [error, setError] = useState<string>("");

  const nav = useNavigate();
  const location = useLocation();
  const { setUser } = useAuth();

  const state = location.state as LocationState | null;
  const from = state?.from?.pathname || "/";

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    try {
      await login(username, password);
      const me = await fetchMe();
      setUser(me);
      nav(from, { replace: true });
    } catch {
      setError("Invalid username or password");
    }
  };

  return (
    <div style={{ maxWidth: 360, margin: "60px auto" }}>
      <h2>Login</h2>
      <form onSubmit={onSubmit}>
        <div style={{ marginBottom: 10 }}>
          <label>Username</label>
          <input
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            style={{ width: "100%" }}
            autoComplete="username"
          />
        </div>

        <div style={{ marginBottom: 10 }}>
          <label>Password</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            style={{ width: "100%" }}
            autoComplete="current-password"
          />
        </div>

        {error && <div style={{ color: "red", marginBottom: 10 }}>{error}</div>}

        <button type="submit">Sign in</button>
      </form>
    </div>
  );
}
