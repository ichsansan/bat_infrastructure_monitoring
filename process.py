import pandas as pd
import numpy as np
import subprocess, config, re, time
from sqlalchemy import create_engine

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
        raw_data = run_shell("docker ps")
    
    data = raw_data.replace('  ', '\t')
    data = data.replace('\t ', '\t')
    while '\t\t' in data: data = data.replace('\t\t', '\t')

    data = [c.split('\t') for c in data.split('\n')]
    header = data[0]
    body = data[1:]

    results = {}
    results['header'] = ('DOCKER NAME', 'NAME','CREATED','STATUS','CHECKLIST','ACTION')

    body_result = {}
    for b in body:
        if len(b) == 7:
            container_id, image, command, created, status, ports, names = b
        elif len(b) == 6:
            container_id, image, command, created, status, names = b
        else: continue
        body_result[names] = {
            'IMAGE': config.DOCKER_ALIAS[names]['name'] if names in config.DOCKER_ALIAS.keys() else image, # image,
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

# def do_restart_services():
#     commands = [
#         "docker restart subs",
#         "docker restart sokket-bat-opc-read",
#         "docker restart watchdog",
#         "docker restart write",
#         "docker restart opc-write-copt"
#     ]
#     results = ""
#     for com in commands:
#         try:
#             results += run_shell(com)
#         except Exception as e:
#             results += str(e) + '\n'
#     return results

def do_database_checking():
    con = "mysql+mysqlconnector://root:P%40ssw0rd@localhost:3306"
    q = f"SHOW DATABASES"
    dbs = pd.read_sql(q, con)
    dbs = [f for f in dbs.values.reshape(-1) if (f.startswith('db_bat')) and (not (f.endswith('_dev')))]
    
    ret = {}
    warnings = []
    
    for db in dbs:
        print(db)

        with create_engine(f"{con}/{db}").connect() as engine:
            ret[db] = []

            # Cek read opc
            for name, table in [['Read OPC','tb_bat_raw']]:
                print(f"Running {name}")
                q = f"""SELECT NOW() AS `now`, 
                        MAX(R.f_date_rec) AS latest_ts, 
                        NOW() - MAX(R.f_date_rec) AS delay 
                        FROM tb_tags_read_conf C
                        LEFT JOIN tb_bat_raw R
                        ON R.f_address_no = C.f_tag_name 
                        WHERE C.f_is_active = 1"""
                try:
                    rawdata = pd.read_sql(q, engine)
                    now, latest_ts, delay = rawdata.iloc[0]
                    if delay < 600:
                        status = True
                        subtitle = f"Data terakhir {latest_ts}"
                    else:
                        status = False
                        subtitle = f"Data telat sejak {latest_ts}"

                    summary = {
                        'title': name,
                        'status': status,
                        'subtitle': subtitle
                    }
                    ret[db].append(summary)
                except Exception as E:
                    message = f"Error fetching Read OPC on {db}: `{E}`"
                    warnings.append(message)

            # Cek write opc
            for name,table in [['Write OPC','tb_opc_write'],['Write OPC COPT','tb_opc_write_copt']]:
                print(f"Running {name}")
                try:
                    try:
                        q = f"""SELECT "{db}" AS db,
                                "{table}" AS `table`,
                                COUNT(*) AS `stucked`,
                                MIN(ts) AS `mintime`
                                FROM {table}
                                """
                        opcwriter = pd.read_sql(q, engine)
                    except:
                        q = f"""SELECT "{db}" AS db,
                                "{table}" AS `table`,
                                COUNT(*) AS `stucked`,
                                "-" AS `mintime`
                                FROM {table}
                                """
                        opcwriter = pd.read_sql(q, engine)

                    _, _, stucked, mintime = opcwriter.iloc[0]
                    if opcwriter.iloc[0]['stucked'] < 5: 
                        status = True
                        subtitle = 'Aman'
                    else: 
                        status = False
                        subtitle = f"Ada penumpukan {stucked} baris sejak {mintime}"
                    summary = {
                        'title': name,
                        'status': status,
                        'subtitle': subtitle
                    }
                    ret[db].append(summary)
                except Exception as E:
                    message = f"Error fetching Read OPC on {db}: `{E}`"
                    warnings.append(message)

            # Cek pemodelan copt
            for name, table in [['COPT Model', 'tb_combustion_model_generation']]:
                print(f"Running {name}")
                try:
                    q = f"""SELECT R.f_value FROM tb_effectivity_config C
                            LEFT JOIN tb_bat_raw R 
                            ON C.f_value = R.f_address_no 
                            WHERE f_description = "COPT enable tag" """
                    copt_status = pd.read_sql(q, engine).replace('False',0).replace('True',1).values[0][0]

                    q = f"""SELECT NOW() AS `now`, MAX(ts) AS `latest_data`, 
                            NOW() - MAX(ts) AS `delay` FROM {table} """
                    copt_generation = pd.read_sql(q, engine)
                    now, latest_data, _ = copt_generation.iloc[0]
                    delay = pd.to_datetime(now) - pd.to_datetime(latest_data)

                    if (copt_status == 1) and (delay > pd.to_timedelta('15min')):
                        status = False
                        subtitle = f"<b>COPT Enable</b>, ada delay rekomendasi sejak {latest_data}"
                    else:
                        status = True
                        if copt_status == 1: subtitle = f"<b>COPT Enable</b>, rekomendasi terakhir: {latest_data}"
                        else: subtitle = f"COPT Disable, rekomendasi terakhir: {latest_data}"

                    summary = {
                        'title': name,
                        'status': status,
                        'subtitle': subtitle
                    }
                    ret[db].append(summary)
                except Exception as E:
                    message = f"Error fetching Read OPC on {db}: `{E}`"
                    warnings.append(message)
    return ret, warnings

if __name__ == '__main__':
    print(get_bat_status())