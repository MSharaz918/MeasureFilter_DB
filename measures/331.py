"""
MIPS Measure 331: Adult Sinusitis: Antibiotic Prescribed
Denominator logic for filtering eligible patients
"""

import pandas as pd
import logging

def filter_patients(df):
    """
    Filter patients eligible for MIPS Measure 331 - Adult Sinusitis: Antibiotic Prescribed
    
    Denominator: Patients aged 18 years and older with a diagnosis of acute sinusitis
    
    Args:
        df (pandas.DataFrame): Patient data
        
    Returns:
        pandas.DataFrame: Filtered data with eligible patients
    """
    try:
        logging.info("Processing MIPS Measure 331 - Adult Sinusitis: Antibiotic Prescribed")
        
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
        
        # Filter for acute sinusitis diagnosis
        diagnosis_columns = [
            'diagnosis', 'Diagnosis', 'icd', 'ICD', 'icd_code', 'ICD_Code',
            'condition', 'Condition', 'primary_diagnosis', 'Primary_Diagnosis',
            'secondary_diagnosis', 'Secondary_Diagnosis'
        ]
        
        sinusitis_found = False
        
        for diag_col in diagnosis_columns:
            if diag_col in eligible_patients.columns:
                # ICD-10 codes for acute sinusitis
                sinusitis_codes = [
                    'J01', 'J01.0', 'J01.1', 'J01.2', 'J01.3', 'J01.4', 'J01.8', 'J01.9',
                    'J01.00', 'J01.01', 'J01.10', 'J01.11', 'J01.20', 'J01.21',
                    'J01.30', 'J01.31', 'J01.40', 'J01.41', 'J01.80', 'J01.81',
                    'J01.90', 'J01.91'
                ]
                
                # Also include text-based sinusitis diagnoses
                sinusitis_terms = [
                    'sinusitis', 'rhinosinusitis', 'acute sinusitis', 'acute rhinosinusitis',
                    'maxillary sinusitis', 'frontal sinusitis', 'ethmoid sinusitis', 'sphenoid sinusitis'
                ]
                
                # Create filters for ICD codes and text terms
                code_filter = eligible_patients[diag_col].astype(str).str.contains(
                    '|'.join(sinusitis_codes), na=False, case=False
                )
                
                text_filter = eligible_patients[diag_col].astype(str).str.lower().str.contains(
                    '|'.join(sinusitis_terms), na=False
                )
                
                # Combine filters
                sinusitis_filter = code_filter | text_filter
                
                if sinusitis_filter.any():
                    eligible_patients = eligible_patients[sinusitis_filter]
                    sinusitis_found = True
                    break
        
        # If no sinusitis diagnosis found, check for related symptoms or visit types
        if not sinusitis_found:
            # Check visit reasons or chief complaints
            reason_columns = [
                'chief_complaint', 'Chief_Complaint', 'visit_reason', 'Visit_Reason',
                'reason_for_visit', 'Reason_for_Visit', 'symptoms', 'Symptoms'
            ]
            
            for reason_col in reason_columns:
                if reason_col in eligible_patients.columns:
                    sinusitis_symptoms = [
                        'sinus', 'sinusitis', 'nasal congestion', 'facial pain',
                        'headache', 'post nasal drip', 'rhinorrhea'
                    ]
                    
                    symptom_filter = eligible_patients[reason_col].astype(str).str.lower().str.contains(
                        '|'.join(sinusitis_symptoms), na=False
                    )
                    
                    if symptom_filter.any():
                        eligible_patients = eligible_patients[symptom_filter]
                        sinusitis_found = True
                        break
        
        # If still no sinusitis patients found, return empty dataframe
        if not sinusitis_found:
            logging.info("Measure 331: No patients with sinusitis diagnosis found")
            return pd.DataFrame(columns=df.columns)
        
        # Additional filtering for appropriate encounter types
        visit_type_columns = ['visit_type', 'Visit_Type', 'encounter_type', 'Encounter_Type']
        visit_type_column = None
        
        for col in visit_type_columns:
            if col in eligible_patients.columns:
                visit_type_column = col
                break
        
        if visit_type_column is not None:
            # Relevant visit types for sinusitis treatment
            relevant_visits = [
                'office visit', 'office', 'outpatient', 'urgent care', 'emergency',
                'consultation', 'follow-up', 'followup'
            ]
            
            visit_filter = eligible_patients[visit_type_column].str.lower().str.contains(
                '|'.join(relevant_visits), na=False
            )
            
            if visit_filter.any():
                eligible_patients = eligible_patients[visit_filter]
        
        logging.info(f"Measure 331: Found {len(eligible_patients)} eligible patients out of {len(df)} total patients")
        
        return eligible_patients.reset_index(drop=True)
        
    except Exception as e:
        logging.error(f"Error in Measure 331 processing: {str(e)}")
        # Return empty dataframe with same columns if error occurs
        return pd.DataFrame(columns=df.columns)
