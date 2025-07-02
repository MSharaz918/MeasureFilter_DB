"""
MIPS Measures Processing Module

This module contains individual measure processing scripts that apply 
denominator logic to filter eligible patients for each MIPS Quality Measure.
"""

__version__ = "1.0.0"
__author__ = "MIPS Measure Filter"

# Available measures
AVAILABLE_MEASURES = {
    '47': 'Advance Care Plan',
    '130': 'Documentation of Current Medications',
    '226': 'Preventive Care and Screening: Tobacco Use',
    '279': 'Depression Screening and Follow-Up Plan',
    '331': 'Adult Sinusitis: Antibiotic Prescribed',
    '317': 'Preventive Care and Screening: Screening for High Blood Pressure'
}

def get_measure_description(measure_number):
    """Get the description for a given measure number"""
    return AVAILABLE_MEASURES.get(str(measure_number), f"Measure {measure_number}")

def get_available_measures():
    """Get list of all available measures"""
    return AVAILABLE_MEASURES
