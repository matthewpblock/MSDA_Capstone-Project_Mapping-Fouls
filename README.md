# MSDA Capstone: Expected-Whistle-Engine (EWE-v3.8) & Strategic Geometry

[!Python 3.8+](https://www.python.org/downloads/)
[!Google BigQuery](https://cloud.google.com/bigquery)
[!License: MIT](https://opensource.org/licenses/MIT)

This repository contains the source code, data schema, and visualization modules for my M.S. in Data Analytics Capstone Project at Northwest Missouri State University. 

Moving beyond traditional descriptive spatial analysis (e.g., standard shot charts), this project introduces **Strategic Geometry**—a prescriptive tactical optimization framework designed to map, predict, and exploit the spatial clustering of NBA fouls.

## Abstract & Methodology

Historically, basketball analytics has heavily focused on shot selection and defensive efficiency, leaving the spatial dynamics of officiating and foul provocation as a largely unexplored frontier. This project bridges that gap by introducing the **Expected-Whistle-Engine (EWE-v3.8)**. 

The EWE-v3.8 utilizes a **Dual-Branch Neural Network** to evaluate foul probabilities across the hardwood:
* **Spatial CNN Branch:** Analyzes normalized $(x, y)$ coordinate data from over 1.4 million synchronized shot and foul events to model geographic "rim gravity" and localized officiating tendencies.
* **Tabular MLP Branch:** Incorporates physical profiles (height, weight, experience) and tactical context (e.g., season FT%) to control for physical leverage and defensive strategies like "Hack-a-Shaq".

By isolating a player's **Signature Delta** (their innate foul-drawing skill vs. the model's geographic baseline) and identifying zones of high **Residual Capacity** (untapped usage potential), the framework outputs the **Strategic Opportunity Value (SOV)**. This allows teams to prescribe **Critical Sections** where players can strategically shift usage to maximize foul-drawing efficiency.

## Repository Structure

* `foulmaps.py` - Core mapping module handling BigQuery data extraction, hexbin transformations, topographical modeling, and matplotlib rendering.
* `data/schemas/` - DDL scripts defining the Google BigQuery Star Schema (optimized via clustering for temporal-spatial synchronization).
* `docs/` - Contains the academic definitions for the proprietary metrics (`metric_definitions.md`) and the comprehensive data dictionary (`data_dictionary.md`).
* `notebooks/` - Exploratory Jupyter notebooks used for initial EDA, coordinate normalization, and neural network prototyping.

## Architecture & Data Pipeline

The project leverages a modern, high-performance cloud data warehouse architecture:
1. **Data Ingestion:** Raw temporal-spatial data is scraped from the NBA Stats API.
2. **ELT Process:** Data is transformed and loaded into a Google BigQuery Star Schema (`capstone_project` dataset). 
3. **Storage:** The schema encompasses over 1.4 million `fct_shots` records and 231,459 verified `fct_fouls`, clustered by `season_id`, `player_id`, and categorical targets for multi-modal neural network training.
4. **Application Layer:** Python modules directly query BigQuery using parameterized execution to render multi-layered **"Critical Section" Foul Maps**.

## Prerequisites & Installation

To run the visualization scripts locally, Python 3.8+ is required. It is highly recommended to use an isolated virtual environment.

```bash
# Clone the repository
git clone https://github.com/your-username/MSDA_Capstone-Project_Mapping-Fouls.git
cd MSDA_Capstone-Project_Mapping-Fouls

# Install required dependencies
pip install -r requirements.txt
```

### Google Cloud Authentication

The visualization engine (`foulmaps.py`) dynamically queries Google BigQuery. You must authenticate via a Service Account with the appropriate IAM roles (`BigQuery Data Viewer`, `BigQuery User`).

Set your environment variables before running:
```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account-file.json"
export BQ_PROJECT_ID="mapping-nba-fouls"
export BQ_DATASET_ID="capstone_project"
```

## Usage: Critical Section Foul Maps

You can generate a bespoke, multi-layered "Critical Section" Foul Map for any player by importing the core module. The map utilizes hexagonal binning (to show shot volume) layered under topographical contours (highlighting overall foul density).

```python
from foulmaps import ind_foul_map

# Generate the Critical Section map for player ID 1628983 (e.g., Shai Gilgeous-Alexander) 
# for the 2023-24 NBA Season
ind_foul_map(player_id="1628983", year=2024)
```

## Academic Citation & License

If you use the concepts of **Strategic Opportunity Value (SOV)**, **Signature Delta**, or the **Expected-Whistle-Engine** in your own research or publications, please cite this repository. 

This project is licensed under the MIT License - see the `LICENSE` file for details.
