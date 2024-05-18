import {
  CognitoUserPool,
  AuthenticationDetails,
  CognitoUser,
} from "amazon-cognito-identity-js";
import { CLIENT_ID, USER_POOL_ID } from "../constants";
import set_cookie from "./setCookie";

export default function authenticateUser(navigate, username) {
  set_cookie("email", username);
  var userPoolData = {
    UserPoolId: USER_POOL_ID, // Replace with your user pool id
    ClientId: CLIENT_ID, // Replace with your app client id
  };

  var userPool = new CognitoUserPool(userPoolData);

  var username = document.getElementById("username").value;
  var password = document.getElementById("password").value;

  var authenticationData = {
    Username: username,
    Password: password,
  };
  var authenticationDetails = new AuthenticationDetails(authenticationData);

  var userData = {
    Username: username,
    Pool: userPool,
  };
  var cognitoUser = new CognitoUser(userData);

  cognitoUser.authenticateUser(authenticationDetails, {
    onSuccess: function (result) {
      console.log(username);
      // navigate("/post-listing");
      navigate("/search-listing", {
        state: { email: username },
      });
    },
    onFailure: function (err) {
      alert("Login failed: " + err.message);
    },
    mfaRequired: function (codeDeliveryDetails) {
      var verificationCode = prompt("Please input verification code", "");
      cognitoUser.sendMFACode(verificationCode, this);
    },
  });
}
