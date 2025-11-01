Project Samarth - BuildForBharat <img src="https://github.com/user-attachments/assets/155f61a6-76e0-4189-a563-249b41d3775e" width="80" height="80" align="left" style="margin-right: 20px;">

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/Python-3.9+-brightgreen.svg)](https://www.python.org/downloads/release/python-390/)
[![Streamlit App](https://img.shields.io/badge/Streamlit-App-red)](https://streamlit.io/)
[![Data Source](https://img.shields.io/badge/Data-Data.gov.in-orange)](https://data.gov.in/)

Project Samarth is a chatbot built using LangGraph and DuckDB, designed to provide accurate, secure, and reliable information about crop production and rainfall data across various states in India.

<img width="1080" height="610" alt="mermaid-diagram-2025-11-01-043129" src="https://github.com/user-attachments/assets/f980acb6-c9c3-42ef-aa52-74cb0b8bebb5" />


## Getting Started

To get started with Project Samarth, follow these steps:

Note: This project requires the use of an API-key of an extrernal LLM, please make sure to configure it properly and store it responsibly

1. **Clone the repository:**
   ```bash
   git clone https://github.com/shreshtha26mtech/Project-Samarth-BuildForBharat.git
   cd Project-Samarth-BuildForBharat
   ```

2. **Install dependencies:**
   ```bash
    pip install -e .
   ```

3. **Run the application:**
   ```bash
   streamlit run main.py
   ```
   After running the application, you will be greeted with an interface similar to this:
   <img width="1304" height="806" alt="image" src="https://github.com/user-attachments/assets/cf1b2898-f8e4-45af-af9b-98ba184c02db" />
   
Now you can ask the questions and it will answer
<img width="1151" height="761" alt="Screenshot 2025-10-31 220826" src="https://github.com/user-attachments/assets/057a1fb2-a1a4-40e7-abc5-c5552bfae165" />


## System Architecture

Project Samarth follows a sophisticated agent-based architecture using LangGraph to process natural language queries about agricultural and rainfall data.
<img width="1080" height="610" alt="mermaid-diagram-2025-11-01-043743" src="https://github.com/user-attachments/assets/184784d3-44e4-4651-ad53-ecedab103345" />

1. **User Query**: The user asks a natural language question through the Streamlit interface (e.g., "What was the rice production in Punjab during 2020?")

2. **Query Processing**: The LangGraph agent processes the query through multiple intelligent nodes:
   - **List Tables**: Identifies available tables in the database
   - **Schema Analysis**: Examines database structure and relationships
   - **Query Generation**: LLM converts the natural language question into optimized SQL queries
   - **Query Execution**: Executes the generated SQL against DuckDB

3. **Data Retrieval**: DuckDB fetches the relevant rows from the pre-loaded agricultural datasets

4. **Response Generation**: The system converts the structured database results into natural language summaries

5. **Presentation**: The final answer is presented to the user through the Streamlit interface

The agent architecture ensures robust query handling with proper error recovery and optimized database interactions.


## Data Sources

The data used by Project Samarth is sourced from [data.gov.in](https://data.gov.in), specifically from these datasets:

1. **[Sub-divisional Monthly Rainfall (1901-2017)](https://www.data.gov.in/resource/sub-divisional-monthly-rainfall-1901-2017)** - Comprehensive rainfall data across Indian sub-divisions
3. **[District-wise Season-wise Crop Production Statistics](https://www.data.gov.in/catalog/district-wise-season-wise-crop-production-statistics-0)** - Detailed crop production data by district and season

**Note:** Ensure you adhere to data.gov.in's terms of use and data policies when using this data. Always check for updates and changes in the dataset schema.

After some preprocessing, this is what the datasets look like:

**rainfall**

| SUBDIVISION              | YEAR | JAN  | FEB  | MAR  | APR  | MAY   | JUN   | JUL   | AUG   | OCT   | NOV   | DEC   | ANNUAL | JF    | MAM   | JJAS  | OND  | State                       | Zone  |
|---------------------------|------|------|------|------|------|-------|-------|-------|-------|-------|-------|-------|---------|-------|-------|-------|------|------------------------------|-------|
| Andaman & Nicobar Islands | 1901 | 49.2 | 87.1 | 29.2 | 2.3  | 528.8 | 517.5 | 365.1 | 481.1 | 388.5 | 558.2 | 33.6  | 3373.2 | 136.3 | 560.3 | 1696.3 | 980.3 | Andaman and Nicobar Islands | South |
| Andaman & Nicobar Islands | 1902 | 0.0  | 159.8 | 12.2 | 0.0  | 446.1 | 537.1 | 228.9 | 753.7 | 197.2 | 359.0 | 160.5 | 3520.7 | 159.8 | 458.3 | 2185.9 | 716.7 | Andaman and Nicobar Islands | South |

**crops**
| column0 | State_Name                   | District_Name | Crop_Year | Season      | Crop               | Area  | Production | Zone  |
|----------|------------------------------|----------------|------------|-------------|--------------------|-------|-------------|-------|
| 0        | Andaman and Nicobar Islands | NICOBARS       | 2000       | Kharif      | Arecanut           | 1254.0 | 2000.0      | South |
| 1        | Andaman and Nicobar Islands | NICOBARS       | 2000       | Kharif      | Other Kharif pulses | 2.0   | 1.0         | South |
| 2        | Andaman and Nicobar Islands | NICOBARS       | 2000       | Kharif      | Rice               | 102.0 | 321.0       | South |


Please note that in order to get the most accurate results from the data, ask questions related to crops for years **2000-2014** and for rainfall related to years **1901-2017**

## Dependencies

This project uses `pyproject.toml` for dependency management. All required packages are specified in the project configuration file.


## Contributions

We welcome contributions to Project Samarth! If you have suggestions for new features, bug fixes, or improvements, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Implement your changes.
4. Submit a pull request.



## License

This project is licensed under the MIT License.

---






