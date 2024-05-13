import { Header, Footer } from "../components";
import { useState } from "react";
import { getBase64 } from "../utils";
import { CREATE_MARKETPLACE_URL } from "../constants";
import "../styles/marketplace-listing.css";

const MarketplaceListing = () => {
  const [title, setTitle] = useState("");
  const [address, setAddress] = useState("");
  const [price, setPrice] = useState("");
  const [description, setDescription] = useState("");
  const [images, setImages] = useState([]);
  const setUploadedImages = (files) => {
    let base64ImagesList = [];
    [...files].map((file) => {
      getBase64(file).then((base64File) => base64ImagesList.push(base64File));
    });
    setImages(base64ImagesList);
  };
  const createMarketplaceListing = () => {
    const reqBody = {
      title: title,
      address: address,
      price: price,
      detailedDescription: description,
      images: images,
    };
    console.log("request body:", reqBody);
    fetch(CREATE_MARKETPLACE_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(reqBody),
    })
      .then((res) => res.json())
      .then((data) => console.log("Response", data))
      .catch((error) =>
        console.log("Error while creating marketplace listing", error)
      );
  };
  return (
    <>
      <Header />
      <div className='preview-box'>
        <div className='title-text'>Add a marketplace lising</div>
        <div className='horizontal-line'></div>
        <div className='marketplace-container'>
          <div className='subtitle-text'>Please add your item's info</div>
          <label htmlFor='files'>Select images:</label>
          <input
            type='file'
            id='files'
            name='files'
            multiple
            onChange={(e) => setUploadedImages(e.target.files)}
          />
          <div className='item-details'>
            <div>Title</div>
            <input
              type='text'
              className='property-input property-address'
              onChange={(e) => setTitle(e.target.value)}
            />
          </div>
          <div className='item-details'>
            <div>Address</div>
            <input
              type='text'
              className='property-input property-address'
              onChange={(e) => setAddress(e.target.value)}
            />
          </div>
          <div className='item-details'>
            <div>Price</div>
            <input
              type='text'
              className='property-input unit-number'
              onChange={(e) => setPrice(e.target.value)}
            />
          </div>
          <div className='item-details'>
            <div>Description</div>
            <textarea
              className='marketplace-description'
              onChange={(e) => setDescription(e.target.value)}
            ></textarea>
          </div>
        </div>
        <div onClick={createMarketplaceListing} className='btn-create-listing'>
          Create listing
        </div>
      </div>
      <Footer />
    </>
  );
};

export default MarketplaceListing;
