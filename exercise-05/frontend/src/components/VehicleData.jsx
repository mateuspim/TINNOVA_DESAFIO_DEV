import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";

import { vehicleService } from "../services/vehicleService";
import LoadingStatus from "./LoadingStatus.jsx";

function VehicleData() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [vehicle, setVehicle] = useState(null);
  const [currentVehicle, setCurrentVehicle] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadVehicle(id);
  }, [id]);

  const loadVehicle = async (vehicleId) => {
    setLoading(true);
    try {
      const response = await vehicleService.getVehicleById(vehicleId);
      setVehicle(response);
      setCurrentVehicle(response);
      setError(null);
    } catch (error) {
      if (error?.status === 404) {
        setError("Vehicle is not found.");
      } else {
        setError("Something went wrong.");
      }
    } finally {
      setLoading(false);
    }
  };

  const goHome = () => {
    navigate("/");
  };

  if (loading) {
    return <LoadingStatus what="vehicle" />;
  }

  if (error) {
    return (
      <div className="vehicle-loader">
        <div className="error-message">
          <h2>Vehicle Not Found</h2>
          <p>{error}</p>
          <button onClick={goHome}>Go to Home</button>
        </div>
      </div>
    );
  }

  const deleteVehicle = async () => {
    setLoading(true);
    try {
      await vehicleService.deleteVehicle(id);
      setVehicle(null);
      setError(null);
      goHome();
    } catch (error) {
      setError("Failed to delete vehicle.");
    } finally {
      setLoading(false);
    }
  };

  const updateVehicle = async (updatedData = null) => {
    setLoading(true);

    const dataToUpdate = updatedData || currentVehicle;

    const allKeys = [
      "brand_id",
      "model",
      "color",
      "year",
      "description",
      "is_sold",
    ];
    const changedFields = {};
    allKeys.forEach((key) => {
      if (
        dataToUpdate.hasOwnProperty(key) &&
        dataToUpdate[key] !== vehicle[key]
      ) {
        changedFields[key] = dataToUpdate[key];
      }
    });

    if (Object.keys(changedFields).length === 0) {
      console.log("No changes detected");
      setLoading(false);
      return;
    }

    // PUT if all fields are present in changedFields, PATCH otherwise
    const isFullUpdate =
      allKeys.every((key) => changedFields.hasOwnProperty(key)) &&
      Object.keys(changedFields).length === allKeys.length;
    const method = isFullUpdate ? "PUT" : "PATCH";

    console.log("Sending", method, "with changed fields:", changedFields);

    try {
      const response = await sendRequest(method, changedFields);
      setVehicle(response);
      setCurrentVehicle(response);
      console.log("Updated vehicle:", response);
    } catch (error) {
      setError("Failed to update vehicle.");
    } finally {
      setLoading(false);
    }
  };

  const sendRequest = async (method, data) => {
    if (method === "PATCH") {
      return await vehicleService.patchVehicle(id, data);
    } else {
      return await vehicleService.updateVehicle(id, data);
    }
  };

  const handleInputChange = (event) => {
    setCurrentVehicle({
      ...currentVehicle,
      [event.target.name]: event.target.value,
    });
  };

  const handleSubmit = () => {
    updateVehicle(currentVehicle);
  };

  return (
    <div className="theme-input-container">
      <h1 className="vehicle-header">
        {vehicle?.brand.name} - {vehicle?.model}
      </h1>
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
            type="text"
            name="brand_id"
            value={currentVehicle?.brand_id || ""}
            onChange={handleInputChange}
            placeholder="Brand ID"
          />
        </div>
        <div className="input-group">
          <label htmlFor="model">Model:</label>
          <input
            type="text"
            name="model"
            value={currentVehicle?.model || ""}
            onChange={handleInputChange}
            placeholder="Model"
          />
        </div>
        <div className="input-group">
          <label htmlFor="year">Year:</label>
          <input
            type="number"
            name="year"
            value={currentVehicle?.year || ""}
            onChange={handleInputChange}
            placeholder="Year"
          />
        </div>
        <div className="input-group">
          <label htmlFor="color">Color:</label>
          <input
            type="text"
            name="color"
            value={currentVehicle?.color || ""}
            onChange={handleInputChange}
            placeholder="Color"
          />
        </div>
        <div className="input-group">
          <label htmlFor="description">Description:</label>
          <textarea
            className="input-group"
            name="description"
            value={currentVehicle?.description || ""}
            onChange={handleInputChange}
            placeholder="Description"
            style={{ width: "100%", height: "100px" }}
          />
        </div>
        <div className="input-group">
          <label htmlFor="is_sold">Is Sold:</label>
          <select
            name="is_sold"
            value={currentVehicle?.is_sold ? "true" : "false"}
            onChange={(e) =>
              setCurrentVehicle({
                ...currentVehicle,
                is_sold: e.target.value === "true",
              })
            }
          >
            <option value="true">Yes</option>
            <option value="false">No</option>
          </select>
        </div>
        <div className="button-group">
          <button type="submit">Update Vehicle</button>
          <button className="warning" type="button" onClick={deleteVehicle}>
            Delete Vehicle
          </button>
        </div>
      </form>
    </div>
  );
}

export default VehicleData;
