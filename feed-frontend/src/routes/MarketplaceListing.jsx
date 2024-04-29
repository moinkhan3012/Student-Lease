import { useNavigate } from "react-router-dom";
import Header from "../components/Header";
import Footer from "../components/Footer";
import "../styles/marketplace-listing.css";

const MarketplaceListing = () => {
  const navigate = useNavigate();
  return (
    <>
      <Header />
      <div className='preview-box'>
        <div className='title-text'>Preview</div>
        <div className='horizontal-line'></div>
        <div className='marketplace-container'>
          <div className='subtitle-text'>Please add your item's info</div>
          <div className='item-details'>
            <div>Title</div>
            <input type='text' className='property-input property-address' />
          </div>
          <div className='item-details'>
            <div>Price</div>
            <input type='text' className='property-input unit-number' />
          </div>
          <div className='item-details'>
            <div>Description</div>
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
    </>
  );
};

export default MarketplaceListing;
