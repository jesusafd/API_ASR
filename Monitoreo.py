import pysnmp
from pysnmp.entity.rfc3413.oneliner import cmdgen
from pysnmp.entity import engine, config
from pysnmp.carrier.asyncore.dgram import udp
from pysnmp.entity.rfc3413 import ntfrcv
import ply.lex
import datetime
import time
import threading
from Worker import Worker

class Monitoreo():
    cmdGen = cmdgen.CommandGenerator()
    @classmethod
    def snmp_query(cls,host,community,oid):
        errorIndication, errorStatus, errorIndex, varBinds = cls.cmdGen.getCmd(
            cmdgen.CommunityData(community),
            cmdgen.UdpTransportTarget((host, 161)),
            oid
        )

        # Revisamos errores e imprimimos resultados
        if errorIndication:
            print(errorIndication)
        else:
            if errorStatus:
                print('%s at %s' % (
                    errorStatus.prettyPrint(),
                    errorIndex and varBinds[int(errorIndex)-1] or '?'
                    )
                )
            else:
                for name, val in varBinds:
                    return(str(val))
    @classmethod
    def grabar(cls,host,community,host_OID,interface_OID):
        result = {}
        result['Tiempo'] = datetime.datetime.utcnow().isoformat()
        result['hostname'] = Monitoreo.snmp_query(host, community, host_OID)
        result['Fa0-0_In_uPackets'] = Monitoreo.snmp_query(host, community, interface_OID)
        with open('resultados.txt', 'a') as f:
            f.write(str(result))
            f.write('\n')

