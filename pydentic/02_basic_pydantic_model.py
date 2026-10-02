"""
02_basic_pydantic_model.py
============================
The Pydantic fix for 01_problem_without_pydantic.py.

Instead of manually checking types inside every function, define ONE
model describing the shape the data must have. Pydantic validates and
coerces automatically when you build the model — "25" (a string) gets
converted to 25 (an int) because int is lax/coercing by default.

Prerequisites: pip install pydantic
"""

from pydantic import BaseModel


class PatientData(BaseModel):
    name: str
    age: int
    weight: float


def add_patient_data(patient: PatientData):
    print(patient.name)
    print(patient.age)
    print(patient.weight)
    print("Data added successfully to the database!")


def update_patient_data(patient: PatientData):
    print(patient.name)
    print(patient.age)
    print(patient.weight)
    print("Data updated successfully in the database!")


if __name__ == "__main__":
    # Raw input — note age and weight arrive as STRINGS here, like they
    # would from a web form, a JSON API, or an LLM tool call.
    patient_data = {"name": "Bappy", "age": "25", "weight": "70.5"}

    # **patient_data unpacks the dict into keyword arguments.
    # Pydantic validates + coerces "25" -> 25, "70.5" -> 70.5 here.
    patient_1 = PatientData(**patient_data)
    add_patient_data(patient_1)

    patient_data_2 = {"name": "Alex", "age": "25", "weight": "70.5"}
    patient_2 = PatientData(**patient_data_2)
    update_patient_data(patient_2)

    # Try this to see a real validation error:
    # PatientData(name="Bad", age="not a number", weight="70.5")
