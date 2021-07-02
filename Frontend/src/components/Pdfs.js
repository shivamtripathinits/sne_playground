import Pdf from "./Pdf";

const Pdfs = ({ list_pdfs }) => {
  let position = 0;
  return (
    <div>
      {list_pdfs.map((pdf) => (
        <div id="row">
          <Pdf key={pdf._id} pdf={pdf} position={(position = position + 1)} />{" "}
        </div>
      ))}
    </div>
  );
};

export default Pdfs;
