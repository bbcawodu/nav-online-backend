import sys
import json

from http_server_pkg.app import app

from get_parameter_validation_functions import GET_PARAMETER_VALIDATION_FUNCTIONS


def init_v1_response_data():
    """
    This function returns a skelleton dictionary that can be used for PIC JSON responses

    :return: (type: dictionary) dictionary that can be used in PIC JSON responses
    """
    return {'Status': {"Error Code": 0, "Warnings": [], "Version": 1.0, "Missing Parameters": []},
            'Data': {}}, []


def parse_and_log_errors(response_raw_data, errors_list):
    """
    This function takes a list of error messages, adds them to a PIC API response dictionary, and adds the
    correct error code

    :param response_raw_data: (type: dictionary) dictionary that can be used in PIC JSON responses
    :param errors_list: (type: list) list of error messages
    :return: (type: dictionary) dictionary that can be used in PIC JSON responses with errors logged
    """
    if errors_list:
        if response_raw_data["Status"]["Error Code"] == 0:
            response_raw_data["Status"]["Error Code"] = 1
        response_raw_data["Status"]["Errors"] = errors_list

        for message in errors_list:
            print(message)
            sys.stdout.flush()


def validate_get_request_parameters(params_to_validate, rqst_errors):
    validated_params = {}

    def run_validation_functions():
        for parameter_to_validate in params_to_validate:
            if parameter_to_validate in GET_PARAMETER_VALIDATION_FUNCTIONS:
                validation_fucntion = GET_PARAMETER_VALIDATION_FUNCTIONS[parameter_to_validate]
                validation_fucntion(validated_params, rqst_errors)
            else:
                raise NotImplementedError("GET parameter :{} does not have a validation function implemented.".format(parameter_to_validate))

    run_validation_functions()

    return validated_params


class JSONGETRspMixin(object):
    parse_GET_request_and_add_response = None
    accepted_GET_request_parameters = None

    def get(self):
        if self.parse_GET_request_and_add_response is None:
            raise NotImplementedError("Need to set class attribute, 'parse_GET_request_and_add_response'.")
        elif self.accepted_GET_request_parameters is None:
            raise NotImplementedError("Need to set class attribute, 'accepted_parameters'. If no parameters are needed, set class attribute to an empty list.")
        else:
            # Initialize dictionary for response data, initialize list for parsing errors
            response_raw_data, rqst_errors = init_v1_response_data()

            # Build dictionary that contains valid Patient Innovation Center GET parameters
            validated_GET_rqst_params = validate_get_request_parameters(self.accepted_GET_request_parameters, rqst_errors)

            if not rqst_errors:
                self.parse_GET_request_and_add_response(validated_GET_rqst_params, response_raw_data, rqst_errors)

            parse_and_log_errors(response_raw_data, rqst_errors)
            json_encoded_response_data = json.dumps(response_raw_data)

            response = app.response_class(
                response=json_encoded_response_data,
                status=200,
                mimetype='application/json'
            )
            return response
