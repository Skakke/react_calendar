import React from "react";
import AppNavBar from "./components/NavBar";

const App: React.FC = () => {
  return (
    <>
      <AppNavBar brand="ToDO WEB" />

      <main style={{ padding: "20px" }}>
        <h1>Welcome to the Calendar App</h1>
        <p>This is your main page content.</p>
      </main>
    </>
  );
};

export default App;
