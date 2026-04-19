# MSDA_Capstone-Project_Mapping-Fouls

This repository contains the source code for my Capstone project for the M.S. in Data Analytics degree at Northwest Missouri State University. The subject is focused on geospatially mapping NBA fouls to discover actionable steps players can take to increase their fouls drawn or decrease their fouling.

## Project Overview
*(Provide a brief abstract of your methodology, findings, and the significance of the research here. Explain what a "Critical Section" Foul Map is.)*

## Data Sources
*(Explain where the NBA foul and shot data comes from—e.g., NBA API, Kaggle, BigQuery Public Datasets—and mention any preprocessing steps you took.)*

## Prerequisites & Installation
To run the scripts and visualizations in this repository, you will need Python 3.8+ and the following libraries installed:

```bash
pip install pandas numpy matplotlib scipy requests pillow google-cloud-bigquery
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
