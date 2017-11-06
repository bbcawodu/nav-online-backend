from sample_twisted_protocol.remote_proto_and_factory import RemoteCalculationFactory
from twisted.trial import unittest
from twisted.test import proto_helpers


class RemoteCalculationTestCase(unittest.TestCase):
    """
    This class tests the RemoteCalculationFactory and RemoteCalculationProtocol that make the calculation class
    available through a network. This class tests the Server Components independent from the client. It does this
    through mimicking client calls to the server factory and protocol classes(which act as the server):
    1) Testing that the server protocol sends the expected result through the network(test StringTransport made
       available by the twisted.test pkg) when it receives a line from the network that expresses an operation.
    """
    def setUp(self):
        # Declare test factory  that instantiates protocol objects, that acts as the server in this instance, that talk
        # to clients
        factory = RemoteCalculationFactory()

        # declare test protocol object that can talk to a client
        self.proto = factory.buildProtocol(('127.0.0.1', 0))

        # declare a fake transport object that acts as the network connection. the connection is used to receive
        # the output of the protocol
        self.tr = proto_helpers.StringTransport()

        # connect the fake transport object to the test protocol
        self.proto.makeConnection(self.tr)

    def _test(self, operation, a, b, expected):
        # make a call to dataReceived method of the test protocol. This acts like a call to the server, simulating
        # data arriving at the test transport, and being passed to the protocol.
        self.proto.dataReceived('%s %d %d\r\n' % (operation, a, b))

        # test that the output of the transport is the expected value of the calculation
        self.assertEqual(int(self.tr.value()), expected)

    def test_add(self):
        return self._test('add', 7, 6, 13)

    def test_subtract(self):
        return self._test('subtract', 82, 78, 4)

    def test_multiply(self):
        return self._test('multiply', 2, 8, 16)

    def test_divide(self):
        return self._test('divide', 14, 3, 4)