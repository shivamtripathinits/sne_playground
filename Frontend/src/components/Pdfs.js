import Pdf from "./Pdf"

const Pdfs = ({list_pdfs}) => {
    return (
        
        <ol >
        {list_pdfs.map((pdf)=>(
           <li id="row"><Pdf key={pdf._id} pdf={pdf}/> </li>
        ))}
        </ol>
        
    )
}

export default Pdfs