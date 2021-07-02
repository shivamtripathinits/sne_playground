import React from "react";
import "./../App.css";
import { AiOutlineFilePdf } from "react-icons/ai";

const Pdf = ({ pdf, position }) => {
  let monthNames = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
  ];
  return (
    <div>
      <div className="items">
        <table width="100%" border="1">
          <th width="5%">
            <div>
              {position}
              {"."}
            </div>
          </th>
          <th width="70%">
            <div style={{ textAlign: "left" }}>{pdf.pdf_name}</div>
          </th>
          <th width="20%">
            <div>
              {monthNames[parseInt(pdf.pdf_date.substr(4, 2)) - 1]}-
              {pdf.pdf_date.substr(0, 4)}
            </div>
          </th>
          <th width="5%">
            <a href={pdf.pdf_link} target="_blank" rel="noopener noreferrer">
              <AiOutlineFilePdf color="red" />
            </a>
          </th>
        </table>
      </div>
    </div>
  );
};

export default Pdf;
