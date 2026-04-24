CREATE TABLE `mapping-nba-fouls.capstone_project.fct_fouls`
(
  event_num STRING,
  season_id STRING,
  game_id STRING,
  period INT64,
  game_clock STRING,
  game_clock_seconds FLOAT64,
  player_id STRING,
  team_id STRING,
  fouled_player_id STRING,
  loc_x INT64,
  loc_y INT64,
  is_shooting_foul BOOL,
  foul_category STRING,
  description STRING,
  distance_from_basket_ft FLOAT64,
  is_3pt INT64
)
CLUSTER BY season_id, player_id, foul_category;