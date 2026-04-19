"""
NBA Foul Geography Visualizer
A module for generating the "Critical Section" Foul Map.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import RegularPolygon
from matplotlib.colors import LinearSegmentedColormap
from scipy.ndimage import gaussian_filter
import requests
from PIL import Image
import os
from io import BytesIO
from google.cloud import bigquery
import warnings

warnings.filterwarnings('ignore')

# --- BRAND & PALETTE SETTINGS ---
BRAND_DARK = '#394146'
BRAND_WHITE = '#E6E6E6'
BRAND_GREY = '#8A8D8F'
FOUL_HIGH = '#CF142B'

foul_cmap = LinearSegmentedColormap.from_list("foul_pressure", [BRAND_GREY, FOUL_HIGH])

PROJECT_ID = os.environ.get("BQ_PROJECT_ID", "mapping-nba-fouls")
DATASET_ID = os.environ.get("BQ_DATASET_ID", "capstone_project")

# --- HELPER FUNCTIONS ---

def draw_court_accurate(ax, color='white', lw=1.5, paint_fill_color=None):
    """Draws an accurate NBA half-court."""
    if paint_fill_color:
        ax.add_patch(patches.Rectangle((-80, -52.5), 160, 190, facecolor=paint_fill_color, alpha=0.25, zorder=1))
    ax.add_patch(patches.Rectangle((-250, -52.5), 500, 470, linewidth=lw, color=color, fill=False, zorder=10))
    ax.plot([-250, 250], [417.5, 417.5], color=color, lw=lw, zorder=10)
    ax.add_patch(patches.Rectangle((-80, -52.5), 160, 190, linewidth=lw, color=color, fill=False, zorder=10))
    ax.add_patch(patches.Rectangle((-60, -52.5), 120, 190, linewidth=lw, color=color, fill=False, zorder=10))
    ax.add_patch(patches.Arc((0, 137.5), 120, 120, theta1=0, theta2=180, linewidth=lw, color=color, zorder=10))
    ax.add_patch(patches.Arc((0, 137.5), 120, 120, theta1=180, theta2=360, linewidth=lw, color=color, linestyle='dashed', zorder=10))
    ax.add_patch(patches.Circle((0, 0), radius=7.5, linewidth=lw, color=color, fill=False, zorder=10))
    ax.plot([-30, 30], [-12.5, -12.5], color=color, lw=lw*1.5, zorder=10)
    ax.add_patch(patches.Arc((0, 0), 80, 80, theta1=0, theta2=180, linewidth=lw, color=color, zorder=10))
    ax.add_patch(patches.Arc((0, 417.5), 40, 40, theta1=180, theta2=360, linewidth=lw, color=color, zorder=10))
    ax.add_patch(patches.Arc((0, 417.5), 120, 120, theta1=180, theta2=360, linewidth=lw, color=color, zorder=10))
    ax.plot([-220, -220], [-52.5, 89.477], color=color, lw=lw, zorder=10)
    ax.plot([220, 220], [-52.5, 89.477], color=color, lw=lw, zorder=10)
    ax.add_patch(patches.Arc((0, 0), 475, 475, theta1=22.13, theta2=157.87, linewidth=lw, color=color, zorder=10))
    ax.add_patch(patches.Rectangle((-86.6, 17.5), 6.6, 10, linewidth=lw, color=color, facecolor=color, zorder=10))
    ax.add_patch(patches.Rectangle((80, 17.5), 6.6, 10, linewidth=lw, color=color, facecolor=color, zorder=10))
    for y_val in [57.5, 87.5, 117.5]:
        ax.plot([-80, -86.6], [y_val, y_val], color=color, lw=lw, zorder=10)
        ax.plot([80, 86.6], [y_val, y_val], color=color, lw=lw, zorder=10)
    ax.plot([-250, -220], [227.5, 227.5], color=color, lw=lw, zorder=10)
    ax.plot([250, 220], [227.5, 227.5], color=color, lw=lw, zorder=10)
    ax.plot([-110, -110], [-52.5, -42.5], color=color, lw=lw, zorder=10)
    ax.plot([110, 110], [-52.5, -42.5], color=color, lw=lw, zorder=10)
    return ax

def get_visual_data(df_s, df_f, grid_w=20, min_cnt=5):
    """Calculates hexbin data and topographic contours."""
    if df_s.empty:
        return [], [], [], None, None, None
        
    hb = plt.hexbin(df_s['loc_x'], df_s['loc_y'], C=df_s['foul_val'], reduce_C_function=np.mean,
                    gridsize=grid_w, extent=[-250, 250, -52.5, 417.5], mincnt=min_cnt, visible=False)
    verts, rates = hb.get_offsets(), hb.get_array()

    hb_c = plt.hexbin(df_s['loc_x'], df_s['loc_y'], gridsize=grid_w, extent=[-250, 250, -52.5, 417.5], mincnt=min_cnt, visible=False)
    counts = hb_c.get_array()

    if not df_f.empty:
        cnts, xedges, yedges = np.histogram2d(df_f['loc_x'], df_f['loc_y'], bins=40, range=[[-250, 250], [-52.5, 417.5]])
        smoothed = gaussian_filter(cnts, sigma=1.5)
    else:
        smoothed, xedges, yedges = None, None, None
        
    plt.close()
    return verts, counts, rates, smoothed, xedges, yedges


# --- MAIN MODULE FUNCTION ---

def ind_foul_map(player_id: str, year: int):
    """
    Generates a Critical Section Foul Map for a given player and season.
    
    Args:
        player_id (str): The NBA Player ID string (e.g., '1628983').
        year (int): The season end year (e.g., 2024 for the 2023-24 season).
    """
    client = bigquery.Client(project=PROJECT_ID)
    
    # Format seasons for query (e.g. 2024 -> ('22024', '42024'))
    seasons_tuple = f"('2{year}', '4{year}')"
    season_title = f"{year-1}-{str(year)[-2:]}"

    # 1. Fetch Player Name & Team
    query_meta = f"""
        SELECT p.player_name, s.team_abbr 
        FROM `{PROJECT_ID}.{DATASET_ID}.fct_shots` s
        JOIN `{PROJECT_ID}.{DATASET_ID}.dim_players` p ON s.player_id = p.player_id
        WHERE s.player_id = '{player_id}' AND s.season_id IN {seasons_tuple} 
        LIMIT 1
    """
    try: 
        meta_df = client.query(query_meta).to_dataframe().iloc[0]
        player_name = meta_df['player_name']
        team_abbr = meta_df['team_abbr']
    except Exception as e: 
        print(f"Warning: Could not fetch metadata for player {player_id}. Error: {e}")
        player_name = "Unknown Player"
        team_abbr = "NBA"

    # 2. Fetch Colors
    color_query = f"SELECT primary_color, secondary_color FROM `{PROJECT_ID}.{DATASET_ID}.dim_teams` WHERE team_abbr = '{team_abbr}'"
    try:
        team_colors = client.query(color_query).to_dataframe().iloc[0]
        primary = team_colors['primary_color']
        secondary = team_colors['secondary_color']
    except Exception as e:
        print(f"Warning: Could not fetch colors for team {team_abbr}. Error: {e}")
        primary = '#007AC1'; secondary = '#EF3B24' # Fallback

    # 3. Fetch Shot & Foul Data
    query_shots = f"SELECT loc_x, loc_y, CAST(is_foul_drawn AS INT64) as foul_val FROM `{PROJECT_ID}.{DATASET_ID}.fct_shots` WHERE player_id = '{player_id}' AND season_id IN {seasons_tuple}"
    df_shots = client.query(query_shots).to_dataframe()

    query_fouls = f"SELECT loc_x, loc_y FROM `{PROJECT_ID}.{DATASET_ID}.fct_fouls` WHERE player_id = '{player_id}' AND season_id IN {seasons_tuple}"
    df_fouls = client.query(query_fouls).to_dataframe()
    
    if df_shots.empty:
        print(f"No shot data found for {player_name} in {season_title}.")
        return

    # 4. Bin Data
    HEX_WIDTH = 25.0
    MAX_R = HEX_WIDTH / np.sqrt(3)
    verts, counts, rates, smoothed, xedges, yedges = get_visual_data(df_shots, df_fouls)

    # 5. Summary Stats
    tot_shots = len(df_shots)
    tot_fouls = len(df_fouls)
    sht_foul_pct = (df_shots['foul_val'].sum() / tot_shots) * 100 if tot_shots > 0 else 0

    # 6. Visualization Rendering
    fig = plt.figure(figsize=(16, 12), facecolor=BRAND_DARK)

    # Main Court Axis
    ax = fig.add_axes([0.05, 0.08, 0.5868, 0.82])
    ax.set_facecolor(BRAND_DARK)
    ax.set_aspect('equal') 

    # Layer 1: Hexagons
    if len(counts) > 0:
        size_ranks = pd.qcut(counts, 5, labels=False, duplicates='drop') + 1
        for pos, rank, rate in zip(verts, size_ranks, rates):
            radius = (rank / 5) * MAX_R
            color = foul_cmap(min(rate / 0.40, 1.0))
            ax.add_patch(RegularPolygon(pos, 6, radius=radius, orientation=0, facecolor=color,
                                        edgecolor=BRAND_DARK, linewidth=0.2, alpha=0.9, zorder=2))

    # Layer 2 & 3: Topography & Court
    if smoothed is not None:
        X, Y = np.meshgrid(xedges[:-1], yedges[:-1])
        lvls = np.percentile(smoothed[smoothed > 0], [50, 75, 90, 98])
        ax.contour(X, Y, smoothed.T, levels=lvls, colors=secondary, linewidths=1.2, alpha=0.6, zorder=6)
        
    draw_court_accurate(ax, color=primary, lw=2, paint_fill_color=primary)
    ax.set_xlim(-260, 260); ax.set_ylim(-65, 480); ax.axis('off')

    # 7. Sidebar
    fig.text(0.68, 0.93, "SUMMARY STATS", color=BRAND_WHITE, fontsize=12, weight='bold')
    fig.text(0.68, 0.90, f"Total Shots: {tot_shots:,}", color=BRAND_WHITE, fontsize=11)
    fig.text(0.68, 0.87, f"Total Fouls Drawn: {tot_fouls:,}", color=BRAND_WHITE, fontsize=11)
    fig.text(0.68, 0.84, f"Shooting Foul Prob: {sht_foul_pct:.1f}%", color=FOUL_HIGH, fontsize=11, weight='bold')
    fig.text(0.68, 0.78, "TOPOGRAPHY: All Foul Density", color=secondary, fontsize=11, weight='bold')

    # Color Legend
    cb_ax = fig.add_axes([0.72, 0.55, 0.02, 0.20])
    sm = plt.cm.ScalarMappable(cmap=foul_cmap, norm=plt.Normalize(vmin=0, vmax=40))
    cb = fig.colorbar(sm, cax=cb_ax)
    cb.outline.set_visible(False)
    cb.ax.yaxis.set_tick_params(color=BRAND_WHITE, labelcolor=BRAND_WHITE)
    cb.set_label('FOUL PROBABILITY (%)', color=BRAND_WHITE, size=10, weight='bold', labelpad=15)

    # Size Legend
    ax_leg = fig.add_axes([0.68, 0.28, 0.15, 0.25])
    ax_leg.set_aspect('equal') 
    ax_leg.axis('off')
    ax_leg.set_xlim(0, 133); ax_leg.set_ylim(0, 166)
    ax_leg.text(0, 160, "SHOT VOLUME (Hex = 2.5ft)", color=BRAND_WHITE, weight='bold', size=11)

    if len(counts) > 0:
        bins = np.round(pd.qcut(counts, 5, retbins=True, duplicates='drop')[1]).astype(int)
        num_bins = len(bins) - 1
        y_spacing = 110 / max(1, (num_bins - 1)) if num_bins > 1 else 0

        for i in range(1, num_bins + 1):
            r_val = (i / 5.0) * MAX_R
            y_pos = 135 - ((i - 1) * y_spacing)
            ax_leg.add_patch(RegularPolygon((30, y_pos), 6, radius=r_val, orientation=np.pi/2,
                                            facecolor=secondary, alpha=0.8))

            if i == 1: label = f"{bins[0]} - {bins[1]} shots"
            elif i == num_bins: label = f"{bins[i-1] + 1}+ shots"
            else: label = f"{bins[i-1] + 1} - {bins[i]} shots"
            ax_leg.text(55, y_pos, label, color=BRAND_GREY, size=10, va='center')

    # Player Photo
    try:
        img_url = f"https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/latest/260x190/{player_id}.png"
        img = Image.open(BytesIO(requests.get(img_url).content)).convert("RGBA")
        ax_photo = fig.add_axes([0.68, 0.08, 0.20, 0.20])
        ax_photo.axis('off')
        ax_photo.imshow(img)
    except Exception as e:
        print(f"Warning: Could not load player photo. Error: {e}")

    # Header
    fig.text(0.05, 0.94, "CRITICAL SECTION // FOUL MAPPING", color=BRAND_WHITE, fontsize=28, fontweight='bold')
    fig.text(0.05, 0.91, f"{player_name.upper()} // {team_abbr} // {season_title} AGGREGATE", color=BRAND_GREY, fontsize=14)

    plt.show()

# --- EXAMPLE USAGE ---
# if __name__ == "__main__":
#    ind_foul_map(player_id="1628983", year=2024)
