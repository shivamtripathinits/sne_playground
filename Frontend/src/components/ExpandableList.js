import './../App.css';
import React, { useState } from 'react';
import Pdfs from './Pdfs';
import {BsChevronDoubleDown} from 'react-icons/bs'
import {BsChevronDoubleUp} from 'react-icons/bs'
import {HiOutlineExternalLink} from 'react-icons/hi'

const ExpandableList = ({ company_code, title, content }) => {
  const [isActive, setIsActive] = useState(false);
  const company_name=[
    "Weyerhaeuser","Facebook","Informacion Corporativa","The Home Depot"
  ]

  return (
    <div className="accordion-item">
      <div className="accordion-title" style={{color:'black',backgroundColor:'silver'}} >
        <div><h2>
          <div className="inline">
            {company_code}{". "}{company_name[company_code-1]} {" "}
          </div>
          <a href={title}  target="_blank" rel="noopener noreferrer">
          <div className="inline">
            <HiOutlineExternalLink/>
          </div> 
          </a></h2></div>
        <div className="expand" onClick={() => setIsActive(!isActive)}>{isActive ? <BsChevronDoubleUp/> : <BsChevronDoubleDown/>}</div>
      </div>
      {isActive && <div className="accordion-content">{<Pdfs list_pdfs={content}/>}</div>}
    </div>
  );
};

export default ExpandableList;