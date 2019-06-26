from datetime import datetime
import requests
import re


class Configuration:
    def __init__(self, api_address, username, password, verify=True):
        self.__session = requests.Session()
        self.__session.headers = {"Content-Type": "application/json"}
        self.__ip = re.sub(string=api_address, pattern="\.", repl="_")
        self.__address = "https://" + api_address
        self.__timeout = 10
        self.__username = username
        self.__password = password
        self.__session.verify = verify

    def __login(self):
        r = self.__session.post(
            url=f"{self.__address}/login",
            data={
                "submitButton": "Login",
                "username": self.__username,
                "password": self.__password,
                "formbutton": "Login",
            },
            headers={
                "Referer": f"{self.__address}/login",
                "Content-Type": "application/x-www-form-urlencoded",
            },
        )

    def backup(self, backup_password="password"):
        self.__login()

        sessionid = ""

        # Load Backup and restore page
        r = self.__session.get(url=f"{self.__address}/backuprestore")

        # Get the sessionid value - required in the POST data to start the backup
        for line in r.text.splitlines():
            if re.search(string=line, pattern="sessionid"):
                line = line.split("/><")
                line = line[0].split("><")
                line = re.sub(string=line[1], pattern='"', repl="")
                sessionid = line.split("value=")[1]
                break

        data = f"sessionid={sessionid}&submitbutton=Create+system+backup+file&backup_password={backup_password}&backup_password_confirm={backup_password}"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        with self.__session.post(
            url=f"{self.__address}/backuprestore",
            data=data,
            headers=headers,
            stream=True,
        ) as r:
            r.raise_for_status()
            timestamp = datetime.utcnow().strftime("%Y_%m_%d__%H_%M_%S")
            filename = f"expressway_{self.__ip}_{timestamp}_backup.tar.gz.enc"

            with open(filename, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
