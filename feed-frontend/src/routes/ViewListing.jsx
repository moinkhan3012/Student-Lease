import { useEffect, useState } from "react";
import { Header, Footer } from "../components";
import "../styles/view-listing.css";
import { useLocation } from "react-router-dom";

const ViewListing = () => {
  const [images, setImages] = useState([
    // "https://via.placeholder.com/50",
    // "https://via.placeholder.com/1000",
  ]);
  const [imagesIndex, setImagesIndex] = useState(0);
  const [address, setAddress] = useState("");
  const [price, setPrice] = useState("");
  const [bedrooms, setBedrooms] = useState("");
  const [bathrooms, setBathrooms] = useState("");
  const { state } = useLocation();
  const isSublet = state.isSublet;
  // console.log(state);
  // console.log(state.listingDetails, isSublet);
  useEffect(() => {
    document.title = "Student Lease | View Listing";
    setAddress(state.listingDetails.address);
    setPrice(
      isSublet ? state.listingDetails.monthlyRent : state.listingDetails.price
    );
    if (isSublet) {
      setBedrooms(state.listingDetails.bedrooms);
      setBathrooms(state.listingDetails.bathrooms);
    }
    setImages(state.listingDetails.base64_images);
  }, []);
  return (
    <>
      <Header />
      <div className='view-container'>
        <div className='listing-view-images'>
          <img
            id='listing-image'
            src={`data:image/png;base64,${images[imagesIndex]}`}
            alt='Listimg image'
          />
          <img
            id='scroll-listing-image-right'
            className='listing-image-scroll'
            src={require("../resources/right-arrow-white.png")}
            alt=''
            onClick={() => setImagesIndex((imagesIndex + 1) % images.length)}
          />
          <img
            id='scroll-listing-image-left'
            className='listing-image-scroll'
            src={require("../resources/left-arrow-white.png")}
            alt=''
            onClick={() =>
              setImagesIndex(
                imagesIndex == 0 ? images.length - 1 : imagesIndex - 1
              )
            }
          />
        </div>
        <div className='listing-view-info'>
          <div className='listing-view-address'>
            {!isSublet && `${state.listingDetails.title} at `}
            {address}
          </div>
          <div className='listing-price'>${price}</div>
          {isSublet && (
            <div className='listing-specific-details'>
              <div className='listing-bedroom-count'>
                <img
                  src={require("../resources/room.png")}
                  id='room-logo'
                  alt=''
                />
                <br />
                {bedrooms} bedrooms
              </div>
              <div className='listing-baths-count'>
                <img
                  src={require("../resources/bath.png")}
                  id='bath-logo'
                  alt=''
                />
                <br />
                {bathrooms} baths
              </div>
            </div>
          )}
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
