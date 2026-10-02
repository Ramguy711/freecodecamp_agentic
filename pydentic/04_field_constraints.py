"""
04_field_constraints.py
=========================
Real constraints using Field() and special types — this is where
Pydantic moves past "right type" into "right type AND right shape".

- EmailStr validates real email format (requires: pip install pydantic[email])
- AnyUrl validates it's a well-formed URL
- Field(gt=0, lt=100) enforces a numeric RANGE, not just "it's an int"
- Field(max_length=...) caps string/list length
- Annotated[] is the more explicit, modern way to attach a Field's
  metadata (title, description, examples) to a type — functionally
  the same as "type = Field(...)" but keeps the type and its
  constraints visibly together, which matters once you have many
  constraints on one field.

Prerequisites: pip install pydantic "pydantic[email]"
"""

from pydantic import BaseModel, EmailStr, AnyUrl, Field
from typing import List, Dict, Optional, Annotated


# ---------------------------------------------------------------------
# Basic Field() constraints
# ---------------------------------------------------------------------

class PatientDataConstrained(BaseModel):
    name: str = Field(max_length=50)
    email: EmailStr
    linkedin_url: AnyUrl
    age: int = Field(gt=0, lt=100)                       # 0 < age < 100
    weight: float
    married: bool = False
    allergies: Optional[List[str]] = Field(max_length=5)  # at most 5 items
    contact_info: Dict[str, str]


# ---------------------------------------------------------------------
# Same idea, written with Annotated — the more explicit modern style.
# Field(strict=True) on weight means NO coercion: pass an int or a
# string here and it will reject it, not silently convert it.
# ---------------------------------------------------------------------

class PatientDataAnnotated(BaseModel):
    name: Annotated[
        str,
        Field(
            max_length=50,
            title="Name of the patient",
            description="Give the name of the patient in less than 50 chars",
            examples=["Bappy", "Alex"],
        ),
    ]
    email: EmailStr
    linkedin_url: AnyUrl
    age: int = Field(gt=0, lt=120)
    weight: Annotated[
        float,
        Field(gt=0, strict=True, description="Weight of the patient in kg"),
    ]
    married: Annotated[bool, Field(default=None, description="Is the patient married or not")]
    allergies: Annotated[Optional[List[str]], Field(default=None, max_length=5)]
    contact_details: Dict[str, str]


def add_patient_data(patient) -> None:
    print(patient.name)
    print(patient.age)
    print(patient.weight)
    print(patient.married)
    print(patient.allergies)
    print("Data added successfully to the database!")


if __name__ == "__main__":
    print("=== Field() constraints ===")
    patient_data = {
        "name": "Bappy",
        "email": "bappy@gmail.com",
        "linkedin_url": "https://www.linkedin.com/in/boktiarahmed73/",
        "age": "25",
        "weight": "70.5",
        "allergies": ["peanuts", "shellfish"],
        "contact_info": {"phone": "123-456-7890"},
    }
    patient_1 = PatientDataConstrained(**patient_data)
    add_patient_data(patient_1)

    print("\n=== Annotated + strict weight (must be a real float, not a string) ===")
    patient_data_2 = {
        "name": "Bappy",
        "email": "bappy@gmail.com",
        "linkedin_url": "https://www.linkedin.com/in/boktiarahmed73/",
        "age": "25",
        "weight": 70.5,          # must be an actual float here — strict=True
        "allergies": ["peanuts", "shellfish"],
        "contact_details": {"phone": "123-456-7890"},
    }
    patient_2 = PatientDataAnnotated(**patient_data_2)
    add_patient_data(patient_2)

    # Try this to see strict=True reject a coercible string:
    # PatientDataAnnotated(**{**patient_data_2, "weight": "70.5"})
    # ValidationError: Input should be a valid number [type=float_type, ...]

    # Try this to see the age range constraint fire:
    # PatientDataConstrained(**{**patient_data, "age": "150"})
    # ValidationError: Input should be less than 100
