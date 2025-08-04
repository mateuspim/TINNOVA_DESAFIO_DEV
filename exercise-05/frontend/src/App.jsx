import "./App.css";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import VehicleList from "./components/VehicleList.jsx";
import VehicleData from "./components/VehicleData.jsx";
import VehicleCreate from "./components/VehicleCreate.jsx";

function App() {
  return (
    <Router>
      <div className="app-container">
        <header>
          <h1>Vehicle Manager</h1>
        </header>
        <main>
          <Routes>
            <Route path="/" element={<VehicleList />} />
            <Route path="/vehicle/" element={<VehicleCreate />} />
            <Route path="/vehicle/:id" element={<VehicleData />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
