import pexpect,json,os,logging,subprocess,argparse,queue,datetime
from threading import Thread
import traceback
import pandas as pd
import threading
from time import sleep

logging.getLogger().setLevel(logging.INFO)
parser = argparse.ArgumentParser('Harqen API')
parser.add_argument('--username', required=False,default='', help='Pass your username here')
args = vars(parser.parse_args())

num_fetch_threads = 100
job_queue = queue.Queue(maxsize=120)
global_lock = threading.Lock()


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def list_candidates():
    df = pd.read_csv("Harqen_Data.csv")
    candidates = list(df["Invite Id"])
    return candidates


def get_candidate_details(i,candidate_id,username):
    try:
        logging.info(bcolors.HEADER+'{}: Getting candidate details for  {} '.format(i,candidate_id)+bcolors.ENDC)
        shell_cmd = 'curl https://va.harqen.com/s/api/v1/candidate/{} -u {}'.format(candidate_id,username)
        child = pexpect.spawn(shell_cmd, encoding='utf-8')
        child.expect('Enter host password for user .*')
        child.sendline('\n')
        output = str(child.read()).strip("\r\n")
        json_output = json.loads(output)
        return json_output
    except Exception as e:
        traceback.print_exc()
        logging.exception(bcolors.FAIL+'{}: Failed to retrieve candidate details for  {} : {}'.format(i,candidate_id,str(e))+bcolors.ENDC)


def get_access_token(media_type,media_id,username):
    shell_cmd = "curl -X POST https://va.harqen.com/s/api/v1/media/accesstoken/{}/{} -u {}".format(media_type,media_id,username)
    child = pexpect.spawn(shell_cmd, encoding='utf-8')
    child.expect('Enter host password for user .*')
    child.sendline('\n')
    output = str(child.read()).strip("\r\n")
    if "message" in output:
        return None
    return output


def download_audio(i,j,media_type,media_id,access_token,candidate_name):
    try:
        if media_type == "audio":
            file_name = os.path.join("downloads",media_id+".mpeg")
        else:
            file_name = os.path.join("downloads",media_id+".mp4")
        shell_cmd = "curl -X GET https://va.harqen.com/s/api/v1/media/{}/{}?accessToken={} --output {} > /dev/null 2>&1".format(media_type,media_id,access_token,file_name)
        os.popen(shell_cmd)
        target_path = os.path.join("/FileStore/tables/ar_harqen",candidate_name,str(j))
        copy_file_to_dbfs(i,file_name,target_path)
        return os.path.join("/FileStore/tables/ar_harqen",candidate_name)
    except Exception:
        return ""


def copy_file_to_dbfs(i,file_path,target_path):
    target_path = os.path.join(target_path,file_path.replace("downloads/",""))
    cmd = "dbfs cp --overwrite {} dbfs:{}".format(file_path,target_path)
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    proc_stdout = process.communicate()[0].strip()
    if process.returncode == 0:
        logging.info(bcolors.OKGREEN+'{}: Copy of {} from local to DBFS Successful'.format(i,file_path)+bcolors.ENDC)
    else:
        logging.exception(bcolors.FAIL+"{}: Copy of {} failed : {}".format(i,file_path,str(proc_stdout.decode("utf-8")))+bcolors.ENDC)


def dump_candidate_details(candidate_json,media_path,candidate_timestamp):
    while global_lock.locked():
        sleep(0.01)
        continue
    global_lock.acquire()
    candidate_json["dbfs_media_location"] = media_path
    file_path = os.path.join("downloads","_".join((candidate_timestamp,"candidate_details.json")))
    with open(file_path, 'a+') as fp:
        json.dump(candidate_json, fp)
        fp.write("\n")
    global_lock.release()


def remove_special_character(string):
    return ''.join(e for e in string if e.isalnum())


def run_candidate_job(i,q,username,candidate_timestamp):
    try:
        while True:
            print('%s: Looking for the next conversion job' % i)
            candidate = q.get()
            json_output = get_candidate_details(str(i),candidate, username)
            candidate_name = "_".join((str(candidate), remove_special_character(json_output["firstName"]), remove_special_character(json_output["lastName"])))
            media_path = None
            if json_output:
                for j,answer in enumerate(json_output.get("answers", [])):
                    media_type = answer["media"]["mediaType"]
                    media_id = str(answer["media"]["id"])
                    logging.info(bcolors.OKBLUE + "{}: Downloading {} {}".format(str(i),media_type, media_id) + bcolors.ENDC)
                    access_token = get_access_token(media_type, media_id, username)
                    if access_token:
                        media_path = download_audio(str(i),j,media_type, media_id, access_token, candidate_name)
                if media_path:
                    dump_candidate_details(json_output, media_path,candidate_timestamp)
            q.task_done()
    except Exception as e:
        print(str(e))
        q.task_done()


if __name__ == "__main__":
    username = args["username"]
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
    candidate_details = list_candidates()
    candidate_timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    for i in range(num_fetch_threads):
        worker = Thread(target=run_candidate_job, args=(i, job_queue,username,candidate_timestamp))
        worker.setDaemon(True)
        worker.start()
    for candidate in candidate_details:
        job_queue.put(candidate)

    # Now wait for the queue to be empty, indicating that we have processed all of the tables.
    print('*** Main thread waiting')
    job_queue.join()
    print('*** Done')

    if len(candidate_details) > 0:
        file_path = os.path.join("downloads","_".join((candidate_timestamp,"candidate_details.json")))
        target_path = '/FileStore/tables/ar_harqen/candidate_jsons/'
        copy_file_to_dbfs("main",file_path, target_path)
        logging.info(bcolors.OKGREEN + 'Copy of JSONs to DBFS Successful' + bcolors.ENDC)


