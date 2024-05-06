import { useEffect, useState } from "react";
import { SearchHeader, Listing } from "../components";
import { VIEW_MARKETPLACE_URL, VIEW_SUBLET_URL } from "../constants";
import "../styles/search-listing.css";

const SearchListing = () => {
  const [subletOrMarketplace, setSubletOrMarketplace] = useState("sublets");
  const [listingDetails, setListingDetails] = useState([]);

  useEffect(() => {
    document.title = "Student Lease | Search listings";
  }, []);
  const searchListings = (searchQuery) => {
    const searchListingsUrl =
      subletOrMarketplace == "sublets" ? VIEW_SUBLET_URL : VIEW_MARKETPLACE_URL;
    console.log("search query", searchQuery);

    fetch(searchListingsUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(searchQuery),
    })
      .then((res) => res.json())
      .then((data) => {
        let listingArray = [];
        console.log(
          `${
            subletOrMarketplace == "sublets" ? "sublet" : "marketplace item"
          } details`,
          JSON.parse(data.body)["details"]
        );
        JSON.parse(data.body)["details"].forEach((listing) => {
          listingArray.push(listing);
        });
        setListingDetails(listingArray);
      })
      .catch((error) =>
        console.log(`Error while fetching ${subletOrMarketplace}`, error)
      );
  };

  return (
    <>
      <SearchHeader
        onClick={searchListings}
        isSublet={subletOrMarketplace == "sublets"}
      />
      <div className='listing-info'>
        <div className='listing-count'>
          {listingDetails.length} {subletOrMarketplace}
        </div>
        <div className='nearby-listings-title-container'>
          <select
            name=''
            className='nearby-listings-title'
            onChange={(e) => {
              setSubletOrMarketplace(e.target.value);
              setListingDetails([]);
            }}
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
          listingDetails.map((details, index) => {
            return (
              <Listing
                key={index}
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
