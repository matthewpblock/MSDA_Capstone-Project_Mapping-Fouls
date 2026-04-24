# Data Warehouse Schemas: Expected-Whistle-Engine (EWE-v3.8)

This directory contains the Data Definition Language (DDL) scripts required to reconstruct the BigQuery data warehouse used for the **Expected-Whistle-Engine (EWE-v3.8)**. The architecture follows a **Star Schema** design, optimized for high-performance geospatial analysis and multi-modal neural network training.

## Star Schema Overview

The warehouse is structured around two primary fact tables and three supporting dimension tables. To optimize query performance across 1.4 million records, critical tables utilize **Clustering** on high-cardinality fields such as `season_id`, `player_id`, and the target variable `is_foul_drawn`.


### Fact Tables

* [cite_start]**`fct_shots`**: The central repository of temporal-spatial synchronized shot attempts. [cite_start]It contains the target variable `is_foul_drawn` and normalized coordinates (`loc_x`, `loc_y`) used for the **Spatial CNN Branch**. 
* [cite_start]**`fct_fouls`**: A granular log of 231,459 verified foul events. [cite_start]It includes categorical flags for `is_shooting_foul` and `foul_category` (e.g., Personal, Loose Ball), which were used to validate the whistle expectancy baselines.

### Dimension Tables

* [cite_start]**`dim_player_seasons`**: Provides the "physical context" for the **Tabular MLP Branch**. [cite_start]This includes biometric features like `height_inches`, `experience_yrs`, and the critical **`ft_pct`** feature used to control for tactical defensive aggression.
* **`dim_games`**: Contains metadata for over 16,000 NBA games, including `is_playoff` flags to facilitate longitudinal stability analysis[cite: 1].
* [cite_start]**`dim_teams`**: Stores team identity data, including primary and secondary colors used for standardizing visual heatmaps and the **Strategic Geometry** case studies[cite: 3].

## Key Feature Definitions

| Column | Data Type | Description |
| :--- | :--- | :--- |
| `loc_x`, `loc_y` | `INT64` | Normalized court coordinates scaled to a 50x47ft half-court model[cite: 4, 5]. |
| `is_foul_drawn` | `BOOL` | Primary target variable; indicates if a shot attempt resulted in a whistle. |
| `ft_pct` | `FLOAT64` | Season-level free-throw proficiency; used to filter "intentional foul" noise. |
| `foul_event_num` | `STRING` | The unique identifier used to link shots in `fct_shots` to foul records in `fct_fouls` via temporal-spatial synchronization. |

## Implementation Instructions

These DDL scripts are compatible with **Google BigQuery Standard SQL**. To deploy this schema:

1. Create a dataset named `capstone_project` within your BigQuery project.
2. Execute the `.sql` files in this directory in the following order to maintain relational integrity:
    * `dim_teams.sql`
    * `dim_games.sql`
    * `dim_player_seasons.sql`
    * `fct_fouls.sql`
    * `fct_shots.sql`