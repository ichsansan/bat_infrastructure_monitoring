import pandas as pd
import numpy as np
import subprocess, config, re, time


def run_shell(command):
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    raw_data = str(p.communicate()[0].decode())
    return raw_data
    
def get_docker_status():
    raw_data = run_shell("docker ps -a")
    
    data = raw_data.replace('  ', '\t')
    data = data.replace('\t ', '\t')
    while '\t\t' in data: data = data.replace('\t\t', '\t')

    data = [c.split('\t') for c in data.split('\n')]
    header = data[0]
    body = data[1:]

    results = {}
    results['header'] = ('DOCKER NAME', 'IMAGE','CREATED','STATUS','ACTION')

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