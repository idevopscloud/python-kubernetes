#!/usr/bin/env python
#
# Copyright 2014 tigmi
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from utils import TimeUtils

class InvolvedObject:
    def __init__(self, json_data):
        # NOTICE: no data copy here
        self.json_data = json_data
        self.Kind = json_data.get('kind', None)
        self.Name = json_data.get('name', None)
        self.Namespace = json_data.get('namespace', None)
        self.Uid = json_data.get('uid', None)
        self.ApiVersion = json_data.get('apiVersion', None)
        self.ResourceVersion = json_data.get('resourceVersion', None)

class Event:
    def __init__(self, json_data):
        self.JsonData = json_data
        self.InvolvedObject = InvolvedObject(json_data.get('involvedObject'))
        self.Metadata = self.JsonData.get('metadata')
        self.Namespace = self.Metadata.get('namespace')
        self.CreationTimeStamp = TimeUtils.ConvertFromGoTime(self.Metadata.get('creationTimestamp'))
        self.DeletionTimeStamp = TimeUtils.ConvertFromGoTime(self.Metadata.get('deletionTimestamp'))
        self.Reason = self.JsonData.get('reason', None)
        self.Message = self.JsonData.get('message', None)
        self.Type = self.JsonData.get('type', None)
        self.Count = self.JsonData.get('count')
        self.DetailedReason = self.__get_detailed_reason()

    def __get_detailed_reason(self):
        detailed_reason = None
        if self.Reason != 'FailedScheduling':
            return detailed_reason

        lines = self.Message.split('\n')
        for line in lines:
            if 'failed to fit in any node' in line:
                continue
            if 'MatchNodeSelector' in line and detailed_reason is None:
                detailed_reason = 'MatchNodeSelector'
            if 'Node didn\'t have enough resource: Memory' in line:
                detailed_reason = 'LackOfMemory'

        return detailed_reason

