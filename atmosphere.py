from math import e, pow, log


def displayAtmosphere(altitude):
    print(
        f"Temperature at {altitude} metres: {round(temperature(altitude), 2)} K")
    print(
        f"Pressure at {altitude} metres: {round(pressure(altitude), 2)} Pa")
    print(
        f"Density at {altitude} metres: {round(density(altitude), 4)} kg/m^3")


def altTemperature(lapseRate, finalAltitude, initialAltitude, initialTemperature):
    finalTemperature = lapseRate * \
        (finalAltitude - initialAltitude) + initialTemperature
    return finalTemperature


def altPressure(initialPressure, initialTemperature, finalTemperature, initialHeight, finalHeight, lapseRate, zone):
    if zone % 2 == 0:
        power = log(finalTemperature/initialTemperature)/lapseRate
    else:
        power = (finalHeight - initialHeight)/initialTemperature

    finalPressure = initialPressure * \
        pow(pow(e, -gravitationalAccelaration/gasConstant), power)
    return finalPressure


def altDensity(initialDensity, initialPressure, finalPressure, initialTemperature, finalTemperature):
    finalDensity = initialDensity * \
        (finalPressure/initialPressure)/(finalTemperature/initialTemperature)
    return finalDensity


# Significant Altitude is defined as the altitude at which a change in zone takes place.
significantAltitude = [0, 11000, 25000, 47000,
                       53000, 79000, 90000, 105000]             # (in m)

# Lapse Rate is defined as the rate of change in temperature with respect to altitude
lapseRates = [-0.0065, 0, 0.003, 0, -0.0045, 0,
              0.004]                                  # (in K/m)

# Physical Constants                                        Units
gravitationalAccelaration = 9.81                            # m/s^2
universalGasConstant = 8.314                                # J/mol.K
nitrogenMolarMass = 28.97                                   # grams/mol
gasConstant = (universalGasConstant*1e3)/nitrogenMolarMass  # J/kg.K

# Sea-level Conditions:

# Temperature at Significant Altitudes      (in N/m^2)
temperatureAtSea = 288.16

# Pressure at Significant Altitudes         (in N/m^2)
pressureAtSea = 101325

# Density at Significant Altitudes          (in kg/m^3)
densityAtSea = 1.225


def temperature(altitude):
    zone = 0
    for i in range(0, 7):
        if altitude > significantAltitude[i + 1]:
            zone = i + 1
        else:
            break

    zoneInitialTemperature = temperatureAtSea
    temperatureAtAltitude = 0

    for i in range(0, zone + 1):
        if altitude > significantAltitude[i + 1]:
            currentAltitude = significantAltitude[i + 1]
        else:
            currentAltitude = altitude

        temperatureAtAltitude = altTemperature(
            lapseRates[i], currentAltitude, significantAltitude[i], zoneInitialTemperature)

        zoneInitialTemperature = temperatureAtAltitude

    return temperatureAtAltitude


def pressure(altitude):
    zone = 0
    for i in range(0, 7):
        if altitude > significantAltitude[i + 1]:
            zone = i + 1
        else:
            break

    zoneInitialTemperature = temperatureAtSea
    temperatureAtAltitude = 0

    zoneInitialPressure = pressureAtSea
    pressureAtAltitude = 0

    for i in range(0, zone + 1):
        if altitude > significantAltitude[i + 1]:
            currentAltitude = significantAltitude[i + 1]
        else:
            currentAltitude = altitude

        temperatureAtAltitude = altTemperature(
            lapseRates[i], currentAltitude, significantAltitude[i], zoneInitialTemperature)

        pressureAtAltitude = altPressure(zoneInitialPressure, zoneInitialTemperature,
                                         temperatureAtAltitude, significantAltitude[i], currentAltitude, lapseRates[i], i)

        zoneInitialTemperature = temperatureAtAltitude
        zoneInitialPressure = pressureAtAltitude

    return pressureAtAltitude


def density(altitude):
    zone = 0
    for i in range(0, 7):
        if altitude > significantAltitude[i + 1]:
            zone = i + 1
        else:
            break

    zoneInitialTemperature = temperatureAtSea
    temperatureAtAltitude = 0

    zoneInitialPressure = pressureAtSea
    pressureAtAltitude = 0

    zoneInitialDensity = densityAtSea
    densityAtAltitude = 0

    for i in range(0, zone + 1):
        if altitude > significantAltitude[i + 1]:
            currentAltitude = significantAltitude[i + 1]
        else:
            currentAltitude = altitude

        temperatureAtAltitude = altTemperature(
            lapseRates[i], currentAltitude, significantAltitude[i], zoneInitialTemperature)

        pressureAtAltitude = altPressure(zoneInitialPressure, zoneInitialTemperature,
                                         temperatureAtAltitude, significantAltitude[i], currentAltitude, lapseRates[i], i)

        densityAtAltitude = altDensity(zoneInitialDensity, zoneInitialPressure,
                                       pressureAtAltitude, zoneInitialTemperature, temperatureAtAltitude)

        zoneInitialTemperature = temperatureAtAltitude
        zoneInitialPressure = pressureAtAltitude
        zoneInitialDensity = densityAtAltitude

    return densityAtAltitude


if __name__ == "__main__":
    altitude = float(input("Altitude (in metres): "))
    displayAtmosphere(altitude)
