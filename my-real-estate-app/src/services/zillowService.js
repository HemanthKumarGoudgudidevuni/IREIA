import axios from 'axios';

const ZILLOW_API_KEY = process.env.REACT_APP_ZILLOW_API_KEY;
const ZILLOW_BASE_URL = 'https://zillow-com1.p.rapidapi.com';

const zillowApi = axios.create({
  baseURL: ZILLOW_BASE_URL,
  headers: {
    'X-RapidAPI-Key': ZILLOW_API_KEY,
    'X-RapidAPI-Host': 'zillow-com1.p.rapidapi.com'
  }
});

export const searchProperties = async (params) => {
  try {
    const response = await zillowApi.get('/propertyExtendedSearch', {
      params: {
        location: params.location,
        home_type: params.propertyType,
        minPrice: params.minPrice,
        maxPrice: params.maxPrice,
        bedsMin: params.bedsMin,
        bathsMin: params.bathsMin,
        sqftMin: params.sqftMin,
        status_type: 'ForRent,ForSale',
        sort: 'Relevance',
        limit: 40
      }
    });
    return response.data;
  } catch (error) {
    console.error('Error fetching properties from Zillow:', error);
    throw error;
  }
};

export const getPropertyDetails = async (zpid) => {
  try {
    const response = await zillowApi.get('/property', {
      params: { zpid }
    });
    return response.data;
  } catch (error) {
    console.error('Error fetching property details:', error);
    throw error;
  }
};

export const getRentalEstimate = async (zpid) => {
  try {
    const response = await zillowApi.get('/rentEstimate', {
      params: { zpid }
    });
    return response.data;
  } catch (error) {
    console.error('Error fetching rental estimate:', error);
    throw error;
  }
}; 