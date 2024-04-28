import { createBrowserRouter } from "react-router-dom";
import App from "../components/App";
import Listing from "./Listing";
import PostListing from "./PostListing";
import PropertyListing from "./PropertyListing";
import ListingType from "./ListingType";
import MarketplaceListing from "./MarketplaceListing";
import ViewSublease from "./ViewSublease";

const router = createBrowserRouter([
  { path: "/", element: <App /> },
  { path: "/listing", element: <Listing /> },
  { path: "/post-listing", element: <PostListing /> },
  { path: "/listing-type", element: <ListingType /> },
  { path: "/property-listing", element: <PropertyListing /> },
  { path: "/marketplace-listing", element: <MarketplaceListing /> },
  { path: "/view-sublease", element: <ViewSublease /> },
]);

export default router;
