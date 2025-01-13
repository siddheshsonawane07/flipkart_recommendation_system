import React, { useState } from "react";
import axios from "axios";

const RecommendationSystem = () => {
  const [userId, setUserId] = useState("");
  const [itemId, setItemId] = useState("");
  const [recommendations, setRecommendations] = useState([]);

  const handleSubmit = async (event) => {
    event.preventDefault(); // Prevent form submission
    try {
      const response = await axios.post("http://127.0.0.1:5000/recommend", {
        user_id: userId,
        item_id: itemId,
      });
      setRecommendations(response.data);
    } catch (error) {
      console.error("Error fetching recommendations:", error);
    }
  };

  return (
    <div>
      <input
        type="text"
        value={userId}
        onChange={(e) => setUserId(e.target.value)}
        placeholder="User ID"
      />
      <input
        type="text"
        value={itemId}
        onChange={(e) => setItemId(e.target.value)}
        placeholder="Item ID"
      />
      <button onClick={handleSubmit}>Get Recommendations</button>
      <ul>
        {recommendations.map((rec) => (
          <li key={rec}>{rec}</li>
        ))}
      </ul>
    </div>
  );
};

export default RecommendationSystem;
