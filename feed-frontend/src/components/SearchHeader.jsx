import { useNavigate } from "react-router-dom";
import { useState } from "react";
import { logout } from "../utils";
import "../styles/search-header.css";

const SearchHeader = ({ onClick, isSublet }) => {
  const navigate = useNavigate();
  const [showLogoutButton, setShowLogoutButton] = useState(false);
  const [listingSearchQuery, setListingSearchQuery] = useState({
    location: "",
    bedrooms: "",
    bathrooms: "",
    monthlyRent: "",
    dateAvailable: "",
    leaseDuration: "",
  });
  const [marketplacesearchQuery, setMarketplaceSearchQuery] = useState({
    location: "",
    price: "",
    label: "",
  });
  return (
    <>
      <div className='search-header-container'>
        <div>
          <input
            className='address-search'
            type='text'
            placeholder='Search address...'
            onChange={(e) => {
              setListingSearchQuery({
                ...listingSearchQuery,
                location: e.target.value,
              });
              setMarketplaceSearchQuery({
                ...marketplacesearchQuery,
                location: e.target.value,
              });
            }}
          />
          <span
            className='btn-search'
            onClick={() =>
              onClick(isSublet ? listingSearchQuery : marketplacesearchQuery)
            }
          >
            Search
          </span>
        </div>
        <img
          className='white-background-logo'
          onClick={() => navigate("/")}
          src={require("../resources/logo-white-background.png")}
          alt=''
        />
        <div className='dropdown'>
          <img
            id='profile-image'
            src={require("../resources/user.png")}
            alt=''
            className='profile-image'
            onClick={() => setShowLogoutButton(!showLogoutButton)}
          />
          {showLogoutButton && (
            <div class='user-image-dropdown-content'>
              <a onClick={logout}>Logout</a>
            </div>
          )}
        </div>
      </div>
      <div className='filters-container-parent'>
        <div className='txt-filters'>Filters</div>
        {isSublet && (
          <div className='filters-container'>
            <div className='filter-container bedroom-filter'>
              <div className='filter-title'>Bedrooms</div>
              <input
                type='text'
                className='txt-bedrooms'
                onChange={(e) =>
                  setListingSearchQuery({
                    ...listingSearchQuery,
                    bedrooms: e.target.value,
                  })
                }
              />
            </div>
            <div className='filter-container bathroom-filter'>
              <div className='filter-title'>Bathrooms</div>
              <input
                type='text'
                className='txt-bathrooms'
                onChange={(e) =>
                  setListingSearchQuery({
                    ...listingSearchQuery,
                    bathrooms: e.target.value,
                  })
                }
              />
            </div>
            <div className='filter-container monthlyRent-filter'>
              <div className='filter-title'>Monthly rent</div>
              <input
                type='text'
                className='txt-monthlyRent'
                onChange={(e) =>
                  setListingSearchQuery({
                    ...listingSearchQuery,
                    monthlyRent: e.target.value,
                  })
                }
              />
            </div>
            <div className='filter-container dateAvailable-filter'>
              <div className='filter-title'>Date available</div>
              <input
                type='date'
                className='txt-dateAvailable'
                onChange={(e) =>
                  setListingSearchQuery({
                    ...listingSearchQuery,
                    dateAvailable: e.target.value,
                  })
                }
              />
            </div>
            <div className='filter-container duration-filter'>
              <div className='filter-title'>Lease duration (in months)</div>
              <input
                type='text'
                className='txt-leaseDuration'
                onChange={(e) =>
                  setListingSearchQuery({
                    ...listingSearchQuery,
                    leaseDuration: e.target.value,
                  })
                }
              />
            </div>
          </div>
        )}
        {!isSublet && (
          <div className='filters-container'>
            <div className='filter-container price-filter'>
              <div className='filter-title'>Price</div>
              <input
                type='text'
                className='txt-price'
                onChange={(e) =>
                  setMarketplaceSearchQuery({
                    ...marketplacesearchQuery,
                    price: e.target.value,
                  })
                }
              />
            </div>
            <div className='filter-container label-filter'>
              <div className='filter-title'>Label</div>
              <input
                type='text'
                className='txt-label'
                onChange={(e) =>
                  setMarketplaceSearchQuery({
                    ...marketplacesearchQuery,
                    label: e.target.value,
                  })
                }
              />
            </div>
          </div>
        )}
      </div>
    </>
  );
};
export default SearchHeader;
