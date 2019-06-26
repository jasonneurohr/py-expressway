import json
import requests
import datetime
from py_expressway import SearchRule, Certificates, Configuration

from lxml import etree

class Expressway:

    def __init__(self, address, username, password, verify=True):
        self.__address = str(address)
        self.__username = str(username)
        self.__password = str(password)
        self.__session = requests.session()
        self.__session.auth = self.get_username(), self.get_password()
        self.__url = "https://" + address
        # Supress requests warnings
        requests.packages.urllib3.disable_warnings()

        self.__session.verify = verify
        self.searchrule = SearchRule.SearchRule(self.__session, self.__address)
        self.certificates = Certificates.Certificates(self.__session, self.__address)
        self.configuration = Configuration.Configuration(self.__address, self.__username, self.__password, verify)
    
    def __str__(self):
        return json.dumps({
            "address": self.__address, 
            "username": self.__username, 
            "password": self.__password
        })
    
    def get_address(self):
        return self.__address

    def set_address(self, address):
        self.__address = str(address)

    def get_username(self):
        return self.__username

    def set_username(self, username):
        self.__username = str(username)

    def get_password(self):
        return self.__password

    def set_password(self, password):
        self.__password = password
    
    def end_session(self):
        self.__session.close()

    def __get_req(self, url):
        try:
            response = self.__session.get(
                url,
                verify=False,
                timeout=5)

        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as err:
            raise

        return response

    def __post_req(self, url, properties=None):
        try:
            response = self.__session.post(
                url,
                verify=False,
                data=json.dumps(properties),
                headers={"Content-Type":"application/json"},
                timeout=10)

        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as err:
            raise

        return response

    def __put_req(self, url, properties=None):
        try:
            response = self.__session.put(
                url,
                verify=False,
                data=json.dumps(properties),
                headers={"Content-Type":"application/json"},
                timeout=5)

        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as err:
            print(err)
            raise

        return response
    
    def __delete_req(self, url, properties=None):
        try:
            response = self.__session.delete(
                url,
                verify=False,
                data=properties,
                timeout=5)

        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as err:
            print(err)
            raise

        return response
    
    def get_dns(self):
        """READ DNS configuration
        """

        url = "https://" + self.__address + "/api/provisioning/common/dns/dns"
        
        return self.__get_req(url).text

    def mod_dns(self, domain_name=None, host_name=None, properties=None):
        """UPDATE DNS configuration

        DNSRequestsPortRange
        DNSRequestsPortRangeEnd
        DNSRequestsPortRangeStart
        DomainName
        SystemHostName

        Args:
            properties (dict): Dictionary of properties

        Returns:
            str: The API response string
        """

        data = {
            "DomainName": domain_name,
            "SystemHostName": host_name
        }

        url = "https://" + self.__address + "/api/provisioning/common/dns/dns"
        return self.__put_req(url, data).json()

    def new_dnsserver(self):
        #TODO : API doesn't appear to work correctly
        """CREATE a new DNS server
        """
        data=None
        url = "https://" + self.__address + "/api/provisioning/common/dns/dnsserver"
        return self.__post_req(url, data).text

    def get_dnsserver(self, properties=None):
        """READ DNS server configuration
        """

        url = "https://" + self.__address + "/api/provisioning/common/dns/dnsserver"
        self.__get_req(url)

    def new_domain(self, domain_name=None, edge_xmpp=None, sip=None, xmpp_federation=None,
        edge_sip=None):
        """CREATE domain

        Args:
            domain_name (str): The domain name
            edge_xmpp (bool): Edge XMPP on/off
            sip (bool): Sip on/off
            xmpp_federation (bool): XMPP federation on/off
            edge_sip (bool): Edge SIP on/off
        """

        data = {
            "Name": domain_name,
            "EdgeXmpp": edge_xmpp,
            "Sip": sip,
            "XmppFederation": xmpp_federation,
            "EdgeSip": edge_sip
        }

        new_dict = dict()

        for k,v in data.items():
            if (v is not None):
                new_dict[k] = v

        url = "https://" + self.__address + "/api/provisioning/common/domain"
        self.__post_req(url, new_dict)

    def get_domain(self, properties=None):
        """READ DNS domain
        """

        url = "https://" + self.__address + "/api/provisioning/common/dns/domain"
        self.__get_req(url)

    def mod_mra(self, enabled="Off", sso="Off"):
        """UPDATE MRA configuration

        Args:
            enabled (str): Turn MRA Off or On
            sso (str): Turn SSO Off or On
        """

        data = dict(
            Enabled = enabled,
            SSO = sso
        )

        url = "https://" + self.__address + "/api/provisioning/common/mra"
        return self.__put_req(url, data).json()

    def get_mra(self):
        """READ MRA configuration
        """

        url = "https://" + self.__address + "/api/provisioning/common/mra"
        self.__get_req(url)

    def mod_sip(self, sip_mode=None, tcp_mode=None, tcp_port=None, **kwargs):
        """UPDATE SIP configuration
        """

        data = dict(
            SipMode = sip_mode,
            TcpMode = tcp_mode,
            TcpPort = tcp_port
        )

        new_dict = dict()

        for k,v in data.items():
            if (v is not None):
                new_dict[k] = v

        if kwargs is not None:
            new_dict.update(kwargs)

        url = "https://" + self.__address + "/api/provisioning/common/protocol/sip/configuration"
        
        return self.__put_req(url, new_dict).json()

    def get_sip(self):
        """READ SIP configuration
        """

        url = "https://" + self.__address + "/api/provisioning/common/protocol/sip"
        self.__get_req(url)

    def mod_qos(self, properties=None):
        """UPDATE QoS configuration
        """

        url = "https://" + self.__address + "/api/provisioning/common/qos"
        self.__put_req(url, json.dumps(properties))

    def get_qos(self):
        """READ QoS configuration
        """

        url = "https://" + self.__address + "/api/provisioning/common/qos"
        self.__get_req(url)

    # def new_searchrule(self, properties=None):
    #     """CREATE search rule

    #     Required:
    #         Priority
    #         Name
    #         TargetName
    #     """

    #     url = "https://" + self.__address + "/api/provisioning/common/searchrule"
    #     return self.__post_req(url, json.dumps(properties)).text

    # def get_searchrule(self):
    #     """READ search rule
    #     """

    #     url = "https://" + self.__address + "/api/provisioning/common/searchrule"
    #     self.__get_req(url)

    def mod_searchrule(self, properties=None):
        """UPDATE search rule
        """

        url = "https://" + self.__address + "/api/provisioning/common/searchrule"
        self.__put_req(url, json.dumps(properties))
    
    def del_searchrule(self, properties=None):
        """DELETE search rule
        """

        url = "https://" + self.__address + "/api/provisioning/common/searchrule"
        self.__delete_req(url, properties)

    def get_ntpserver(self):
        """READ NTP server configuration
        """

        url = "https://" + self.__address + "/api/provisioning/common/time/ntpserver"
        self.__get_req(url)

    def new_ntpserver(self, properties=None):
        """CREATE NTP server
        """

        url = "https://" + self.__address + "/api/provisioning/common/time/ntpserver"
        self.__post_req(url, json.dumps(properties))
    
    def mod_ntpserver(self, properties=None):
        """UPDATE NTP server
        """

        url = "https://" + self.__address + "/api/provisioning/common/time/ntpserver"
        self.__put_req(url, properties)

    def del_ntpserver(self, properties=None):
        """DELETE NTP server
        """

        url = "https://" + self.__address + "/api/provisioning/common/time/ntpserver"
        self.__delete_req(url, properties)
    
    def get_ntpstatus(self):
        """READ NTP status
        """

        url = "https://" + self.__address + "/api/provisioning/common/time/status"
        self.__get_req(url)

    def get_timezone(self):
        """READ timezone configuration
        """

        url = "https://" + self.__address + "/api/provisioning/common/time/timezone"
        self.__get_req(url)

    def mod_timezone(self, properties=None):
        """UPDATE timezone configuration
        """

        url = "https://" + self.__address + "/api/provisioning/common/time/timezone"
        self.__put_req(url, properties)

    def get_transform(self):
        """READ transform
        """

        url = "https://" + self.__address + "/api/provisioning/common/transform"
        self.__get_req(url)

    def new_transform(self, properties=None):
        """CREATE transform
        """

        url = "https://" + self.__address + "/api/provisioning/common/transform"
        self.__post_req(url, properties)

    def mod_transform(self, properties=None):
        """UPDATE transform
        """

        url = "https://" + self.__address + "/api/provisioning/common/transform"
        self.__put_req(url, properties)

    def del_transform(self, properties=None):
        """DELETE transform
        """

        url = "https://" + self.__address + "/api/provisioning/common/transform"
        self.__delete_req(url, properties)

    def get_neighborzone(self):
        """READ neighorzone
        """

        url = "https://" + self.__address + "/api/provisioning/common/zone/neighborzone"
        self.__get_req(url)

    def new_neighborzone(self, zone_name=None, peer_address=None, **kwargs):
        """CREATE neighborzone

        Args:
            zone_name (str): name of the zone
            peer_address (list): list of peer addresses preferably FQDN's
        """

        if (zone_name is None or peer_address is None):
            return dict("Error", "Missing name or peerAddress arguments")

        data = {
            "Name": zone_name,
            "PeerAddress": peer_address
        }

        url = "https://" + self.__address + "/api/provisioning/common/zone/neighborzone"
        response = self.__post_req(url, data)
        return(response.json())
    
    def mod_neighborzone(self, properties=None):
        """UPDATE neighborzone
        """

        url = "https://" + self.__address + "/api/provisioning/common/zone/neighborzone"
        self.__put_req(url, properties)

    def del_neighborzone(self, properties=None):
        """DELETE neighborzone
        """

        url = "https://" + self.__address + "/api/provisioning/common/zone/neighborzone"
        self.__delete_req(url, properties)

    def get_cucmserver(self):
        """GET CUCM server configuration
        """

        url = "https://" + self.__address + "/api/provisioning/controller/server/cucm"
        self.__get_req(url)

    def new_cucmserver(self, publisher=None, axl_username=None, axl_password=None, properties=None):
        """CREATE CUCM server configuration

        Args:
            publisher: CUCM publisher FQDN
            axl_username: CUCM AXL service account
            axl_password: CCUCM AXL service account password
        """

        data = dict(
            Publisher = publisher,
            AxlUsername = axl_username,
            AxlPassword = axl_password
        )

        new_dict = dict()

        for k,v in data.items():
            if (v is not None):
                new_dict[k] = v

        if properties is not None:
            new_dict.update(properties)


        url = "https://" + self.__address + "/api/provisioning/controller/server/cucm"
        try:
            return self.__post_req(url, data).json()
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as err:
            return {"Error": "Timeout or Connection Error"}
            
    def del_cucmserver(self, properties=None):
        """DELETE CUCM server configuration
        """

        url = "https://" + self.__address + "/api/provisioning/controller/server/cucm"
        self.__delete_req(url, properties)

    def get_zone_traversalclient(self):
        """READ traversalclient zone
        """

        url = "https://" + self.__address + "/api/provisioning/controller/zone/traversalclient"
        self.__get_req(url)

    def new_zone_traversalclient(self, properties=None):
        """CREATE traversalclient zone
        """

        url = "https://" + self.__address + "/api/provisioning/controller/zone/traversalclient"
        self.__post_req(url, properties)

    def mod_zone_traversalclient(self, properties=None):
        """UPDATE traversalclient zone
        """

        url = "https://" + self.__address + "/api/provisioning/controller/zone/traversalclient"
        self.__put_req(url, json.dumps(properties))

    def del_zone_traversalclient(self, properties=None):
        """DELETE traversaclient zone
        """

        url = "https://" + self.__address + "/api/provisioning/controller/zone/traversalclient"
        self.__delete_req(url, properties)

    def get_turn(self):
        """READ TURN configuration
        """

        url = "https://" + self.__address + "/api/provisioning/edge/traversal/turn"
        self.__get_req(url)

    def mod_turn(self, properties=None):
        """UPDATE TURN configuration
        """

        url = "https://" + self.__address + "/api/provisioning/edge/traversal/turn"
        self.__put_req(url, properties)

    def get_zone_traversalserver(self):
        """READ traversalserver zone configuration
        """

        url = "https://" + self.__address + "/api/provisioning/edge/zone/traversalserver"
        self.__get_req(url)

    def new_zone_traversalserver(self, properties=None):
        """CREATE traversalserver zone
        """

        url = "https://" + self.__address + "/api/provisioning/edge/zone/traversalserver"
        return self.__post_req(url, properties).json()

    def mod_zone_traversalserver(self, properties=None):
        """UPDATE traversalserver zone configuration
        """

        url = "https://" + self.__address + "/api/provisioning/edge/zone/traversalserver"
        self.__put_req(url, properties)

    def del_zone_traversalserver(self, properties=None):
        """DELETE traversalserver zone
        """

        url = "https://" + self.__address + "/api/provisioning/edge/zone/traversalserver"
        self.__delete_req(url, properties)

    def get_uczone_traversalclient(self):
        """READ traversalclient zone
        """

        url = "https://" + self.__address + "/api/provisioning/controller/zone/unifiedcommunicationstraversal"
        self.__get_req(url)

    def new_uczone_traversalclient(self, zone_name=None, peer_address=None,
        auth_user=None, auth_pass=None, accept_proxy_reg=False, sip_port=None, **kwargs):
        """CREATE traversalclient zone

        Args:
            zone_name (str): name of the zone
            peer_address (list): list of peer addresses preferably FQDN's
            auth_user (str): zone auth user
            auth_pass (str): zone auth pass
        """

        if (zone_name is None or peer_address is None):
            return dict("Error", "Missing name or peerAddress arguments")

        if (accept_proxy_reg):
            accept_proxy_reg = "Allow"
        else:
            accept_proxy_reg = "Deny"

        data = {
            "Name": zone_name,
            "PeerAddress": peer_address,
            "AuthenticationUserName": auth_user,
            "AuthenticationPassword": auth_pass,
            "AcceptProxiedRegistrations": accept_proxy_reg,
            "SIPPort": sip_port
        }

        data.update(kwargs)

        url = "https://" + self.__address + "/api/provisioning/controller/zone/unifiedcommunicationstraversal"

        try:
            return self.__post_req(url, data).json()
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as err:
            return json.dumps({"Error": "Timeout or Connection Error"})

    def mod_uczone_traversalclient(self, properties=None):
        """UPDATE traversalclient zone
        """

        url = "https://" + self.__address + "/api/provisioning/controller/zone/unifiedcommunicationstraversal"
        self.__put_req(url, json.dumps(properties))

    def del_uczone_traversalclient(self, properties=None):
        """DELETE traversaclient zone
        """

        url = "https://" + self.__address + "/api/provisioning/controller/zone/unifiedcommunicationstraversal"
        self.__delete_req(url, properties)

    def get_optionkey(self):
        """READ option keys
        """

        url = "https://" + self.__address + "/api/provisioning/optionkey"
        self.__get_req(url)

    def new_optionkey(self, properties=None):
        """CREATE option key
        """

        url = "https://" + self.__address + "/api/provisioning/optionkey"
        self.__post_req(url, properties)

    def del_optionkey(self, properties=None):
        """DELETE option key
        """

        url = "https://" + self.__address + "/api/provisioning/optionkey"
        self.__delete_req(url, properties)

    def get_statusxml(self):
        url = "https://" + self.__address + "/status.xml"

        try:
            return self.__get_req(url)
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as err:
            return json.dumps({"Error": "Timeout or Connection Error"})
    
    def get_serial(self):
        ns = {'ns': 'http://www.tandberg.no/XML/CUIL/1.0'}

        status_xml = etree.fromstring(self.get_statusxml().text)

        return {"Serial": status_xml.find(
            "ns:SystemUnit[@item='1']/ns:Hardware[@item='1']/ns:SerialNumber[@item='1']",
            namespaces=ns).text}
    
    def get_license_detail(self):
        ns = {'ns': 'http://www.tandberg.no/XML/CUIL/1.0'}

        status_xml = etree.fromstring(self.get_statusxml().text)

        current_call_count = 0
        calls = status_xml.find("ns:Calls[@item='1']", namespaces=ns)

        for call in calls:
            current_call_count += 1
        
        data = dict()

        data['collaboration_edge_in_use'] = status_xml.find(
            "ns:ResourceUsage[@item='1']/ns:Calls[@item='1']/ns:CollaborationEdge[@item='1']/ns:Current[@item='1']",
            namespaces=ns).text
        
        # No data point for collaboration edge limit.
        
        data['traversal_in_use'] = status_xml.find(
            "ns:ResourceUsage[@item='1']/ns:Calls[@item='1']/ns:Traversal[@item='1']/ns:Current[@item='1']",
            namespaces=ns).text

        data['traversal_limit'] = status_xml.find(
            "ns:SystemUnit[@item='1']/ns:Software[@item='1']/ns:Configuration[@item='1']/ns:TraversalCalls[@item='1']",
            namespaces=ns).text

        data['non_traversal_in_use'] = status_xml.find(
            "ns:ResourceUsage[@item='1']/ns:Calls[@item='1']/ns:NonTraversal[@item='1']/ns:Current[@item='1']",
            namespaces=ns).text

        data['non_traversal_limit'] = status_xml.find(
            "ns:SystemUnit[@item='1']/ns:Software[@item='1']/ns:Configuration[@item='1']"
            "/ns:NonTraversalCalls[@item='1']",
            namespaces=ns).text

        data['current_registrations'] = status_xml.find(
            "ns:ResourceUsage[@item='1']/ns:Registrations[@item='1']/ns:Current[@item='1']", namespaces=ns).text

        data['concurrent_calls'] = current_call_count

        return data

    def get_version(self):
        ns = {'ns': 'http://www.tandberg.no/XML/CUIL/1.0'}

        status_xml = etree.fromstring(self.get_statusxml().text)

        return {"Version": status_xml.find(
            "ns:SystemUnit[@item='1']/ns:Software[@item='1']/ns:Version[@item='1']",
            namespaces=ns).text}

    def get_uptime(self):
        ns = {'ns': 'http://www.tandberg.no/XML/CUIL/1.0'}

        status_xml = etree.fromstring(self.get_statusxml().text)

        return {"Uptime": status_xml.find(
            "ns:SystemUnit[@item='1']/ns:Uptime[@item='1']",
            namespaces=ns).text}