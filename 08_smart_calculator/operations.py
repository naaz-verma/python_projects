"""
Math operations for Smart Calculator.
Teaches: Functions, parameters, return values, conditionals, error handling.
"""

import math


# --- Basic Math ---

def add(a, b):
    """Add two numbers."""
    return a + b


def subtract(a, b):
    """Subtract b from a."""
    return a - b


def multiply(a, b):
    """Multiply two numbers."""
    return a * b


def divide(a, b):
    """Divide a by b. Returns error message if b is zero."""
    if b == 0:
        return "Error: Cannot divide by zero!"
    return a / b


def calculate(a, b, operator):
    """
    Perform a basic math operation based on the operator symbol.
    Teaches: Dictionary as a dispatch map, function references.
    """
    operations = {
        "+": add,
        "-": subtract,
        "*": multiply,
        "/": divide,
    }
    func = operations.get(operator)
    if func:
        return func(a, b)
    return "Error: Invalid operator"


# --- Power & Root ---

def power(base, exponent):
    """Calculate base raised to the exponent."""
    return base ** exponent


def square_root(number):
    """Calculate square root. Returns error for negative numbers."""
    if number < 0:
        return "Error: Cannot find square root of a negative number!"
    return math.sqrt(number)


# --- Percentage ---

def percentage(value, total):
    """Calculate what percentage 'value' is of 'total'."""
    if total == 0:
        return "Error: Total cannot be zero!"
    return (value / total) * 100


def percentage_of(percent, total):
    """Calculate a given percentage of a total."""
    return (percent / 100) * total


def percentage_change(old_value, new_value):
    """Calculate percentage increase or decrease."""
    if old_value == 0:
        return "Error: Old value cannot be zero!"
    change = ((new_value - old_value) / abs(old_value)) * 100
    return change


# --- Average ---

def average(numbers):
    """Calculate the average of a list of numbers."""
    if len(numbers) == 0:
        return "Error: No numbers provided!"
    return sum(numbers) / len(numbers)
