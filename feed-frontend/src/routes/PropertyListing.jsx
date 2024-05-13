import { useLocation, useNavigate } from "react-router-dom";
import { Header, Footer } from "../components";
import { useEffect, useState } from "react";
import { getBase64 } from "../utils";
import "../styles/header.css";
import "../styles/property-listing.css";
import { CREATE_SUBLET_URL } from "../constants";

const PropertyListing = () => {
  useEffect(() => {
    document.title = "Student Lease | Add property details";
  });
  const navigate = useNavigate();
  const { state } = useLocation();
  const { address, unitNumber, propertyType } = state;
  const [monthlyRent, setMonthlyRent] = useState("0");
  const [securityDeposit, setSecurityDeposit] = useState("0");
  const [bedrooms, setBedrooms] = useState("0");
  const [bathrooms, setBathrooms] = useState("0");
  const [area, setArea] = useState("0");
  const [dateAvailable, setDateAvailable] = useState("");
  const [leaseDuration, setLeaseDuration] = useState("");
  const [laundry, setLaundry] = useState();
  const [description, setDescription] = useState("");
  const [ac, setAc] = useState(false);
  const [balconyOrDeck, setBalconyOrDeck] = useState(false);
  const [furnished, setfurnished] = useState(false);
  const [hardwoodFloor, setHardwoodFloor] = useState(false);
  const [wheelchairAccess, setWheelchairAccess] = useState(false);
  const [garageParking, setGarageParking] = useState(false);
  const [offStreetParking, setOffStreetParking] = useState(false);
  const [preferenceMale, setPreferenceMale] = useState(false);
  const [preferenceFemale, setPreferenceFemale] = useState(false);
  const [nonBinary, setNonBinary] = useState(false);
  const [smoker, setSmoker] = useState(false);
  const [nonSmoker, setNonSmoker] = useState(false);
  const [vegetarian, setVegetarian] = useState(false);
  const [nonVegetarian, setnonVegetarian] = useState(false);
  const [images, setImages] = useState([]);
  const setUploadedImages = (files) => {
    let base64ImagesList = [];
    [...files].map((file) => {
      getBase64(file).then((base64File) => base64ImagesList.push(base64File));
    });
    setImages(base64ImagesList);
  };
  const createListing = () => {
    const reqBody = {
      monthlyRent: parseInt(monthlyRent),
      securityDeposit: parseInt(securityDeposit),
      bedrooms: parseInt(bedrooms),
      bathrooms: parseInt(bathrooms),
      squareFeet: parseInt(area),
      dateAvailable: dateAvailable,
      leaseDuration: parseInt(leaseDuration),
      amenities: {
        laundry: laundry,
        ac: ac,
        balconyOrDeck: balconyOrDeck,
        furnished: furnished,
        hardwoodFloor: hardwoodFloor,
        wheelchairAccess: wheelchairAccess,
        garageParking: garageParking,
        offStreetParking: offStreetParking,
      },
      preferences: {
        preferenceMale: preferenceMale,
        preferenceFemale: preferenceFemale,
        nonBinary: nonBinary,
        smoker: smoker,
        nonSmoker: nonSmoker,
        vegetarian: vegetarian,
        nonVegetarian: nonVegetarian,
      },
      detailedDescription: description,
      images: images,
      address: address + ", " + unitNumber,
      roomType: propertyType,
      title: address + ", " + unitNumber,
    };
    console.log("Request body:", reqBody);
    fetch(CREATE_SUBLET_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ reqBody }),
    })
      .then((res) => {
        res
          .json()
          .then((data) => console.log("Response body", JSON.parse(data.body)));
      })
      .catch((error) => console.log("Error while processing", error));
  };
  return (
    <>
      <Header />
      <div className='my-properties-back'>
        <img
          className='back-arrow'
          src={require("../resources/left-arrow.png")}
          alt=''
        />
        <a
          className='properties-page'
          onClick={() => navigate("/create-property-listing")}
        >
          {" "}
          Add a property
        </a>
      </div>
      <div className='listing-info'>
        <div className='listing-info-header-text'>Listing Information</div>
        <label htmlFor='files'>Select images:</label>
        <input
          type='file'
          id='files'
          name='files'
          multiple
          onChange={(e) => setUploadedImages(e.target.files)}
        />
        <div className='property-detail-field'>
          <div className='property-detail-field-title'>Monthly rent</div>
          <input type='text' onChange={(e) => setMonthlyRent(e.target.value)} />
        </div>
        <div className='property-detail-field'>
          <div className='property-detail-field-title'>Security deposit</div>
          <input
            type='text'
            onChange={(e) => setSecurityDeposit(e.target.value)}
          />
        </div>
        <div className='horizontal-box'>
          <div className='property-detail-field'>
            <div className='property-detail-field-title'>Bedrooms</div>
            <input type='text' onChange={(e) => setBedrooms(e.target.value)} />
          </div>
          <div className='property-detail-field horizontal-flex-grow'>
            <div className='property-detail-field-title'>Bathrooms</div>
            <input type='text' onChange={(e) => setBathrooms(e.target.value)} />
          </div>
          <div className='property-detail-field horizontal-flex-grow'>
            <div className='property-detail-field-title'>Area (in sqft)</div>
            <input type='text' onChange={(e) => setArea(e.target.value)} />
          </div>
        </div>
        <div className='property-detail-field'>
          <div className='property-detail-field-title'>Date available</div>
          <input
            type='date'
            onChange={(e) => setDateAvailable(e.target.value)}
          />
        </div>
        <div className='property-detail-field'>
          <div className='property-detail-field-title'>
            Lease duration (in months)
          </div>
          <input
            type='text'
            onChange={(e) => setLeaseDuration(e.target.value)}
          />
        </div>

        <div className='horizontal-box'>
          <div>
            <div className='listing-info-header-text'>Amenities</div>
            <input
              type='checkbox'
              id='amenity1'
              name='amenity1'
              value='ac'
              onChange={(e) => setAc(e.target.checked)}
            />

            <label htmlFor='amenity1'>A/C</label>
            <br />
            <input
              type='checkbox'
              id='amenity2'
              name='amenity2'
              value='balcony'
              onChange={(e) => setBalconyOrDeck(e.target.checked)}
            />
            <label htmlFor='amenity2'>Balcony or deck</label>
            <br />
            <input
              type='checkbox'
              id='amenity3'
              name='amenity3'
              value='furnished'
              onChange={(e) => setfurnished(e.target.checked)}
            />
            <label htmlFor='amenity3'>Furnished</label>
            <br />
            <input
              type='checkbox'
              id='amenity4'
              name='amenity4'
              value='floor'
              onChange={(e) => setHardwoodFloor(e.target.checked)}
            />
            <label htmlFor='amenity4'>Hardwood floor</label>
            <br />
            <input
              type='checkbox'
              id='amenity5'
              name='amenity5'
              value='wheelchair'
              onChange={(e) => setWheelchairAccess(e.target.checked)}
            />
            <label htmlFor='amenity5'>Wheelchair access</label>
            <br />
            <input
              type='checkbox'
              id='amenity6'
              name='amenity6'
              value='garage-parking'
              onChange={(e) => setGarageParking(e.target.checked)}
            />
            <label htmlFor='amenity6'>Garage parking</label>
            <br />
            <input
              type='checkbox'
              id='amenity7'
              name='amenity7'
              value='off-street-parking'
              onChange={(e) => setOffStreetParking(e.target.checked)}
            />
            <label htmlFor='amenity7'>Off-street parking</label>
            <br />
          </div>
          <div className='horizontal-flex-grow-prefs'>
            <div className='listing-info-header-text'>Preferences</div>
            <input
              type='checkbox'
              id='preference1'
              name='preference1'
              value='male'
              onChange={(e) => setPreferenceMale(e.target.checked)}
            />
            <label htmlFor='preference1'>Male</label>
            <br />
            <input
              type='checkbox'
              id='preference2'
              name='preference2'
              value='female'
              onChange={(e) => setPreferenceFemale(e.target.checked)}
            />
            <label htmlFor='preference2'>Female</label>
            <br />
            <input
              type='checkbox'
              id='preference3'
              name='preference3'
              value='non-binary'
              onChange={(e) => setNonBinary(e.target.checked)}
            />
            <label htmlFor='preference3'>Non binary</label>
            <br />
            <input
              type='checkbox'
              id='preference4'
              name='preference4'
              value='smoker'
              onChange={(e) => setSmoker(e.target.checked)}
            />
            <label htmlFor='preference4'>Smoker</label>
            <br />
            <input
              type='checkbox'
              id='preference5'
              name='preference5'
              onChange={(e) => setNonSmoker(e.target.checked)}
              value='non-smoker'
            />
            <label htmlFor='preference5'>Non smoker</label>
            <br />
            <input
              type='checkbox'
              id='preference6'
              name='preference6'
              value='vegetarian'
              onChange={(e) => setVegetarian(e.target.checked)}
            />
            <label htmlFor='preference6'>Vegetarian</label>
            <br />
            <input
              type='checkbox'
              id='preference7'
              name='preference7'
              value='non-vegetarian'
              onChange={(e) => setnonVegetarian(e.target.checked)}
            />
            <label htmlFor='non-vegetarian'>Non vegetarian</label>
            <br />
          </div>
        </div>

        <div className='listing-info-header-text'>Laundry</div>
        <input
          type='radio'
          name='fav_language'
          value='none'
          onChange={(e) => setLaundry(e.target.value)}
        />
        <label htmlFor='html'>None</label>
        <br />
        <input
          type='radio'
          name='fav_language'
          value='in-unit'
          onChange={(e) => setLaundry(e.target.value)}
        />
        <label htmlFor='css'>In unit</label>
        <div className='listing-info-header-text'>Detailed description</div>
        <div className='property-detail-field-title'>About the property</div>
        <textarea
          className='property-description'
          onChange={(e) => setDescription(e.target.value)}
        ></textarea>
        <br />
        <a className='publish-listing' onClick={createListing}>
          Publish listing
        </a>
      </div>
      <div className='property-listing-footer'>
        <Footer />
      </div>
    </>
  );
};

export default PropertyListing;
