import py_expressway
import unittest
import responses
import io
from unittest.mock import MagicMock


class TestExpressway(unittest.TestCase):

  def setUp(self):
    self.test_address = "dummy"
    self.exp = py_expressway.Expressway(self.test_address, "dummy", "dummy")

    # API Paths

    self.api_neighborzone = "/api/provisioning/common/zone/neighborzone"
    self.api_uczone = "/api/provisioning/controller/zone/unifiedcommunicationstraversal"
    self.api_dns = "/api/provisioning/common/dns/dns"
    self.api_sip = "/api/provisioning/common/protocol/sip/configuration"
    self.api_mra = "/api/provisioning/common/mra"
    self.api_cucm = "/api/provisioning/controller/server/cucm"
    self.api_searchrule = "/api/provisioning/common/searchrule"
    self.api_statusxml = "/status.xml"

 
  @responses.activate
  def test_new_neighborzone(self):
    # arrange
    responses.add(
      responses.POST, 
      'https://{address}{path}'.format(
        address=self.test_address,
        path=self.api_neighborzone), 
      json={'Message': 'Successfully created Neighbor zone'}, status=200)
   
    # act
    response = self.exp.new_neighborzone(zone_name="test", peer_address=["2.2.2.2"])

    # assert
    self.assertDictEqual({'Message': 'Successfully created Neighbor zone'}, response)

  @responses.activate
  def test_new_neighborzone_already_exists(self):
    # arrange
    responses.add(
      responses.POST, 
      'https://{address}{path}'.format(
        address=self.test_address,
        path=self.api_neighborzone), 
      json={'Message': 'Neighbor zone name already exists'}, status=200)
   
    # act
    response = self.exp.new_neighborzone(zone_name="test", peer_address=["2.2.2.2"])

    # assert
    self.assertDictEqual({'Message': 'Neighbor zone name already exists'}, response)

  @responses.activate
  def test_new_uczone_traversalclient_timeout(self):
    # arrange
    responses.add(
      responses.POST, 
      'https://{address}{path}'.format(
        address=self.test_address,
        path=self.api_uczone), 
      json={'Error': 'Timeout or Connection Error'}, status=200)
   
    # act
    response = self.exp.new_uczone_traversalclient(zone_name="test uc client",
  peer_address=["127.0.0.1"], auth_user="ucuser", auth_pass="asdf", sip_port=7010)

    # assert
    self.assertDictEqual({'Error': 'Timeout or Connection Error'}, response)

  @responses.activate
  def test_mod_dns(self):
    # arrange
    responses.add(
      responses.PUT,
      'https://{address}{path}'.format(
        address=self.test_address,
        path=self.api_dns),
      json={'Message': 'Operation was successful'}, status=200)
   
    # act
    response = self.exp.mod_dns(domain_name="dummy.com", host_name="dummy")

    # assert
    self.assertDictEqual({'Message': 'Operation was successful'}, response)

  @responses.activate
  def test_mod_sip(self):
    # arrange
    responses.add(
      responses.PUT,
      'https://{address}{path}'.format(
        address=self.test_address,
        path=self.api_sip),
      json={'Message': 'Successfully updated the SIP Configuration'}, status=200)
   
    # act
    response = self.exp.mod_sip(tcp_mode="on", sip_mode="on", tcp_port=1234)

    # assert
    self.assertDictEqual({'Message': 'Successfully updated the SIP Configuration'}, response)

  @responses.activate
  def test_mod_mra(self):
    # arrange
    responses.add(
      responses.PUT,
      'https://{address}{path}'.format(
        address=self.test_address,
        path=self.api_mra),
      json={'Message': 'Operation was successful'}, status=200)
   
    # act
    response = self.exp.mod_mra(enabled="On")

    # assert
    self.assertDictEqual({'Message': 'Operation was successful'}, response)

  @responses.activate
  def test_new_cucmserver_timeout(self):
    # arrange
    responses.add(
      responses.POST,
      'https://{address}{path}'.format(
        address=self.test_address,
        path=self.api_cucm),
      json={'Error': 'Timeout or Connection Error'}, status=200)
   
    # act
    response = self.exp.new_cucmserver(publisher="1.1.1.1", axl_username="admin", axl_password="dummy")

    # assert
    # self.assertDictEqual({'Message': 'CommandError: Socket Error: Timeout'}, response) # Occurs if the lib allows EXP to timeout
    self.assertDictEqual({'Error': 'Timeout or Connection Error'}, response)

  @responses.activate
  def test_get_serial(self):

    xml_buffered_reader = io.BufferedReader(io.open("tests/status.xml", "rb"))

    # arrange
    responses.add(
      responses.GET,
      'https://{address}{path}'.format(
        address=self.test_address,
        path=self.api_statusxml),
      content_type="text/xml",
      body=xml_buffered_reader.read(), status=200)

    xml_buffered_reader.close()
   
    # act
    response = self.exp.get_serial()

    # assert
    self.assertDictEqual({'Serial': '017DB2D0'}, response)

  @responses.activate
  def test_get_license_detail(self):

    xml_buffered_reader = io.BufferedReader(io.open("tests/status.xml", "rb"))

    # arrange
    responses.add(
      responses.GET,
      'https://{address}{path}'.format(
        address=self.test_address,
        path=self.api_statusxml),
      content_type="text/xml",
      body=xml_buffered_reader.read(), status=200)

    xml_buffered_reader.close()
   
    # act
    response = self.exp.get_license_detail()

    # assert
    self.assertDictEqual({'collaboration_edge_in_use': '0', 'traversal_in_use': '0', 'traversal_limit': '1', 'non_traversal_in_use': '0', 'non_traversal_limit': '1', 'current_registrations': '0', 'concurrent_calls': 0}, response)

  @responses.activate
  def test_get_version(self):

    xml_buffered_reader = io.BufferedReader(io.open("tests/status.xml", "rb"))

    # arrange
    responses.add(
      responses.GET,
      'https://{address}{path}'.format(
        address=self.test_address,
        path=self.api_statusxml),
      content_type="text/xml",
      body=xml_buffered_reader.read(), status=200)

    xml_buffered_reader.close()
   
    # act
    response = self.exp.get_version()

    # assert
    self.assertDictEqual({'Version': 'X8.11.3'}, response)

  @responses.activate
  def test_new_searchrule(self):
    # arrange
    responses.add(
      responses.POST, 
      'https://{address}{path}'.format(
        address=self.test_address,
        path=self.api_searchrule), 
      json={'Message': 'Successfully created the Search Rule'}, status=201)
   
    # act
    response = self.exp.searchrule.add(Priority="10", Name="test", TargetName="test")
    
    # assert
    self.assertDictEqual({'Message': 'Successfully created the Search Rule'}, response)

if __name__ == '__main__':
  unittest.main()