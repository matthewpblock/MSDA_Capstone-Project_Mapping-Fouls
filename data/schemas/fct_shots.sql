CREATE TABLE `mapping-nba-fouls.capstone_project.fct_shots`
(
  event_num STRING,
  season_id STRING,
  game_id STRING,
  period INT64,
  game_clock_seconds FLOAT64,
  game_clock STRING,
  player_id STRING,
  team_id STRING,
  loc_x INT64,
  loc_y INT64,
  is_made BOOL,
  is_foul_drawn BOOL,
  foul_event_num STRING,
  attempt_type STRING,
  shot_distance FLOAT64,
  shot_distance_ft FLOAT64,
  is_3pt INT64
)
CLUSTER BY season_id, player_id, is_foul_drawn;