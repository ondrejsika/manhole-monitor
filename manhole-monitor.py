import argparse

from twisted.internet import protocol, reactor
from twisted.internet.task import LoopingCall
from twisted.protocols.basic import LineReceiver


parser = argparse.ArgumentParser('manhole monitor')
parser.add_argument('host')
parser.add_argument('port', type=int)
parser.add_argument('wait', type=int)
parser.add_argument('py_file')
parser.add_argument('--show-input', action='store_true')


args = parser.parse_args()


py_code = open(args.py_file).read()


class ManholeMonProtocol(LineReceiver):
    def connectionMade(self):
        loop = LoopingCall(self._call)
        loop.start(args.wait)

    def lineReceived(self, data):
        if not args.show_input:
            if '>>> ' in data:
                return
        print data

    def _call(self):
        self.transport.write(py_code)

class ManholeMonFactory(protocol.ClientFactory):
    def buildProtocol(self, addr):
        return ManholeMonProtocol()


reactor.connectTCP(args.host, args.port, ManholeMonFactory())
reactor.run()

