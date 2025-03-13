import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Get wavelength values between 400 and 800. Kept in nm to avoid float result being used in absorption_spectrum calculation.

wavelength = np.linspace(400, 800, 100)
temperature = 5800

#Define filter to remove light around target wavelength
def wavelength_filter(wavelength, target_wavelength, bandwidth=65):
    return np.where((wavelength > target_wavelength - bandwidth) & (wavelength < target_wavelength + bandwidth), 0, 1)

# Define non-linear blackbody source spectrum function
def planck_law(wavelength, temperature):
    h = 6.626e-34 # Planck's constant (Js)
    c = 2.997e8 # Speed of light (m/s)
    k = 1.381e-23 # Boltzmann constant (J/K)

    return (2*h*c**2) / ((wavelength * 1e-9)**5 * (np.exp(h * c / (wavelength *1e-9 * k * temperature)) -1))

# Make atmospheric absorption spectrum
def absorption_spectrum(wavelength):

    return 0.5 + 0.4 * np.sin((wavelength - 400) * np.pi / 200)

# Create blackbody spectrum for a given temperature
source_spectrum = planck_law(wavelength, temperature)

# Normalise source spectrum
source_spectrum /= np.sum(source_spectrum)


#Add absorption bands maybe (Gaussian)

# Work out observed spectrum = of source_spectrum X atmospheric_absorption
observed_spectrum = source_spectrum * (1 - absorption_spectrum(wavelength))


#Apply filter to remove red light (620 - 750 nm) so 685 nm +/- 65
filter_curve = wavelength_filter(wavelength, target_wavelength=685, bandwidth=65)
filtered_spectrum = observed_spectrum * filter_curve

# Create DataFrame
spectral_data = pd.DataFrame({
    'Wavelength (nm)': wavelength,
    'Source Spectrum': source_spectrum,
    'Atmospheric Absorption': absorption_spectrum (wavelength),
    'Observed Spectrum': observed_spectrum})

# Plot data
fig, ax1 = plt.subplots(figsize=(10, 6))

# 1st y axis
ax1.plot(wavelength, source_spectrum * 100, linestyle='--', label='Source Spectrum', color='red')
ax1.plot(wavelength, observed_spectrum * 100, linewidth=2, label='Observed Spectrum')
ax1.plot(wavelength, filtered_spectrum * 100, linewidth=2, linestyle="dotted", label='Filtered Spectrum')

ax1.set_xlabel('Wavelength (nm)')
ax1.set_ylabel('Intensity (%)')

ax1.set_ylim(0, 5) # this is set to 110 so source spectrum is visible
ax1.legend(loc='upper left')
ax1.grid()

# 2nd y Axis
ax2 = ax1.twinx()
ax2.plot(wavelength, absorption_spectrum(wavelength) * 100, linestyle='-.', label='Atmospheric Absorption')
ax2.set_ylabel('Intensity (%)')
ax2.set_ylim(0, 110)
ax2.legend(loc='upper right')
ax2.grid()

plt.title('Spectral Data Visualisation')
plt.show()
