from netmiko import ConnectHandler
import time
import datetime

def session_worker_cisco_ios(hostname, output_q, router, output_dict, method):
   # output_dict = {}
    with open(PATH_INPUT+hostname) as f:
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
    if "confirm" in output:
        output += device_session.send_command_timing("y", strip_prompt=False, strip_command=False) # in case 'y' confirmation is needed
    output += device_session.save_config()
    with open(PATH+hostname,'a+') as the_file:
        the_file.write(output)
        the_file.write("\r\n")
    output_dict[hostname+".log"]  = output
    output_q.put(output_dict)
    time.sleep(2)
    device_session.disconnect()

def session_worker_mikrotik(hostname, output_q, router, output_dict, method, PATH_INPUT, PATH):
   # output_dict = {}
    print(PATH_INPUT)
    with open(PATH_INPUT+hostname) as f:
        lines = f.read().splitlines()
    print(lines)
    device_session = ConnectHandler(**router)
    print(lines)
    time.sleep(2)
    output_dict[hostname+"_"+method] = ""
    datetime_then = datetime.datetime.now()
    output = f"##############################################\r\n# {hostname} config started at: "+str(datetime_then)+" #\r\n||||||||||||||||||||||||||||||||||||||||||||||\r\n"
    for line in lines:
        output += device_session.send_command(line)
    if "confirm" in output:
        output += device_session.send_command_timing("y", strip_prompt=False, strip_command=False) # in case 'y' confirmation is needed
    # output += device_session.save_config()
    output += f"||||||||||||||||||||||||||||||||||||||||||||||\r\n# {hostname} config completed in "+str((datetime.datetime.now()-datetime_then).total_seconds())+" seconds. #\r\n##############################################\r\n"
    print(output)
    with open(PATH+hostname,'a+') as the_file:
        the_file.write(output)
        the_file.write("\r\n")
    output_dict[hostname+".log"]  = output
    output_q.put(output_dict)
    time.sleep(2)
    device_session.disconnect()
