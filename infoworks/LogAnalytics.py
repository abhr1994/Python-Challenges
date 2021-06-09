import requests, traceback, datetime, argparse, json, logging
from collections import OrderedDict
from datetime import timezone
import pandas as pd
from infoworks.LogAnalyticsDataCollector import post_data
from freshdesk import *
from statistics import mean
parser = argparse.ArgumentParser('Log Analytics')
parser.add_argument('--time_range', required=False,default=1, help='Pass the time in minutes')
args = vars(parser.parse_args())


class CustomError(Exception):
    def __init__(self, message):
        self.message = message
        super(CustomError, self).__init__(self.message)


def get_bearer_token():
    # YWRtaW5AaW5mb3dvcmtzLmlvOjEyMzQ1Ng==
    url = '{protocol}://{ip}:{port}/v2/user/auth_token'.format(ip='10.16.11.2', port=2999, protocol='http')
    headers = {
        'Authorization': 'Basic <>',
        'Content-Type': 'application/json'
    }
    response = requests.request("GET", url, headers=headers)
    bearer_token = response.json().get("result", None)
    headers_bearer = {
        'Authorization': 'Bearer ' + bearer_token,
        'Content-Type': 'application/json'
    }
    return headers_bearer


headers = get_bearer_token()


def get_source_name(config, source_id):
    try:
        url = '{protocol}://{ip}:{port}/v3/sources/{source_id}'.format(
            ip=config['ip'],
            port=config['port'],
            protocol=config['protocol'],
            source_id=source_id
        )
        print(url)
        response = requests.request("GET", url, headers=headers)
        if response is not None:
            response = response.json().get("result", None)
            if response:
                src_name = response.get("name")
            else:
                src_name = "None"
            return src_name
    except:
        raise CustomError("Unable to get source name")


def get_tablegroup_id(config, job_id, source_id):
    try:
        url = '{protocol}://{ip}:{port}/v3/sources/{source_id}/jobs/{job_id}'.format(
            ip=config['ip'],
            port=config['port'],
            protocol=config['protocol'],
            job_id=job_id,
            source_id=source_id
        )
        print(url)
        response = requests.request("GET", url, headers=headers)
        if response is not None:
            response = response.json().get("result", None)
            table_group_id = response.get("sub_entity_id")
            processedAt = response.get("processed_at")
            job_end_time = response.get("last_updated")
            status = response.get("status")
            return table_group_id, processedAt, job_end_time, status
    except:
        raise CustomError("Unable to get table group details from the Job Id")


def get_table_group_name(config, table_group_id, source_id):
    try:
        url = '{protocol}://{ip}:{port}/v3/sources/{source_id}/table-groups/{table_group_id}'.format(
            ip=config['ip'],
            port=config['port'],
            protocol=config['protocol'],
            table_group_id=table_group_id,
            source_id=source_id
        )
        print(url)
        response = requests.request("GET", url, headers=headers)

        if response is not None:
            response = response.json().get("result", None)
            return response.get('name'), response.get('tables')
    except:
        raise CustomError("Unable to get table group info")


def get_ingestion_metrics_url(config, job_id, source_id):
    try:
        combinedJobMetric = []
        url = '{protocol}://{ip}:{port}/v3/sources/{source_id}/jobs/{job_id}/reports/job-metrics'.format(
            ip=config['ip'],
            port=config['port'],
            protocol=config['protocol'],
            job_id=job_id,
            source_id=source_id
        )
        print(url)
        response = requests.request("GET", url, headers=headers)
        if response is not None:
            result = response.json().get("result", [])
            while (len(result) > 0):
                combinedJobMetric.extend(result)
                nextUrl = '{protocol}://{ip}:{port}{next}'.format(next=response.json().get('links')['next'],
                                                                  ip=config['ip'],
                                                                  port=config['port'],
                                                                  protocol=config['protocol'],
                                                                  )
                response = callurl(nextUrl)
                result = response.json().get("result", [])
            return combinedJobMetric
    except Exception as e:
        print(e)
        raise CustomError("Unable to get ingestion job metrics info")


