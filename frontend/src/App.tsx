import { BrowserRouter, Routes, Route } from "react-router-dom";
import { AuthProvider } from "./auth/AuthContext";
import RequireAuth from "./auth/RequireAuth";
import Navbar from "./components/NavBar";
import Login from "./pages/Login";

function Home() {
  return <div style={{ padding: 20, alignItems: "center"  }}>Welcome 👋 You are logged in.</div>;
}

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Navbar /> {/* Always visible */}

        <Routes>
          <Route path="/login" element={<Login />} />

          <Route
            path="/"
            element={
              <RequireAuth>
                <Home />
              </RequireAuth>
            }
          />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}
