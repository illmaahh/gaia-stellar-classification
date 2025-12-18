import numpy as np
import matplotlib.pyplot as plt

def clean_data(df):
    df = df[df["parallax"] > 0]
    df = df[df["parallax_error"] / df["parallax"] < 0.2]
    return df

def compute_absolute_magnitude(df):
    df["distance_pc"] = 1000 / df["parallax"]
    df["abs_mag"] = df["phot_g_mean_mag"] - 5 * np.log10(df["distance_pc"]) + 5
    return df

def select_halo_candidates(df):
    return df[(df["bp_rp"] < 0.8) & (df["abs_mag"] > 3)]

def plot_hr_diagram(df, halo, output_path):
    plt.scatter(df["bp_rp"], df["abs_mag"], s=1, alpha=0.3, label="All stars")
    plt.scatter(halo["bp_rp"], halo["abs_mag"], s=8, color="crimson", label="Halo candidates")
    plt.gca().invert_yaxis()
    plt.xlabel("BP − RP")
    plt.ylabel("Absolute G magnitude")
    plt.title("Gaia DR3 Hertzsprung–Russell Diagram")
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

def plot_sky_map(halo, output_path):
    plt.scatter(halo["ra"], halo["dec"], s=3, alpha=0.7)
    plt.xlabel("Right Ascension (deg)")
    plt.ylabel("Declination (deg)")
    plt.title("Sky Distribution of Halo Star Candidates")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
