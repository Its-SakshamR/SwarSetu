import React, { useState } from "react";
import API from "../api/api";
import { useNavigate } from "react-router-dom";

function Login() {

  const navigate = useNavigate();

  const [username,setUsername] = useState("");
  const [password,setPassword] = useState("");

  const login = async () => {

    try {

      const res = await API.post("auth/login/",{
        username,
        password
      });

      const token = res.data.token;

      localStorage.setItem("token",token);

      alert("Login successful");

      navigate("/songs");

    } catch (err) {

      console.error(err);
      alert("Login failed");
    }
  };

  return (
    <div>

      <h2>Login</h2>

      <input
        placeholder="Username"
        value={username}
        onChange={(e)=>setUsername(e.target.value)}
      />

      <br/>

      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e)=>setPassword(e.target.value)}
      />

      <br/>

      <button onClick={login}>Login</button>

    </div>
  );
}

export default Login;