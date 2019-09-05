from rest_framework.response import Response
from rest_framework.views import status


def validate_request_data(fn):
    def decorated(*args, **kwargs):
        # args[0] == GenericView Object
        title = args[0].request.data.get('title', '')
        amount = args[0].request.data.get('amount', '')
        if not title or not amount:
            return Response(
                data={
                    'message': 'Both title and amount are required to add a record.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        return fn(*args, **kwargs)
    return decorated
