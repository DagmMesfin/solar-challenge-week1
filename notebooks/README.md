# Notebooks

This directory contains Jupyter notebooks used for data exploration, analysis, and visualization.

## Files

- `compare_countries.ipynb`: Compares solar irradiance metrics (GHI, DNI, DHI) across Benin, Sierra Leone, and Togo. Includes statistical testing (e.g., ANOVA or Kruskal–Wallis), visual summaries (boxplots, bar charts), and written observations.
- `benin_eda.ipynb`
- `sierraleone_eda.ipynb`
- `togo_eda.ipynb`:
  These three notebooks follow the same structure and analysis process for each respective country. They include:
  * Data loading and preprocessing
  * Time series analysis of solar irradiance metrics (GHI, DNI, DHI) and Ambient Temperature
  * Distribution analysis for GHI, DNI, and DHI
  * Correlation heatmaps and scatter plots for meteorological variables (e.g., humidity vs temperature)
  * Summary statistics and trends visualization

## Notes
- All notebooks rely on cleaned datasets found in the `data/` directory.
- The EDA workflow is consistent across all countries for fair comparison and uniform insights.

