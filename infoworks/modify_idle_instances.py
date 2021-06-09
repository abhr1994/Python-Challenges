import argparse
import requests
import sys

class Databricks(object):

    def __init__(self, **kwargs):
        self.host = kwargs['host'] if 'host' in kwargs else None
        self.token = kwargs['token'] if 'token' in kwargs else None
        self.instance_pool_id = kwargs['instance_pool_id'] if 'instance_pool_id' in kwargs else None
        self.instance_pool_name = kwargs['instance_pool_name'] if 'instance_pool_name' in kwargs else None
        self.nodetype_id = kwargs['nodetype_id'] if 'nodetype_id' in kwargs else None
        self.min_idle_instances = kwargs['min_idle_instances'] if 'min_idle_instances' in kwargs else None
        self.max_cap = kwargs['max_cap'] if 'max_cap' in kwargs else None
        self.idle_time = kwargs['idle_time'] if 'idle_time' in kwargs else None

    def modify_idle_nodes(self):
        DOMAIN = self.host
        TOKEN = self.token
        instance_pool_id = self.instance_pool_id
        instance_pool_name = self.instance_pool_name
        nodetype_id = self.nodetype_id
        min_idle_instances = self.min_idle_instances
        max_cap = self.max_cap
        idle_time = self.idle_time
        if int(max_cap) == -1:
            response = requests.post(
                'https://%s/api/2.0/instance-pools/edit' % (DOMAIN),
                headers={'Authorization': 'Bearer %s' % TOKEN},
                json={
                    "instance_pool_id": instance_pool_id,
                    "instance_pool_name": instance_pool_name,
                    "node_type_id": nodetype_id,
                    "min_idle_instances": int(min_idle_instances),
                    "idle_instance_autotermination_minutes": int(idle_time)
                }
            )
        else:
            response = requests.post(
                'https://%s/api/2.0/instance-pools/edit' % (DOMAIN),
                headers={'Authorization': 'Bearer %s' % TOKEN},
                json={
                      "instance_pool_id": instance_pool_id,
                      "instance_pool_name": instance_pool_name,
                      "node_type_id": nodetype_id,
                      "min_idle_instances": int(min_idle_instances),
                      "max_capacity": int(max_cap),
                      "idle_instance_autotermination_minutes" : int(idle_time)
                }
            )
        if response.status_code == 200:
            print("The response from the API is: {}".format(response.json()))
        else:
            print("Error editing the cluster pool: %s: %s" % (response.json()["error_code"], response.json()["message"]))

class Input(object):
    def __init__(self):
        pass

    def get(self):
        parser = argparse.ArgumentParser(description='Launch cluster in the cluster pool')
        parser.add_argument('-s', '--host', dest='host', required=True, help="Databricks Server URL")
        parser.add_argument('-t', '--token', dest='token', required=True, help="Databricks User Token")
        parser.add_argument('-insid', '--instance_pool_id', dest='instance_pool_id', required=True,help="Pass the Instance Pool ID")
        parser.add_argument('-insname', '--instance_pool_name', dest='instance_pool_name', required=True,help="Pass the Instance Pool Name")
        parser.add_argument('-nodetype', '--nodetype_id', dest='nodetype_id', required=True,help="Pass the Nodetype here")
        parser.add_argument('-minidle', '--min_idle_instances', dest='min_idle_instances',default=0, required=False,help="Pass the number of minimum idle instances to maintain ")
        parser.add_argument('-maxcap', '--max_cap', dest='max_cap', default=100, required=False,help="Pass the number of max idle instances to maintain ")
        parser.add_argument('-idle', '--idle_time', dest='idle_time', default=2, required=False,help="The number of minutes that idle instances will be active ")
        parse_input = parser.parse_args()
        if not parse_input.host or not parse_input.token or not parse_input.instance_pool_id or not parse_input.instance_pool_name or not parse_input.nodetype_id:
            print("Databricks credentials or mandatory fields are not passed")
            parser.print_help()
            sys.exit(1)

        return parse_input

if __name__ == '__main__':
    input = Input()
    parse_input = input.get()
    dbObj=Databricks(host=parse_input.host,token=parse_input.token,instance_pool_id=parse_input.instance_pool_id,instance_pool_name=parse_input.instance_pool_name,nodetype_id=parse_input.nodetype_id,min_idle_instances=parse_input.min_idle_instances,max_cap=parse_input.max_cap,idle_time=parse_input.idle_time)
    dbObj.modify_idle_nodes()
    print("Modified Idle Nodes to {}".format(str(parse_input.min_idle_instances)))
