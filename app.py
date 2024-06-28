from flask import Flask, request, render_template
import ipaddress

app = Flask(__name__)

def ip_range_to_cidr(ip_range):
    try:
        start_ip_str, end_ip_str = ip_range.split('-')
        start_ip = ipaddress.IPv4Address(start_ip_str.strip())
        end_ip = ipaddress.IPv4Address(end_ip_str.strip())
        
        if int(end_ip) < int(start_ip):
            return []

        cidr_list = []
        while int(start_ip) <= int(end_ip):
            max_prefix_len = start_ip.max_prefixlen
            while max_prefix_len > 0:
                mask = (1 << max_prefix_len) - 1
                if int(start_ip) & mask == int(start_ip) and int(start_ip) + (1 << (32 - max_prefix_len)) - 1 <= int(end_ip):
                    break
                max_prefix_len -= 1
            cidr = ipaddress.IPv4Network((int(start_ip), max_prefix_len), strict=False)
            cidr_list.append(str(cidr))
            start_ip = cidr.broadcast_address + 1
        
        return cidr_list
    except Exception as e:
        print(f"Error: {e}")  # Debug print
        return []

@app.route('/', methods=['GET', 'POST'])
def index():
    cidr_list = []
    ip_range = ""
    if request.method == 'POST':
        ip_range = request.form['ip_range']
        print(f"Received IP range: {ip_range}")  # Debug print
        cidr_list = ip_range_to_cidr(ip_range)
        print(f"Generated CIDR list: {cidr_list}")  # Debug print
    return render_template('index.html', ip_range=ip_range, cidr_list=cidr_list)

if __name__ == '__main__':
    app.run(debug=True)
