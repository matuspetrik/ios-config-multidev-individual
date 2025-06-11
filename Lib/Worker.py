from netmiko import ConnectHandler
import time
import datetime
import Lib.Configurations as Configs
import sys

def session_worker_cisco_ios(hostname, output_q, router, output_dict, method):
    ''' A session worker for Cisco IOS devices.
    '''
   # output_dict = {}
    with open(PATH_CONFIG+hostname) as f:
        lines = f.read().splitlines()
    device_session = ConnectHandler(**router)
    time.sleep(2)
    device_session.enable()
    output_list = []
    output_dict[hostname+"_"+method] = ""
    output = "##############################################\r\n# Device config started at: "+str(datetime.datetime.now())+" #\r\n##############################################\r\n"
    output += device_session.send_config_set(lines, delay_factor=4)
    #output += device_session.send_command("write\r\n")  # uncomment if you want the config to be written
    #output += device_session.send_command("\r\n") 
    #output += device_session.save_config() 
#    output = net_connect.send_command_timing(command)
    #print(output)
    if "confirm" in output: # in case 'y' confirmation is needed
        output += device_session.send_command_timing("y", strip_prompt=False,
                                                     strip_command=False) 
    output += device_session.save_config()
    with open(PATH_LOG+hostname,'a+') as the_file:
        the_file.write(output)
        the_file.write("\r\n")
    output_dict[hostname+".log"]  = output
    output_q.put(output_dict)
    time.sleep(2)
    device_session.disconnect()

def session_worker_mikrotik(
                            hostname,
                            output_q,
                            router,
                            output_dict,
                            common_config,
                            method,
                            PATH_CONFIG,
                            PATH_LOG,
                            ):
    ''' A session worker for Mikrotik OS devices.
    '''
    lines = Configs.return_full_config(PATH_CONFIG, hostname, common_config)
    device_session = ConnectHandler(**router)
    # print(device_session)
    output_dict[hostname+"_"+method] = ""
    datetime_then = datetime.datetime.now()
    output = f"### {hostname} config started at: { str(datetime_then) } ###\r\n\r\n"
    for line in lines:
        status = "OK"
        try:
            tmp_output = device_session.send_command(line)
            if "failure:" in tmp_output.strip().lower():
                status = "FAIL"
                output += f"{ status } ---> { line }\r\n"
                output += f"{ tmp_output }\r\n"
            else:
                output += f"{ status } ---> { line }\r\n"
            if "confirm" in output: # in case 'y' confirmation is needed
                output += device_session.send_command_timing(
                    "y",
                    strip_prompt=False,
                    strip_command=False
                    ) 
        except Exception as e:
            status = "FAIL"
            output += f"{ status } -> { line }, { e }\r\n"
    output += f"\r\n### {hostname} config completed in "+str((datetime.datetime.now()\
        -datetime_then).total_seconds())+" seconds. ###\r\n"
    Configs.write_log(PATH_LOG+hostname, output)
    # print(output)
    output_dict[hostname+".log"]  = output
    # output_dict[hostname]  = output
    output_q.put(output_dict)
    device_session.disconnect()
    time.sleep(2)

def session_worker_general(**kwargs):
    if 'mikrotik' in kwargs.get('device_type'):
        session_worker_mikrotik(
            kwargs.get('hostname'),
            kwargs.get('output_q'),
            kwargs.get('router'),
            kwargs.get('output_dict'),
            kwargs.get('common_config'),
            kwargs.get('method'),
            kwargs.get('PATH_CONFIG'),
            kwargs.get('PATH_LOG'),
        )
    elif 'cisco_ios' in kwargs.get('device_type'):
        session_worker_cisco_ios(
            # hostname,
            # output_q,
            # router,
            # output_dict,
            # method="ssh"
            kwargs.get('hostname'),
            kwargs.get('output_q'),
            kwargs.get('router'),
            kwargs.get('output_dict'),
            kwargs.get('method'),
            kwargs.get('common_config'),
            kwargs.get('PATH_CONFIG'),
            kwargs.get('PATH_LOG')
        )