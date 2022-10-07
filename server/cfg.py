class cfg:
    def readCfgFile(self):
        with open('ini.cfg') as f:
            return [line for line in f.readlines()]

    def __init__(self):
        self.file = self.readCfgFile()
        self.broker = self.file[0].replace('broker = ','').replace('\n','')
        self.host = self.file[1].replace('host = ','').replace('\n','')
        self.port = int(self.file[2].replace('port = ','').replace('\n',''))
        self.user = self.file[3].replace('user = ','').replace('\n','')
        self.password = self.file[4].replace('password = ','').replace('\n','')

'''config = cfg()

print(config.broker)
print(config.host)
print(config.port)
print(config.user)
print(config.password)'''
    