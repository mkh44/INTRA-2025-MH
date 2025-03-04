import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Get wavelength values between 400 and 800. Kept in nm to avoid float result being used in absorption_spectrum calculation.

wavelength = np.linspace(400, 800, 100)
temperature = 5800

# Define non-linear blackbody source spectrum function
def planck_law(wavelength, temperature):
    h = 6.626e-34 # Planck's constant (Js)
    c = 2.997e8 # Speed of light (m/s)
    k = 1.381e-23 # Boltzmann constant (J/K)

    return (2*h*c**2) / ((wavelength * 1e-9)**5 * (np.exp(h * c / (wavelength *1e-9 * k * temperature)) -1))

# Create blackbody spectrum for a given temperature
source_spectrum = planck_law(wavelength, temperature)

# Normalise source spectrum
source_spectrum /= np.sum(source_spectrum)

# Make atmospheric absorption spectrum
def absorption_spectrum(wavelength):

    return 0.5 + 0.4 * np.sin((wavelength - 400) * np.pi / 200)

#Add absorption bands maybe (Gaussian)

# Work out observed spectrum = of source_spectrum X atmospheric_absorption
observed_spectrum = source_spectrum * (1 - absorption_spectrum(wavelength))

#Define filter to remove light around target wavelength
def wavelength_filter(wavelength, target_wavelength, bandwidth=20):
    return np.where((wavelength > target_wavelength - bandwidth) & (wavelength < target_wavelength + bandwidth), 0, 1)

#Apply filter to remove red light (620 - 750 nm)
Filter_curve = wavelength_filter(wavelength,)

# Create DataFrame
spectral_data = pd.DataFrame({
    'Wavelength (nm)': wavelength,
    'Source Spectrum': source_spectrum,
    'Atmospheric Absorption': absorption_spectrum (wavelength),
    'Observed Spectrum': observed_spectrum})

# Plot data
plt.figure(figsize=(10, 6))
line1, = plt.plot(wavelength, source_spectrum, linestyle='--', label='Source Spectrum')
line2, = plt.plot(wavelength, absorption_spectrum(wavelength), linestyle='-.', label='Atmospheric Absorption')
line3, = plt.plot(wavelength, observed_spectrum, linewidth=2, label='Observed Spectrum')
plt.xlabel('Wavelength (nm)')
plt.ylabel('Intensity / Absorption')
plt.title('Spectral Data Visualisation')
plt.legend()
plt.grid()
plt.show()
