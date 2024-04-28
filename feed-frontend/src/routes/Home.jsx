import { useEffect } from "react";
import Footer from "../components/Footer";
import "../styles/home.css";

const Home = () => {
  useEffect(() => {
    document.title = "Student Lease | Login";
  }, []);
  return (
    <>
      <div className='container'>
        <img
          src={require("../resources/home1.png")}
          alt=''
          className='home-image'
        />
        <div className='login-flex'>
          <div className='title1'>List home for subleasing</div>
          <div className='subtitle1'>
            Sign in for a more personalized experience
          </div>
          <div className='login'>Sign In</div>
        </div>
      </div>
      <div className='description-flex'>
        <div>
          <div className='subtitle2'>
            <span id='sublet-text-specific'>Sublet</span> a Home
          </div>
          <div className='description'>
            We are creating a seamless online <br /> experience - from shopping
            on the <br /> largest rental network, to <br />
            applying, to paying rent.
          </div>
          <div id='find-sublet-div'>
            <span className='find-sublets'>Find Sublets</span>
          </div>
        </div>
        <img
          className='home-animated'
          src={require("../resources/home-animated.png")}
          alt=''
        />
      </div>
      <Footer />
    </>
  );
};

export default Home;
