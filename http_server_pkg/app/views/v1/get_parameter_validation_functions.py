import datetime
import re
from urllib2 import unquote
import json
from sqlalchemy_blocking_orm_models.presence_db_models import INTENT_KEYWORDS
from sqlalchemy_blocking_orm_models.presence_db_models import INTENT_KEYWORD_FIELD_NAMES_W_TYPES

from flask import request


PARAMS_WITH_ALL_AS_ACCEPTED_VALUE = [
    'id',
    'session_id'
]


def validate_get_rqst_parameter_id(validated_params, rqst_errors):
    param_name = 'id'

    if request.args.get(param_name):
        validate_int_get_rqst_param(validated_params, param_name, rqst_errors)

        if request.args.get(param_name) != "all":
            validate_int_list_get_rqst_param(validated_params, param_name, rqst_errors)


def validate_get_rqst_parameter_session_id(validated_params, rqst_errors):
    param_name = 'session_id'

    if request.args.get(param_name):
        validate_int_get_rqst_param(validated_params, param_name, rqst_errors)

        if request.args.get(param_name) != "all":
            validate_int_list_get_rqst_param(validated_params, param_name, rqst_errors)


def validate_get_rqst_parameter_intent(validated_params, rqst_errors):
    param_name = 'intent'

    if request.args.get(param_name):
        validate_url_encoded_string_get_rqst_param(validated_params, param_name, rqst_errors)


def validate_get_rqst_parameter_first_name(validated_params, rqst_errors):
    param_name = 'first_name'

    if request.args.get(param_name):
        validate_string_get_rqst_param(validated_params, param_name, rqst_errors)

        validate_string_list_get_rqst_param(validated_params, param_name, rqst_errors)


def validate_get_rqst_parameter_last_name(validated_params, rqst_errors):
    param_name = 'last_name'

    if request.args.get(param_name):
        validate_string_get_rqst_param(validated_params, param_name, rqst_errors)

        validate_string_list_get_rqst_param(validated_params, param_name, rqst_errors)


def validate_get_rqst_parameter_email(validated_params, rqst_errors):
    param_name = 'email'

    if request.args.get(param_name):
        validate_string_get_rqst_param(validated_params, param_name, rqst_errors)

        validate_string_list_get_rqst_param(validated_params, param_name, rqst_errors)


def validate_get_rqst_parameter_time_delta_in_days(validated_params, rqst_errors):
    param_name = 'time_delta_in_days'

    if request.args.get(param_name):
        validate_time_delta_in_days_get_rqst_param(validated_params, param_name, rqst_errors)


def validate_get_rqst_parameter_min_date(validated_params, rqst_errors):
    param_name = 'min_date'

    if request.args.get(param_name):
        validate_yyyy_mm_dd_timestamp_get_rqst_param(validated_params, param_name, rqst_errors)


def validate_get_rqst_parameter_max_date(validated_params, rqst_errors):
    param_name = 'max_date'

    if request.args.get(param_name):
        validate_yyyy_mm_dd_timestamp_get_rqst_param(validated_params, param_name, rqst_errors)


def validate_get_rqst_parameter_full_name(validated_params, rqst_errors):
    param_name = 'full_name'

    if request.args.get(param_name):
        validate_url_encoded_string_get_rqst_param(validated_params, param_name, rqst_errors)


def validate_int_get_rqst_param(validated_params, param_name, rqst_errors):
    unvalidated_param_value = request.args.get(param_name)

    try:
        validated_param_value = int(unvalidated_param_value)
    except ValueError:
        if unvalidated_param_value == 'all' and param_name in PARAMS_WITH_ALL_AS_ACCEPTED_VALUE:
            validated_param_value = unvalidated_param_value
        else:
            rqst_errors.append('Invalid {}, {} must be a base 10 integer'.format(param_name, param_name))
            validated_param_value = None

    validated_params[param_name] = validated_param_value


def validate_int_list_get_rqst_param(validated_params, param_name, rqst_errors):
    unvalidated_param_value = request.args.get(param_name)

    validated_param_value_list = re.findall("\d+", unvalidated_param_value)
    for indx, element in enumerate(validated_param_value_list):
        validated_param_value_list[indx] = int(element)
    validated_params["{}_{}".format(param_name, "list")] = validated_param_value_list

    if not validated_param_value_list:
        rqst_errors.append('Invalid {}, {}s must be base 10 integers'.format(param_name, param_name))

    number_of_commas = len(re.findall(r",", unvalidated_param_value))
    number_of_parameters_there_should_be = number_of_commas + 1
    if number_of_parameters_there_should_be != len(validated_param_value_list):
        rqst_errors.append(
            'List of {}s is formatted wrong. Values must be base 10 integers separated by commas'.format(param_name))


