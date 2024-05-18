import { useNavigate } from "react-router-dom";
import "../styles/post-listing.css";
import { useEffect } from "react";
import { getCookieValue } from "../utils";

const ListingType = () => {
  const navigate = useNavigate();
  useEffect(() => {
    document.title = "Student Lease | Select listing type";
  }, []);
  return (
    <div className='background'>
      <div className='sublet-title-text'>
        List your sublet. Screen tenants <br />
        Sign a lease. Get paid
      </div>
      <div className='sublet-subtitle-text'>
        All in one with StudentLease Sublet Manager
      </div>
      <div className='choose-listing-type'>
        <a
          href=''
          className='sublet-button marketplace-listing'
          onClick={() => navigate("/marketplace-listing")}
        >
          Marketplace listing
        </a>
        <a
          onClick={() => navigate("/create-property-listing")}
          className='sublet-button property-listing'
        >
          Property listing
        </a>
      </div>
    </div>
  );
};

export default ListingType;
