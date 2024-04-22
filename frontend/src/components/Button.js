import React, {useState} from "react";
import "../styles/Button.css";
import {zipFiles} from "../static/script";

const Button = () => {
 const [clicked, setClicked] = useState(false);

 const handleClick = () => {
  alert(`An email containing a downloadable version of the docket has been sent`);
  setClicked(true);
  zipFiles();
 };

 return (
  <div>
   <button
    style={{background: !clicked ? "green" : "gray"}}
    onClick={
     !clicked
      ? () => {
         handleClick();
        }
      : null
    }
    disabled={clicked}>
    {!clicked ? "Download" : "Downloaded"}
   </button>
  </div>
 );
};

export default Button;
