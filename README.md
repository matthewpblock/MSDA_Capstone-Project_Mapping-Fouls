# MSDA_Capstone-Project_Mapping-Fouls

This repository contains the source code for my Capstone project for the M.S. in Data Analytics degree at Northwest Missouri State University. The subject is focused on geospatially mapping NBA fouls to discover actionable steps players can take to increase their fouls drawn or decrease their fouling.

## Abstract & Methodology
Historically, basketball analytics has heavily focused on shot charts and defensive efficiency. However, the spatial mapping of fouls remains a largely unexplored frontier. This project aims to highlight the spatial clustering of drawn and committed fouls across the NBA to help teams generate strategic insights.

The tool generates a **"Critical Section" Foul Map**. Using hexagonal binning, it maps a player's shot locations layered with topographical contours that highlight overall foul density. The intensity of the color corresponds to the probability of drawing a shooting foul in that zone.

## Repository Structure
* `/foulmaps.py` - Core mapping module handling data extraction, transformations, and visualization rendering.
* `/notebooks/` - Contains exploratory Jupyter notebooks used for initial data analysis (if applicable).
* `/data/` - Holds mock datasets and data dictionary references.

## Data Pipeline
Data is queried dynamically from a Google BigQuery data warehouse. It relies on two main fact tables and two dimension tables:
* `fct_shots`: Geographic data (x, y coordinates) for every shot taken, along with foul outcome flags.
* `fct_fouls`: Geographic data for committed and drawn fouls.
* `dim_players` & `dim_teams`: Dimensional metadata for linking names, abbreviations, and primary team hex colors.

*Note: The raw data is scraped from the NBA Stats API and loaded into BigQuery via a separate ELT process.*

## Prerequisites & Installation
To run the scripts and visualizations in this repository, you will need Python 3.8+. It is recommended to run this in an isolated virtual environment.

```bash
# Clone the repository
git clone https://github.com/your-username/MSDA_Capstone-Project_Mapping-Fouls.git
cd MSDA_Capstone-Project_Mapping-Fouls

# Install dependencies
pip install -r requirements.txt
```

You will also need to authenticate with Google Cloud to access the BigQuery datasets. Set the following environment variables:
```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account-file.json"
export BQ_PROJECT_ID="mapping-nba-fouls"
export BQ_DATASET_ID="capstone_project"
```

## Usage
You can generate an individual player's Foul Map by importing the module and running the `ind_foul_map` function:
```python
from foulmaps import ind_foul_map

# Generate a map for player ID 1628983 for the 2023-24 season
ind_foul_map(player_id="1628983", year=2024)
```

## License
*(Consider adding an academic or open-source license statement here, such as MIT or Apache 2.0.)*
