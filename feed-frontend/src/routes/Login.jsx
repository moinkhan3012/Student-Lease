import { authenticateUser } from "../utils";

const Login = () => {
  return (
    <>
      <label for='username'>Username:</label>
      <input type='text' id='username' name='username' required />

      <label for='password'>Password:</label>
      <input type='password' id='password' name='password' required />

      <button type='submit' onClick={authenticateUser}>
        Login
      </button>
    </>
  );
};

export default Login;
