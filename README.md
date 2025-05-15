# Spectral Data Visualisation: Blackbody Radiation and Atmospheric Absorption

This python script simulates the emission spectrum of a blackbody, applies atmospheric absorption effects, including Rayleigh scattering, filters specific wavelength bands and visualises the resulting photon counts with error bars. 

## Installation

Install required Python libraries using:

```bash
pip install numpy pandas matplotlib
```

## Usage
Use the script in the file:
```python
photon_counting_non-linear_spectrum
```
When prompted, enter the temperature of the blackbody in Kelvin or press Enter to use the default, the approximate surface temperature of the Sun (5780 K). You will then be prompted to enter the number of photons to use (default 1,000,000). Choose an atmospheric model; Rayleigh scattering only or Rayleigh scattering with Ozone absorption bands. Choose how many filters to apply (0-2). You will be prompted to enter the target wavelength and bandwidth for each filter. The resulting spectra will be plotted.

## Roadmap
The program is modular and templated to allow for new features. In the future we plan to include more atmospheric models; humidity, time dependant models (sunset/sunrise) etc. and include options for other thermal sources not just blackbody. We also plan to generate spectra using actual observation data & compare their variance against each other.
