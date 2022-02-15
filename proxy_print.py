proxies = open('proxies.txt').read().splitlines()



for proxy in proxies:
    host, port, *user = proxy.split(':')
    print(host + ':' + port)