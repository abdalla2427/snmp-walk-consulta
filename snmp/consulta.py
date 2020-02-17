from config.configuracao import ip, port, consultas_a_serem_feitas, resultado_consultas
from pysnmp.hlapi import *
import sys, json

def load_mib(path=consultas_a_serem_feitas):
    mib = {}
    with open(path, "r") as f:
        x = f.read()
        mib = json.loads(x)
    return mib

def get_and_save_to_json( mib, host=ip, port=port, engine=SnmpEngine(), context=ContextData()):
    dicionario = {}
    for feature in mib:
        for (errorIndication,
            errorStatus,
            errorIndex,
            varBinds) in getCmd(engine,
                                CommunityData("public"),
                                UdpTransportTarget((host, port)),
                                context,
                                ObjectType(ObjectIdentity(mib[feature])),
                                lookupMib=False,
                                lexicographicMode=False):

            if errorIndication:
                print(errorIndication, file=sys.stderr)
                break

            elif errorStatus:
                print("%s at %s" % (errorStatus.prettyPrint(),
                                    errorIndex and varBinds[int(errorIndex) - 1][0] or "?"), file=sys.stderr)
                break

            else:
                k = 0
                for varBind in varBinds:
                    k +=1
                    print("%s = %s" % varBind)
                    dicionario.update({feature + " " + str(k): str(varBind[1])})

    with open(resultado_consultas, "w") as fp:
        json.dump(dicionario, fp, ensure_ascii=False, indent=4)

def main():
    get_and_save_to_json(load_mib())

if __name__ == "__main__":
    main()