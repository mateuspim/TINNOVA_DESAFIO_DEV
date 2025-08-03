const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "/api";

class ApiService {
  async request(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    const config = {
      headers: {
        "Content-Type": "application/json",
        ...options.headers,
      },
      ...options,
    };

    console.log("Sending request:", {
      url,
      method: options.method,
      body: options.body,
    });

    const response = await fetch(url, config);

    if (!response.ok) {
      const error = new Error(`HTTP error! status: ${response.status}`);
      error.status = response.status;
      const responseBody = await response.text();
      error.detail = JSON.parse(responseBody).detail;
      throw error;
    }

    // Handle 204 No Content or empty body
    if (response.status === 204) {
      return {};
    }

    const responseText = await response.text();
    try {
      return responseText ? JSON.parse(responseText) : {};
    } catch (e) {
      return {};
    }
  }

  // GET request
  async get(endpoint) {
    return this.request(endpoint, { method: "GET" });
  }

  // POST request
  async post(endpoint, data) {
    return this.request(endpoint, {
      method: "POST",
      body: JSON.stringify(data),
    });
  }

  // PUT request
  async put(endpoint, data) {
    return this.request(endpoint, {
      method: "PUT",
      body: JSON.stringify(data),
    });
  }

  // PATCH request
  async patch(endpoint, data) {
    return this.request(endpoint, {
      method: "PATCH",
      body: JSON.stringify(data),
    });
  }

  // DELETE request
  async delete(endpoint) {
    return this.request(endpoint, { method: "DELETE" });
  }
}

export default new ApiService();
