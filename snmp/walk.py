from configuracao.configuracao import ip, port, oid
from pysnmp.hlapi import *
import os, json, datetime

def walk_from_oid(ip=ip, port=port, oid=oid, engine=SnmpEngine(), context=ContextData()):
    _logger = []
    dicionario = {}
    erro = False
    for (errorIndication,
        errorStatus,
        errorIndex,
        varBinds) in nextCmd(engine,
                            CommunityData('public'),
                            UdpTransportTarget((ip, port)),
                            context,
                            ObjectType(ObjectIdentity(oid).loadMibs()),
                            lookupMib=True,
                            lexicographicMode=True):
        if errorIndication:
            erro = True
            _logger.append(errorIndication)
            break
        elif errorStatus:
            print('%s at %s' % (errorStatus.prettyPrint(),
                                errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
            break
        else:
            for varBind in varBinds:
                dicionario.update({str(varBind[0].prettyPrint()) : str(varBind[0])})
    return dicionario, erro, _logger
    
def write_to_json(dicionario, erro, _logger, ip=ip):
    if (os.path.exists("repo/" + ip)):
        if not erro:
            with open("repo/" + ip + "/dicionario.json", "w+") as fp:
                json.dump(di, fp, ensure_ascii=False, indent=4)

        else:
             with open("repo/" + ip + "/logger.txt", "a+") as fp:
                for _log in _logger:
                    fp.write(str(_log) + '  @' + str(datetime.datetime.now()) + '\n')

    else:
        if not erro:
            os.mkdir("repo/" + ip)
            with open("repo/" + ip + "/dicionario.json", "w+") as fp:
                json.dump(di, fp, ensure_ascii=False, indent=4)
                
        else:
            os.mkdir("repo/" + ip)
            with open("repo/" + ip + "/logger.txt", "a+") as fp:
                for _log in _logger:
                    fp.write(str(_log) + '  @' + str(datetime.datetime.now()) + '\n')

if __name__ == "__main__":
    di, erro, _logger = walk_from_oid()
    write_to_json(di, erro, _logger)