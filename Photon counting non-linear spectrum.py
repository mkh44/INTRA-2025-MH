import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Get wavelength values between 400 and 800
wavelength = np.linspace(400, 800, 100)

# Define non-linear blackbody source spectrum
def planck_law(wavelength, temperature):
    h = 6.626e-34 # Planck's constant (Js)
    c = 2.997e8 # Speed of light (m/s)
    k = 1.381e-23 # Boltzmann constant (J/K)

    return (2*h*c**2) / ((wavelength * 1e-9)**5) * 1/(np.exp(h*c / (wavelength * 1e-9) * k * temperature) - 1)

# Define blackbody spectrum for a given temperature
temperature =5800
source_spectrum = planck_law(wavelength, temperature)

# Normalise source spectrum
source_spectrum /= np.sum(source_spectrum)

# Make atmospheric absorption spectrum
def absorption_spectrum(wavelength, temperature):

    return 0.5 + 0.4 * np.sin((wavelength - 400) * np.pi / 200)

#Add absorption bands maybe (Gaussian)

# Work out observed spectrum = of source_spectrum X atmospheric_absorption
observed_spectrum = source_spectrum * (1 - absorption_spectrum)

# Create DataFrame
spectral_data = pd.DataFrame({
    'Wavelength (nm)': wavelength,
    'Source Spectrum': source_spectrum,
    'Atmospheric Absorption': absorption_spectrum,
    'Observed Spectrum': observed_spectrum})

# Plot data
plt.figure(figsize=(10, 6))
line1, = plt.plot(wavelength, source_spectrum, linestyle='--', label='Source Spectrum')
line2, = plt.plot(wavelength, absorption_spectrum, linestyle='-.', label='Atmospheric Absorption')
line3, = plt.plot(wavelength, observed_spectrum, linewidth=2, label='Observed Spectrum')
plt.xlabel('Wavelength (nm)')
plt.ylabel('Intensity / Absorption')
plt.title('Spectral Data Visualisation')
plt.legend()
plt.grid()
plt.show()
