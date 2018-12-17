import datetime
import os
import uuid

class Utilities(object):

    def new_uuid(self):
        id = uuid.uuid4()
        return str(id)