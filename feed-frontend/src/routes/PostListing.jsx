import { useNavigate } from "react-router-dom";
import "../styles/post-listing.css";
import { useEffect } from "react";

const PostListing = () => {
  const navigate = useNavigate();
  useEffect(() => {
    document.title = "Student Lease | Post listing";
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
          onClick={() => navigate("/search-listing")}
        >
          Search for sublease
        </a>
        <div
          onClick={() => navigate("/listing-type")}
          className='sublet-button property-listing'
        >
          Post your listing
        </div>
      </div>
    </div>
  );
};

export default PostListing;
