import os

import dpath.util

ARRAY_IDENTIFIER = "[]/"
MULTI_FIELDS_IDENTIFIER = ","
MAPPING_FROM_TO_SEPARATOR = "->"
RESULT_TYPE_SEPARATOR = ":"

ARRAY_RESULT_TYPE = "array"
STRING_RESULT_TYPE = "string"
SINGLE_STRING_RESULT_TYPE = "single_string"


def map_ticket_fields(ticket, mappings):
    result = {}
    for mapping in mappings:
        mapping_from, mapping_to, mapping_result_type = __parse_mapping(mapping)
        result[mapping_to] = __adjust_result(__map_field(ticket, mapping_from, []), mapping_result_type)
    return result


def __adjust_result(results, mapping_result_type):
    if STRING_RESULT_TYPE == mapping_result_type:
        return os.linesep.join(filter(lambda result: result is not None, results))

    if SINGLE_STRING_RESULT_TYPE == mapping_result_type:
        if len(results) != 1:
            raise TypeError("Not single result: " + str(results))
        return results[0]

    if ARRAY_RESULT_TYPE == mapping_result_type:
        return mapping_result_type

    raise TypeError("Not known type: " + mapping_result_type)


def __parse_mapping(mapping):
    mapping_from, mapping_to = mapping.split(MAPPING_FROM_TO_SEPARATOR)

    mapping_result_type = "array"
    if RESULT_TYPE_SEPARATOR in mapping_to:
        mapping_result_type, mapping_to = mapping_to.split(RESULT_TYPE_SEPARATOR)

    return mapping_from, mapping_to, mapping_result_type


def __map_field(data, key, results):
    if MULTI_FIELDS_IDENTIFIER in key:
        for field_key in key.split(MULTI_FIELDS_IDENTIFIER):
            __map_field(data, field_key, results)
        return results

    if ARRAY_IDENTIFIER in key:
        key_of_array, key_in_array = __split_array_key(key)
        for array_element in dpath.util.get(data, key_of_array):
            __map_field(array_element, key_in_array, results)
        return results

    __add_field_value_to_result(data, key, results)

    return results


def __add_field_value_to_result(data, key, results):
    field_value = dpath.util.get(data, key)
    if isinstance(field_value, list):
        for array_element_value in field_value:
            results.append(array_element_value)
    else:
        results.append(field_value)


def __split_array_key(key):
    key_parts = key.split(ARRAY_IDENTIFIER)
    return key_parts[0], ARRAY_IDENTIFIER.join(key_parts[1:])
