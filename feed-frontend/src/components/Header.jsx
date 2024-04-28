import { useNavigate } from "react-router-dom";
import "../styles/header.css";

export default function Header() {
  const navigate = useNavigate();
  return (
    <div className='header' onClick={() => navigate("/")}>
      Student Lease
    </div>
  );
}
