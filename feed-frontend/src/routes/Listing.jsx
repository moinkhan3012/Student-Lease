import { useNavigate } from "react-router-dom";
import Header from "../components/Header";
import Footer from "../components/Footer";
import "../styles/listing.css";
import { useEffect } from "react";

const Listing = () => {
  useEffect(() => {
    document.title = "Student Lease | Add a property";
  });
  const navigate = useNavigate();
  return (
    <div className='container-listing'>
      <Header />
      <div className='add-property'>
        <div className='title-text'>Add a property</div>
        <div className='horizontal-line'></div>
        <div className='property-container'>
          <div className='subtitle-text'>Please add your property's info</div>
          <div className='property-details'>
            <div>Property address</div>
            <input type='text' className='property-input property-address' />
          </div>
          <div className='property-details'>
            <div>Unit number</div>
            <input type='text' className='property-input unit-number' />
          </div>
          <div className='property-details'>
            <div>Property type</div>
            <input type='text' className='property-input property-type' />
          </div>
        </div>
        <div
          onClick={() => navigate("/property-listing")}
          className='btn-create-listing'
        >
          Create listing
        </div>
      </div>
      <div className='footer-listing'>
        <Footer />
      </div>
    </div>
  );
};

export default Listing;
