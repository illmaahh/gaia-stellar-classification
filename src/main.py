# STEP 1: Import libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from astroquery.gaia import Gaia
import plotly.express as px

# STEP 2: Download Gaia data
print("Downloading Gaia data...")

query = """
SELECT TOP 20000
source_id,
ra, dec,
parallax, parallax_error,
phot_g_mean_mag,
bp_rp
FROM gaiadr3.gaia_source
WHERE parallax IS NOT NULL
AND bp_rp IS NOT NULL
AND phot_g_mean_mag < 18
"""

job = Gaia.launch_job(query)
data = job.get_results().to_pandas()

print("Data downloaded")

# STEP 3: Clean data
data = data[data["parallax"] > 0]
data = data[data["parallax_error"] / data["parallax"] < 0.2]

# STEP 4: Calculate distance and absolute magnitude
data["distance_pc"] = 1000 / data["parallax"]
data["abs_mag"] = data["phot_g_mean_mag"] - 5 * np.log10(data["distance_pc"]) + 5

# STEP 5: Select halo star candidates
halo = data[(data["bp_rp"] < 0.8) & (data["abs_mag"] > 3)]

print("Halo stars found:", len(halo))

# STEP 6: HR diagram (AUTOMATICALLY OPENS)
plt.figure(figsize=(6,6))
plt.scatter(data["bp_rp"], data["abs_mag"], s=1, alpha=0.3)
plt.scatter(halo["bp_rp"], halo["abs_mag"], s=6, color="red")
plt.gca().invert_yaxis()
plt.xlabel("BP - RP")
plt.ylabel("Absolute G magnitude")
plt.title("Gaia HR Diagram")
plt.savefig("figures/hr_diagram.png")
plt.show()


# STEP 8: Interactive plot (ZOOM + HOVER)
fig = px.scatter(
    halo,
    x="bp_rp",
    y="abs_mag",
    title="Interactive HR Diagram (Halo Stars)",
)
fig.update_yaxes(autorange="reversed")
fig.show()

# STEP 9: Save results
halo.to_csv("results/halo_stars.csv", index=False)

print("Project completed successfully")