def get_running_jobs(config):
    try:
        combinedJobs = []
        filter_condition = "{ \"$and\": [{ \"jobType\": { \"$in\": [\"source_crawl\",\"source_cdc_merge\",\"source_semistructured_crawl\",\"pipeline_build\"]}},{\"status\":{\"$in\":[\"running\"]}} ] }"
        url = '{protocol}://{ip}:{port}/v3/admin/jobs?filter={filter_condition}&limit=20&offset=0'.format(
            ip=config['ip'],
            port=config['port'],
            protocol=config['protocol'],
            filter_condition=filter_condition
        )
        print(url)
        response = requests.request("GET", url, headers=headers)
        if response is not None:
            result = response.json().get("result", [])
            while (len(result) > 0):
                combinedJobs.extend(result)
                next_url = response.json().get('links')['next']
                nextUrl = '{protocol}://{ip}:{port}{next}'.format(next=next_url,
                                                                  ip=config['ip'],
                                                                  port=config['port'],
                                                                  protocol=config['protocol'],
                                                                  )
                response = callurl(nextUrl)
                result = response.json().get("result", [])
            return combinedJobs
    except Exception as e:
        print(e)
        raise CustomError("Unable to get running jobs")


def get_history_jobs(config,date_string,entity_id,sub_entity_id,job_type):
    try:
        combinedJobs = []
        if job_type=="pipeline":
            filter_condition = "{ \"$and\": [{\"last_upd\": {\"$gte\": {\"$date\": \""+ date_string + "\"}}},{\"entityId\":\""+entity_id+"\"},{\"status\":{\"$in\":[\"success\",\"completed\",\"succeded\"]}} ] }"
        else:
            filter_condition = "{ \"$and\": [{\"last_upd\": {\"$gte\": {\"$date\": \""+ date_string + "\"}}},{\"entityId\":\""+entity_id+"\"},{\"subEntityId\":\""+sub_entity_id+"\"},{\"status\":{\"$in\":[\"success\",\"completed\",\"succeded\"]}} ] }"
        url = '{protocol}://{ip}:{port}/v3/admin/jobs?filter={filter_condition}&limit=20&offset=0'.format(
            ip=config['ip'],
            port=config['port'],
            protocol=config['protocol'],
            filter_condition = filter_condition
        )
        print(url)
        response = requests.request("GET", url, headers=headers)
        if response is not None:
            result = response.json().get("result", [])
            while (len(result) > 0):
                combinedJobs.extend(result)
                next_url = response.json().get('links')['next']
                nextUrl = '{protocol}://{ip}:{port}{next}'.format(next=next_url,
                                                                  ip=config['ip'],
                                                                  port=config['port'],
                                                                  protocol=config['protocol'],
                                                                  )
                response = callurl(nextUrl)
                result = response.json().get("result", [])
            return combinedJobs
    except Exception as e:
        print(e)
        raise CustomError("Unable to get history jobs")

def get_job_url(config,date_string):
    try:
        combinedJobs = []
        filter_condition = "{ \"$and\": [{\"last_upd\": {\"$gte\": {\"$date\": \""+ date_string + "\"}}}, { \"jobType\": { \"$in\": [\"source_crawl\",\"source_cdc_merge\",\"source_semistructured_crawl\",\"pipeline_build\"]}},{\"status\":{\"$in\":[\"failed\",\"completed\",\"canceled\"]}} ] }"
        url = '{protocol}://{ip}:{port}/v3/admin/jobs?filter={filter_condition}&limit=20&offset=0'.format(
            ip=config['ip'],
            port=config['port'],
            protocol=config['protocol'],
            filter_condition=filter_condition
        )
        print(url)
        response = requests.request("GET", url, headers=headers)
        if response is not None:
            result = response.json().get("result", [])
            while (len(result) > 0):
                combinedJobs.extend(result)
                next_url = response.json().get('links')['next']
                nextUrl = '{protocol}://{ip}:{port}{next}'.format(next=next_url,
                                                                  ip=config['ip'],
                                                                  port=config['port'],
                                                                  protocol=config['protocol'],
                                                                  )
                response = callurl(nextUrl)
                result = response.json().get("result", [])
            return combinedJobs
    except Exception as e:
        print(e)
        raise CustomError("Unable to get job metrics info")


