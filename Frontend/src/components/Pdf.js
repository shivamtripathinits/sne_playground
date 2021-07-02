import React from "react";
import "./../App.css";
import {AiOutlineFilePdf} from 'react-icons/ai'



const Pdf = ({ pdf }) => {
  let monthNames = ["January","February","March","April","May","June","July","August","September","October","November","December"];
  return (
    <div >
      <div className="items">
            <div className="inline">
              {pdf.pdf_name}
            </div>
            <div className="inline">
                <a href={pdf.pdf_link} target="_blank" rel="noopener noreferrer"><AiOutlineFilePdf color="red"/></a>
            </div>
            <div className="inline" id="datte">
              {monthNames[parseInt(pdf.pdf_date.substr(4, 2)) - 1]}-
              {pdf.pdf_date.substr(0, 4)}
            </div>
      </div>
    </div>
  );
};

export default Pdf;