def validate_float_get_rqst_param(validated_params, param_name, rqst_errors):
    unvalidated_param_value = request.args.get(param_name)

    try:
        validated_param_value = float(unvalidated_param_value)
    except ValueError:
        rqst_errors.append('Invalid {}, {}s must be a float'.format(param_name, param_name))
        validated_param_value = None
    except TypeError:
        rqst_errors.append('Invalid {}, {}s must be a float'.format(param_name, unvalidated_param_value))
        validated_param_value = None

    validated_params[param_name] = validated_param_value


def validate_string_get_rqst_param(validated_params, param_name, rqst_errors):
    unvalidated_param_value = request.args.get(param_name)

    validated_param_value = unvalidated_param_value

    validated_params[param_name] = validated_param_value


def validate_string_list_get_rqst_param(validated_params, param_name, rqst_errors):
    unvalidated_param_value = request.args.get(param_name)

    validated_param_value_list = re.findall(r"[@\w. '-]+", unvalidated_param_value)
    validated_params["{}_{}".format(param_name, "list")] = validated_param_value_list

    if not validated_param_value_list:
        rqst_errors.append('Invalid {}, {}s must be ascii encoded strings.'.format(param_name, param_name))

    number_of_commas = len(re.findall(r",", unvalidated_param_value))
    number_of_parameters_there_should_be = number_of_commas + 1
    if number_of_parameters_there_should_be != len(validated_param_value_list):
        rqst_errors.append('List of {}s is formatted wrong. Values must be ascii strings separated by commas'.format(param_name))


def validate_url_encoded_string_get_rqst_param(validated_params, param_name, rqst_errors):
    unvalidated_param_value = request.args.get(param_name)

    validated_param_value = unquote(unvalidated_param_value)

    validated_params[param_name] = validated_param_value


def validate_url_encoded_string_list_get_rqst_param(validated_params, param_name, rqst_errors):
    unvalidated_param_value = request.args.get(param_name)
    url_decoded_param_value = unquote(unvalidated_param_value)

    validated_param_value_list = re.findall(r"[@\w. '-]+", url_decoded_param_value)
    validated_params["{}_{}".format(param_name, "list")] = validated_param_value_list

    error_message = 'Comma separated list of {}s is formatted wrong. Values must be ascii strings that have all non-ascii characters url encoded.'.format(param_name)
    if not validated_param_value_list:
        rqst_errors.append(error_message)

    number_of_commas = len(re.findall(r",", unvalidated_param_value))
    number_of_parameters_there_should_be = number_of_commas + 1
    if number_of_parameters_there_should_be != len(validated_param_value_list):
        rqst_errors.append(error_message)


def validate_bool_get_rqst_param(validated_params, param_name, rqst_errors):
    accepted_unvalidated_values = (
        'true',
        'false'
    )

    unvalidated_values_that_equal_true = (
        'true'
    )

    unvalidated_param_value = request.args.get(param_name).lower()
    if unvalidated_param_value not in accepted_unvalidated_values:
        rqst_errors.append("Value for {} is not type boolean".format(param_name))

    validated_param_value = unvalidated_param_value in unvalidated_values_that_equal_true
    validated_params[param_name] = validated_param_value


def validate_yyyy_mm_dd_timestamp_get_rqst_param(validated_params, param_name, rqst_errors):
    unvalidated_param_value = request.args.get(param_name)

    try:
        validated_param_value = datetime.datetime.strptime(unvalidated_param_value, '%Y-%m-%d')
    except ValueError:
        rqst_errors.append('{} parameter value must be a valid date formatted like: YYYY-MM-DD.'.format(param_name))
        validated_param_value = None

    validated_params[param_name] = validated_param_value


def validate_time_delta_in_days_get_rqst_param(validated_params, param_name, rqst_errors):
    unvalidated_param_value = request.args.get(param_name)

    try:
        validated_param_value = int(unvalidated_param_value)
    except ValueError:
        rqst_errors.append('Invalid {} param value. Value must be a base 10 integer.'.format(param_name))
        validated_param_value = None
    else:
        validated_param_value = datetime.timedelta(days=validated_param_value)

    validated_params[param_name] = validated_param_value


