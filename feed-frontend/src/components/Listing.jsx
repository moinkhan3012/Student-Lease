import { useState } from "react";
import { useNavigate } from "react-router-dom";

const Listing = ({ listingDetails, isSublet }) => {
  const navigate = useNavigate();
  let bedsAndDistance;
  if (isSublet) {
    bedsAndDistance =
      listingDetails.bedrooms +
      " bedrooms , " +
      listingDetails.bathrooms +
      " bathrooms";
  } else {
    bedsAndDistance = listingDetails.distance
      ? listingDetails.distance + " miles"
      : "";
  }
  const [isLiked, setIsLiked] = useState(listingDetails.isLiked);
  const likeUnlike = () => {
    setIsLiked(!isLiked);
    // TODO: Update like unlike in database
  };
  const viewSublease = () => {
    console.log(listingDetails.id);
    // navigate("/view-sublease", { state: { id: listingDetails.id } });
  };
  return (
    <>
      <div className='listing-container'>
        <img
          className='listing-image'
          src={require("../resources/home.png")}
          alt='listing image'
        />
        <div id='listing-details-container'>
          <div className='listing-address'>{listingDetails.address}</div>
          <div className='beds-and-distance'>{bedsAndDistance}</div>
          <div className='listing-dateAvailable'>
            {isSublet && listingDetails.dateAvailable}
          </div>
          <div className='monthlyRent'>
            {isSublet && "$" + listingDetails.monthlyRent + "/month"}
          </div>
          <img
            src={require(isLiked
              ? "../resources/logo-liked.png"
              : "../resources/logo-like.png")}
            alt=''
            className='like-button'
            onClick={likeUnlike}
          />
        </div>
      </div>
    </>
  );
};

export default Listing;
