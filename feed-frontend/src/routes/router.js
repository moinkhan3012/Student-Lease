import { createBrowserRouter } from "react-router-dom";
import Home from "./Home";
import CreatePropertyListing from "./CreatePropertyListing";
import PostListing from "./PostListing";
import PropertyListing from "./PropertyListing";
import ListingType from "./ListingType";
import MarketplaceListing from "./MarketplaceListing";
import SearchListing from "./SearchListing";
import ViewListing from "./ViewListing";
import Login from "./Login";
import SignUp from "./SignUp";

const router = createBrowserRouter([
  { path: "/", element: <Home /> },
  { path: "/login", element: <Login /> },
  { path: "/signup", element: <SignUp /> },
  { path: "/create-property-listing", element: <CreatePropertyListing /> },
  { path: "/post-listing", element: <PostListing /> },
  { path: "/listing-type", element: <ListingType /> },
  { path: "/property-listing", element: <PropertyListing /> },
  { path: "/marketplace-listing", element: <MarketplaceListing /> },
  { path: "/search-listing", element: <SearchListing /> },
  { path: "/view-listing", element: <ViewListing /> },
]);

export default router;