class HTTPParamValidatorBase:
    param_name = None
    param_types = None
    accepted_param_types = [
        'int',
        'int_list'
        'str',
        'url_encoded_str'
    ]
    is_list_of_params = None

    @classmethod
    def check_that_instance_attributes_are_init(cls):
        if cls.param_name is None:
            raise NotImplementedError("cls.param_name must be set to a non null value in order to use this function.")
        if cls.param_types is None:
            raise NotImplementedError("cls.param_types must be set to a non null value in order to use this function.")
        elif not isinstance(cls.param_types, list):
            raise NotImplementedError("cls.param_types must be set to a list whose values are in: {} in order to use this function.".format(json.dumps(cls.accepted_param_types)))
        if cls.is_list_of_params is None:
            raise NotImplementedError(
                "cls.is_list_of_params must be set to a non null value in order to use this function.")

    @classmethod
    def validate_get_rqst_parameter(cls, validated_params, rqst_errors):
        cls.check_that_instance_attributes_are_init()

        for param_type in cls.param_types:
            if param_type == 'int':
                if request.args.get(cls.param_name):
                    validate_int_get_rqst_param(validated_params, cls.param_name, rqst_errors)

                    validated_param_value = validated_params[cls.param_name]
                    if cls.is_list_of_params and validated_param_value != "all":
                        validate_int_list_get_rqst_param(validated_params, cls.param_name, rqst_errors)
            elif param_type == 'int_list':
                if request.args.get(cls.param_name):
                    unvalidated_param_value = request.args.get(cls.param_name)
                    if unvalidated_param_value != "all":
                        validate_int_list_get_rqst_param(validated_params, cls.param_name, rqst_errors)
            elif param_type == 'str':
                if request.args.get(cls.param_name):
                    validate_string_get_rqst_param(validated_params, cls.param_name, rqst_errors)
            elif param_type == 'url_encoded_str':
                pass
            else:
                raise NotImplementedError("param_type: {} must be in this set of accepted values {}.".format(param_type, json.dumps(cls.accepted_param_types)))


def validate_get_rqst_parameter_keyword_clicks(intent_keyword):
    keyword_field_name = "{}_clicks".format(intent_keyword)

    def return_function(validated_params, rqst_errors):
        if request.args.get(keyword_field_name):
            validate_int_get_rqst_param(validated_params, keyword_field_name, rqst_errors)

    return return_function


def validate_get_rqst_parameter_keyword_hover_time(intent_keyword):
    keyword_field_name = "{}_hover_time".format(intent_keyword)

    def return_function(validated_params, rqst_errors):
        if request.args.get(keyword_field_name):
            validate_float_get_rqst_param(validated_params, keyword_field_name, rqst_errors)

    return return_function


def set_intent_keyword_http_get_param_validation_functions(validation_functions):
    for intent_keyword in INTENT_KEYWORDS:
        for field_name, field_type in INTENT_KEYWORD_FIELD_NAMES_W_TYPES.items():
            if field_name == 'clicks':
                validation_function_for_keyword = validate_get_rqst_parameter_keyword_clicks(intent_keyword)
            elif field_name == "hover_time":
                validation_function_for_keyword = validate_get_rqst_parameter_keyword_hover_time(intent_keyword)

            validation_functions["{}_{}".format(intent_keyword, field_name)] = validation_function_for_keyword


GET_PARAMETER_VALIDATION_FUNCTIONS = {
    "id": validate_get_rqst_parameter_id,
    'intent': validate_get_rqst_parameter_intent,
    "first_name": validate_get_rqst_parameter_first_name,
    "last_name": validate_get_rqst_parameter_last_name,
    "email": validate_get_rqst_parameter_email,
    "time_delta_in_days": validate_get_rqst_parameter_time_delta_in_days,
    "min_date": validate_get_rqst_parameter_min_date,
    "max_date": validate_get_rqst_parameter_max_date,
    'full_name': validate_get_rqst_parameter_full_name,
    'session_id': validate_get_rqst_parameter_session_id
}


set_intent_keyword_http_get_param_validation_functions(GET_PARAMETER_VALIDATION_FUNCTIONS)
