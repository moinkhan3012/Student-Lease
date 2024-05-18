import { useState } from "react";
import { registerUser } from "../utils";

const SignUp = () => {
  const [useremail, setUseremail] = useState("");
  return (
    <>
      <h2>Sign Up Form</h2>
      <label htmlFor='email'>Email:</label>
      <input
        type='email'
        id='email'
        name='email'
        onChange={(e) => setUseremail(e.target.value)}
        required
      />

      <label htmlFor='name'>Name:</label>
      <input type='text' id='name' name='name' required />

      <label htmlFor='password'>Password:</label>
      <input type='password' id='password' name='password' required />

      <button type='submit' onClick={() => registerUser(useremail)}>
        Sign Up
      </button>
    </>
  );
};

export default SignUp;
