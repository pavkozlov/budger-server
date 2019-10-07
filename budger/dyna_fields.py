from rest_framework import generics, serializers


class DynaFieldsListView(generics.ListAPIView):
    """
    A ListAPIView that can parse fields query attr
    """
    def get_serializer_context(self):
        params = self.request.query_params
        if 'fields' in params:
            return {
                'fields': params['fields'].split(',')
            }


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs['context'].pop('fields', None) if 'context' in kwargs else None

        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)
