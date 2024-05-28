// import './App.css';
// import Header from './components/Header';
// // import Body from './components/Body';
// import Footer from './components/Footer';
// import { Outlet } from 'react-router-dom';

// function App() {

//   return (
//    <div className='scrollbar-hide overflow-hidden'>
//    <Header/>
//    <Outlet/>
//    <Footer/>
//    </div>

//   );
// }

// export default App;

import React, { Component } from "react";
import { Router, Route, Routes } from "react-router-dom";
import Temp from "./Temp";
import Temp2 from "./Temp2";

class App extends Component {
  render() {
    return (
      <div>
        {/* <Router>
          <h1>Product Recommendations</h1>
          <Routes>
            <Route path="/" element={<Temp />} />
            <Route path="/recommend" element={<Temp2 userId={8000} />} />
          </Routes>
        </Router> */}

        <Temp />
        <br />
        <br />
        <br />
        <h1> Madarchod ML</h1>
        <br />
        <br />
        <br />
        <br />
        <Temp2 userId={80000} />
      </div>
    );
  }
}
export default App;
