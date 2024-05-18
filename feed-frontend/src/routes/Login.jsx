import { useState } from "react";
import { authenticateUser } from "../utils";
import { useNavigate } from "react-router-dom";

const Login = () => {
  const navigate = useNavigate();
  const [username, setUsername] = useState("");
  return (
    <>
      <label htmlFor='username'>Username:</label>
      <input
        type='text'
        id='username'
        name='username'
        onChange={(e) => setUsername(e.target.value)}
        required
      />

      <label htmlFor='password'>Password:</label>
      <input type='password' id='password' name='password' required />

      <button
        type='submit'
        onClick={() => authenticateUser(navigate, username)}
      >
        Login
      </button>
    </>
  );
};

export default Login;
