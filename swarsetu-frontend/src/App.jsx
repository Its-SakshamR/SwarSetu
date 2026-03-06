import React from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";

import Login from "./pages/Login";
import Signup from "./pages/Signup";
import SongsList from "./pages/SongsList";
import Editor from "./pages/Editor";

function PrivateRoute({ children }) {
  const token = localStorage.getItem("token");
  return token ? children : <Navigate to="/login" />;
}

function App() {
  return (
    <BrowserRouter>
      <Routes>

        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />

        <Route
          path="/songs"
          element={
            <PrivateRoute>
              <SongsList />
            </PrivateRoute>
          }
        />

        <Route
          path="/editor/:songId"
          element={
            <PrivateRoute>
              <Editor />
            </PrivateRoute>
          }
        />

        <Route path="*" element={<Navigate to="/songs" />} />

      </Routes>
    </BrowserRouter>
  );
}

export default App;