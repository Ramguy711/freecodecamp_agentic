"""
06_nested_models_and_serialization.py
========================================
Two final pieces:

1. Nested models — a Pydantic model can be a field INSIDE another
   Pydantic model. This is how you represent real-world structure
   (a patient has an address; an address isn't just a flat string).

2. Serialization — turning a validated model back into a plain dict
   (.model_dump()) or a JSON string (.model_dump_json()). This is
   exactly the direction your MCP tools need to go: a Pydantic model
   validates the incoming tool arguments, and serialization is how
   you'd send a clean, validated result back out.
"""

from pydantic import BaseModel


class Address(BaseModel):
    city: str
    state: str
    pin: str


class PatientData(BaseModel):
    name: str
    gender: str
    age: int
    address: Address   # <- a full Pydantic model nested as a field


if __name__ == "__main__":
    print("=== Nested models ===")
    address_dict = {"city": "gurgaon", "state": "haryana", "pin": "122001"}
    address1 = Address(**address_dict)

    # You can pass an already-built model instance as the nested field:
    patient_dict = {"name": "Kishor", "gender": "male", "age": 40, "address": address1}
    patient1 = PatientData(**patient_dict)

    print(patient1)
    print(patient1.name)
    print(patient1.address)        # the nested Address model, printed whole
    print(patient1.address.city)   # dot-access straight through to the nested field

    print("\n=== Serialization ===")
    # .model_dump() -> a plain Python dict (nested models become nested dicts)
    as_dict = patient1.model_dump()
    print(as_dict)
    print(type(as_dict))

    # .model_dump_json() -> a JSON string, ready to send over a network,
    # write to a file, or return from an MCP tool.
    as_json = patient1.model_dump_json()
    print(as_json)
    print(type(as_json))
