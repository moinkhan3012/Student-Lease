import { useEffect, useState } from "react";
import { SearchHeader, Listing } from "../components";
import "../styles/search-listing.css";

const SearchListing = () => {
  const [subletOrMarketplace, setSubletOrMarketplace] = useState("sublets");
  let [listingDetails, setListingDetails] = useState([]);

  const searchListings = (searchQuery) => {
    console.log(searchQuery);
    fetch(
      "http://localhost:5000?" +
        new URLSearchParams({
          ...searchQuery,
          subletOrMarketplace: subletOrMarketplace,
        })
    )
      .then((res) =>
        res.json().then((data) => setListingDetails(data.listings))
      )
      .catch((err) => console.log("Failed to fetch listings from server"));
  };

  useEffect(() => {
    document.title = "Student Lease | Search listings";
    // TODO: Make a request with filters to fetch listing details
    fetch("http://localhost:5000")
      .then((res) =>
        res.json().then((data) => setListingDetails(data.listings))
      )
      .catch((err) => console.log("Failed to fetch listings from server"));
  }, []);
  useEffect(() => {
    // console.log("changed to", subletOrMarketplace);
  }, [subletOrMarketplace]);
  return (
    <>
      <SearchHeader onClick={searchListings} />
      <div className='listing-info'>
        <div className='listing-count'>
          {listingDetails.length} {subletOrMarketplace}
        </div>
        <div className='nearby-listings-title-container'>
          <select
            name=''
            className='nearby-listings-title'
            onChange={(e) => setSubletOrMarketplace(e.target.value)}
          >
            <option value='sublets'>Sublets</option>
            <option value='items'>Items</option>
          </select>{" "}
          near you
        </div>
        <div className='select-listing-text'>
          Select property for further details
        </div>
        {listingDetails.length > 0 &&
          listingDetails.map((details) => {
            return (
              <Listing
                key={details.id}
                listingDetails={details}
                isSublet={subletOrMarketplace == "sublets"}
              />
            );
          })}
      </div>
    </>
  );
};

export default SearchListing;