def callurl(url):
    try:
        print("url {url}".format(url=url))
        response = requests.request("GET", url, headers=headers)
        if response is not None:
            return response
    except:
        raise CustomError("Unable to get response for url: {url}".format(url=url))


def get_table_info(config, source_id, table_id):
    try:
        url = '{protocol}://{ip}:{port}/v3/sources/{source_id}/tables/{table_id}'.format(
            ip=config['ip'],
            port=config['port'],
            protocol=config['protocol'],
            source_id=source_id,
            table_id=table_id
        )
        print(url)
        response = requests.request("GET", url, headers=headers)

        if response is not None:
            response = response.json().get("result", None)
            return response
    except:
        raise CustomError("Unable to get ingestion job metrics info")


def send_events_to_loganalytics(metrics_data,table_name):
    azure_log_customer_id = ''
    azure_log_shared_key = ''
    data_json = json.dumps(metrics_data)
    try:
        post_data(azure_log_customer_id, azure_log_shared_key, data_json, table_name)
    except Exception as error:
        logging.error("Unable to send data to Azure Log")
        logging.error(error)


def trigger_logic_app(job,job_url):
    url = "https://prod-04.centralus.logic.azure.com:443/workflows/a362b6c5441f4a368bc82d25b6387636/triggers/manual/paths/invoke?api-version=2016-10-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=jS7_KvGKCSXyk8zAlLKEerWoSROPXfSUi0xdYt8GfN4"
    payload=json.dumps({"job":job,"job_url":job_url})
    headers = {'Content-Type': 'application/json'}
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)


