import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { AuthProvider } from "./auth/AuthContext";
import RequireAuth from "./auth/RequireAuth";
import Navbar from "./components/NavBar";
import Login from "./pages/Login";


export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Navbar /> {/* 👈 Always visible */}

        <Routes>
          <Route path="/login" element={<Login />} />

          <Route
            path="/"
            element={
              <RequireAuth>
              
              </RequireAuth>
            }
          />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}
