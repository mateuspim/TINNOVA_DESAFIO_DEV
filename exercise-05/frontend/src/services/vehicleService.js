import api from "./api";

export const vehicleService = {
  // GET /api/vehicles/ - List vehicles (paginated and with filters)
  async getVehicles(filters = {}) {
    const params = new URLSearchParams();

    if (filters.page) params.append("page", filters.page);
    if (filters.size) params.append("size", filters.size);
    if (filters.year) params.append("year", filters.year);
    if (filters.brand_id) params.append("brand_id", filters.brand_id);
    if (filters.color) params.append("color", filters.color);
    if (filters.is_sold !== undefined)
      params.append("is_sold", filters.is_sold);

    const queryString = params.toString();
    return api.get(`/vehicles/${queryString ? "?" + queryString : ""}`);
  },

  // GET /api/vehicles/{id} - Get vehicle by ID
  async getVehicleById(id) {
    return api.get(`/vehicles/${id}`);
  },

  // POST /api/vehicles/ - Create new vehicle
  async createVehicle(vehicleData) {
    return api.post("/vehicles/", vehicleData);
  },

  // PUT /api/vehicles/{id} - Update complete vehicle
  async updateVehicle(id, vehicleData) {
    return api.put(`/vehicles/${id}`, vehicleData);
  },

  // PATCH /api/vehicles/{id} - Partially update vehicle
  async patchVehicle(id, vehicleData) {
    return api.patch(`/vehicles/${id}`, vehicleData);
  },

  // DELETE /api/vehicles/{id} - Delete vehicle
  async deleteVehicle(id) {
    return api.delete(`/vehicles/${id}`);
  },
};