if __name__ == "__main__":
    try:
        client_config = {'protocol': 'http', 'ip': '10.16.11.2', 'port': 3001}
        delay = int(args['time_range'])
        now = datetime.datetime.now(tz=timezone.utc) - datetime.timedelta(minutes=delay)
        date_string = now.strftime('%Y-%m-%dT%H:%M:%SZ')
        #date_string = "2020-11-10T06:04:13Z"
        job_metrics_final = []
        list_of_jobs_obj = get_job_url(client_config,date_string)
        try:
            for job in list_of_jobs_obj:
                job_id = job["id"]
                job_entity_type = job["entity_type"]
                job_status = job["status"]
                if job_status == "failed" or job_status == "canceled":
                    job_url = "http://10.16.11.2:3000/job/logs?jobId={}".format(job_id)
                    trigger_logic_app(job_id,job_url)
                    location = "/opt/infoworks/temp/"+job_id+".zip"
                    location = "/Users/infoworks/Downloads/"+job_id+".zip"
                    download_infoworks_job_logs('10.16.11.2',job_id,headers,location)
                    create_freshdesk_ticket_with_attachment(job_id,job_entity_type,location)
                if job_entity_type == "source":
                    src_id = job["entity_id"]
                    src_name = get_source_name(client_config, src_id)
                    try:
                        tg_id, processedAt, job_end_time, job_status = get_tablegroup_id(client_config, job_id,src_id)
                        table_group_name, all_tables_list = get_table_group_name(client_config, tg_id, src_id)
                    except:
                        # This means the job is non-tablegroup job
                        table_group_name = ""
                        all_tables_list = []
                    ing_metrics = get_ingestion_metrics_url(client_config, str(job_id), src_id)
                    successful_tables = []
                    if ing_metrics is not None:
                        tables_list = list(set([i['table_id'] for i in ing_metrics]))
                        df = pd.DataFrame(ing_metrics)
                        for table_id in tables_list:
                            successful_tables.append(table_id)
                            filter1 = df["table_id"] == table_id
                            table = {}
                            if len(df.loc[filter1]) > 1:
                                # Incremental Job
                                filter2 = df["job_type"] == "CDC"
                                filter3 = df["job_type"] == "MERGE"
                                cdc_output = df.loc[filter1 & filter2].to_dict('records')[0]
                                merge_output = df.loc[filter1 & filter3].to_dict('records')[0]
                                for item in ['source_id', 'fetch_records_count', 'job_id', 'job_start_time']:
                                    table[item] = cdc_output[item]
                                for item in ['job_end_time', 'job_status', 'target_records_count']:
                                    table[item] = merge_output[item]
                                table['job_type'] = "INCREMENTAL"
                            else:
                                table = df.loc[filter1].to_dict('records')[0]
                            table_name_url = get_table_info(client_config, table.get('source_id'), table_id)
                            table_name = table_name_url.get('name')
                            table["source_name"] = src_name
                            table["table_group_name"] = table_group_name
                            table["table_name"] = table_name
                            import math

                            if math.isnan(table.get('target_records_count')):
                                table['pre_target_count'] = None
                                table['target_records_count'] = None
                            else:
                                if table["job_status"] == "FAILED":
                                    table['pre_target_count'] = table.get('target_records_count')
                                    table['target_records_count'] = int(table.get('target_records_count'))
                                else:
                                    table['pre_target_count'] = int(
                                        table.get('target_records_count') - int(table.get('fetch_records_count')))
                                    table['target_records_count'] = int(table.get('target_records_count'))
                            if table.get('job_type') == "CDC":
                                table['job_type'] = "INCREMENTAL"
                            od = OrderedDict()
                            table['job_start_time'] = table['job_start_time'].split('.')[0].replace('T', ' ')
                            table['job_end_time'] = table['job_end_time'].split('.')[0].replace('T', ' ')
                            table['fetch_records_count'] = int(table['fetch_records_count'])
                            for key in ['job_id', 'job_type', 'job_start_time', 'job_end_time', 'job_duration', 'job_status',
                                        'source_name',
                                        'table_group_name',
                                        'table_name', 'pre_target_count', 'fetch_records_count',
                                        'target_records_count']:
                                od[key] = table[key]
                            job_metrics_final.append(od)

                    for table in all_tables_list:
                        if table['table_id'] not in successful_tables:
                            tableInfo = get_table_info(client_config, src_id, table['table_id'])
                            table_name = tableInfo.get("name")
                            row_count = tableInfo.get('row_count', 0)
                            synctype = tableInfo.get('configuration').get('sync_type')
                            job_duration = tableInfo.get("job_duration")
                            temp = {
                                'job_id': job_id,
                                'job_type': synctype.upper(),
                                'job_start_time': processedAt.split('.')[0].replace('T', ' '),
                                'job_end_time': job_end_time.split('.')[0].replace('T', ' '),
                                'job_duration': job_duration,
                                'job_status': job_status.upper(),
                                "source_name": src_name, "table_group_name": table_group_name, "table_name": table_name,
                                "pre_target_count": row_count, "fetch_records_count": 0,
                                "target_records_count": row_count}
                            job_metrics_final.append(temp)
                    log_type = "source_ingestion_metrics"
                    send_events_to_loganalytics(job_metrics_final,log_type)
                elif job_entity_type == "pipeline":
                    job_details = []
                    od = OrderedDict()
                    od["job_id"] = job["id"]
                    od["job_type"] = job["type"]
                    od["pipeline_id"] = job["entity_id"]
                    od["job_start_time"] = job["created_at"].split('.')[0].replace('T', ' ')
                    od["job_end_time"] = job["last_updated"].split('.')[0].replace('T', ' ')
                    od["duration"] = job["duration"]
                    od["status"] = job["status"]
                    job_details.append(od)
                    log_type = "pipeline_job_metrics"
                    send_events_to_loganalytics(job_details,log_type)
                else:
                    pass
        except Exception as e:
            print(str(e))
            traceback.print_exc()

    except Exception as e:
        print(str(e))
        traceback.print_exc()

    #Alert for long running jobs
    try:
        client_config = {'protocol': 'http', 'ip': '10.16.11.2', 'port': 3001}
        running_jobs = get_running_jobs(client_config)
        delay = 30
        now = datetime.datetime.now(tz=timezone.utc) - datetime.timedelta(days=delay)
        date_string = now.strftime('%Y-%m-%dT%H:%M:%SZ')
        for job in running_jobs:
            hist_jobs = get_history_jobs(client_config,date_string,job["entity_id"],job.get("sub_entity_id"),job.get("entity_type"))
            duration_list = [ int(i["duration"]) for i in hist_jobs ]
            avg_duration = int(mean(duration_list))
            print(hist_jobs)
            print(avg_duration)
            if job["duration"] >= 3*avg_duration:
                #Raise an alert
                pass

    except Exception as e:
        print(str(e))
        traceback.print_exc()
