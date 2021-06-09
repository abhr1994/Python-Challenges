import argparse
import requests
import sys

class Databricks(object):

    def __init__(self, **kwargs):
        self.host = kwargs['host'] if 'host' in kwargs else None
        self.token = kwargs['token'] if 'token' in kwargs else None
        self.cluster_id = kwargs['cluster_id'] if 'cluster_id' in kwargs else None

    def start_cluster(self):
        DOMAIN = self.host
        TOKEN = self.token
        cluster_id = self.cluster_id

        response = requests.post(
            'https://%s/2.0/clusters/start' % (DOMAIN),
            headers={'Authorization': 'Bearer %s' % TOKEN},
            json={
                "cluster_id": cluster_id,
            }
        )
        if response.status_code == 200:
            print("Started the cluster")
        else:
            print("Error starting cluster: %s: %s" % (response.json()["error_code"], response.json()["message"]))

class Input(object):
    def __init__(self):
        pass

    def get(self):
        parser = argparse.ArgumentParser(description='Launch cluster in the cluster pool')
        parser.add_argument('-s', '--host', dest='host', required=True, help="Databricks Server URL")
        parser.add_argument('-t', '--token', dest='token', required=True, help="Databricks User Token")
        parser.add_argument('-c', '--cluster_id', dest='cluster_id', required=True, help="Pass the cluster ID to start")

        parse_input = parser.parse_args()
        if not parse_input.host or not parse_input.token or not parse_input.cluster_id:
            print("Databricks credentials not provided")
            parser.print_help()
            sys.exit(1)

        return parse_input

if __name__ == '__main__':
    input = Input()
    parse_input = input.get()
    dbObj=Databricks(host=parse_input.host,token=parse_input.token,cluster_id=parse_input.cluster_id)
    dbObj.start_cluster()