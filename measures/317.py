"""
MIPS Measure 317: Preventive Care and Screening: Screening for High Blood Pressure
Denominator logic for filtering eligible patients
"""

import pandas as pd
import logging

def filter_patients(df):
    """
    Filter patients eligible for MIPS Measure 317 - Preventive Care and Screening: Screening for High Blood Pressure
    
    Denominator: Patients aged 18 years and older
    
    Args:
        df (pandas.DataFrame): Patient data
        
    Returns:
        pandas.DataFrame: Filtered data with eligible patients
    """
    try:
        logging.info("Processing MIPS Measure 317 - Preventive Care and Screening: Screening for High Blood Pressure")
        
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
        
        # Filter for appropriate encounter types for blood pressure screening
        visit_type_columns = ['visit_type', 'Visit_Type', 'encounter_type', 'Encounter_Type']
        visit_type_column = None
        
        for col in visit_type_columns:
            if col in filtered_df.columns:
                visit_type_column = col
                break
        
        if visit_type_column is not None:
            # Relevant visit types for blood pressure screening
            relevant_visits = [
                'office visit', 'office', 'outpatient', 'consultation', 'follow-up', 'followup',
                'preventive', 'wellness', 'annual', 'physical', 'check-up', 'checkup',
                'routine', 'screening', 'urgent care'
            ]
            
            # Create case-insensitive filter
            visit_filter = eligible_patients[visit_type_column].str.lower().str.contains(
                '|'.join(relevant_visits), na=False
            )
            
            if visit_filter.any():
                eligible_patients = eligible_patients[visit_filter]
        
        # Exclude patients with end-stage renal disease or on dialysis
        diagnosis_columns = [
            'diagnosis', 'Diagnosis', 'icd', 'ICD', 'icd_code', 'ICD_Code',
            'condition', 'Condition', 'primary_diagnosis', 'Primary_Diagnosis',
            'secondary_diagnosis', 'Secondary_Diagnosis'
        ]
        
        for diag_col in diagnosis_columns:
            if diag_col in eligible_patients.columns:
                # Exclude ESRD and dialysis patients
                exclusion_conditions = [
                    'N18.6',  # End stage renal disease
                    'Z99.2',  # Dependence on renal dialysis
                    'dialysis', 'ESRD', 'end stage renal'
                ]
                
                exclusion_filter = eligible_patients[diag_col].astype(str).str.contains(
                    '|'.join(exclusion_conditions), na=False, case=False
                )
                
                # Remove patients with exclusion conditions
                eligible_patients = eligible_patients[~exclusion_filter]
                break
        
        # Also check for CPT codes related to outpatient visits (if available)
        cpt_columns = ['cpt', 'CPT', 'cpt_code', 'CPT_Code', 'procedure_code', 'Procedure_Code']
        cpt_column = None
        
        for col in cpt_columns:
            if col in filtered_df.columns:
                cpt_column = col
                break
        
        if cpt_column is not None:
            # Common outpatient visit CPT codes
            outpatient_cpts = [
                '99201', '99202', '99203', '99204', '99205',  # New patient office visits
                '99211', '99212', '99213', '99214', '99215',  # Established patient office visits
                '99381', '99382', '99383', '99384', '99385', '99386', '99387',  # New patient preventive
                '99391', '99392', '99393', '99394', '99395', '99396', '99397',  # Established patient preventive
                'G0438', 'G0439'  # Annual wellness visits
            ]
            
            cpt_filter = eligible_patients[cpt_column].astype(str).isin(outpatient_cpts)
            
            if cpt_filter.any():
                # If we have CPT codes, use them to further refine the selection
                if visit_type_column is not None:
                    # Combine visit type and CPT filters
                    combined_filter = (
                        eligible_patients[visit_type_column].str.lower().str.contains(
                            '|'.join(relevant_visits), na=False
                        ) | cpt_filter
                    )
                    eligible_patients = eligible_patients[combined_filter]
                else:
                    eligible_patients = eligible_patients[cpt_filter]
        
        logging.info(f"Measure 317: Found {len(eligible_patients)} eligible patients out of {len(df)} total patients")
        
        return eligible_patients.reset_index(drop=True)
        
    except Exception as e:
        logging.error(f"Error in Measure 317 processing: {str(e)}")
        # Return empty dataframe with same columns if error occurs
        return pd.DataFrame(columns=df.columns)
