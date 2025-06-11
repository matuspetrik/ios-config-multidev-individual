import sys

def identify_config(file_path):
    with open(file_path, 'r') as file:
        content = file.read().lower()

    # Cisco IOS distinctive patterns
    cisco_keywords = [
        'interface ', 'hostname ', 'ip route', 'router ospf', 'line vty',
        'enable secret', 'access-list', 'service password-encryption',
        'banner motd', 'no shutdown'
    ]

    # MikroTik RouterOS distinctive patterns
    mikrotik_keywords = [
        '/interface', '/ip address', '/system', '/routing', '/firewall',
        '/user', '/tool', '/log', '/queue', '/ppp', '/ip firewall filter',
        '/ip'
    ]

    # Count keyword matches
    cisco_score = sum(content.count(keyword) for keyword in cisco_keywords)
    mikrotik_score = sum(content.count(keyword) for keyword in mikrotik_keywords)

    # Determine result
    if cisco_score > mikrotik_score:
        confidence = cisco_score / (cisco_score + mikrotik_score)
        # return f"Cisco IOS Configuration (Confidence: {confidence:.2%})"
        return "cisco_ios_ssh"
    elif mikrotik_score > cisco_score:
        confidence = mikrotik_score / (cisco_score + mikrotik_score)
        # return f"MikroTik RouterOS Configuration (Confidence: {confidence:.2%})"
        return "mikrotik_routeros"
    else:
        return "Unknown Configuration Type"

def get_common_config(PATH_INPUT, common_config_file="common_config"):
    # If a special file called `common_config` is present
    # in the config directory content of this file will be
    # pushed to the device.
    with open(PATH_INPUT+common_config_file) as f:
        lines = f.read().splitlines()

    device_type = identify_config(PATH_INPUT+common_config_file)
    # Try if `common_config` file exists, if so, notify to be included
    # in the config
    common_config = []
    try:
        while True:
            user_input = input(f"NOTE: A special file called `common_config` "
                               f"of type {device_type} found. Continue? [Y/n]: ")\
                                   .strip().lower()
            if 'n' in user_input:
                print(f"NOTE: Okay , a special file called `common_config` "
                      "not used. Continuing as usual..")
                return 0
            else:
                return(lines)
    except:
        print(f"NOTE: A special file called `common_config` not found. "
               "Continuing as usual..")
        return 0

def return_full_config(PATH_INPUT, hostname, common_config):
    ''' Return device configuration including `common_config`.
        Input: lines.lst(), common_config.lst()
        Output: full_config.lst()
    '''
    with open(PATH_INPUT+hostname) as f:
        lines = f.read().splitlines()
    for line in common_config:
        lines.append(line)
    return(lines)

def write_log(filename, input):
    ''' Write input to filename.
        Input: filename (full path), input (text to write).
        Output: A written file.
    '''
    with open(filename,'a+') as f:
        f.write(input+"\r\n")
    return 1

def get_device_type(each):
    ''' Get device type statically
    '''
    while True:
        user_input = input(f"Device type determination by config file was "
                        "UNSUCCESSFUL. Provide manually:\r\n\
                        [C]isco IOS (prompt for each device)\r\n\
                        [Ci]sco IOS (no further prompts) \r\n\
                        [M]ikrotik (prompt for each device)\r\n\
                        [Mi]krotik (no further prompts)\r\n\
                        [Q]uit\r\n\
                        Your choice: "
                        ).strip().lower()
        allowed_options = ['c', 'm', 'q', 'ci', 'mi']
        if user_input in allowed_options:
            if user_input == "m":
                return "mikrotik_routeros"
            if user_input == "mi":
                each.for_each = False
                return "mikrotik_routeros"
            if user_input == "c":
                return "cisco_ios_ssh"
            if user_input == "ci":
                each.for_each = False
                return "cisco_ios_ssh"
            if user_input == "q":
                sys.exit()
            break
        else:
            print(f"Provide valid option.")


class ForEach:

    def __init__(self):
        self.for_each = True