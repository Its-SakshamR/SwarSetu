import React, { useState } from "react";
import API from "../api/api";
import { useNavigate } from "react-router-dom";

function Signup() {

  const navigate = useNavigate();

  const [username,setUsername] = useState("");
  const [password,setPassword] = useState("");

  const signup = async () => {

    try {

      await API.post("auth/signup/",{
        username,
        password
      });

      alert("Account created!");

      navigate("/login");

    } catch {
      alert("Signup failed");
    }
  };

  return (
    <div>

      <h2>Signup</h2>

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

      <button onClick={signup}>Signup</button>

    </div>
  );
}

export default Signup;