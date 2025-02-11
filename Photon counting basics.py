import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Get wavelength values between 400 and 800
wavelength = np.linspace(400, 800, 100)

# Define simple linear progression for source spectrum
source_spectrum = np.linspace(1, 10, 100)

# Define different linear progression for atmospheric absorption spectrum
atmospheric_absorption = np.linspace(0, 1, 100)

# Work out observed spectrum = of source_spectrum X atmospheric_absorption
observed_spectrum = source_spectrum * atmospheric_absorption

# Create DataFrame
spectral_data = pd.DataFrame({
    'Wavelength (nm)': wavelength,
    'Source Spectrum': source_spectrum,
    'Atmospheric Absorption': atmospheric_absorption,
    'Observed Spectrum': observed_spectrum})

# Plot data
plt.figure(figsize=(10, 6))
line1, = plt.plot(wavelength, source_spectrum, linestyle='--', label='Source Spectrum')
line2, = plt.plot(wavelength, atmospheric_absorption, linestyle='-.', label='Atmospheric Absorption')
line3, = plt.plot(wavelength, observed_spectrum, linewidth=2, label='Observed Spectrum')
plt.xlabel('Wavelength (nm)')
plt.ylabel('Intensity / Absorption')
plt.title('Spectral Data Visualisation')
plt.legend()
plt.grid()
plt.show()