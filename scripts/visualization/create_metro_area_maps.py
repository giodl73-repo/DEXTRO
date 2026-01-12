#!/usr/bin/env python3
"""
Create focused maps for major metro areas showing congressional districts.

This script generates detailed maps for the top 20 MSAs (Metropolitan Statistical Areas)
showing how congressional districts are configured within major urban areas.

Example usage:
    python scripts/visualization/create_metro_area_maps.py --year 2020 --version v2
    python scripts/visualization/create_metro_area_maps.py --year 2020 --version v2 --metros "New York" "Los Angeles"
"""

import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.patheffects as path_effects
import pickle
from pathlib import Path
import argparse
import sys
import os
from tqdm import tqdm

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Import configuration files
try:
    from scripts.config_2020 import STATE_CONFIG_2020
    STATE_CONFIG = STATE_CONFIG_2020
except ImportError:
    STATE_CONFIG = None

# Top 20 MSAs by population (2020 Census)
# Each metro pinned to its primary state for organization
TOP_METROS = {
    # State: [(metro_name, short_name), ...]
    'NY': [("New York-Newark-Jersey City, NY-NJ-PA", "new_york")],
    'CA': [
        ("Los Angeles-Long Beach-Anaheim, CA", "los_angeles"),
        ("San Francisco-Oakland-Berkeley, CA", "san_francisco"),
        ("Riverside-San Bernardino-Ontario, CA", "riverside"),
        ("San Diego-Chula Vista-Carlsbad, CA", "san_diego"),
    ],
    'IL': [("Chicago-Naperville-Elgin, IL-IN-WI", "chicago")],
    'TX': [
        ("Dallas-Fort Worth-Arlington, TX", "dallas"),
        ("Houston-The Woodlands-Sugar Land, TX", "houston"),
    ],
    'VA': [("Washington-Arlington-Alexandria, DC-VA-MD-WV", "washington")],
    'PA': [("Philadelphia-Camden-Wilmington, PA-NJ-DE-MD", "philadelphia")],
    'FL': [
        ("Miami-Fort Lauderdale-Pompano Beach, FL", "miami"),
        ("Tampa-St. Petersburg-Clearwater, FL", "tampa"),
    ],
    'GA': [("Atlanta-Sandy Springs-Alpharetta, GA", "atlanta")],
    'MA': [("Boston-Cambridge-Newton, MA-NH", "boston")],
    'AZ': [("Phoenix-Mesa-Chandler, AZ", "phoenix")],
    'MI': [("Detroit-Warren-Dearborn, MI", "detroit")],
    'WA': [("Seattle-Tacoma-Bellevue, WA", "seattle")],
    'MN': [("Minneapolis-St. Paul-Bloomington, MN-WI", "minneapolis")],
    'CO': [("Denver-Aurora-Lakewood, CO", "denver")],
    'MO': [("St. Louis, MO-IL", "st_louis")],
}


def load_all_states_with_districts(us_dir, year='2020'):
    """Load all states with their district assignments."""
    us_dir = Path(us_dir)

    all_tracts = []

    # Get position for progress reporting
    position = int(os.environ.get('TQDM_POSITION', '-1'))
    send_status = position >= 0

    def report_progress(msg):
        if send_status:
            print(f"STATUS:{position}:{msg}", flush=True)

    if send_status:
        report_progress("Loading state district data")

    # Load state config
    if STATE_CONFIG is None:
        raise ValueError("Could not load STATE_CONFIG. Import from scripts.config_2020 failed.")

    # Iterate through states
    for state_code, config in STATE_CONFIG.items():
        state_name = config['name']

        state_dir = us_dir / 'states' / state_name.lower().replace(' ', '_')
        tracts_file = f'data/raw/{state_code.lower()}_tracts_{year}.parquet'
        assignments_file = state_dir / 'final_assignments.pkl'

        if not Path(tracts_file).exists():
            continue

        tracts = gpd.read_parquet(tracts_file)

        if assignments_file.exists():
            with open(assignments_file, 'rb') as f:
                assignments = pickle.load(f)
            tracts['district'] = [assignments[i] for i in range(len(tracts))]
        else:
            # Single-district state
            tracts['district'] = 1

        tracts['state_code'] = state_code
        tracts['state_name'] = state_name

        all_tracts.append(tracts)

    us_tracts = pd.concat(all_tracts, ignore_index=True)

    # Create unique district IDs across all states
    us_tracts['unique_district_id'] = (
        us_tracts.groupby(['state_code', 'district']).ngroup() + 1
    )

    return us_tracts


