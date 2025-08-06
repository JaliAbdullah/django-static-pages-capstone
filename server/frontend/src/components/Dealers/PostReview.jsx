import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import "./Dealers.css";
import "../assets/style.css";
import Header from '../Header/Header';


const PostReview = () => {
  const [dealer, setDealer] = useState({});
  const [review, setReview] = useState("");
  const [model, setModel] = useState();
  const [year, setYear] = useState("");
  const [date, setDate] = useState("");
  const [carmodels, setCarmodels] = useState([]);
  const [purchase, setPurchase] = useState(true);

  let curr_url = window.location.href;
  let root_url = curr_url.substring(0,curr_url.indexOf("postreview"));
  let params = useParams();
  let id =params.id;
  let dealer_url = root_url+`djangoapp/dealer/${id}`;
  let review_url = root_url+`djangoapp/add_review`;
  let carmodels_url = root_url+`djangoapp/get_cars`;

  const postreview = async ()=>{
    console.log("Post review button clicked");
    
    let name = sessionStorage.getItem("firstname")+" "+sessionStorage.getItem("lastname");
    console.log("Session storage contents:", {
      firstname: sessionStorage.getItem("firstname"),
      lastname: sessionStorage.getItem("lastname"),
      username: sessionStorage.getItem("username")
    });
    
    //If the first and second name are stores as null, use the username
    if(name.includes("null")) {
      name = sessionStorage.getItem("username");
    }
    
    console.log("Final name:", name);
    
    if(review === "" || date === "") {
      alert("Review and date are mandatory")
      return;
    }
    
    if(purchase && (!model || year === "" || model === "")) {
      alert("Car details are mandatory for purchase reviews")
      return;
    }

    let make_chosen = "";
    let model_chosen = "";
    
    if(purchase && model) {
      let model_split = model.split(" ");
      make_chosen = model_split[0];
      model_chosen = model_split[1];
    }

    let jsoninput = JSON.stringify({
      "name": name,
      "dealership": parseInt(id),
      "review": review,
      "purchase": purchase,
      "purchase_date": date,
      "car_make": make_chosen || "",
      "car_model": model_chosen || "",
      "car_year": purchase && year ? parseInt(year) : 0,
    });

    console.log(jsoninput);
    const res = await fetch(review_url, {
      method: "POST",
      headers: {
          "Content-Type": "application/json",
      },
      body: jsoninput,
  });

  const json = await res.json();
  console.log("Response from server:", json);
  if (json.status === 200) {
      window.location.href = window.location.origin+"/dealer/"+id;
  } else {
      alert("Error posting review: " + (json.message || "Unknown error"));
  }

  }
  const get_dealer = async ()=>{
    const res = await fetch(dealer_url, {
      method: "GET"
    });
    const retobj = await res.json();
    
    if(retobj.status === 200) {
      let dealerobjs = Array.from(retobj.dealer)
      if(dealerobjs.length > 0)
        setDealer(dealerobjs[0])
    }
  }

  const get_cars = async ()=>{
    const res = await fetch(carmodels_url, {
      method: "GET"
    });
    const retobj = await res.json();
    
    let carmodelsarr = Array.from(retobj.CarModels)
    setCarmodels(carmodelsarr)
  }
  useEffect(() => {
    get_dealer();
    get_cars();
  },[]);


  return (
    <div>
      <Header/>
      <div  style={{margin:"5%"}}>
      <h1 style={{color:"darkblue"}}>{dealer.full_name}</h1>
      <textarea id='review' cols='50' rows='7' onChange={(e) => setReview(e.target.value)}></textarea>
      <div className='input_field'>
      {purchase ? 'Purchase Date' : 'Visit Date'} <input type="date" onChange={(e) => setDate(e.target.value)}/>
      </div>
      
      <div className='input_field'>
      Did you purchase this car? 
      <label style={{marginLeft: '10px'}}>
        <input 
          type="radio" 
          value={true} 
          checked={purchase === true} 
          onChange={() => setPurchase(true)}
          style={{marginRight: '5px'}}
        />
        Yes
      </label>
      <label style={{marginLeft: '20px'}}>
        <input 
          type="radio" 
          value={false} 
          checked={purchase === false} 
          onChange={() => setPurchase(false)}
          style={{marginRight: '5px'}}
        />
        No
      </label>
      </div>
      
      {purchase && (
        <>
          <div className='input_field'>
          Car Make 
          <select name="cars" id="cars" onChange={(e) => setModel(e.target.value)}>
          <option value="" selected disabled hidden>Choose Car Make and Model</option>
          {carmodels.map(carmodel => (
              <option value={carmodel.CarMake+" "+carmodel.CarModel}>{carmodel.CarMake} {carmodel.CarModel}</option>
          ))}
          </select>        
          </div >

          <div className='input_field'>
          Car Year <input type="number" onChange={(e) => setYear(e.target.value)} max={2023} min={2015}/>
          </div>
        </>
      )}

      <div>
      <button className='postreview' onClick={postreview}>Post Review</button>
      </div>
    </div>
    </div>
  )
}
export default PostReview
