from rest_framework import response, status


def input_must_have(required_fields):
    def real_decorator(function):
        def wrapper(*args):
            # Получаем request.data
            data = args[1].data

            # Если пришла строка
            if type(required_fields) is str:
                nested_fields = required_fields.split('/')
                for field in nested_fields:
                    if field in data:
                        if len(nested_fields) > 1:
                            data = data[field]
                    else:
                        return response.Response(
                            {'error': '{} not found.'.format(field)},
                            status=status.HTTP_400_BAD_REQUEST
                        )

            # Если пришёл список
            elif type(required_fields) is list:
                for field in required_fields:
                    nested_fields = field.split('/')
                    for f in nested_fields:
                        if f in data:
                            if len(nested_fields) > 1:
                                data = data[f]
                        else:
                            return response.Response(
                                {'error': '{} not found.'.format(f)},
                                status=status.HTTP_400_BAD_REQUEST
                            )

            # Вызвать обертываемую функцию и вернуть результат
            return function(*args)

        return wrapper

    return real_decorator
