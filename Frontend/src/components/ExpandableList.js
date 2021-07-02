import "./../App.css";
import React, { useState, useEffect } from "react";
import Pdfs from "./Pdfs";
import { BsChevronDoubleDown } from "react-icons/bs";
import { BsChevronDoubleUp } from "react-icons/bs";
import { HiOutlineExternalLink } from "react-icons/hi";

const ExpandableList = ({ company_code, title, content }) => {
  // const [isActive, setIsActive] = useState(false);
  const [data, setData] = useState([]);
  let [limit, setLimit] = useState(0);
  let [total, setTotal] = useState(content.length);
  const company_name = [
    "Weyerhaeuser",
    "Facebook",
    "Informacion Corporativa",
    "The Home Depot",
  ];

  useEffect(() => {
    getContent();
  }, [content, limit]);
  const incLimit = () => {
    console.log("islimit ", limit, total);
    if (total < 10) {
      setLimit(limit + total);

      setTotal(0);
    } else {
      setLimit(limit + 10);

      setTotal((total -= 10));
    }
    console.log("islimit ", limit, total);
  };
  const decLimit = () => {
    console.log("dislimit ", limit, total);
    if (limit < 10) {
      setTotal(total + limit);
      setLimit(0);
    } else {
      if (limit % 10 !== 0) {
        const rem = limit % 10;
        setLimit(limit - (limit % 10));
        setTotal(total + rem);
      } else {
        setLimit(limit - 10);
        setTotal(total + 10);
      }
    }
    console.log("dislimit ", limit, total);
  };

  const getContent = async () => {
    const d = content.slice([0], [limit]);
    setData(d);
  };

  return (
    <div className="accordion-item">
      <div
        className="accordion-title"
        style={{ color: "black", backgroundColor: "silver" }}
      >
        <div>
          <h2>
            <div className="inline">
              {company_code}
              {". "}
              {company_name[company_code - 1]}
            </div>
            <a href={title} target="_blank" rel="noopener noreferrer">
              <div className="inline">
                <HiOutlineExternalLink />
              </div>
            </a>
          </h2>
        </div>
        {total == content.length && (
          <div className="expand" onClick={incLimit}>
            {<BsChevronDoubleDown />}
          </div>
        )}
        {/* {total < content.length && (
          <div className="expand" onClick={decLimit}>
            {<BsChevronDoubleUp />}
          </div>
        )} */}
      </div>
      {total < 1000 && (
        <div className="accordion-content">{<Pdfs list_pdfs={data} />}</div>
      )}
      {total > 0 && limit !== 0 && (
        <div className="expand" onClick={incLimit}>
          {<BsChevronDoubleDown />}
        </div>
      )}
      {total < content.length && (
        <div className="expand" onClick={decLimit}>
          {<BsChevronDoubleUp />}
        </div>
      )}
    </div>
  );
};

export default ExpandableList;
