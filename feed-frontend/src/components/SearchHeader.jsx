import { useNavigate } from "react-router-dom";
import { useState } from "react";
import { logout } from "../utils";
import "../styles/search-header.css";

const SearchHeader = ({ onClick }) => {
  const navigate = useNavigate();
  const [showLogoutButton, setShowLogoutButton] = useState(false);
  const [searchQuery, setSearchQuery] = useState({
    address: "",
    bedroom: "",
    bathroom: "",
    dateAvailable: "",
    leaseDuration: "",
  });
  return (
    <>
      <div className='search-header-container'>
        <div>
          <input
            className='address-search'
            type='text'
            placeholder='Search address...'
            onChange={(e) =>
              setSearchQuery({
                ...searchQuery,
                address: e.target.value,
              })
            }
          />
          <span className='btn-search' onClick={() => onClick(searchQuery)}>
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
        <div className='filters-container'>
          <div className='filter-container bedroom-filter'>
            <div
              className='filter-title'
              onChange={(e) =>
                setSearchQuery({
                  ...searchQuery,
                  bedroom: e.target.value,
                })
              }
            >
              Bedrooms
            </div>
            <input type='text' className='txt-bedrooms' />
          </div>
          <div className='filter-container bathroom-filter'>
            <div
              className='filter-title'
              onChange={(e) =>
                setSearchQuery({
                  ...searchQuery,
                  bathroom: e.target.value,
                })
              }
            >
              Bathrooms
            </div>
            <input type='text' className='txt-bathrooms' />
          </div>
          <div className='filter-container monthlyRent-filter'>
            <div
              className='filter-title'
              onChange={(e) =>
                setSearchQuery({
                  ...searchQuery,
                  monthlyRent: e.target.value,
                })
              }
            >
              Monthly rent
            </div>
            <input type='text' className='txt-monthlyRent' />
          </div>
          <div className='filter-container dateAvailable-filter'>
            <div
              className='filter-title'
              onChange={(e) =>
                setSearchQuery({
                  ...searchQuery,
                  dateAvailable: e.target.value,
                })
              }
            >
              Date available
            </div>
            <input type='date' className='txt-dateAvailable' />
          </div>
          <div className='filter-container duration-filter'>
            <div
              className='filter-title'
              onChange={(e) =>
                setSearchQuery({
                  ...searchQuery,
                  leaseDuration: e.target.value,
                })
              }
            >
              Lease duration (in months)
            </div>
            <input type='text' className='txt-leaseDuration' />
          </div>
        </div>
      </div>
    </>
  );
};
export default SearchHeader;
