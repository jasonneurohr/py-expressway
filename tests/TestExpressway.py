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
        self.api_uczone = (
            "/api/provisioning/controller/zone/unifiedcommunicationstraversal"
        )
        self.api_dns = "/api/provisioning/common/dns/dns"
        self.api_sip = "/api/provisioning/common/protocol/sip/configuration"
        self.api_mra = "/api/provisioning/common/mra"
        self.api_cucm = "/api/provisioning/controller/server/cucm"
        self.api_searchrule = "/api/provisioning/common/searchrule"
        self.api_statusxml = "/status.xml"
        self.api_rootcert = "/api/provisioning/certs/root"
        self.api_servercert = "/api/provisioning/certs/server"
        self.api_gencsr = "/provisioning/certs/generate_csr"

    @responses.activate
    def test_new_neighborzone(self):
        # arrange
        responses.add(
            responses.POST,
            "https://{address}{path}".format(
                address=self.test_address, path=self.api_neighborzone
            ),
            json={"Message": "Successfully created Neighbor zone"},
            status=200,
        )

        # act
        response = self.exp.new_neighborzone(zone_name="test", peer_address=["2.2.2.2"])

        # assert
        self.assertDictEqual(
            {"Message": "Successfully created Neighbor zone"}, response
        )

    @responses.activate
    def test_new_neighborzone_already_exists(self):
        # arrange
        responses.add(
            responses.POST,
            "https://{address}{path}".format(
                address=self.test_address, path=self.api_neighborzone
            ),
            json={"Message": "Neighbor zone name already exists"},
            status=200,
        )

        # act
        response = self.exp.new_neighborzone(zone_name="test", peer_address=["2.2.2.2"])

        # assert
        self.assertDictEqual({"Message": "Neighbor zone name already exists"}, response)

    @responses.activate
    def test_new_uczone_traversalclient_timeout(self):
        # arrange
        responses.add(
            responses.POST,
            "https://{address}{path}".format(
                address=self.test_address, path=self.api_uczone
            ),
            json={"Error": "Timeout or Connection Error"},
            status=200,
        )

        # act
        response = self.exp.new_uczone_traversalclient(
            zone_name="test uc client",
            peer_address=["127.0.0.1"],
            auth_user="ucuser",
            auth_pass="asdf",
            sip_port=7010,
        )

        # assert
        self.assertDictEqual({"Error": "Timeout or Connection Error"}, response)

    @responses.activate
    def test_mod_dns(self):
        # arrange
        responses.add(
            responses.PUT,
            "https://{address}{path}".format(
                address=self.test_address, path=self.api_dns
            ),
            json={"Message": "Operation was successful"},
            status=200,
        )

        # act
        response = self.exp.mod_dns(domain_name="dummy.com", host_name="dummy")

        # assert
        self.assertDictEqual({"Message": "Operation was successful"}, response)

    @responses.activate
    def test_mod_sip(self):
        # arrange
        responses.add(
            responses.PUT,
            "https://{address}{path}".format(
                address=self.test_address, path=self.api_sip
            ),
            json={"Message": "Successfully updated the SIP Configuration"},
            status=200,
        )

        # act
        response = self.exp.mod_sip(tcp_mode="on", sip_mode="on", tcp_port=1234)

        # assert
        self.assertDictEqual(
            {"Message": "Successfully updated the SIP Configuration"}, response
        )

    @responses.activate
    def test_mod_mra(self):
        # arrange
        responses.add(
            responses.PUT,
            "https://{address}{path}".format(
                address=self.test_address, path=self.api_mra
            ),
            json={"Message": "Operation was successful"},
            status=200,
        )

        # act
        response = self.exp.mod_mra(enabled="On")

        # assert
        self.assertDictEqual({"Message": "Operation was successful"}, response)

    @responses.activate
    def test_new_cucmserver_timeout(self):
        # arrange
        responses.add(
            responses.POST,
            "https://{address}{path}".format(
                address=self.test_address, path=self.api_cucm
            ),
            json={"Error": "Timeout or Connection Error"},
            status=200,
        )

        # act
        response = self.exp.new_cucmserver(
            publisher="1.1.1.1", axl_username="admin", axl_password="dummy"
        )

        # assert
        # self.assertDictEqual({'Message': 'CommandError: Socket Error: Timeout'}, response) # Occurs if the lib allows EXP to timeout
        self.assertDictEqual({"Error": "Timeout or Connection Error"}, response)

    @responses.activate
    def test_get_serial(self):

        xml_buffered_reader = io.BufferedReader(io.open("tests/status.xml", "rb"))

        # arrange
        responses.add(
            responses.GET,
            "https://{address}{path}".format(
                address=self.test_address, path=self.api_statusxml
            ),
            content_type="text/xml",
            body=xml_buffered_reader.read(),
            status=200,
        )

        xml_buffered_reader.close()

        # act
        response = self.exp.get_serial()

        # assert
        self.assertDictEqual({"Serial": "017DB2D0"}, response)

    @responses.activate
    def test_get_license_detail(self):

        xml_buffered_reader = io.BufferedReader(io.open("tests/status.xml", "rb"))

        # arrange
        responses.add(
            responses.GET,
            "https://{address}{path}".format(
                address=self.test_address, path=self.api_statusxml
            ),
            content_type="text/xml",
            body=xml_buffered_reader.read(),
            status=200,
        )

        xml_buffered_reader.close()

        # act
        response = self.exp.get_license_detail()

        # assert
        self.assertDictEqual(
            {
                "collaboration_edge_in_use": "0",
                "traversal_in_use": "0",
                "traversal_limit": "1",
                "non_traversal_in_use": "0",
                "non_traversal_limit": "1",
                "current_registrations": "0",
                "concurrent_calls": 0,
            },
            response,
        )

    @responses.activate
    def test_get_version(self):

        xml_buffered_reader = io.BufferedReader(io.open("tests/status.xml", "rb"))

        # arrange
        responses.add(
            responses.GET,
            "https://{address}{path}".format(
                address=self.test_address, path=self.api_statusxml
            ),
            content_type="text/xml",
            body=xml_buffered_reader.read(),
            status=200,
        )

        xml_buffered_reader.close()

        # act
        response = self.exp.get_version()

        # assert
        self.assertDictEqual({"Version": "X8.11.3"}, response)

    @responses.activate
    def test_new_searchrule(self):
        # arrange
        responses.add(
            responses.POST,
            "https://{address}{path}".format(
                address=self.test_address, path=self.api_searchrule
            ),
            json={"Message": "Successfully created the Search Rule"},
            status=201,
        )

        # act
        response = self.exp.searchrule.add(
            Priority="10", Name="test", TargetName="test"
        )

        # assert
        self.assertDictEqual(
            {"Message": "Successfully created the Search Rule"}, response
        )

    @responses.activate
    def test_get_servercert(self):
        # arrange

        cert_pem = """-----BEGIN CERTIFICATE-----
MIIEbDCCA1SgAwIBAgIBATANBgkqhkiG9w0BAQsFADCBtDE6MDgGA1UECgwxVGVt
cG9yYXJ5IENBIGE5YjdiOTRlLTMwZmUtNDAwNC05NjU1LThhOTdkOWUxYmZlNjE6
MDgGA1UECwwxVGVtcG9yYXJ5IENBIGE5YjdiOTRlLTMwZmUtNDAwNC05NjU1LThh
OTdkOWUxYmZlNjE6MDgGA1UEAwwxVGVtcG9yYXJ5IENBIGE5YjdiOTRlLTMwZmUt
NDAwNC05NjU1LThhOTdkOWUxYmZlNjAeFw0xOTA1MTMxMjExMTZaFw0yMDA1MTIx
MjExMTZaMIGaMUMwQQYDVQQKDDpUZW1wb3JhcnkgQ2VydGlmaWNhdGUgNWNlNzZj
MzYtMDMyZC00NDFmLWE5MjctMmUzYjAyMzIwNDUwMUMwQQYDVQQLDDpUZW1wb3Jh
cnkgQ2VydGlmaWNhdGUgNWNlNzZjMzYtMDMyZC00NDFmLWE5MjctMmUzYjAyMzIw
NDUwMQ4wDAYDVQQDDAVjaXNjbzCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoC
ggEBANMUHKvn4AG3xHbe+5Te6ylBnmNnZo/MRgbmg3M+70weWotMyfY8NhGwkd9k
O62074FB82WKeMOnFDRFO0ywF4KrEh/5HjoY13DF+S5kWRImYmvuzeKXUNtllR6A
EztVRVveWyfLej2CGyBj6Plp4Yk6ap5l482w5n8cNLLExiDbZRVzf06v+3DZHiAY
Nkee2squVQFUgMQjXJwl9WW95OmBr5kOkXnfIS6ZWjtA6KlDxW7SbitJRr0f4wsn
fmeq1Bu/4NfTGZOYn5M1zlFhzp6c01PhIEvDRXi74Ps3Wh7nTVY/KwQmMmLRM8NC
KvJZIQIigbkK3i5WFOF4AiBcWVsCAwEAAaOBoDCBnTAJBgNVHRMEAjAAMCQGCWCG
SAGG+EIBDQQXFhVUZW1wb3JhcnkgQ2VydGlmaWNhdGUwHQYDVR0OBBYEFG+2IAAa
bDl+0DEUDKnrpFBgPKoaMB8GA1UdIwQYMBaAFF7AD1419Y7lkB9bT1M5zp9bAE3G
MAsGA1UdDwQEAwIF4DAdBgNVHSUEFjAUBggrBgEFBQcDAQYIKwYBBQUHAwIwDQYJ
KoZIhvcNAQELBQADggEBAGBDoukr7QrPpJX2cvgarCPpamxcEBE1LSBZ1ON4AmQC
G9e+YEeSW1y7Qoq6u/dfwVzt62dTwnPq7GHRNv41Tuc+uRljKJ7Ht1Ku1tJ6xyVx
xfa3Dw8VK0bHB4htQZjnbkB+F4cWRaWBmEY3xLUKBvoyFqjvOzXsXmci6T4fuH1b
8IY9rlNDZOoO+jJ7Itl6djV1JqmSvIe+KRFzgmkiu00gGg5edx+cDCYBzpue+WWb
UVPZ233hfj708Rx3h5LPaGH+EJ2jUvF5KJWq8tM8s3rLVegw0F76dz9lyL4ZLWgP
hlnM5msIT8iiSlJP0yAK5cWyJU6iCA8nMMrVJcC+E/s=
-----END CERTIFICATE-----
"""

        responses.add(
            responses.GET,
            "https://{address}{path}".format(
                address=self.test_address, path=self.api_servercert
            ),
            content_type="text/html",
            body=cert_pem,
            status=200,
        )

        # act
        response = self.exp.certificates.get(cert_type="server")

        # assert
        self.assertDictEqual({"certificate": cert_pem}, response)

    @responses.activate
    def test_add_rootcert(self):
        # arrange

        cert = """-----BEGIN CERTIFICATE-----
MIIDxTCCAq2gAwIBAgIBADANBgkqhkiG9w0BAQsFADCBgzELMAkGA1UEBhMCVVMx
EDAOBgNVBAgTB0FyaXpvbmExEzARBgNVBAcTClNjb3R0c2RhbGUxGjAYBgNVBAoT
EUdvRGFkZHkuY29tLCBJbmMuMTEwLwYDVQQDEyhHbyBEYWRkeSBSb290IENlcnRp
ZmljYXRlIEF1dGhvcml0eSAtIEcyMB4XDTA5MDkwMTAwMDAwMFoXDTM3MTIzMTIz
NTk1OVowgYMxCzAJBgNVBAYTAlVTMRAwDgYDVQQIEwdBcml6b25hMRMwEQYDVQQH
EwpTY290dHNkYWxlMRowGAYDVQQKExFHb0RhZGR5LmNvbSwgSW5jLjExMC8GA1UE
AxMoR28gRGFkZHkgUm9vdCBDZXJ0aWZpY2F0ZSBBdXRob3JpdHkgLSBHMjCCASIw
DQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBAL9xYgjx+lk09xvJGKP3gElY6SKD
E6bFIEMBO4Tx5oVJnyfq9oQbTqC023CYxzIBsQU+B07u9PpPL1kwIuerGVZr4oAH
/PMWdYA5UXvl+TW2dE6pjYIT5LY/qQOD+qK+ihVqf94Lw7YZFAXK6sOoBJQ7Rnwy
DfMAZiLIjWltNowRGLfTshxgtDj6AozO091GB94KPutdfMh8+7ArU6SSYmlRJQVh
GkSBjCypQ5Yj36w6gZoOKcUcqeldHraenjAKOc7xiID7S13MMuyFYkMlNAJWJwGR
tDtwKj9useiciAF9n9T521NtYJ2/LOdYq7hfRvzOxBsDPAnrSTFcaUaz4EcCAwEA
AaNCMEAwDwYDVR0TAQH/BAUwAwEB/zAOBgNVHQ8BAf8EBAMCAQYwHQYDVR0OBBYE
FDqahQcQZyi27/a9BUFuIMGU2g/eMA0GCSqGSIb3DQEBCwUAA4IBAQCZ21151fmX
WWcDYfF+OwYxdS2hII5PZYe096acvNjpL9DbWu7PdIxztDhC2gV7+AJ1uP2lsdeu
9tfeE8tTEH6KRtGX+rcuKxGrkLAngPnon1rpN5+r5N9ss4UXnT3ZJE95kTXWXwTr
gIOrmgIttRD02JDHBHNA7XIloKmf7J6raBKZV8aPEjoJpL1E/QYVN8Gb5DKj7Tjo
2GTzLH4U/ALqn83/B2gX2yKQOC16jdFU8WnjXzPKej17CuPKf1855eJ1usV2GDPO
LPAvTK33sefOT6jEm0pUBsV/fdUID+Ic/n4XuKxe9tQWskMJDE32p2u0mYRlynqI
4uJEvlz36hz1
-----END CERTIFICATE-----"""

        responses.add(
            responses.POST,
            "https://{address}{path}".format(
                address=self.test_address, path=self.api_rootcert
            ),
            json={"Message": "Root Certificate updated."},
            status=200,
        )

        # act
        response = self.exp.certificates.add(cert_pem=cert, cert_type="root")

        # assert
        self.assertDictEqual({"Message": "Root Certificate updated."}, response)

    @responses.activate
    def test_get_rootcert(self):
        # arrange

        cert_pem = """-----BEGIN CERTIFICATE-----
MIIEPTCCAyWgAwIBAgIJAJlc6NPlZZgQMA0GCSqGSIb3DQEBCwUAMIG0MTowOAYD
VQQKDDFUZW1wb3JhcnkgQ0EgYTliN2I5NGUtMzBmZS00MDA0LTk2NTUtOGE5N2Q5
ZTFiZmU2MTowOAYDVQQLDDFUZW1wb3JhcnkgQ0EgYTliN2I5NGUtMzBmZS00MDA0
LTk2NTUtOGE5N2Q5ZTFiZmU2MTowOAYDVQQDDDFUZW1wb3JhcnkgQ0EgYTliN2I5
NGUtMzBmZS00MDA0LTk2NTUtOGE5N2Q5ZTFiZmU2MB4XDTE5MDUxMzEyMTExNloX
DTI0MDUxMTEyMTExNlowgbQxOjA4BgNVBAoMMVRlbXBvcmFyeSBDQSBhOWI3Yjk0
ZS0zMGZlLTQwMDQtOTY1NS04YTk3ZDllMWJmZTYxOjA4BgNVBAsMMVRlbXBvcmFy
eSBDQSBhOWI3Yjk0ZS0zMGZlLTQwMDQtOTY1NS04YTk3ZDllMWJmZTYxOjA4BgNV
BAMMMVRlbXBvcmFyeSBDQSBhOWI3Yjk0ZS0zMGZlLTQwMDQtOTY1NS04YTk3ZDll
MWJmZTYwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQChtebYHz4v2fiK
NcWct6nWAs3Mr+xA5mvgH/6T7Lbrlz4bOCDmS25nMwNBu9T5ebb4Q8kDv4QqqPAE
+EhIb0Dm05YMOsV3axTFaDWUmslAwIBU35FyBgubC/Xi6wf8gWuTlZQ/nI/f/dKD
D8ujdQD4O49+dP+XdOf83tCN45eO/UsVgiBy2dTL0FTuDpRC0wezZ28kiXhTXe/q
Vxjijk/ENkJU1PhKOU/6HJ3j8cZJG6IpHw96Z2Qw0ZU9/7d5a/zD3uu7YUCxsjYs
2MCL7Odhr7NdG1FSfy6nJiGqduZI0FHW1b7k3zUdf+qOOMxvv3Q4l6Q0dIE6zRm2
YMwL9toXAgMBAAGjUDBOMB0GA1UdDgQWBBRewA9eNfWO5ZAfW09TOc6fWwBNxjAf
BgNVHSMEGDAWgBRewA9eNfWO5ZAfW09TOc6fWwBNxjAMBgNVHRMEBTADAQH/MA0G
CSqGSIb3DQEBCwUAA4IBAQBy/XLPOuiTbQQ2xIzne1JpD8MANpuZ54/svJwMGPQt
c2Cu9YnpQVC3oDlVjTNVMYxoKqsgrOlnbPMupFIdgPYCVG2jKOdI4Dnv6gS5VLCw
aAZr/iUdzVYLnW6tXTp1h90ff5qKX1vTi4ReAvNiImtqUL0CpwucfjsSW/JKpqlU
T3H2HzGL3ighSlJr7734cjpMGa1+j4CfF6ySjAoiPowzgyFTpUjzIBMMYTZufL4m
cxgJ5rAeLRzKUnpxKKIBju7qnRAuLeB6AzyHKasmMB5BJcdUBnj7pGKVjD7nDgS2
4C6+uj5VCMhwozro/mkD4+yXivLferaCTefGDaY83XFs
-----END CERTIFICATE-----
-----BEGIN CERTIFICATE-----
MIIDxTCCAq2gAwIBAgIBADANBgkqhkiG9w0BAQsFADCBgzELMAkGA1UEBhMCVVMx
EDAOBgNVBAgTB0FyaXpvbmExEzARBgNVBAcTClNjb3R0c2RhbGUxGjAYBgNVBAoT
EUdvRGFkZHkuY29tLCBJbmMuMTEwLwYDVQQDEyhHbyBEYWRkeSBSb290IENlcnRp
ZmljYXRlIEF1dGhvcml0eSAtIEcyMB4XDTA5MDkwMTAwMDAwMFoXDTM3MTIzMTIz
NTk1OVowgYMxCzAJBgNVBAYTAlVTMRAwDgYDVQQIEwdBcml6b25hMRMwEQYDVQQH
EwpTY290dHNkYWxlMRowGAYDVQQKExFHb0RhZGR5LmNvbSwgSW5jLjExMC8GA1UE
AxMoR28gRGFkZHkgUm9vdCBDZXJ0aWZpY2F0ZSBBdXRob3JpdHkgLSBHMjCCASIw
DQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBAL9xYgjx+lk09xvJGKP3gElY6SKD
E6bFIEMBO4Tx5oVJnyfq9oQbTqC023CYxzIBsQU+B07u9PpPL1kwIuerGVZr4oAH
/PMWdYA5UXvl+TW2dE6pjYIT5LY/qQOD+qK+ihVqf94Lw7YZFAXK6sOoBJQ7Rnwy
DfMAZiLIjWltNowRGLfTshxgtDj6AozO091GB94KPutdfMh8+7ArU6SSYmlRJQVh
GkSBjCypQ5Yj36w6gZoOKcUcqeldHraenjAKOc7xiID7S13MMuyFYkMlNAJWJwGR
tDtwKj9useiciAF9n9T521NtYJ2/LOdYq7hfRvzOxBsDPAnrSTFcaUaz4EcCAwEA
AaNCMEAwDwYDVR0TAQH/BAUwAwEB/zAOBgNVHQ8BAf8EBAMCAQYwHQYDVR0OBBYE
FDqahQcQZyi27/a9BUFuIMGU2g/eMA0GCSqGSIb3DQEBCwUAA4IBAQCZ21151fmX
WWcDYfF+OwYxdS2hII5PZYe096acvNjpL9DbWu7PdIxztDhC2gV7+AJ1uP2lsdeu
9tfeE8tTEH6KRtGX+rcuKxGrkLAngPnon1rpN5+r5N9ss4UXnT3ZJE95kTXWXwTr
gIOrmgIttRD02JDHBHNA7XIloKmf7J6raBKZV8aPEjoJpL1E/QYVN8Gb5DKj7Tjo
2GTzLH4U/ALqn83/B2gX2yKQOC16jdFU8WnjXzPKej17CuPKf1855eJ1usV2GDPO
LPAvTK33sefOT6jEm0pUBsV/fdUID+Ic/n4XuKxe9tQWskMJDE32p2u0mYRlynqI
4uJEvlz36hz1
-----END CERTIFICATE-----"""

        responses.add(
            responses.GET,
            "https://{address}{path}".format(
                address=self.test_address, path=self.api_rootcert
            ),
            content_type="text/html",
            body=cert_pem,
            status=200,
        )

        # act
        response = self.exp.certificates.get(cert_type="root")

        # assert
        self.assertDictEqual({"certificate": cert_pem}, response)

    @responses.activate
    def test_add_servercert(self):
        # arrange

        cert = """-----BEGIN CERTIFICATE-----
MIIEbDCCA1SgAwIBAgIBATANBgkqhkiG9w0BAQsFADCBtDE6MDgGA1UECgwxVGVt
cG9yYXJ5IENBIGE5YjdiOTRlLTMwZmUtNDAwNC05NjU1LThhOTdkOWUxYmZlNjE6
MDgGA1UECwwxVGVtcG9yYXJ5IENBIGE5YjdiOTRlLTMwZmUtNDAwNC05NjU1LThh
OTdkOWUxYmZlNjE6MDgGA1UEAwwxVGVtcG9yYXJ5IENBIGE5YjdiOTRlLTMwZmUt
NDAwNC05NjU1LThhOTdkOWUxYmZlNjAeFw0xOTA1MTMxMjExMTZaFw0yMDA1MTIx
MjExMTZaMIGaMUMwQQYDVQQKDDpUZW1wb3JhcnkgQ2VydGlmaWNhdGUgNWNlNzZj
MzYtMDMyZC00NDFmLWE5MjctMmUzYjAyMzIwNDUwMUMwQQYDVQQLDDpUZW1wb3Jh
cnkgQ2VydGlmaWNhdGUgNWNlNzZjMzYtMDMyZC00NDFmLWE5MjctMmUzYjAyMzIw
NDUwMQ4wDAYDVQQDDAVjaXNjbzCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoC
ggEBANMUHKvn4AG3xHbe+5Te6ylBnmNnZo/MRgbmg3M+70weWotMyfY8NhGwkd9k
O62074FB82WKeMOnFDRFO0ywF4KrEh/5HjoY13DF+S5kWRImYmvuzeKXUNtllR6A
EztVRVveWyfLej2CGyBj6Plp4Yk6ap5l482w5n8cNLLExiDbZRVzf06v+3DZHiAY
Nkee2squVQFUgMQjXJwl9WW95OmBr5kOkXnfIS6ZWjtA6KlDxW7SbitJRr0f4wsn
fmeq1Bu/4NfTGZOYn5M1zlFhzp6c01PhIEvDRXi74Ps3Wh7nTVY/KwQmMmLRM8NC
KvJZIQIigbkK3i5WFOF4AiBcWVsCAwEAAaOBoDCBnTAJBgNVHRMEAjAAMCQGCWCG
SAGG+EIBDQQXFhVUZW1wb3JhcnkgQ2VydGlmaWNhdGUwHQYDVR0OBBYEFG+2IAAa
bDl+0DEUDKnrpFBgPKoaMB8GA1UdIwQYMBaAFF7AD1419Y7lkB9bT1M5zp9bAE3G
MAsGA1UdDwQEAwIF4DAdBgNVHSUEFjAUBggrBgEFBQcDAQYIKwYBBQUHAwIwDQYJ
KoZIhvcNAQELBQADggEBAGBDoukr7QrPpJX2cvgarCPpamxcEBE1LSBZ1ON4AmQC
G9e+YEeSW1y7Qoq6u/dfwVzt62dTwnPq7GHRNv41Tuc+uRljKJ7Ht1Ku1tJ6xyVx
xfa3Dw8VK0bHB4htQZjnbkB+F4cWRaWBmEY3xLUKBvoyFqjvOzXsXmci6T4fuH1b
8IY9rlNDZOoO+jJ7Itl6djV1JqmSvIe+KRFzgmkiu00gGg5edx+cDCYBzpue+WWb
UVPZ233hfj708Rx3h5LPaGH+EJ2jUvF5KJWq8tM8s3rLVegw0F76dz9lyL4ZLWgP
hlnM5msIT8iiSlJP0yAK5cWyJU6iCA8nMMrVJcC+E/s=
-----END CERTIFICATE-----"""

        responses.add(
            responses.POST,
            "https://{address}{path}".format(
                address=self.test_address, path=self.api_servercert
            ),
            json={"Message": "OK"},
            status=200,
        )

        # act
        response = self.exp.certificates.add(cert_pem=cert, cert_type="server")

        # assert
        self.assertDictEqual({"Message": "OK"}, response)

        # Message will be "Message": "Bad Request" if there is a problem

    @responses.activate
    def test_add_csr(self):
        # if existing then {"Message": "Conflict"}
        raise NotImplementedError

if __name__ == "__main__":
    unittest.main()

