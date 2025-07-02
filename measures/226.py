"""
MIPS Measure 226: Preventive Care and Screening: Tobacco Use
Denominator logic for filtering eligible patients
"""

import pandas as pd
import logging

def filter_patients(df):
    """
    Filter patients eligible for MIPS Measure 226 - Preventive Care and Screening: Tobacco Use
    
    Denominator: Patients aged 18 years and older seen for preventive care
    
    Args:
        df (pandas.DataFrame): Patient data
        
    Returns:
        pandas.DataFrame: Filtered data with eligible patients
    """
    try:
        logging.info("Processing MIPS Measure 226 - Preventive Care and Screening: Tobacco Use")
        
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
        
        # Filter patients aged 18 and older
        eligible_patients = filtered_df[filtered_df[age_column] >= 18]
        
        # Filter for preventive care visits
        visit_type_columns = ['visit_type', 'Visit_Type', 'encounter_type', 'Encounter_Type']
        visit_type_column = None
        
        for col in visit_type_columns:
            if col in filtered_df.columns:
                visit_type_column = col
                break
        
        if visit_type_column is not None:
            # Filter for preventive care visit types
            preventive_visits = [
                'preventive', 'prevention', 'wellness', 'annual', 'physical',
                'check-up', 'checkup', 'screening', 'routine'
            ]
            
            # Create case-insensitive filter
            preventive_filter = eligible_patients[visit_type_column].str.lower().str.contains(
                '|'.join(preventive_visits), na=False
            )
            
            if preventive_filter.any():
                eligible_patients = eligible_patients[preventive_filter]
        
        # Also check for CPT codes related to preventive care (if available)
        cpt_columns = ['cpt', 'CPT', 'cpt_code', 'CPT_Code', 'procedure_code', 'Procedure_Code']
        cpt_column = None
        
        for col in cpt_columns:
            if col in filtered_df.columns:
                cpt_column = col
                break
        
        if cpt_column is not None:
            # Common preventive care CPT codes
            preventive_cpts = [
                '99381', '99382', '99383', '99384', '99385', '99386', '99387',  # New patient preventive
                '99391', '99392', '99393', '99394', '99395', '99396', '99397',  # Established patient preventive
                'G0438', 'G0439'  # Annual wellness visits
            ]
            
            cpt_filter = eligible_patients[cpt_column].astype(str).isin(preventive_cpts)
            
            if cpt_filter.any():
                # Combine with existing filter or use as primary filter
                if visit_type_column is not None:
                    eligible_patients = eligible_patients[
                        eligible_patients[visit_type_column].str.lower().str.contains(
                            '|'.join(preventive_visits), na=False
                        ) | cpt_filter
                    ]
                else:
                    eligible_patients = eligible_patients[cpt_filter]
        
        logging.info(f"Measure 226: Found {len(eligible_patients)} eligible patients out of {len(df)} total patients")
        
        return eligible_patients.reset_index(drop=True)
        
    except Exception as e:
        logging.error(f"Error in Measure 226 processing: {str(e)}")
        # Return empty dataframe with same columns if error occurs
        return pd.DataFrame(columns=df.columns)
