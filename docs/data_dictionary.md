# Data Dictionary: Expected-Whistle-Engine (EWE-v3.8)

This document provides a comprehensive technical reference for the attributes within the `mapping-nba-fouls` data warehouse. These features power the **Dual-Branch Neural Network** and the **Strategic Geometry** framework.

---

## 1. Fact Tables

### `fct_shots`
The central hub for the **Spatial CNN Branch**, containing synchronized shot and whistle events.

| Attribute | Type | Description |
| :--- | :--- | :--- |
| `event_num` | `STRING` | Unique ID for the shot attempt within a specific game. |
| `season_id` | `STRING` | Standard NBA season identifier (e.g., '22023'). |
| `game_id` | `STRING` | Unique identifier for the game event. |
| `loc_x` | `INT64` | Normalized x-coordinate on a 50x47ft half-court model. |
| `loc_y` | `INT64` | Normalized y-coordinate on a 50x47ft half-court model. |
| `is_made` | `BOOL` | Binary flag: `TRUE` if the field goal was successful. |
| `is_foul_drawn` | `BOOL` | **Target Variable**: `TRUE` if a foul was whistled during the attempt. |
| `foul_event_num` | `STRING` | Key used for temporal-spatial synchronization with `fct_fouls`. |
| `shot_distance_ft` | `FLOAT64` | Euclidean distance from the center of the rim in feet. |

### `fct_fouls`
Granular logs of verified foul occurrences used to validate the whistle expectancy baselines.

| Attribute | Type | Description |
| :--- | :--- | :--- |
| `fouled_player_id` | `STRING` | ID of the player who drew the contact. |
| `is_shooting_foul` | `BOOL` | `TRUE` if the whistle resulted in free throw attempts. |
| `foul_category` | `STRING` | Classification (e.g., Shooting, Personal, Loose Ball). |
| `is_3pt` | `INT64` | Flag indicating if the fouled attempt was a three-point shot. |

---

## 2. Dimension Tables

### `dim_player_seasons`
Biometric and performance context for the **Tabular MLP Branch**.

| Attribute | Type | Description |
| :--- | :--- | :--- |
| `full_name` | `STRING` | The player's formal name. |
| `height_inches` | `INT64` | Physical height used to model structural leverage. |
| `ft_pct` | `FLOAT64` | **Critical Feature**: Seasonal FT% used to filter "intentional foul" noise. |
| `experience_yrs` | `INT64` | NBA service time; controls for veteran officiating bias. |
| `FTA` | `INT64` | Total Free Throw Attempts for the season. |

### `dim_games` & `dim_teams`
Metadata for longitudinal stability and visual standardization.

| Attribute | Type | Description |
| :--- | :--- | :--- |
| `is_playoff` | `BOOL` | Flag for regular season vs. postseason analysis. |
| `primary_color` | `STRING` | Hex code for team-specific visual mapping. |

---

## 3. Proprietary Strategic Metrics

These metrics are derived through the **Expected-Whistle-Engine** and drive the paper's final analysis.

| Metric | Context | Definition |
| :--- | :--- | :--- |
| **Signature Delta** | Skill Isolation | [cite_start]The residual between actual and model-predicted foul rates[cite: 314, 330]. |
| **Residual Capacity** | Headroom | [cite_start]The inverse of current shot frequency in a specific coordinate[cite: 315, 350, 550]. |
| **Signature Specialist** | Outliers | [cite_start]Players whose Signature Delta is statistically significant (formerly "Artisans")[cite: 359, 512]. |

### SOV Formula
[cite_start]The **Strategic Opportunity Value (SOV)** is the central composite metric of this study[cite: 315, 344]:

$$SOV = Localized Efficiency \times P(Whistle) \times \frac{1}{Volume}$$

---