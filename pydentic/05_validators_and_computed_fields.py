"""
05_validators_and_computed_fields.py
======================================
Three related features, in the order they build on each other:

1. @field_validator — custom validation/transformation logic for ONE
   field, beyond what Field(gt=, max_length=, etc.) can express.
   Runs after Pydantic's own type validation passes.

2. @model_validator(mode='after') — validation that depends on
   MULTIPLE fields at once (can't be expressed on a single field).
   Runs after all individual fields have already validated.

3. @computed_field — a derived value calculated FROM other fields,
   exposed as if it were a real field (shows up in .model_dump(),
   serialization, etc.) without being something you pass in yourself.

Note: @model_validator as a classmethod is deprecated in newer Pydantic
(2.12+) in favor of an instance method — this file uses the instance
method form, which is the current correct way to write it.
"""

from pydantic import (
    BaseModel, EmailStr, AnyUrl, Field,
    field_validator, model_validator, computed_field,
)
from typing import List, Dict, Optional, Annotated


# ---------------------------------------------------------------------
# 1. field_validator — custom logic for individual fields
# ---------------------------------------------------------------------

class PatientDataFieldValidator(BaseModel):
    name: str
    email: EmailStr
    age: int
    weight: float
    married: bool
    allergies: List[str]
    contact_details: Dict[str, str]

    @field_validator("email")
    @classmethod
    def email_validator(cls, value):
        """Only allow emails from an approved domain list — EmailStr
        checks FORMAT, this checks a business rule on top of that."""
        valid_domains = ["hdfc.com", "icici.com"]
        domain_name = value.split("@")[-1]
        if domain_name not in valid_domains:
            raise ValueError("Not a valid domain")
        return value

    @field_validator("name")
    @classmethod
    def transform_name(cls, value):
        """Validators can also TRANSFORM the value, not just check it —
        whatever this returns becomes the field's final stored value."""
        return value.upper()


# ---------------------------------------------------------------------
# 2. model_validator — logic that spans multiple fields together
# ---------------------------------------------------------------------

class PatientDataModelValidator(BaseModel):
    name: str
    email: EmailStr
    age: int
    weight: float
    married: bool
    allergies: List[str]
    contact_details: Dict[str, str]

    @model_validator(mode="after")
    def validate_emergency_contact(self):
        """age alone isn't invalid, and contact_details alone isn't
        invalid — the RULE is about the combination of the two, which
        is exactly what model_validator (not field_validator) is for."""
        if self.age > 60 and "emergency" not in self.contact_details:
            raise ValueError("Patients older than 60 must have an emergency contact")
        return self


# ---------------------------------------------------------------------
# 3. computed_field — a value derived from other fields
# ---------------------------------------------------------------------

class PatientDataComputed(BaseModel):
    name: str
    email: EmailStr
    age: int
    weight: float
    height: float
    married: bool
    allergies: List[str]
    contact_details: Dict[str, str]

    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight / (self.height ** 2), 2)


if __name__ == "__main__":
    print("=== field_validator: domain check + name uppercased ===")
    patient_data = {
        "name": "bappy",
        "email": "bappy@hdfc.com",
        "age": "25",
        "weight": 70.5,
        "married": "True",
        "allergies": ["peanuts", "shellfish"],
        "contact_details": {"phone": "123-456-7890"},
    }
    patient_1 = PatientDataFieldValidator(**patient_data)
    print(patient_1.name)   # BAPPY — transformed by the validator
    print(patient_1.email)

    # Try this to see the domain validator reject it:
    # PatientDataFieldValidator(**{**patient_data, "email": "bappy@gmail.com"})
    # ValidationError: Not a valid domain

    print("\n=== model_validator: emergency contact required over age 60 ===")
    patient_data_2 = {
        "name": "bappy",
        "email": "bappy@hdfc.com",
        "age": "70",
        "weight": 70.5,
        "married": "True",
        "allergies": ["peanuts", "shellfish"],
        "contact_details": {"phone": "123-456-7890", "emergency": "987-654-3210"},
    }
    patient_2 = PatientDataModelValidator(**patient_data_2)
    print(f"{patient_2.name}, age {patient_2.age} — validated OK")

    # Try this (same age, but no emergency contact) to see it fail:
    # PatientDataModelValidator(**{**patient_data_2, "contact_details": {"phone": "123"}})
    # ValidationError: Patients older than 60 must have an emergency contact

    print("\n=== computed_field: BMI derived from weight + height ===")
    patient_data_3 = {**patient_data_2, "height": 1.75}
    patient_3 = PatientDataComputed(**patient_data_3)
    print(f"BMI: {patient_3.bmi}")
