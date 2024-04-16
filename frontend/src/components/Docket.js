import React from "react";
import "../styles/Docket.css"; // Import the CSS file
import Button from "./Button";

const Docket = ({
 title,
 email,
 id,
 link,
 docket_type,
 docket_agency,
 documents_containing,
 total_documents,
 comment_date_range,
 comments_containing,
 total_comments,
}) => {
 return (
  <div className="search-result">
   <div className="container-1">
    <p>{docket_agency}</p>
    <h2>{title}</h2>
    <p>{docket_type}</p>
    <p>
     <a href={link} target="_blank" rel="noopener noreferrer">
      {id}
     </a>
    </p>
   </div>
   <div className="container-2">
    <div className="left-half">
     <p>
      {comments_containing} comments relate to your term out of the {total_comments} total comments
      in this docket.
     </p>
     <p>Comment Date Range: {comment_date_range}</p>
     <p>
      {documents_containing} documents relate to your term out of the {total_documents} total
      documents in this docket.
     </p>
    </div>
    <Button email={email} docketID={id} />
   </div>
  </div>
 );
};

export default Docket;
