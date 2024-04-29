import { useNavigate } from "react-router-dom";
import "../styles/search-header.css";
import { useState } from "react";

const SearchHeader = ({ onClick }) => {
  const navigate = useNavigate();
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
