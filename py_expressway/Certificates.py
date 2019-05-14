import json
import requests
from os.path import join
from tempfile import TemporaryFile, TemporaryDirectory


class Certificates:
    def __init__(self, api_session, api_address):
        self.__session = api_session
        self.__session.headers = {"Content-Type": "application/json"}
        self.__address = "https://" + api_address
        self.__timeout = 10

    def add(self, cert_type: str, cert_pem: str):
        """Adds a certificate to the root trust store
      
        :param cert_pem:
        :return:
        """

        uri = ""

        # Check the certificate type and update the API address
        if cert_type is "root":
            uri = self.__address + "/api/provisioning/certs/root"

        if cert_type is "server":
            uri = self.__address + "/api/provisioning/certs/server"

            # Is there a pending CSR? If no return

        # Write the cert pem str to a file in a temporary directory
        with TemporaryDirectory() as tmp_dir:

            # Define the full path
            cert_file = join(tmp_dir, "cert.txt")

            # Write the cert pem to the file
            with open(file=cert_file, mode="w") as fh:
                fh.write(cert_pem)

            # Open the file
            with open(file=cert_file, mode="rb") as fh:

                # Submit the request to the Expressway API
                try:
                    response = self.__session.post(
                        uri, timeout=self.__timeout, files={"file": fh}
                    )

                except (
                    requests.exceptions.Timeout,
                    requests.exceptions.ConnectionError,
                ) as err:
                    raise Exception(err)

                return response.json()

    def get(self, cert_type: str):
        """Gets all certificate from the root trust store
        """

        uri = ""

        # Check the certificate type and update the API address
        if cert_type is "root":
            uri = self.__address + "/api/provisioning/certs/root"

        if cert_type is "server":
            uri = self.__address + "/api/provisioning/certs/server"

        try:
            response = self.__session.get(
                uri, timeout=self.__timeout
            )

        except (
            requests.exceptions.Timeout,
            requests.exceptions.ConnectionError,
        ) as err:
            raise Exception(err)

        return {"certificate": response.text}

    def get_csr(self):
        """Returns
        """
        try:
            response = self.__session.get(
                self.__address + "/api/provisioning/certs/generate_csr",
                timeout=self.__timeout,
            )

        except (
            requests.exceptions.Timeout,
            requests.exceptions.ConnectionError,
        ) as err:
            raise Exception(err)

        if response.status_code is 404:
            # No current CSR
            return response.json()

        if response.status_code is 200:
            return {"certificate": response.text}

    def add_csr(
        self,
        country: str,
        province: str,
        locality: str,
        organization: str,
        organizational_unit: str,
        additional_fqdns: list = None,
        key_length: int = 4096,
        digest_algorithm: str = "sha256",
        email: str = None,
    ):
        """Generate a new CSR request
        """

        data = {
            "Additional_FQDNS": additional_fqdns or [],
            "Country": country,
            "KeyLength": key_length,
            "DigestAlgorithm": digest_algorithm,
            "Province": province,
            "Locality": locality,
            "Organization": organization,
            "OrganizationalUnit": organizational_unit,
            "Email": email or "",
        }

        try:
            response = self.__session.post(
                self.__address + "/api/provisioning/certs/generate_csr",
                json=data,
                timeout=self.__timeout,
            )

        except (
            requests.exceptions.Timeout,
            requests.exceptions.ConnectionError,
        ) as err:
            raise Exception(err)

        return response.json()
