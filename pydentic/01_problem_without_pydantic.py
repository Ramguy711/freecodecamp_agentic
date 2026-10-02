"""
01_problem_without_pydantic.py
================================
What validation looks like WITHOUT Pydantic — manual type checks,
scattered across every function that needs them.

Run this and notice: it works, but every function that touches
patient data has to repeat the same isinstance/range checks. Miss
one check in one function, and bad data slips through silently.
This is the problem Pydantic solves (see 02_basic_pydantic_model.py).
"""


def add_patient_data(name: str, age: int):
    if type(name) == str and type(age) == int:
        if age >= 0:
            print(name)
            print(age)
            print("Data added successfully to the database!")
        else:
            raise ValueError("Age cannot be negative.")
    else:
        raise TypeError(
            "Invalid data type for name or age. "
            "Name should be a string and age should be an integer."
        )


def update_patient_data(name: str, age: int):
    if type(name) == str and type(age) == int:
        if age >= 0:
            print(name)
            print(age)
            print("Data updated successfully in the database!")
        else:
            raise ValueError("Age cannot be negative.")
    else:
        raise TypeError(
            "Invalid data type for name or age. "
            "Name should be a string and age should be an integer."
        )


if __name__ == "__main__":
    add_patient_data("Bappy", 25)

    # Try uncommenting these to see the manual checks fail loudly:
    # add_patient_data("Bappy", -5)        # ValueError: Age cannot be negative.
    # add_patient_data(123, 25)            # TypeError: Invalid data type...
