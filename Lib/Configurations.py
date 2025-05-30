

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
