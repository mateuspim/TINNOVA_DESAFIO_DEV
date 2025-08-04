import { useState, useEffect } from "react";
import { vehicleService } from "../services/vehicleService";
import { brandService } from "../services/brandService";
import { useNavigate } from "react-router-dom";
import Box from "@mui/material/Box";
import { DataGrid } from "@mui/x-data-grid";

const VehicleList = () => {
  const [vehicles, setVehicles] = useState([]);
  const [brands, setBrands] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [totalPages, setTotalPages] = useState(1);
  const navigate = useNavigate();
  const [filters, setFilters] = useState({
    page: 1,
    size: 20,
    year: "",
    brand_id: "",
    color: "",
    is_sold: "",
  });

  // Load brands only once
  useEffect(() => {
    const loadBrands = async () => {
      try {
        const response = await brandService.getBrands();
        setBrands(response.items);
      } catch (error) {
        console.error("Erro ao carregar marcas:", error);
      }
    };
    loadBrands();
  }, []);

  const sanitizeFilters = (filters) => {
    const sanitized = {};
    Object.entries(filters).forEach(([key, value]) => {
      if (
        value !== "" &&
        value !== undefined &&
        !(typeof value === "number" && isNaN(value))
      ) {
        sanitized[key] = value;
      }
    });
    return sanitized;
  };

  // Load vehicles whenever filters change
  useEffect(() => {
    loadVehicles();
  }, [filters]);

  const loadVehicles = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await vehicleService.getVehicles(
        sanitizeFilters(filters)
      );
      setVehicles(response.items);
      setTotalPages(response.total);
    } catch (error) {
      setError("Erro ao carregar veículos.");
      setVehicles([]);
    } finally {
      setLoading(false);
    }
  };

  // Reset page to 1 when any filter except page/size changes
  const handleFilterChange = (key, value) => {
    setFilters((prev) => {
      if (key === "page") {
        return { ...prev, page: value };
      }
      if (key === "size") {
        return { ...prev, size: value, page: 1 };
      }
      return { ...prev, [key]: value, page: 1 };
    });
  };

  const columns = [
    { field: "id", headerName: "ID", width: 90 },
    {
      field: "model",
      headerName: "Vehicle model",
      width: 150,
      editable: false,
    },
    {
      field: "brand",
      headerName: "Brand",
      width: 150,
      editable: false,
      renderCell: (params) => <span>{params.row.brand.name}</span>,
    },
    {
      field: "year",
      headerName: "Year",
      width: 90,
      editable: false,
    },
    {
      field: "description",
      headerName: "Description",
      width: 150,
      editable: false,
    },
    {
      field: "color",
      headerName: "Color",
      width: 110,
      editable: false,
    },
    {
      field: "is_sold",
      headerName: "Sold",
      width: 90,
      editable: false,
      renderCell: (params) => <span>{params.row.is_sold ? "Yes" : "No"}</span>,
    },
    {
      field: "edit",
      headerName: "Edit",
      sortable: false,
      width: 160,
      renderCell: (params) => (
        <button onClick={() => navigate(`/vehicle/${params.row.id}`)}>
          Edit
        </button>
      ),
    },
  ];

  {
    !loading && vehicles.length === 0 && <div>No vehicle found</div>;
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

  return (
    <Box sx={{ height: 920, width: "100%" }}>
      <form
        onSubmit={(e) => {
          e.preventDefault();
        }}
        style={{ marginBottom: "1rem" }}
      >
        <label>
          Ano:
          <input
            type="number"
            value={filters.year}
            onChange={(e) => handleFilterChange("year", e.target.value)}
            style={{ width: 80, marginLeft: 4, marginRight: 12 }}
          />
        </label>
        <label>
          Marca:
          <select
            value={filters.brand_id}
            onChange={(e) => handleFilterChange("brand_id", e.target.value)}
            style={{ marginLeft: 4, marginRight: 12 }}
          >
            <option value="">Todas</option>
            {brands.map((brand) => (
              <option key={brand.id} value={brand.id}>
                {brand.name}
              </option>
            ))}
          </select>
        </label>
        <label>
          Cor:
          <input
            type="text"
            value={filters.color}
            onChange={(e) => handleFilterChange("color", e.target.value)}
            style={{ width: 100, marginLeft: 4, marginRight: 12 }}
          />
        </label>
        <label>
          Vendido:
          <select
            value={filters.is_sold}
            onChange={(e) =>
              handleFilterChange(
                "is_sold",
                e.target.value === "" ? "" : e.target.value === "true"
              )
            }
            style={{ marginLeft: 4, marginRight: 12 }}
          >
            <option value="">Todas</option>
            <option value="true">Sim</option>
            <option value="false">Não</option>
          </select>
        </label>
      </form>
      <button
        type="button"
        onClick={() =>
          setFilters({
            page: 1,
            size: 20,
            year: "",
            brand_id: "",
            color: "",
            is_sold: "",
          })
        }
      >
        Limpar filtros
      </button>
      <br></br>
      <br></br>
      <DataGrid
        rows={vehicles}
        columns={columns}
        rowCount={totalPages}
        pagination
        paginationMode="server"
        page={filters.page - 1}
        pageSize={filters.size}
        onPageChange={(newPage) => handleFilterChange("page", newPage + 1)}
        onPageSizeChange={(newSize) => handleFilterChange("size", newSize)}
        pageSizeOptions={[5, 10, 15, 20, 50]}
        loading={loading}
        disableRowSelectionOnClick
      />
    </Box>
  );
};

export default VehicleList;
