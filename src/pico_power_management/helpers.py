# -----------------------------------------
#                 NOTES 
# -----------------------------------------

# Dieter Steinhauser
# 10/2023
# Helper methods

# -----------------------------------------
#               IMPORTS
# -----------------------------------------


# -----------------------------------------
#                Class:
# -----------------------------------------

def check_type(value, name, expected_type):
    """
    Check if the value is of the expected data type.

    :param value: The value to check.
    :param name: The variable name.
    :param expected_type: The expected data type.
    :raises ValueError: If the value is not of the expected type.
    """
    if value is None:
        return None

    if not isinstance(value, expected_type):

        expected_type = [val.__name__ for val in expected_type] if isinstance(expected_type, (tuple, list)) else expected_type.__name__
        raise ValueError(f"Incorrect {name}: '{value}'. {name} is not of type {expected_type}")
    

def check_range(value, name, min_value, max_value):
    """
    Check if the value is within a specified range.

    :param value: The value to check.
    :param name: The variable name.
    :param min_value: The minimum allowed value.
    :param max_value: The maximum allowed value.
    :raises ValueError: If the value is outside the specified range.
    """
    if value is None:
        return None

    if not (min_value <= value <= max_value):
        raise ValueError(f"Incorrect {name}: '{value}'. {name} is not within the range [{min_value}, {max_value}]")
    

def check_str(value, name, expected_value):
    """
    Check if the value is one of the expected strings.

    :param value: The value to check.
    :param name: The variable name.
    :param min_value: expected string value or list of values
    :raises ValueError: If the value is outside the specified range.
    """
    if value is None:
        return None

    if isinstance(expected_value, str):
        if not value == expected_value:
            raise ValueError(f"Incorrect {name}: '{value}'. {name} is not the same as the expected string {expected_value}")
        
    if isinstance(expected_value, (list, tuple)):
        if value not in expected_value:
           raise ValueError(f"Incorrect {name}: '{value}'. {name} is not one of the expected strings {expected_value}") 
        


def check_list(value, name, expected_value):
    """
    Check if the value is one of the expected values of a list.

    :param value: The value to check.
    :param name: The variable name.
    :param min_value: expected list of values
    :raises ValueError: If the value is outside the specified range.
    """
    if value is None:
        return None

    if value not in expected_value:
        raise ValueError(f"Incorrect {name}: '{value}'. {name} is not one of the expected values {expected_value}") 




def read_modify(read_data, modify_data, bit_mask):
    """
    Helper method to write data without editing.

    The first parantheses clears fields that are being edited while others are untouched.
    The second parantheses restricts the modifying data to the bits we want edited.
    performing a bitwise OR then allows for the RMW cycle to be complete.

    :param read_data: current data from the device
    :type read_data: int
    :param modify_data: Data to be edited
    :type modify_data: int
    :param modify_data: field mask of the data being edited.
    :type modify_data: int
    :return: write_data
    :rtype: int
    """
    write_data = (read_data & ~bit_mask) | (modify_data & bit_mask) 
    return write_data
    
# def check_enum(value, name, key_enum):
#     """
#     Check if the value is a valid enum value.
# 
#     :param value: The value to check.
#     :param name: The variable name.
#     :param key_enum: A dictionary or enum containing valid values.
#     :raises ValueError: If the value is not a valid enum value.
#     """
#     key_names = [key.name for key in key_enum] 
# 
#     if value is None:
#         return None
# 
#     if not isinstance(value, (str, key_enum)):
#         raise ValueError(f"{name} '{value}' is not valid. Possible values are: {key_names}")
# 
#     if isinstance(value, str):
#         if value not in key_names:
#             raise ValueError(f"{name} '{value}' is not valid. Possible strings are: {key_names}")
#     
#         return key_enum[value]
#         
#     if not isinstance(value, key_enum):
#         raise ValueError(f"{name} '{value}' is not valid. Possible Enum objects are: {key_names}")
#     
#     return value
#     
