import pandas as pd
import numpy as np
import subprocess, config, re, time

debug_mode = False

def run_shell(command):
    if debug_mode:
        print(f"Executing `command`")
        raw_data = ""
    else:
        p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        raw_data = str(p.communicate()[0].decode())
    return raw_data
    
def get_docker_status():
    if debug_mode:
        raw_data = f"""CONTAINER ID   IMAGE                                     COMMAND                  CREATED         STATUS        PORTS                      NAMES
db5184c563f9   192.168.32.6:5000/bat-fuse-pct1:v3.0      "/docker-entrypoint.…"   16 hours ago    Up 16 hours   0.0.0.0:80->80/tcp         bat-fuse-pct1
c0487e55e3ca   services-combustion-pct1:v1.5.5           "python3 ./Combustio…"   2 days ago      Up 2 days     0.0.0.0:8083->8083/tcp     services-combustion-pct1
f2dae35fbc56   ml-runner-pct1:v1.6                       "python3 ./MLrunner.…"   2 weeks ago     Up 6 days     0.0.0.0:5002->5000/tcp     ml-runner-pct1
400771e03008   combustion-scheduler-api-pct1:v1.5.4      "python3 ./Scheduler…"   2 weeks ago     Up 2 weeks                               combustion-scheduler-api-pct1
ff225e0c0594   e5cc9ac3a9aa                              "python /home/watchd…"   2 months ago    Up 43 hours                              watchdog
32b4b7d89859   801663c08a2a                              "/bin/sh read_opc.sh"    2 months ago    Up 43 hours   0.0.0.0:57888->57888/tcp   read_write_pct1
1e3ef1d4c048   192.168.32.6:5000/soket-bat-pct1:v1.6.1   "java -Xmx32G -jar a…"   3 months ago    Up 2 months   0.0.0.0:8081->8081/tcp     soket-bat-pct1
239e816e37be   mariadb:latest                            "docker-entrypoint.s…"   15 months ago   Up 2 months   0.0.0.0:3306->3306/tcp     mariadb
a9d79d7a7541   registry:2                                "/entrypoint.sh /etc…"   19 months ago   Up 2 months   0.0.0.0:5000->5000/tcp     registry"""
    else:
        raw_data = run_shell("docker ps -a")
    
    data = raw_data.replace('  ', '\t')
    data = data.replace('\t ', '\t')
    while '\t\t' in data: data = data.replace('\t\t', '\t')

    data = [c.split('\t') for c in data.split('\n')]
    header = data[0]
    body = data[1:]

    results = {}
    results['header'] = ('DOCKER NAME', 'IMAGE','CREATED','STATUS','CHECKLIST','ACTION')

    body_result = {}
    for b in body:
        if len(b) == 7:
            container_id, image, command, created, status, ports, names = b
        elif len(b) == 6:
            container_id, image, command, created, status, names = b
        else: continue
        body_result[names] = {
            'IMAGE': image,
            'CREATED': created,
            'STATUS': status
        }

    results['body'] = body_result
    return results

def get_bat_status():
    sopt_enable_desc = "SOOT BLOWER OPERATION ON/OFF (Main Start/Stop)"
    copt_enable_desc = "COMBUSTION ENABLE"

    data = {}
    for unitname in config.UNIT_CONFIG.keys():
        db_config = config.UNIT_CONFIG[unitname]
        con = f'mysql+mysqlconnector://root:P%40ssw0rd@{db_config["HOST"]}:3306/{db_config["DB"]}'

        q = f"""SELECT conf.f_description, raw.f_value FROM tb_sootblow_conf_tags conf
                LEFT JOIN tb_sootblow_raw raw 
                ON conf.f_tag_name = raw.f_address_no 
                WHERE conf.f_description = "{sopt_enable_desc}"
                UNION 
                SELECT conf.f_description, raw.f_value FROM tb_tags_read_conf conf 
                LEFT JOIN tb_bat_raw raw
                ON conf.f_tag_name = raw.f_address_no 
                WHERE conf.f_description = "{copt_enable_desc}"
                """
        df = pd.read_sql(q, con).set_index('f_description')
        data[f'sootblow{unitname[-1]}'] = df.loc[sopt_enable_desc, 'f_value']
        data[f'combustion{unitname[-1]}'] = df.loc[copt_enable_desc, 'f_value']
    return data

def do_restart_individual_service(dockername):
    docker_status = get_docker_status()
    docker_status = pd.DataFrame(docker_status['body']).T
    
    if dockername not in docker_status.index:
        return ValueError('Docker name not found!')
    
    command = f"docker restart {dockername}"
    try:
        results = run_shell(command)
        return
    except Exception as e:
        raise SyntaxError(f"{e}")

def do_restart_services():
    commands = [
        "docker restart subs",
        "docker restart sokket-bat-opc-read",
        "docker restart watchdog",
        "docker restart write",
        "docker restart opc-write-copt"
    ]
    results = ""
    for com in commands:
        try:
            results += run_shell(com)
        except Exception as e:
            results += str(e) + '\n'
    return results

if __name__ == '__main__':
    print(get_bat_status())