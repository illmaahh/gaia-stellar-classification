from astroquery.gaia import Gaia

def fetch_gaia_data(limit=30000):
    query = f"""
    SELECT TOP {limit}
    source_id, ra, dec,
    parallax, parallax_error,
    phot_g_mean_mag, bp_rp
    FROM gaiadr3.gaia_source
    WHERE parallax IS NOT NULL
    AND phot_g_mean_mag < 18
    AND bp_rp IS NOT NULL
    """

    job = Gaia.launch_job(query)
    return job.get_results().to_pandas()
