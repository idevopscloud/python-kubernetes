import unittest
import sys
import json
import time

sys.path.append('../')
import kubernetes

base_url = 'http://172.30.10.185:8080/api/v1'
kube_client = kubernetes.Api(base_url=base_url)

class ResourceQuotaTestCase(unittest.TestCase):
    def setUp(self):
        self.namespace = 'jeff-101-qa1-pro'
        self.quota_name = 'quota'
        self.json_data = {
          "kind": "ResourceQuota",
          "apiVersion": "v1",
          "metadata": {
            "name": self.quota_name,
            "namespace": self.namespace,
          },
          "spec": {
            "hard": {
              "memory": "20Gi"
            }
          }
        }

    def runTest(self):
        kube_client.DeleteResourceQuota(self.quota_name,
                                        namespace=self.namespace)
        kube_client.CreateResourceQuota(json.dumps(self.json_data), namespace=self.namespace)
        time.sleep(5)
        quota = kube_client.GetResourceQuota(self.quota_name, namespace=self.namespace)
        self.assertTrue(quota.hard is not None)
        self.assertTrue(quota.used is not None)

        kube_client.DeleteResourceQuota(self.quota_name, namespace=self.namespace)
        quota = kube_client.GetResourceQuota(self.quota_name, namespace=self.namespace)
        self.assertTrue(quota is None)

class EventTestCase(unittest.TestCase):
    def setUp(self):
        self.namespace = 'idevops-release'

    def runTest(self):
        try:
            events = kube_client.GetEvents('bad_namespace')
        except Exception as e:
            print e

        #events = kube_client.GetEvents(self.namespace, involved_obj_kind='Pod')
        events = kube_client.GetEvents(self.namespace, involved_obj_kind='Pod', involved_obj_name='core-575d6861763a6-cfu65')
        event = events[-1]
        #print event.InvolvedObject.Name, event.Reason, str(event.CreationTimeStamp), str(event.DeletionTimeStamp)
        #print event.DetailedReason

        events_json = kube_client.GetEventsJson(self.namespace)
        print events_json

class NodeTestCase(unittest.TestCase):
    def test_GetNodes(self):
        nodes = kube_client.GetNodes()
        for node in nodes:
            print node.name, node.mem_request_used

    def test_GetNodeJson(self):
        node_name = '172.30.10.185'
        node_json = kube_client.GetNodeJson(node_name)
        print node_json

if __name__ == '__main__':
    nodeTestSuite = unittest.TestSuite()
    nodeTestSuite.addTest(NodeTestCase('test_GetNodes'))
    nodeTestSuite.addTest(NodeTestCase('test_GetNodeJson'))

    unittest.TextTestRunner(verbosity=2).run(nodeTestSuite)

