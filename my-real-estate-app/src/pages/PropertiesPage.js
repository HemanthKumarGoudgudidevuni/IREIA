import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { GoogleMap, LoadScript, Marker, InfoWindow } from '@react-google-maps/api';
import { 
  Box, 
  Container, 
  Grid, 
  Typography, 
  CircularProgress,
  Pagination,
  Chip,
  Slider,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  TextField,
  Button,
  Card,
  CardContent,
  CardMedia,
  IconButton,
  Tooltip
} from '@mui/material';
import { 
  FilterList, 
  Map, 
  List, 
  Favorite, 
  Share, 
  LocationOn,
  Bed,
  Bathtub,
  SquareFoot
} from '@mui/icons-material';
import { searchProperties } from '../services/zillowService';
import '../styles/PropertiesPage.css';

const PropertiesPage = () => {
  const navigate = useNavigate();
  const [properties, setProperties] = useState([]);
  const [selectedProperty, setSelectedProperty] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');
  const [currentPage, setCurrentPage] = useState(1);
  const [viewMode, setViewMode] = useState('grid'); // 'grid' or 'list'
  const [filters, setFilters] = useState({
    priceRange: [0, 2000000],
    beds: '',
    baths: '',
    propertyType: '',
    sortBy: 'price_asc'
  });
  const [showFilters, setShowFilters] = useState(false);
  const propertiesPerPage = 6;
  const [mapCenter, setMapCenter] = useState({ lat: 42.3601, lng: -71.0589 });
  const [mapZoom, setMapZoom] = useState(12);

  useEffect(() => {
    const fetchProperties = async () => {
      try {
        setIsLoading(true);
    const query = new URLSearchParams(window.location.search);
        const location = query.get("location") || "Boston, MA";
        const propertyType = query.get("type") || "Houses";
        
        const params = {
          location,
          propertyType,
          status_type: 'ForRent,ForSale',
          ...filters
        };

        const response = await searchProperties(params);
        
        if (response?.props) {
          setProperties(response.props);
          if (response.props.length > 0) {
            const firstProp = response.props[0];
            setMapCenter({
              lat: firstProp.latitude,
              lng: firstProp.longitude
            });
          }
        } else {
          setError("No properties found in this area.");
        }
      } catch (err) {
        console.error("Error fetching properties:", err);
        setError("Unable to fetch properties. Please try again later.");
      } finally {
        setIsLoading(false);
      }
    };

    fetchProperties();
  }, [filters]);

  const handlePropertyClick = (property) => {
    setSelectedProperty(property);
    setMapCenter({
      lat: property.latitude,
      lng: property.longitude
    });
    setMapZoom(15);
  };

  const handleMarkerClick = (property) => {
    setSelectedProperty(property);
  };

  const handleFilterChange = (field, value) => {
    setFilters(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handlePageChange = (event, value) => {
    setCurrentPage(value);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const indexOfLast = currentPage * propertiesPerPage;
  const indexOfFirst = indexOfLast - propertiesPerPage;
  const currentProperties = properties.slice(indexOfFirst, indexOfLast);
  const totalPages = Math.ceil(properties.length / propertiesPerPage);

  return (
    <Box className="properties-page">
      <Container maxWidth="xl">
        <Box className="properties-header">
          <Typography variant="h4" component="h1" gutterBottom>
            Available Properties
          </Typography>
          <Box className="view-controls">
            <Tooltip title="Grid View">
              <IconButton 
                onClick={() => setViewMode('grid')}
                color={viewMode === 'grid' ? 'primary' : 'default'}
              >
                <Grid />
              </IconButton>
            </Tooltip>
            <Tooltip title="List View">
              <IconButton 
                onClick={() => setViewMode('list')}
                color={viewMode === 'list' ? 'primary' : 'default'}
              >
                <List />
              </IconButton>
            </Tooltip>
            <Tooltip title="Filters">
              <IconButton 
                onClick={() => setShowFilters(!showFilters)}
                color={showFilters ? 'primary' : 'default'}
              >
                <FilterList />
              </IconButton>
            </Tooltip>
          </Box>
        </Box>

        {showFilters && (
          <Box className="filters-section">
            <Grid container spacing={2}>
              <Grid item xs={12} sm={6} md={3}>
                <Typography gutterBottom>Price Range</Typography>
                <Slider
                  value={filters.priceRange}
                  onChange={(e, newValue) => handleFilterChange('priceRange', newValue)}
                  valueLabelDisplay="auto"
                  min={0}
                  max={2000000}
                  step={10000}
                />
              </Grid>
              <Grid item xs={12} sm={6} md={3}>
                <FormControl fullWidth>
                  <InputLabel>Bedrooms</InputLabel>
                  <Select
                    value={filters.beds}
                    onChange={(e) => handleFilterChange('beds', e.target.value)}
                  >
                    <MenuItem value="">Any</MenuItem>
                    <MenuItem value="1">1+</MenuItem>
                    <MenuItem value="2">2+</MenuItem>
                    <MenuItem value="3">3+</MenuItem>
                    <MenuItem value="4">4+</MenuItem>
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={12} sm={6} md={3}>
                <FormControl fullWidth>
                  <InputLabel>Bathrooms</InputLabel>
                  <Select
                    value={filters.baths}
                    onChange={(e) => handleFilterChange('baths', e.target.value)}
                  >
                    <MenuItem value="">Any</MenuItem>
                    <MenuItem value="1">1+</MenuItem>
                    <MenuItem value="2">2+</MenuItem>
                    <MenuItem value="3">3+</MenuItem>
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={12} sm={6} md={3}>
                <FormControl fullWidth>
                  <InputLabel>Property Type</InputLabel>
                  <Select
                    value={filters.propertyType}
                    onChange={(e) => handleFilterChange('propertyType', e.target.value)}
                  >
                    <MenuItem value="">Any</MenuItem>
                    <MenuItem value="Houses">Houses</MenuItem>
                    <MenuItem value="Apartments">Apartments</MenuItem>
                    <MenuItem value="Condos">Condos</MenuItem>
                  </Select>
                </FormControl>
              </Grid>
            </Grid>
          </Box>
        )}

        <Box className="properties-container">
          <Box className="properties-list">
            {isLoading ? (
              <Box className="loading-container">
                <CircularProgress />
                <Typography>Loading properties...</Typography>
              </Box>
            ) : error ? (
              <Typography color="error" className="error-message">
                {error}
              </Typography>
          ) : (
            <>
                <Grid container spacing={3} className={viewMode === 'grid' ? 'property-grid' : 'property-list'}>
                  {currentProperties.map((property) => (
                    <Grid item xs={12} sm={viewMode === 'grid' ? 6 : 12} key={property.zpid}>
                      <Card 
                        className="property-card"
                        onClick={() => handlePropertyClick(property)}
                      >
                        <CardMedia
                          component="img"
                          height="200"
                          image={property.imgSrc || '/default-property.jpg'}
                          alt={property.address}
                        />
                        <CardContent>
                          <Typography variant="h6" component="h3">
                            {property.address}
                          </Typography>
                          <Box className="property-meta">
                            <Chip icon={<LocationOn />} label={property.city} size="small" />
                            <Chip icon={<Bed />} label={`${property.bedrooms} beds`} size="small" />
                            <Chip icon={<Bathtub />} label={`${property.bathrooms} baths`} size="small" />
                            <Chip icon={<SquareFoot />} label={`${property.livingArea} sq ft`} size="small" />
                          </Box>
                          <Typography variant="h5" color="primary">
                            ${property.price?.toLocaleString()}
                          </Typography>
                          <Typography variant="body2" color="text.secondary">
                            Rent: ${property.rentZestimate?.toLocaleString()}/month
                          </Typography>
                          <Box className="property-actions">
                            <IconButton>
                              <Favorite />
                            </IconButton>
                            <IconButton>
                              <Share />
                            </IconButton>
                          </Box>
                        </CardContent>
                      </Card>
                    </Grid>
                  ))}
                </Grid>

                <Box className="pagination-container">
                  <Pagination
                    count={totalPages}
                    page={currentPage}
                    onChange={handlePageChange}
                    color="primary"
                    size="large"
                  />
                </Box>
              </>
            )}
          </Box>

          <Box className="map-container">
            <LoadScript googleMapsApiKey="AIzaSyAC2_CrKzi9aSnFXsQdwixcuEVzPmdNbnk">
              <GoogleMap
                mapContainerStyle={{ width: '100%', height: '100%' }}
                center={mapCenter}
                zoom={mapZoom}
                options={{
                  styles: [
                    {
                      featureType: "poi",
                      elementType: "labels",
                      stylers: [{ visibility: "off" }]
                    }
                  ]
                }}
              >
                {properties.map((property) => (
                  <Marker
                    key={property.zpid}
                    position={{ lat: property.latitude, lng: property.longitude }}
                    onClick={() => handleMarkerClick(property)}
                    icon={{
                      url: `data:image/svg+xml;charset=UTF-8,${encodeURIComponent(`
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">
                          <path fill="${selectedProperty?.zpid === property.zpid ? '#1976d2' : '#f44336'}" d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7z"/>
                        </svg>
                      `)}`,
                      scaledSize: new window.google.maps.Size(24, 24),
                      anchor: new window.google.maps.Point(12, 12)
                    }}
                  />
                ))}

                {selectedProperty && (
                  <InfoWindow
                    position={{ lat: selectedProperty.latitude, lng: selectedProperty.longitude }}
                    onCloseClick={() => setSelectedProperty(null)}
                  >
                    <Box className="info-window">
                      <Typography variant="h6">{selectedProperty.address}</Typography>
                      <Typography variant="subtitle1" color="primary">
                        ${selectedProperty.price?.toLocaleString()}
                      </Typography>
                      <Typography variant="body2">
                        Rent: ${selectedProperty.rentZestimate?.toLocaleString()}/month
                      </Typography>
                      <Box className="property-meta">
                        <Chip icon={<Bed />} label={`${selectedProperty.bedrooms} beds`} size="small" />
                        <Chip icon={<Bathtub />} label={`${selectedProperty.bathrooms} baths`} size="small" />
                        <Chip icon={<SquareFoot />} label={`${selectedProperty.livingArea} sq ft`} size="small" />
                      </Box>
                    </Box>
                  </InfoWindow>
                )}
              </GoogleMap>
            </LoadScript>
          </Box>
        </Box>
      </Container>
    </Box>
  );
};

export default PropertiesPage;