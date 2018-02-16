import json


class NamedObject(object):
    def __init__(self):
        self.classname = self.__class__.__name__

    def to_dict(self):

        def obj_dict(obj):
            return obj.__dict__

        return json.loads(json.dumps(self, default=obj_dict))#, indent=4, sort_keys=False))
