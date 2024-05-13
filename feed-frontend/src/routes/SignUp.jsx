import { registerUser } from "../utils";

const SignUp = () => {
  return (
    <>
      <h2>Sign Up Form</h2>
      <label htmlFor='email'>Email:</label>
      <input type='email' id='email' name='email' required />

      <label htmlFor='name'>Name:</label>
      <input type='text' id='name' name='name' required />

      <label htmlFor='password'>Password:</label>
      <input type='password' id='password' name='password' required />

      <button type='submit' onClick={registerUser}>
        Sign Up
      </button>
    </>
  );
};

export default SignUp;
