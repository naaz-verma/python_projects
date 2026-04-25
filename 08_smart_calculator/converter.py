"""
Unit converter for Smart Calculator.
Teaches: Dictionaries, conditionals, mathematical formulas, function design.
"""

from constants import LENGTH_UNITS, WEIGHT_UNITS


def convert_length(value, from_unit, to_unit):
    """
    Convert between length units using a base-unit approach.
    All units are first converted to meters (base), then to the target unit.
    """
    # Convert to base unit (meters)
    value_in_meters = value * LENGTH_UNITS[from_unit]
    # Convert from base unit to target
    result = value_in_meters / LENGTH_UNITS[to_unit]
    return round(result, 6)


def convert_weight(value, from_unit, to_unit):
    """
    Convert between weight units using a base-unit approach.
    All units are first converted to grams (base), then to the target unit.
    """
    # Convert to base unit (grams)
    value_in_grams = value * WEIGHT_UNITS[from_unit]
    # Convert from base unit to target
    result = value_in_grams / WEIGHT_UNITS[to_unit]
    return round(result, 6)


def convert_temperature(value, from_unit, to_unit):
    """
    Convert between temperature units.
    Uses direct formulas since temperature conversion is not linear.
    Teaches: if/elif chains, mathematical formulas.
    """
    if from_unit == to_unit:
        return value

    # First convert everything to Celsius
    if from_unit == "Fahrenheit":
        celsius = (value - 32) * 5 / 9
    elif from_unit == "Kelvin":
        celsius = value - 273.15
    else:
        celsius = value

    # Then convert Celsius to target
    if to_unit == "Fahrenheit":
        return round((celsius * 9 / 5) + 32, 2)
    elif to_unit == "Kelvin":
        return round(celsius + 273.15, 2)
    else:
        return round(celsius, 2)
