import { useState } from "react";
import { useNavigate } from "react-router-dom";

import { vehicleService } from "../services/vehicleService";

function VehicleCreate() {
  const navigate = useNavigate();
  const [vehicle, setVehicle] = useState({
    brand_id: "",
    model: "",
    year: "",
    color: "",
    description: "",
    is_sold: false,
  });
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const goHome = () => {
    navigate("/");
  };

  if (error) {
    return (
      <div className="error-message">
        <h2>Error while creating vehicle</h2>
        <p>{error?.detail || error.message}</p>
        <button onClick={goHome}>Go to Home</button>
      </div>
    );
  }

  if (loading) {
    return <div>Loading...</div>;
  }

  const createVehicle = async (vehicle) => {
    setLoading(true);
    try {
      await vehicleService.createVehicle(vehicle);
      navigate("/");
    } catch (error) {
      setError(error);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = () => {
    createVehicle(vehicle);
  };

  return (
    <div className="theme-input-container">
      <h1 className="vehicle-header">Add new vehicle</h1>
      <form
        className="vehicle-form"
        onSubmit={(e) => {
          e.preventDefault();
          handleSubmit();
        }}
      >
        <div className="input-group">
          <label htmlFor="brand_id">Brand ID:</label>
          <input
            type="number"
            name="brand_id"
            value={vehicle.brand_id}
            onChange={(e) =>
              setVehicle({
                ...vehicle,
                brand_id: e.target.value,
              })
            }
            placeholder="Brand ID"
            required
          />
        </div>
        <div className="input-group">
          <label htmlFor="model">Model:</label>
          <input
            type="text"
            name="model"
            value={vehicle.model}
            onChange={(e) =>
              setVehicle({
                ...vehicle,
                model: e.target.value,
              })
            }
            placeholder="Model"
            required
          />
        </div>
        <div className="input-group">
          <label htmlFor="year">Year:</label>
          <input
            type="number"
            name="year"
            value={vehicle.year}
            onChange={(e) =>
              setVehicle({
                ...vehicle,
                year: e.target.value,
              })
            }
            placeholder="Year"
            required
          />
        </div>
        <div className="input-group">
          <label htmlFor="color">Color:</label>
          <input
            type="text"
            name="color"
            value={vehicle.color}
            onChange={(e) =>
              setVehicle({
                ...vehicle,
                color: e.target.value,
              })
            }
            placeholder="Color"
            required
          />
        </div>
        <div className="input-group">
          <label htmlFor="description">Description:</label>
          <textarea
            name="description"
            value={vehicle.description}
            onChange={(e) =>
              setVehicle({
                ...vehicle,
                description: e.target.value,
              })
            }
            placeholder="Description"
            style={{ width: "100%", height: "100px" }}
            required
          />
        </div>
        <div className="input-group">
          <label htmlFor="is_sold">Is Sold:</label>
          <select
            name="is_sold"
            value={vehicle.is_sold.toString()}
            onChange={(e) =>
              setVehicle({
                ...vehicle,
                is_sold: e.target.value === "true",
              })
            }
            required
          >
            <option value="false">No</option>
            <option value="true">Yes</option>
          </select>
        </div>
        <div className="button-group">
          <button type="submit" disabled={loading}>
            {loading ? "Creating..." : "Create Vehicle"}
          </button>
        </div>
      </form>
    </div>
  );
}

export default VehicleCreate;
