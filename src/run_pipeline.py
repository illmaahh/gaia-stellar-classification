import pandas as pd
from config import set_plot_style
from gaia_query import fetch_gaia_data
from analysis import (
    clean_data,
    compute_absolute_magnitude,
    select_halo_candidates,
    plot_hr_diagram,
    plot_sky_map
)

def main():
    set_plot_style()

    print("Fetching Gaia DR3 data...")
    df = fetch_gaia_data()

    print("Cleaning data...")
    df = clean_data(df)

    print("Computing absolute magnitudes...")
    df = compute_absolute_magnitude(df)

    print("Selecting halo candidates...")
    halo = select_halo_candidates(df)

    print(f"Halo candidates identified: {len(halo)}")

    print("Saving plots...")
    plot_hr_diagram(df, halo, "figures/hr_diagram.png")
    plot_sky_map(halo, "figures/sky_distribution.png")

    halo.to_csv("results/halo_star_candidates.csv", index=False)
    print("Pipeline completed successfully.")

if __name__ == "__main__":
    main()
