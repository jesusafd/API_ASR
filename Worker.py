import pysnmp
import threading
from pysnmp.entity.rfc3413.oneliner import cmdgen
from pysnmp.entity import engine, config
from pysnmp.carrier.asyncore.dgram import udp
from pysnmp.entity.rfc3413 import ntfrcv
class Worker(threading.Thread):

	
	estado = 20.0
	def getEstado(self):
		return self.estado
	def cbFun(self,snmpEngine, stateReference, contextEngineId, contextName, varBinds, cbCtx):
		result = {}
		mensaje = ""
		for name, val in varBinds:   
			tmp = str(val)
			#print(tmp)
			if tmp == "Interface FastEthernet2/0, changed state to up":
				self.estado = "UP"
				mensaje += tmp
				
				#print("Estado de la interfaz: "+tmp)
				result['Tiempo'] = datetime.datetime.utcnow().isoformat()
				mensaje+=",en el tiempo: "+ datetime.datetime.utcnow().isoformat()
				result['Estado'] = self.estado
				with open('resultados_traps.txt','a') as f:
					f.write(mensaje)
					f.write('\n')
			if tmp == "administratively down":
				self.estado = "DOWN"
				mensaje += "Interface FastEthernet2/0, changed state to: "+tmp
				#print("Estado de la interfaz: "+tmp)
				result['Tiempo'] = datetime.datetime.utcnow().isoformat()
				mensaje+=",en el tiempo: "+ datetime.datetime.utcnow().isoformat()
				result['Estado'] = self.estado
				with open('resultados_traps.txt', 'a') as f:
					f.write(mensaje)
					f.write('\n')
				mensaje = ""
	def run(self):
		snmpEngine = engine.SnmpEngine()
		TrapAgentAddress = '10.0.1.2';
		Port = 162;
		config.addTransport(snmpEngine, udp.domainName + (1,), udp.UdpTransport().openServerMode((TrapAgentAddress, Port)))
		config.addV1System(snmpEngine, 'public', 'public')
		ntfrcv.NotificationReceiver(snmpEngine, self.cbFun)
		snmpEngine.transportDispatcher.jobStarted(1)
		try:
			snmpEngine.transportDispatcher.runDispatcher()
		except:
			snmpEngine.transportDispatcher.closeDispatcher()
			raise




