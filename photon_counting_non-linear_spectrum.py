import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Get wavelength values between 400 and 800. Kept in nm to avoid float result being used in absorption_spectrum calculation.
wavelength = np.linspace(400, 800, 100)

# defining constants
h = 6.626e-34  # Planck's constant (Js)
c = 2.997e8  # Speed of light (m/s)
k = 1.381e-23  # Boltzmann constant (J/K)

# Get user input for temperature, defaulting to 5780 K if no input given
def get_temperature():
    while True:
        user_input = input('Enter temperature of blackbody in Kelvin (default; 5780 K): ').strip()
        if user_input == '': # default value if input is empty
            temperature = 5780
            print(f'The temperature is: {temperature} K')
            return 5780
        try:
            temperature = float(user_input)
            print(f'The temperature is: {temperature} K')
            return temperature
        except ValueError:
            print('Invalid input. Please enter a valid number or press enter for default (5780 K)')

# Defining variable temperature
temperature = get_temperature()


# Define filter to remove light around target wavelength
def wavelength_filter(spectrum, wavelength, target_wavelength, bandwidth):
    filter_mask = np.where((wavelength > target_wavelength - bandwidth) & (wavelength < target_wavelength + bandwidth), 0, 1)
    return spectrum * filter_mask

# Define non-linear blackbody source spectrum function
def source_spectrum(wavelength, temperature):
    source_spectrum = (2*h*c**2) / ((wavelength * 1e-9)**5 * (np.exp(h * c / (wavelength *1e-9 * k * temperature)) -1))
    source_spectrum /= np.sum(source_spectrum)
    return source_spectrum

# Defining function for atmospheric absorption spectrum
def absorption_spectrum(wavelength):
    absorption_spectrum = 0.5 + 0.4 * np.sin((wavelength - 400) * np.pi / 200)
    return absorption_spectrum

# Defining function for observed spectrum = of source_spectrum X atmospheric_absorption
def observed_spectrum(wavelength, temperature):
     return source_spectrum(wavelength, temperature) * (1 - absorption_spectrum(wavelength))

# Function to calculate photon counts from intensity and normalise to 100% scale
def get_photon_counts(spectrum, wavelength):
    photon_counts = (spectrum * (wavelength * 1e-9)) / (h * c)
    photon_counts /= np.sum(photon_counts)
    photon_counts *= 100
    return photon_counts

# Defining variables
source_spec = source_spectrum(wavelength, temperature)
absorption_spec = absorption_spectrum(wavelength)
observed_spec = observed_spectrum(wavelength, temperature)
photon_counts = get_photon_counts(observed_spec, wavelength)

# Apply filter to remove red light (620 - 750 nm) so 685 nm +/- 65
filter_curve = wavelength_filter(observed_spec, wavelength, target_wavelength=685, bandwidth=65)
filtered_spectrum = observed_spec * filter_curve


# Calculating expectation wavelength from photon counts
expectation_wavelength = np.sum(wavelength * photon_counts) / np.sum(photon_counts)
print(f'Expectation wavelength (photon counts weighted): {expectation_wavelength:.2f} nm')

# Error bars
std_dev = np.sqrt(photon_counts + photon_counts**2)
std_error = std_dev / np.sqrt(1000) #assumes 1000 measurements (can be changed later)


# Create DataFrame
spectral_data = pd.DataFrame({
    'Wavelength (nm)': wavelength,
    'Source Spectrum': source_spec,
    'Atmospheric Absorption': absorption_spec,
    'Observed Spectrum': observed_spec,
    'Filtered Spectrum': filtered_spectrum,
    'Standard Error': std_error,})

# Plot data
fig, ax1 = plt.subplots(figsize=(10, 6))

# Plot source spectrum
ax1.plot(wavelength, source_spec * 100, linestyle='--', label='Source Spectrum', color='red')

# Plot observed spectrum with error bars
ax1.errorbar(wavelength, observed_spec * 100, yerr=std_error, fmt='o', markersize=2, label='Observed Spectrum (%) with Error', ecolor='black', capsize=3)

# Plot filtered spectrum
ax1.plot(wavelength, filtered_spectrum * 100, linewidth=2, linestyle="dotted", label='Filtered Spectrum')

ax1.set_xlabel('Wavelength (nm)')
ax1.set_ylabel('Intensity (%)')

ax1.set_ylim(0, np.max(source_spec) * 110) # this is set to 110 so source spectrum is visible
ax1.legend(loc='upper left')
ax1.grid()

# 2nd y Axis
ax2 = ax1.twinx()
ax2.plot(wavelength, absorption_spec * 100, linestyle='-.', label='Atmospheric Absorption', color='purple')
ax2.set_ylabel('Intensity (%)')
ax2.set_ylim(0, 110)
ax2.legend(loc='upper right')
ax2.grid()

plt.title('Spectral Data Visualisation')
plt.show()
