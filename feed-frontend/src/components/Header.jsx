import { useNavigate } from "react-router-dom";
import "../styles/header.css";

export default function Header() {
  const navigate = useNavigate();
  return (
    <>
      <div className='header-container'>
        <span className='header' onClick={() => navigate("/")}>
          Student Lease
        </span>
        <img
          className='white-background-logo'
          onClick={() => navigate("/")}
          src={require("../resources/logo-white-background.png")}
          alt=''
        />
      </div>
    </>
  );
}
