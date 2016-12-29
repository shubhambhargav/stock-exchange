import abc

from db.fields import Field


class StockMarket(object):

    __metaclass__ = abc.ABCMeta

    def __init__(self, *args, **kwargs):
        self.fields = {}
        self.input_fields = []
        self.output_fields = []

        for k, v in self.__class__.__dict__.items():
            if isinstance(v, Field):
                self.fields[k] = v
                if v.inp:
                    self.input_fields.append((k, v.inp))
                if v.out:
                    self.output_fields.append((k, v.out))

        self.transactions = []
        self.pending = []

    def _input_to_native(self, obj):
        native_object = {}
        expected = []
        for col in self.input_fields:
            to_key, from_key = col
            
            f = self.fields[to_key]
            v = obj.get(from_key, None)

            if v is None:
                if not f.required:
                    continue
                elif f.default is not None:
                    v = f.default
                else:
                    expected.append(from_key)
                    continue
            
            f.validate(v)

            native_object[to_key] = f.validated_value

        if len(expected) > 0:
            native_object = {}
            msg = "Expected '%s', but not found from source" % (','.join(expected))
            raise ValueError(msg)


        return native_object

    def _native_to_output(self, native_object):
        output_object = {}
        expected = []
        for col in self.output_fields:
            from_key, to_key = col
            
            f = self.fields[from_key]
            v = native_object.get(from_key, None)

            if v is None:
                if not f.required:
                    continue
                elif f.default is not None:
                    v = f.default
                else:
                    expected.append(from_key)
            
            f.validate(v)
            output_object[to_key] = f.validated_value

        if len(expected) > 0:
            msg = "Expected '%s', but not found for target" % (','.join(expected))
            raise ValueError(msg)

        return output_object

    def execute(self, order_entry):
        native_object = self._input_to_native(order_entry)

        transactions, native_object = self.process_data(native_object)

        if transactions:
            for t in transactions:
                validated_output = self._native_to_output(t)
                self.transactions.append(validated_output)
        if native_object:
            self.append_pending(native_object)

    @abc.abstractmethod
    def process_data(self, native_object):
        # Process data
        processed_object = native_object
        return processed_object, native_object

    @abc.abstractmethod
    def append_pending(self, native_object):
        return None


