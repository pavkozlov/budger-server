from rest_framework import response, status


def check_field(required_fields, data):
    nested_fields = required_fields.split('/')
    received_data = data

    for field in nested_fields:

        if field in received_data:
            if len(nested_fields) > 1:
                received_data = received_data[field]
        else:
            message = 'Error: {} not found'.format(field)
            return False, message

    return True, None


def input_must_have(required_fields):
    def real_decorator(function):
        def wrapper(*args):
            # Получаем request.data
            data = args[1].data

            # Если пришла строка
            if isinstance(required_fields, str):
                check_result, message = check_field(required_fields, data)
                if not check_result:
                    return response.Response({'error': message}, status=status.HTTP_400_BAD_REQUEST)

            # Если пришёл список
            elif isinstance(required_fields, list):
                for field in required_fields:
                    check_result, message = check_field(field, data)
                    if not check_result:
                        return response.Response({'error': message}, status=status.HTTP_400_BAD_REQUEST)

            return function(*args)

        return wrapper

    return real_decorator
