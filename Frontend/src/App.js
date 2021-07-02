
import './App.css';
import Axios from 'axios'
import Header from './components/Header';
import React,{useState,useEffect} from 'react';
import ExpandableList from './components/ExpandableList';

function App() {
  
  const project_list=[
    "http://investor.weyerhaeuser.com/events-and-presentations",
    "https://investor.fb.com/investor-events/",
    "https://informacioncorporativa.entel.cl/investors/presentations",
    "http://ir.homedepot.com/events-and-presentations"
  ]
  let [scraps,setScraps]=useState([])
  const [one,enable1]=useState(false)
  const [two,enable2]=useState(false)
  const [three,enable3]=useState(false)
  const [four,enable4]=useState(false)
  let [sort, setSort] = useState(0);

  let options =null
  const sort_array=["Newest First","Oldest First","A to Z","Z to A"];
  
  const [selected, setSelected] = React.useState("Newest First");

  const changeSelectOptionHandler = (event) => {
    setSelected(event.target.value);
  };

  options=sort_array.map((x)=><option key={x}>{x}</option>)

  if(selected==="Oldest First")
    sort=1
  else if(selected==="Newest First")
    sort=2
  else if(selected==="A to Z")
    sort=3
  else if(selected==="Z to A")
    sort=4

  useEffect(() => {
    fetchScraps();
  }, []);

  const fetchScraps=async()=>{
    const response=await Axios('http://localhost:8000/');
    setScraps(response.data)    
  }

  const sortScraps = (k) => {
    if (sort === 1) return k.sort((a, b) => a.pdf_date - b.pdf_date);
    else if (sort === 2) return k.sort((a, b) => b.pdf_date - a.pdf_date);
    else if (sort === 3)
      return k.sort((a, b) => a.pdf_name.localeCompare(b.pdf_name));
    else if (sort === 4)
      return k.sort((a, b) => b.pdf_name.localeCompare(a.pdf_name));
    else return k;
  };

  return (

    <div className="App">
      <div className="first_heading"> 
        <Header title="Scrapped Items"/>
      </div>
      <div className="second_heading">
        <Header title="Company Selector"/>
      </div>
    
      <div className="company_images">
      <table style={{borderSpacing:10,width:'100%'}}> 
      <th style={{padding:20}}><img class="image_button"style={one?{borderWidth:8}:{borderWidth:'thin'}} src="logos/logo_0.png" alt="Company 1" onClick={()=>enable1(!one)}></img></th>
      <th ><img class="image_button" style={two?{borderWidth:8}:{borderWidth:'thin'}} src="logos/logo_1.png" alt="Company 2" onClick={()=>enable2(!two)}></img></th>
      <th ><img class="image_button" style={three?{borderWidth:8,backgroundColor:'blue'}:{borderWidth:'thin',backgroundColor:'blue'}} src="logos/logo_2.png" alt="Company 3" onClick={()=>enable3(!three)}></img></th>
      <th><img class="image_button" style={four?{borderWidth:8,backgroundColor:'orange'}:{borderWidth:'thin',backgroundColor:'orange'}} src="logos/logo_3.png" alt="Company 4" onClick={()=>enable4(!four)}></img></th>
      </table>
      </div>
      
      <form style={{marginBlock:10}}>  
        <label>Sort By: </label>
        <select onChange={changeSelectOptionHandler}>
          {options}
        </select>
      </form> 

      <div className="show">
      { one && <ExpandableList company_code={1} title={project_list[0]} content={sortScraps(scraps.filter((x) => x.company_code === 0))}/>}
      {two && <ExpandableList company_code={2} title={project_list[1]} content={sortScraps(scraps.filter((x) => x.company_code === 1))}/>}
      {three && <ExpandableList company_code={3} title={project_list[2]} content={sortScraps(scraps.filter((x) => x.company_code === 2))}/>}
      {four && <ExpandableList company_code={4} title={project_list[3]} content={sortScraps(scraps.filter((x) => x.company_code === 3))}/>}
      {!one && !two && !three && !four && <h1 style={{color:'white'}}>Please Select a company</h1> }
      </div>
    </div>

  );

}


export default App;