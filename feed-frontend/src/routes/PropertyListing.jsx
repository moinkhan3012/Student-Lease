import { useNavigate } from "react-router-dom";
import Header from "../components/Header";
import "../styles/header.css";
import "../styles/property-details.css";

const PropertyListing = () => {
  const navigate = useNavigate();
  return (
    <>
      <Header />
      <div className='my-properties-back'>
        <img
          className='back-arrow'
          src={require("../resources/left-arrow.png")}
          alt=''
        />
        <a className='properties-page' onClick={() => navigate("/listing")}>
          {" "}
          Add a property
        </a>
      </div>
      <div className='listing-info'>
        <div className='listing-info-header-text'>Listing Information</div>
        <div className='property-detail-field'>
          <div className='property-detail-field-title'>Monthly rent</div>
          <input type='text' />
        </div>
        <div className='property-detail-field'>
          <div className='property-detail-field-title'>Security deposit</div>
          <input type='text' />
        </div>
        <div className='horizontal-box'>
          <div className='property-detail-field'>
            <div className='property-detail-field-title'>Bedrooms</div>
            <input type='text' />
          </div>
          <div className='property-detail-field horizontal-flex-grow'>
            <div className='property-detail-field-title'>Bathrooms</div>
            <input type='text' />
          </div>
          <div className='property-detail-field horizontal-flex-grow'>
            <div className='property-detail-field-title'>Area (in sqft)</div>
            <input type='text' />
          </div>
        </div>
        <div className='property-detail-field'>
          <div className='property-detail-field-title'>Date available</div>
          <input type='date' />
        </div>
        <div className='property-detail-field'>
          <div className='property-detail-field-title'>Lease duration</div>
          <input type='text' />
        </div>

        <div className='horizontal-box'>
          <div>
            <div className='listing-info-header-text'>Amenities</div>
            <input type='checkbox' id='amenity1' name='amenity1' value='ac' />
            <label for='amenity1'>A/C</label>
            <br />
            <input
              type='checkbox'
              id='amenity2'
              name='amenity2'
              value='balcony'
            />
            <label for='amenity2'>Balcony or deck</label>
            <br />
            <input
              type='checkbox'
              id='amenity3'
              name='amenity3'
              value='furnished'
            />
            <label for='amenity3'>Furnished</label>
            <br />
            <input
              type='checkbox'
              id='amenity4'
              name='amenity4'
              value='floor'
            />
            <label for='amenity4'>Hardwood floor</label>
            <br />
            <input
              type='checkbox'
              id='amenity5'
              name='amenity5'
              value='wheelchair'
            />
            <label for='amenity5'>Wheelchair access</label>
            <br />
            <input
              type='checkbox'
              id='amenity6'
              name='amenity6'
              value='garage-parking'
            />
            <label for='amenity6'>Garage parking</label>
            <br />
            <input
              type='checkbox'
              id='amenity7'
              name='amenity7'
              value='off-street-parking'
            />
            <label for='amenity7'>Off-street parking</label>
            <br />
          </div>
          <div className='horizontal-flex-grow-prefs'>
            <div className='listing-info-header-text'>Preferences</div>
            <input
              type='checkbox'
              id='preference1'
              name='preference1'
              value='male'
            />
            <label for='preference1'>Male</label>
            <br />
            <input
              type='checkbox'
              id='preference2'
              name='preference2'
              value='female'
            />
            <label for='preference2'>Female</label>
            <br />
            <input
              type='checkbox'
              id='preference3'
              name='preference3'
              value='non-binary'
            />
            <label for='preference3'>Non binary</label>
            <br />
            <input
              type='checkbox'
              id='preference4'
              name='preference4'
              value='smoker'
            />
            <label for='preference4'>Smoker</label>
            <br />
            <input
              type='checkbox'
              id='preference5'
              name='preference5'
              value='non-smoker'
            />
            <label for='preference5'>Non smoker</label>
            <br />
            <input
              type='checkbox'
              id='preference6'
              name='preference6'
              value='vegetarian'
            />
            <label for='preference6'>Vegetarian</label>
            <br />
            <input
              type='checkbox'
              id='preference7'
              name='preference7'
              value='off-street-parking'
            />
            <label for='non-vegetarian'>Non vegetarian</label>
            <br />
          </div>
        </div>
        <div className='listing-info-header-text'>Detailed description</div>
        <div className='property-detail-field-title'>About the property</div>
        <textarea className='property-description'></textarea>
        <br />
        <a href='' className='publish-listing'>
          Publish listing
        </a>
      </div>
    </>
  );
};

export default PropertyListing;
