import React, { useState, useEffect } from "react";
import axios from "axios";

const Recommendation = ({ userId }) => {
  const [recommendations, setRecommendations] = useState([]);

  useEffect(() => {
    const fetchRecommendations = async () => {
      try {
        const response = await axios.get(
          `http://127.0.0.1:5000//recommend/${userId}`
        );
        setRecommendations(response.data);
      } catch (error) {
        console.error("Error fetching recommendations:", error);
      }
    };

    fetchRecommendations();
  }, [userId]);

  return (
    <div>
      <h1>Recommendations for User {userId}</h1>
      <ul>
        {recommendations.map((product, index) => (
          <li key={index}>
            <h2>{product[1]}</h2>
            <img src={product[2]} alt={product[1]} />
            <p>{product[3]}</p>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Recommendation;
