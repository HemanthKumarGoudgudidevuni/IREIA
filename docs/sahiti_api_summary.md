# API Summary: Crime, Market Trend, and Population Data Extraction

## Overview

This repository provides analysis and extraction scripts for three key data sources:

1. **Crime Data** – Fetches crime incident records from any city(right now i am extracting Los Angeles) using a public data endpoint.
2. **Market Trend Data** – Extracts recent tweets about the location trends, latest news, trends via Twitter API v2.
3. **Population Data** – Retrieves population estimates for major U.S. cities using the U.S. Census Bureau's ACS5 2020(we can modify) API.

I have scripts and their corresponding data will support urban analytics, market sentiment evaluation, and demographic analysis for strategic decision-making.

---

## API Requests Tested

### 1. Crime Data API
- **API Name:** Los Angeles Crime Data API
- **Tested Endpoint:** `GET https://data.lacity.org/resource/2nrs-mtv8.json`
- **Request Parameters:** 
  - Pagination using `$limit` (1000 records per call) and `$offset` (incremented to fetch up to 5000 records)
- **Authentication:** None required (Public API)
- **Rate Limits:** Standard public API limits apply


### 2. Market Trend Data API (Twitter)
- **API Name:** Twitter API v2 – Recent Tweet Search
- **Tested Endpoint:** `GET https://api.twitter.com/2/tweets/search/recent`
- **Request Parameters:**
  - **Query:** `(locality trend OR crime) lang:en`
  - **Tweet Fields:** `created_at`, `text`, `public_metrics`
  - **Max Results:** 10 tweets per request
- **Authentication:** Bearer token required
- **Rate Limits:** 450 requests per 15-minute window


### 3. Population Data API (Census)
- **API Name:** U.S. Census Bureau ACS5 2020
- **Tested Endpoint:** `GET https://api.census.gov/data/2020/acs/acs5`
- **Request Parameters:**
  - **Data Fields:** `NAME` (geographic identifier) and `B01003_001E` (total population)
  - **Locations:** Iterates through a list of major U.S. cities identified by state and county FIPS codes
- **Authentication:** API key required

---

## Sample Data Response Format

### 1. Crime Data Response
\```json
{
    "dr_no": "201305761",
    "date_rptd": "2020-01-31T00:00:00.000",
    "date_occ": "2020-01-31T00:00:00.000",
    "time_occ": "2015",
    "area": "13",
    "area_name": "Newton",
    "rpt_dist_no": "1377",
    "part_1_2": "1",
    "crm_cd": "230",
    "crm_cd_desc": "ASSAULT WITH DEADLY WEAPON, AGGRAVATED ASSAULT",
    "mocodes": "1822 0416 1218",
    "vict_age": "69",
    "vict_sex": "F",
    "vict_descent": "H",
    "premis_cd": "101",
    "premis_desc": "STREET",
    "weapon_used_cd": "500",
    "weapon_desc": "UNKNOWN WEAPON/OTHER WEAPON",
    "status": "IC",
    "status_desc": "Invest Cont",
    "crm_cd_1": "230",
    "location": "5700    DUARTE                       ST",
    "lat": "33.9907",
    "lon": "-118.2422"
}
\```

### 2. Population Data Response (Sample for Multiple Cities)
\```
🔹 Data for San Francisco, CA:
['NAME', 'B01003_001E', 'state', 'county', 'tract']
['Census Tract 101.01, San Francisco County, California', '2045', '06', '075', '010101']
['Census Tract 101.02, San Francisco County, California', '1920', '06', '075', '010102']

🔹 Data for Los Angeles, CA:
['NAME', 'B01003_001E', 'state', 'county', 'tract']
['Census Tract 1997, Los Angeles County, California', '3006', '06', '037', '199700']
['Census Tract 1998.01, Los Angeles County, California', '3618', '06', '037', '199801']

🔹 Data for New York City, NY:
['NAME', 'B01003_001E', 'state', 'county', 'tract']
['Census Tract 165, New York County, New York', '6674', '36', '061', '016500']
['Census Tract 166, New York County, New York', '6002', '36', '061', '016600']
\```

## Data Field Descriptions

### Crime Data Fields
| Field Name | Description | Example Value |
|------------|-------------|---------------|
| dr_no | Unique identifier for the crime report | "201305761" |
| date_rptd | Date crime was reported | "2020-01-31T00:00:00.000" |
| area_name | Police district name | "Newton" |
| crm_cd_desc | Description of the crime | "ASSAULT WITH DEADLY WEAPON" |
| vict_age | Age of the victim | "69" |
| location | Street address of incident | "5700 DUARTE ST" |
| lat/lon | Geographic coordinates | "33.9907", "-118.2422" |

### Population Data Fields
| Field Name | Description | Example Value |
|------------|-------------|---------------|
| NAME | Census tract identifier | "Census Tract 101.01, San Francisco County, California" |
| B01003_001E | Total population count | "2045" |
| state | State FIPS code | "06" |
| county | County FIPS code | "075" |
| tract | Census tract code | "010101" |

## Data Integration & Analysis Guidelines

### 1. Data Preprocessing Requirements
- **Crime Data:**
  - Convert timestamps to standardized format
  - Validate coordinate pairs
  - Handle missing values in optional fields
  
- **Population Data:**
  - Parse tract identifiers for hierarchical analysis
  - Validate population counts
  - Group by geographic regions

### 2. Common Integration Scenarios
- Mapping crime incidents with population density
- Analyzing crime patterns in relation to demographic data
- Creating geographic visualizations of both datasets

### 3. Error Handling Considerations
- Handle API rate limiting gracefully
- Implement retry logic for failed requests
- Validate data completeness and integrity
- Log any data quality issues

## Next Steps & Recommendations

### Immediate Implementation Tasks
1. Set up automated data validation pipelines
2. Implement proper error handling and logging
3. Create data quality monitoring dashboards
4. Establish regular data refresh schedules

### Future Enhancements
1. Add support for additional cities and regions
2. Implement real-time data streaming where applicable
3. Develop advanced analytics capabilities
4. Create automated reporting systems

---

## Additional Resources

- [Los Angeles Open Data Portal](https://data.lacity.org/)
- [Census Bureau API Documentation](https://www.census.gov/data/developers/guidance.html)
- [Twitter API Documentation](https://developer.twitter.com/en/docs/twitter-api)
