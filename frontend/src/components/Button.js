import React, {useState} from "react";
import "../styles/Button.css";

const Button = () => {
 const [clicked, setClicked] = useState(false);

 const handleClick = () => {
  setClicked(true);
  alert("The docket is being sent to your email", "Mirrulations");
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
