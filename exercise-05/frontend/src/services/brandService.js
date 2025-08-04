import api from './api';

export const brandService = {
  // GET /api/brands/ - List brands (paginated)
  async getBrands(page = 1, size = 50) {
    return api.get(`/brands/?page=${page}&size=${size}`);
  },

  // GET /api/brands/resolve?name={name} - Resolve brand by name
  async getBrandByName(name) {
    return api.get(`/brands/resolve?name=${encodeURIComponent(name)}`);
  },

  // POST /api/brands/ - Create new brand
  async createBrand(brandData) {
    return api.post('/brands/', brandData);
  },

  // DELETE /api/brands/{id} - Delete brand
  async deleteBrand(id) {
    return api.delete(`/brands/${id}`);
  }
};