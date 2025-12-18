# ---------------------------------------------
# Gaia-based Stellar Classification Project
# ---------------------------------------------

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from astroquery.gaia import Gaia

# ---------------------------------------------
# STEP 1: Query Gaia DR3 data
# ---------------------------------------------

query = """
SELECT TOP 30000
source_id,
ra, dec,
parallax, parallax_error,
phot_g_mean_mag,
bp_rp
FROM gaiadr3.gaia_source
WHERE parallax IS NOT NULL
AND phot_g_mean_mag < 18
AND bp_rp IS NOT NULL
"""

print("Querying Gaia DR3...")
job = Gaia.launch_job(query)
results = job.get_results()
df = results.to_pandas()
print("Data downloaded:", len(df), "rows")

# ---------------------------------------------
# STEP 2: Data cleaning
# ---------------------------------------------

df = df[df["parallax"] > 0]
df = df[df["parallax_error"] / df["parallax"] < 0.2]

print("After cleaning:", len(df), "rows")

# ---------------------------------------------
# STEP 3: Compute distance and absolute magnitude
# ---------------------------------------------

df["distance_pc"] = 1000 / df["parallax"]
df["abs_mag"] = df["phot_g_mean_mag"] - 5 * np.log10(df["distance_pc"]) + 5

# ---------------------------------------------
# STEP 4: Identify halo star candidates
# ---------------------------------------------

halo_candidates = df[
    (df["bp_rp"] < 0.8) &
    (df["abs_mag"] > 3)
]

print("Halo candidates found:", len(halo_candidates))

# ---------------------------------------------
# STEP 5: HR Diagram
# ---------------------------------------------

plt.figure(figsize=(6, 6))
plt.scatter(df["bp_rp"], df["abs_mag"], s=1, alpha=0.3, label="All stars")
plt.scatter(
    halo_candidates["bp_rp"],
    halo_candidates["abs_mag"],
    s=6, color="red", label="Halo candidates"
)
plt.gca().invert_yaxis()
plt.xlabel("BP − RP")
plt.ylabel("Absolute G magnitude")
plt.title("HR Diagram from Gaia DR3")
plt.legend()
plt.tight_layout()
plt.savefig("figures/hr_diagram.png")
plt.show()

# ---------------------------------------------
# STEP 6: Sky distribution plot
# ---------------------------------------------

plt.figure(figsize=(7, 4))
plt.scatter(
    halo_candidates["ra"],
    halo_candidates["dec"],
    s=2
)
plt.xlabel("Right Ascension (deg)")
plt.ylabel("Declination (deg)")
plt.title("Sky distribution of halo star candidates")
plt.tight_layout()
plt.savefig("figures/sky_distribution.png")
plt.show()

# ---------------------------------------------
# STEP 7: Save results
# ---------------------------------------------

halo_candidates.to_csv("results/halo_star_candidates.csv", index=False)
print("Results saved in results/ folder")