def create_metro_map(metro_name, metro_geometry, us_tracts, places_gdf, output_file, dpi=150):
    """
    Create a focused map for a single metro area.

    Args:
        metro_name: Name of the MSA
        metro_geometry: Shapely geometry of the MSA boundary
        us_tracts: GeoDataFrame with all tracts and district assignments
        places_gdf: GeoDataFrame with city/place boundaries
        output_file: Path to save the map
        dpi: Resolution for output image
    """

    # Find tracts within or intersecting the metro boundary
    metro_tracts = us_tracts[us_tracts.intersects(metro_geometry)].copy()

    if len(metro_tracts) == 0:
        print(f"  WARNING: No tracts found in {metro_name}")
        return False

    # Get unique districts in this metro
    metro_districts = metro_tracts.groupby(['state_code', 'district']).first().reset_index()

    print(f"  {metro_name}: {len(metro_districts)} districts, {len(metro_tracts)} tracts")

    # Dissolve tracts into districts
    districts_gdf = metro_tracts.dissolve(by=['state_code', 'district'], as_index=False)
    districts_gdf['district_label'] = districts_gdf.apply(
        lambda row: f"{row['state_code']}-{row['district']}", axis=1
    )

    # Project to appropriate CRS for plotting (Albers Equal Area)
    districts_proj = districts_gdf.to_crs('EPSG:5070')

    # Get extent with 10% margin
    minx, miny, maxx, maxy = districts_proj.total_bounds
    margin = 0.10
    width = maxx - minx
    height = maxy - miny
    extent = [
        minx - margin * width,
        maxx + margin * width,
        miny - margin * height,
        maxy + margin * height
    ]

    # Create figure
    fig, ax = plt.subplots(figsize=(14, 10), dpi=dpi)

    # Plot districts with distinct colors
    n_districts = len(districts_gdf)
    cmap = plt.colormaps.get_cmap('tab20').resampled(n_districts)

    for idx, (_, district) in enumerate(districts_proj.iterrows()):
        district_geom = gpd.GeoSeries([district.geometry], crs='EPSG:5070')
        district_geom.plot(
            ax=ax,
            color=cmap(idx),
            edgecolor='black',
            linewidth=0.8,
            alpha=0.7
        )

        # Add district label at centroid
        centroid = district.geometry.centroid
        if centroid.within(district.geometry):
            ax.text(
                centroid.x, centroid.y,
                district['district_label'],
                fontsize=10,
                fontweight='bold',
                ha='center',
                va='center',
                color='white',
                zorder=10
            ).set_path_effects([
                path_effects.Stroke(linewidth=2, foreground='black'),
                path_effects.Normal()
            ])

    # Add cities/places labels if available
    if places_gdf is not None and len(places_gdf) > 0:
        # Filter places within metro area
        metro_places = places_gdf[places_gdf.intersects(metro_geometry)].copy()

        if len(metro_places) > 0:
            # Show top 10 cities by population
            metro_places = metro_places.nlargest(10, 'population')
            metro_places_proj = metro_places.to_crs('EPSG:5070')

            for _, place in metro_places_proj.iterrows():
                centroid = place.geometry.centroid
                ax.text(
                    centroid.x, centroid.y,
                    place['NAME'],
                    fontsize=7,
                    ha='center',
                    va='top',
                    color='black',
                    fontweight='normal',
                    alpha=0.7,
                    zorder=5
                )

    # Set extent and styling
    ax.set_xlim(extent[0], extent[1])
    ax.set_ylim(extent[2], extent[3])
    ax.set_aspect('equal')
    ax.axis('off')

    # Title
    plt.title(
        f"{metro_name}\nCongressional Districts",
        fontsize=16,
        fontweight='bold',
        pad=20
    )

    # Save
    output_file.parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(output_file, dpi=dpi, bbox_inches='tight')
    plt.close()

    return True


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Create focused maps for major metro areas showing congressional districts'
    )
    parser.add_argument(
        '--year',
        type=int,
        default=2020,
        help='Census year (default: 2020)'
    )
    parser.add_argument(
        '--version',
        type=str,
        default='v2',
        help='Output version (default: v2)'
    )
    parser.add_argument(
        '--output-dir',
        type=str,
        default=None,
        help='Output directory (default: outputs/us_{year}_{version})'
    )
    parser.add_argument(
        '--dpi',
        type=int,
        default=150,
        help='Image resolution (default: 150)'
    )
    parser.add_argument(
        '--metros',
        type=str,
        nargs='*',
        default=None,
        help='Specific metros to generate (default: all top 20)'
    )

    args = parser.parse_args()

    # Set output directory
    if args.output_dir:
        output_dir = Path(args.output_dir)
    else:
        output_dir = Path(f'outputs/us_{args.year}_{args.version}')

    # Get position for progress reporting
    position = int(os.environ.get('TQDM_POSITION', '-1'))
    send_status = position >= 0
    is_standalone = not send_status

    def report_progress(msg):
        if send_status:
            print(f"STATUS:{position}:{msg}", flush=True)

    # Banner
    if is_standalone:
        print(f"\n{'='*80}")
        print(f"Creating Metro Area District Maps")
        print(f"{'='*80}")
        print(f"Year: {args.year}")
        print(f"Version: {args.version}")
        print(f"Output: {output_dir}/states/*/maps/metros/*.png")
        print(f"DPI: {args.dpi}")
        print(f"{'='*80}\n")

    # Load CBSA boundaries
    cbsa_file = f'data/raw/us_cbsa_{args.year}.parquet'
    if not Path(cbsa_file).exists():
        print(f"ERROR: CBSA boundaries not found at {cbsa_file}")
        print(f"Run: python scripts/data/geography/download_metro_boundaries.py --year {args.year}")
        return 1

    report_progress("Loading MSA boundaries")
    cbsa_gdf = gpd.read_parquet(cbsa_file)

    # Filter to MSAs only (exclude Micropolitan)
    msa_gdf = cbsa_gdf[cbsa_gdf['LSAD'] == 'M1'].copy()
    print(f"Loaded {len(msa_gdf)} Metropolitan Statistical Areas")

    # Load all state districts
    report_progress("Loading state districts")
    us_tracts = load_all_states_with_districts(output_dir, year=str(args.year))
    print(f"Loaded {len(us_tracts)} tracts with district assignments")

    # Load places data for city labels
    places_all = []
    for state_code in STATE_CONFIG.keys():
        places_file = f'data/raw/{state_code.lower()}_places_{args.year}.parquet'
        if Path(places_file).exists():
            places = gpd.read_parquet(places_file)
            places['state_code'] = state_code
            places_all.append(places)

    if places_all:
        places_gdf = pd.concat(places_all, ignore_index=True)
        print(f"Loaded {len(places_gdf)} cities/places")
    else:
        places_gdf = None
        print("WARNING: No places data found. Maps will not include city labels.")

    # Process metros by state
    total_metros = 0
    successful = 0
    failed = 0

    for state_code, metros_list in TOP_METROS.items():
        state_name = STATE_CONFIG[state_code]['name']
        state_dir = output_dir / 'states' / state_name.lower().replace(' ', '_') / 'maps' / 'metros'

        print(f"\nProcessing {state_code} ({state_name}): {len(metros_list)} metro(s)")

        for metro_name, short_name in metros_list:
            total_metros += 1

            # Create output filename
            output_file = state_dir / f"{short_name}.png"

            # Skip if already exists
            if output_file.exists():
                successful += 1
                print(f"  [SKIP] Already exists: {output_file}")
                continue

            report_progress(f"Creating metro map {total_metros}: {metro_name}")

            # Find metro in MSA dataset
            metro_match = msa_gdf[msa_gdf['NAME'] == metro_name]

            if len(metro_match) == 0:
                # Try partial match
                metro_short = metro_name.split(',')[0]
                metro_match = msa_gdf[msa_gdf['NAME'].str.startswith(metro_short)]

            if len(metro_match) == 0:
                print(f"  [X] MSA not found in dataset: {metro_name}")
                failed += 1
                continue

            metro_row = metro_match.iloc[0]
            metro_geometry = metro_row.geometry

            try:
                success = create_metro_map(
                    metro_name=metro_name,
                    metro_geometry=metro_geometry,
                    us_tracts=us_tracts,
                    places_gdf=places_gdf,
                    output_file=output_file,
                    dpi=args.dpi
                )

                if success:
                    successful += 1
                    print(f"  [OK] Saved: {output_file}")
                else:
                    failed += 1

            except Exception as e:
                print(f"  [ERROR] creating map for {metro_name}: {e}")
                import traceback
                traceback.print_exc()
                failed += 1
                continue

    # Summary
    if is_standalone:
        print(f"\n{'='*80}")
        print(f"Metro Area Maps Complete")
        print(f"{'='*80}")
        print(f"Total Metros: {total_metros}")
        print(f"Successful: {successful}")
        print(f"Failed: {failed}")
        print(f"Output: {output_dir}/states/*/maps/metros/*.png")
        print(f"{'='*80}\n")

    return 0 if failed == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
