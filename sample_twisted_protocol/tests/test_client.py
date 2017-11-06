from sample_twisted_protocol.remote_client import RemoteCalculationClient
from twisted.trial import unittest
from twisted.test import proto_helpers


class ClientCalculationTestCase(unittest.TestCase):
    """
        This class tests the RemoteCalculationClient that accesses the  calculation class made available through a
        network(By the RemoteCalculationFactory and RemoteCalculationProtocol). This class tests the client class
        independent from the server. It does this by making calls to the client protocol components, which make calls
        to the network it's connected to(test StringTransport from twisted test pkg). Tests are run by making a call
        to the client method, which is connected to the test network:
        1) Testing that the client sends the correct line through the network, and
        2) also testing that the client can interpret the the received line, turning it into an expected result.
    """
    def setUp(self):
        self.tr = proto_helpers.StringTransport()
        self.proto = RemoteCalculationClient()
        self.proto.makeConnection(self.tr)

    def _test(self, operation, a, b, expected):
        d = getattr(self.proto, operation)(a, b)
        self.assertEqual(self.tr.value(), '%s %d %d\r\n' % (operation, a, b))
        self.tr.clear()
        d.addCallback(self.assertEqual, expected)
        self.proto.dataReceived("%d\r\n" % (expected,))
        return d

    def test_add(self):
        return self._test('add', 7, 6, 13)

    def test_subtract(self):
        return self._test('subtract', 82, 78, 4)

    def test_multiply(self):
        return self._test('multiply', 2, 8, 16)

    def test_divide(self):
        return self._test('divide', 14, 3, 4)
