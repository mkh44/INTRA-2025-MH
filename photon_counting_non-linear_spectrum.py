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

# get photon number input from user
def get_photon_number():
    while True:
        user_input = input('Enter total number of photons (default: 1e6): ').strip()
        if user_input == '':
            photon_number = 1e6
            print(f'Using default photon count: {int(photon_number)} photons')
            return photon_number
        try:
            photon_number = float(user_input)
            print(f'Using default photon count: {int(photon_number)} photons')
            return photon_number
        except ValueError:
            print('Invalid input. Please enter a valid number or press enter for default (1e6 photons)')

# Define filter to remove light around target wavelength
def wavelength_filter(spectrum, wavelength, target_wavelength, bandwidth):
    filter_mask = np.where((wavelength > target_wavelength - bandwidth) & (wavelength < target_wavelength + bandwidth), 0, 1)
    filtered_spectrum = spectrum * filter_mask
    #filtered_spectrum /= np.sum(filtered_spectrum)
    return filtered_spectrum

# Define non-linear blackbody source spectrum function
def source_spectrum(wavelength, temperature):
    source_spectrum = (2*h*c**2) / ((wavelength * 1e-9)**5 * (np.exp(h * c / (wavelength *1e-9 * k * temperature)) -1))
    source_spectrum /= np.sum(source_spectrum)
    return source_spectrum

# Defining function for atmospheric absorption spectrum
#def absorption_spectrum(wavelength):
    #absorption_spectrum = 0.5 + 0.4 * np.sin((wavelength - 400) * np.pi / 200)
    #return absorption_spectrum

# Defining function for atmospheric absorption spectrum based on rayleigh scattering
def absorption_spectrum(wavelength):
    #normalising rayleigh scattering component
    rayleigh_scatter = (1 / wavelength**4)
    rayleigh_scatter /= np.max(rayleigh_scatter) #normalising to max value of 1

    #additional absorption effects like ozone absorption bands to be added here
    additional_absorption = 0.5 + 0.4 * np.sin((wavelength - 400) * np.pi / 200)

    absorption = 0.6 * rayleigh_scatter + 0.4 * additional_absorption
    return np.clip(absorption, 0, 1)

# Defining function for observed spectrum = of source_spectrum X atmospheric_absorption
def observed_spectrum(wavelength, temperature):
     return source_spectrum(wavelength, temperature) * (1 - absorption_spectrum(wavelength))

# Function to calculate photon counts from intensity and normalise to 100% scale
def get_photon_counts(spectrum, wavelength, total_photons=1e6):
    photon_counts = (spectrum * (wavelength * 1e-9)) / (h * c)
    photon_counts /= np.sum(photon_counts)
    photon_counts *= total_photons
    return photon_counts

# Defining variables
source_spec = source_spectrum(wavelength, temperature)
absorption_spec = absorption_spectrum(wavelength)
observed_spec = observed_spectrum(wavelength, temperature)
photon_counts = get_photon_counts(observed_spec, wavelength)

# Apply filter to remove red light (620 - 750 nm) so 685 nm +/- 65
filtered_spec = wavelength_filter(observed_spec, wavelength, target_wavelength=685, bandwidth=65)


# Calculating expectation wavelength from photon counts
expectation_wavelength = np.sum(wavelength * photon_counts) / np.sum(photon_counts)
print(f'Expectation wavelength (photon counts weighted): {expectation_wavelength:.2f} nm')

# Error bars
std_error = np.sqrt(photon_counts) #poisson std dev = root of mean or root of no of events
#std_error = std_dev / photon_counts


# Create DataFrame
spectral_data = pd.DataFrame({
    'Wavelength (nm)': wavelength,
    'Source Spectrum': source_spec,
    'Atmospheric Absorption': absorption_spec,
    'Observed Spectrum': observed_spec,
    'Filtered Spectrum': filtered_spec,
    'Standard Error': std_error,})

photon_number = get_photon_number()

#Photon counts scaling
source_counts = get_photon_counts(source_spec, wavelength)
observed_counts = get_photon_counts(observed_spec, wavelength)
filtered_counts = get_photon_counts(filtered_spec, wavelength)

# Plot data
fig, ax1 = plt.subplots(figsize=(10, 6))

# Plot source spectrum
ax1.plot(wavelength, source_counts, linestyle='--', label='Source Spectrum', color='blue')

# Plot observed spectrum
ax1.plot(wavelength, observed_counts, '-', markersize=2, color='#23a0de', label='Observed Spectrum')

# plot error bars with increased transparency
ax1.errorbar(wavelength, observed_counts, yerr=std_error, fmt='none', ecolor='#23a0de', capsize=3, alpha=0.2, label='Observed Spectrum Error')

# Plot filtered spectrum
ax1.plot(wavelength, filtered_counts, linewidth=2, linestyle="dotted", label='Filtered Spectrum', color='#3262a8')

ax1.set_xlabel('Wavelength (nm)')
ax1.set_ylabel('Photon Counts')


ax1.set_ylim(0, max(np.max(source_counts), np.max(observed_counts), np.max(filtered_counts)) * 1.2)
ax1.legend(loc='upper left')
ax1.grid(False)

#Axis colours
ax1.spines['left'].set_color('blue')
ax1.tick_params(axis='y', colors='blue')

# 2nd y Axis
ax2 = ax1.twinx()
ax2.plot(wavelength, absorption_spec * 100, linestyle='-.', label='Atmospheric Absorption', color='red')
ax2.set_ylabel('Intensity (%)')
ax2.set_ylim(0, 110)
ax2.legend(loc='upper right')
ax2.grid(False)

#Axis colour
ax2.spines['right'].set_color('red')
ax2.tick_params(axis='y', colors='#d13d32')
ax2.spines['left'].set_visible(False) # this gets rid of black overlay on left hand y-axis

plt.title('Spectral Data Visualisation')
plt.show()
