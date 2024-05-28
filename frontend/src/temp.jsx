import React, { useState } from "react";
import axios from "axios";

function Temp() {
  const [userId, setUserId] = useState("");
  const [orderId, setOrderId] = useState("");
  const [productId, setProductId] = useState("");
  const [productName, setProductName] = useState("");
  const [price, setPrice] = useState("");
  const [brand, setBrand] = useState("");

  const getCurrentDate = () => {
    const date = new Date();
    const day = String(date.getDate()).padStart(2, "0");
    const month = String(date.getMonth() + 1).padStart(2, "0");
    const year = date.getFullYear();
    return `${day}-${month}-${year}`;
  };

  const handleLogInteraction = async (e) => {
    e.preventDefault();
    const currentDate = getCurrentDate();

    const interactionData = {
      oid: orderId,
      uid: userId,
      date: currentDate,
      product_name: productName,
      pid: productId,
      price: price,
      brand: brand,
    };

    try {
      const response = await axios.post(
        "http://127.0.0.1:5000/log_interaction",
        interactionData
      );
      console.log(response.data.message);
      setUserId("");
      setOrderId("");
      setProductId("");
      setPrice("");
      setBrand("");
      setProductName("");
    } catch (error) {
      console.error("Error logging interaction:", error);
    }
  };

  return (
    <div>
      <h1>User Interaction Logger</h1>
      <form onSubmit={handleLogInteraction}>
        <div>
          <label>User ID:</label>
          <input
            type="text"
            value={userId}
            onChange={(e) => setUserId(e.target.value)}
          />
        </div>
        <div>
          <label>Product Name:</label>
          <input
            type="text"
            value={productName}
            onChange={(e) => setProductName(e.target.value)}
          />
        </div>
        <div>
          <label>Order ID:</label>
          <input
            type="text"
            value={orderId}
            onChange={(e) => setOrderId(e.target.value)}
          />
        </div>
        <div>
          <label>Product ID:</label>
          <input
            type="text"
            value={productId}
            onChange={(e) => setProductId(e.target.value)}
          />
        </div>
        <div>
          <label>Price:</label>
          <input
            type="text"
            value={price}
            onChange={(e) => setPrice(e.target.value)}
          />
        </div>
        <div>
          <label>Brand:</label>
          <input
            type="text"
            value={brand}
            onChange={(e) => setBrand(e.target.value)}
          />
        </div>
        <button type="submit">Log Interaction</button>
      </form>
    </div>
  );
}

export default Temp;
