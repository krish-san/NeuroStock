import React, { useEffect, useState } from "react";
import "./Dashboard.css";
import axios from "axios";
import { Pie } from "react-chartjs-2";
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend
} from "chart.js";

ChartJS.register(ArcElement, Tooltip, Legend);

const Dashboard = () => {
  const [weather, setWeather] = useState(null);
  const [forecast, setForecast] = useState([]);
  const [discountItems, setDiscountItems] = useState([]);
  const [restockItems, setRestockItems] = useState([]);
  const [selectedDay, setSelectedDay] = useState(null);

  // Fetch all backend data
  useEffect(() => {
    axios.get("http://localhost:8000/weather/current").then(res => setWeather(res.data));
    axios.get("http://localhost:8000/weather/forecast").then(res => setForecast(res.data));
    axios.get("http://localhost:8000/inventory/discounts").then(res => setDiscountItems(res.data));
    axios.get("http://localhost:8000/inventory/restock").then(res => setRestockItems(res.data));
  }, []);

  const calendarData = (() => {
    const today = new Date();
    const days = [];
    const weatherMap = ["Sunny", "Rainy", "Cloudy", "Clear", "Storm"];
    const items = ["Milk", "Bread", "Soup", "Juice", "Cereal", "Snacks"];
    for (let i = 0; i < 7; i++) {
      const date = new Date(today);
      date.setDate(today.getDate() + i);
      days.push({
        date: date.toISOString().split("T")[0],
        weekday: date.toLocaleDateString("en-US", { weekday: "short" }),
        weather: weatherMap[i % weatherMap.length],
        high_demand: items[i % items.length],
        special_event: i === 3 ? "Festival" : i === 5 ? "Sale" : ""
      });
    }
    return days;
  })();

  const chartData = {
    labels: ["Snacks", "Beverages", "Dairy", "Essentials"],
    datasets: [
      {
        label: "Category Breakdown",
        data: [12, 19, 8, 6],
        backgroundColor: ["#FF6384", "#36A2EB", "#FFCE56", "#a0e082"],
        hoverOffset: 5
      }
    ]
  };

  const scenarios = {
    "Rain for 3 days": "↑ Soup, ↑ Tea/Coffee, ↓ Ice Cream",
    "Heatwave": "↑ Juices, ↑ Water, ↓ Soups",
    "Festival": "↑ Sweets, ↑ Snacks, ↓ Essentials",
    "Cold snap": "↑ Instant Noodles, ↑ Coffee, ↓ Soft Drinks"
  };

  return (
    <div className="dashboard-container">
      <h1>🧠 NeuroStock</h1>
      <p>Smart Inventory Assistant</p>

      {/* Weather Info */}
      <div className="weather-box">
        <h3>🌦️ Current Weather</h3>
        {weather ? (
          <p>{weather.description} | 🌡️ {weather.temperature}°C</p>
        ) : (
          <p>Loading weather...</p>
        )}
      </div>

      {/* Calendar */}
      <div className="calendar-container">
        <h3>📅 Demand Calendar</h3>
        <div className="calendar-grid">
          {calendarData.map((day, index) => (
            <div
              key={index}
              className={`calendar-day ${selectedDay === index ? "selected" : ""}`}
              onClick={() => setSelectedDay(index)}
            >
              <div>{day.weekday}</div>
              <div>{day.date.split("-")[2]}</div>
              <div className="weather-tag">{day.weather}</div>
              {day.special_event && <div className="event-tag">{day.special_event}</div>}
            </div>
          ))}
        </div>
        {selectedDay !== null && (
          <div className="calendar-detail">
            <h4>Details for {calendarData[selectedDay].weekday}, {calendarData[selectedDay].date}</h4>
            <p>🌤 Weather: {calendarData[selectedDay].weather}</p>
            <p>🔥 High Demand: {calendarData[selectedDay].high_demand}</p>
            {calendarData[selectedDay].special_event && (
              <p>🎉 Event: {calendarData[selectedDay].special_event}</p>
            )}
          </div>
        )}
      </div>

      {/* Pie Chart */}
      <div className="chart-section">
        <h3>📊 Inventory Category Breakdown</h3>
        <div className="chart-wrapper">
          <Pie data={chartData} />
        </div>
      </div>

      {/* Discount Alerts */}
      <div className="alerts">
        <h3>🏷️ Suggested Discounts</h3>
        {discountItems.length > 0 ? (
          <ul>
            {discountItems.map((item, i) => (
              <li key={i}>{item.name} - Expires in {item.days_to_expiry} days</li>
            ))}
          </ul>
        ) : <p>No discount-needed items.</p>}
      </div>

      {/* Restock Alerts */}
      <div className="alerts">
        <h3>🚨 Restock Alerts</h3>
        {restockItems.length > 0 ? (
          <ul>
            {restockItems.map((item, i) => (
              <li key={i}>{item.name} - Only {item.stock} left</li>
            ))}
          </ul>
        ) : <p>Stock levels are good.</p>}
      </div>

      {/* Scenario Simulation */}
      <div className="scenario">
        <h3>🔮 Scenario Simulator</h3>
        <select onChange={(e) => alert(scenarios[e.target.value])}>
          <option>Select a scenario</option>
          {Object.keys(scenarios).map((key, idx) => (
            <option key={idx}>{key}</option>
          ))}
        </select>
      </div>
    </div>
  );
};

export default Dashboard;

