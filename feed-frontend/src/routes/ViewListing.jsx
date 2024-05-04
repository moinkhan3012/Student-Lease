import { useEffect } from "react";
import { Header, Footer } from "../components";
import "../styles/view-listing.css";

const ViewListing = ({ listingDetails, isSublet }) => {
  useEffect(() => {
    document.title = "Student Lease | View Listing";
  }, []);
  return (
    <>
      <Header />
      <div className='view-container'>
        <div className='listing-view-images'>
          <img src={require("../resources/home.png")} alt='' />
        </div>
        <div className='listing-view-info'>
          <div className='listing-view-address'>73 Cornelia Street, #7</div>
          <div className='listing-price'>$3300</div>
          <div className='listing-specific-details'>
            <div className='listing-bedroom-count'>
              <img
                src={require("../resources/room.png")}
                id='room-logo'
                alt=''
              />
              <br />1 room
            </div>
            <div className='listing-baths-count'>
              <img
                src={require("../resources/bath.png")}
                id='bath-logo'
                alt=''
              />
              <br />1 bath
            </div>
          </div>
          <div className='listing-owner'>
            Listed by <br />
            <div className='listing-owner-info'>
              <img
                src={require("../resources/user.png")}
                alt=''
                id='listing-profile-image'
              />
              <div className='listing-username'>Peter Bailey</div>
            </div>
            <div className='listing-owner-chat'>Click to ask a question</div>
          </div>
        </div>
      </div>
      <div className='footer-listing'>
        <Footer />
      </div>
    </>
  );
};

export default ViewListing;
