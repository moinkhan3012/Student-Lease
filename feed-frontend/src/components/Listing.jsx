import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/listing.css";
import { UPDATE_CLICKS_URL } from "../constants";

const Listing = ({ listingDetails, isSublet }) => {
  // console.log("listing details", listingDetails);
  const image = listingDetails.base64_images[0];
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
  const updateClicks = async (listingId) => {
    // console.log("updating click");
    // const reqBody = { listingId: listingId };
    // fetch(UPDATE_CLICKS_URL, {
    //   method: "POST",
    //   headers: {
    //     "Content-Type": "application/json",
    //   },
    //   body: JSON.stringify(reqBody),
    // })
    //   .then((res) => res.json())
    //   .then((data) => console.log(data));
  };
  const viewSublease = () => {
    updateClicks(listingDetails.id);
    navigate("/view-listing", {
      state: { listingDetails: listingDetails, isSublet: isSublet },
    });
  };
  return (
    <>
      <div className='listing-container' onClick={viewSublease}>
        <img
          className='listing-image'
          src={`data:image/png;base64,${image}`}
          alt='listing image'
        />
        <div id='listing-details-container'>
          <div className='listing-address'>{listingDetails.address}</div>
          <div className='beds-and-distance'>
            {isSublet ? bedsAndDistance : listingDetails.title}
          </div>
          {isSublet && (
            <div className='listing-dateAvailable'>
              Date available: {listingDetails.dateAvailable}
            </div>
          )}
          <div className='monthlyRent'>
            {isSublet
              ? "$" + listingDetails.monthlyRent + "/month"
              : "$" + listingDetails.price}
          </div>
          {/* <img
            src={require(isLiked
              ? "../resources/logo-liked.png"
              : "../resources/logo-like.png")}
            alt=''
            className='like-button'
            onClick={likeUnlike}
          /> */}
        </div>
      </div>
    </>
  );
};

export default Listing;
