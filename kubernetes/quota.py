import json
import copy

class ResourceQuota(object):
    def __init__(self, json_data):
        self.json_data = copy.deepcopy(json_data)
        self.name = json_data['metadata']['name']
        self.namespace = json_data['metadata']['namespace']
        self.hard = self.json_data['status'].get('hard', None)
        self.used = self.json_data['status'].get('used', None)

