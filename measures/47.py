"""
MIPS Measure 47: Advance Care Plan
Denominator logic for filtering eligible patients
"""

import pandas as pd
import logging

def filter_patients(df):
    """
    Filter patients eligible for MIPS Measure 47 - Advance Care Plan
    
    Denominator: Patients aged 65 years and older
    
    Args:
        df (pandas.DataFrame): Patient data
        
    Returns:
        pandas.DataFrame: Filtered data with eligible patients
    """
    try:
        logging.info("Processing MIPS Measure 47 - Advance Care Plan")
        
        # Make a copy to avoid modifying original data
        filtered_df = df.copy()
        
        # Check if required columns exist
        age_columns = ['age', 'Age', 'AGE', 'patient_age', 'Patient_Age']
        age_column = None
        
        for col in age_columns:
            if col in filtered_df.columns:
                age_column = col
                break
        
        if age_column is None:
            # If no age column found, try to derive from date of birth
            dob_columns = ['dob', 'DOB', 'date_of_birth', 'Date_of_Birth', 'birth_date', 'Birth_Date']
            dob_column = None
            
            for col in dob_columns:
                if col in filtered_df.columns:
                    dob_column = col
                    break
            
            if dob_column is not None:
                # Calculate age from date of birth
                try:
                    filtered_df[dob_column] = pd.to_datetime(filtered_df[dob_column])
                    today = pd.Timestamp.now()
                    filtered_df['calculated_age'] = (today - filtered_df[dob_column]).dt.days / 365.25
                    age_column = 'calculated_age'
                except:
                    logging.warning("Could not calculate age from date of birth")
        
        if age_column is None:
            logging.warning("No age or date of birth column found. Returning all patients.")
            return filtered_df
        
        # Convert age to numeric, handling any non-numeric values
        filtered_df[age_column] = pd.to_numeric(filtered_df[age_column], errors='coerce')
        
        # Filter patients aged 65 and older
        eligible_patients = filtered_df[filtered_df[age_column] >= 65]
        
        logging.info(f"Measure 47: Found {len(eligible_patients)} eligible patients out of {len(df)} total patients")
        
        return eligible_patients.reset_index(drop=True)
        
    except Exception as e:
        logging.error(f"Error in Measure 47 processing: {str(e)}")
        # Return empty dataframe with same columns if error occurs
        return pd.DataFrame(columns=df.columns)
