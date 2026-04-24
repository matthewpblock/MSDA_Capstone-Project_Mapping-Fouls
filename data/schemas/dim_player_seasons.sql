CREATE TABLE `mapping-nba-fouls.capstone_project.dim_player_seasons`
(
  player_id STRING,
  season_id STRING,
  full_name STRING,
  team_at_time STRING,
  position STRING,
  height_inches INT64,
  weight_lbs STRING,
  country STRING,
  school STRING,
  draft_year STRING,
  draft_round STRING,
  draft_number STRING,
  ft_pct FLOAT64,
  experience_yrs INT64,
  FTA INT64
)
CLUSTER BY player_id, season_id;