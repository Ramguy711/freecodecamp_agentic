"""
03_complex_types_and_optional_fields.py
=========================================
Two things in one file, since they build on each other directly:

PART A - Complex types: List and Dict fields work exactly like the
simple fields in 02, just with richer type hints.

PART B - Required vs Optional: a field with "= default_value" becomes
optional. Optional[X] = None means "this can be X, or it can be
missing/None entirely" — different from just having a default.
"""

from pydantic import BaseModel
from typing import List, Dict, Optional


# ---------------------------------------------------------------------
# PART A: Complex types (List, Dict, bool)
# ---------------------------------------------------------------------

class PatientDataComplex(BaseModel):
    name: str
    age: int
    weight: float
    married: bool
    allergies: List[str]           # must be a list of strings
    contact_info: Dict[str, str]   # must be a dict of string -> string


def add_patient_data_complex(patient: PatientDataComplex):
    print(patient.name)
    print(patient.age)
    print(patient.weight)
    print("Data added successfully to the database!")


# ---------------------------------------------------------------------
# PART B: Required and Optional fields
# ---------------------------------------------------------------------

class PatientDataOptional(BaseModel):
    name: str
    age: int
    weight: float
    married: bool = False                      # optional, defaults to False
    allergies: Optional[List[str]] = None       # optional, defaults to None
    contact_info: Dict[str, str]                # still required — no default


def add_patient_data_optional(patient: PatientDataOptional):
    print(patient.name)
    print(patient.age)
    print(patient.weight)
    print(patient.married)
    print(patient.allergies)
    print("Data added successfully to the database!")


if __name__ == "__main__":
    print("=== Part A: complex types ===")
    patient_data = {
        "name": "Bappy",
        "age": "25",
        "weight": "70.5",
        "married": "True",
        "allergies": ["peanuts", "shellfish"],
        "contact_info": {"email": "bappy@example.com", "phone": "123-456-7890"},
    }
    patient_1 = PatientDataComplex(**patient_data)
    add_patient_data_complex(patient_1)

    print("\n=== Part B: optional fields (married and allergies omitted) ===")
    patient_data_2 = {
        "name": "Bappy",
        "age": "25",
        "weight": "70.5",
        "contact_info": {"email": "bappy@example.com", "phone": "123-456-7890"},
    }
    patient_2 = PatientDataOptional(**patient_data_2)
    add_patient_data_optional(patient_2)
    # married printed False, allergies printed None — both filled by
    # their defaults since the input dict never mentioned them.
