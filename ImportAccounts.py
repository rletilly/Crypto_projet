def readAccounts():
    response = {}
    with open('database.txt','rb') as file :
        lines = file.readlines()
    for line in lines:
        registerLine = line.decode().split(',')
        username = registerLine[0].encode()
        response[username] = {}
        response[username]['accounts'] = []
        response[username]['password'] = registerLine[1].encode()

    for client in response:
        for line in lines:
            registerLine = line.decode().split(',')
            if client == registerLine[0].encode() : 
                
                account = {'accountNumber': int(registerLine[2][3]), 'balance': int(registerLine[3])}
                response[client]['accounts'].append(account)
    return response

def writeAccounts(response):
    with open('database.txt','w') as file :
        for client in response :
            for account in response[client]['accounts'] :
                line = str(client.decode())+','+str(response[client]['password'].decode())+','+str(client.decode())+'00'+str(account['accountNumber'])+','+str(account['balance'])+'\n'
                str(line)
                file.writelines(line)



