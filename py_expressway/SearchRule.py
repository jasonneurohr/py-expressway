import json
import requests


class SearchRule:
  def __init__(self, api_session, api_address):
    self.__session = api_session
    self.__session.headers = {"Content-Type": "application/json"}
    self.__address = "https://" + api_address
    self.__timeout = 10

  def add(self, **kwargs):
    """CREATE search rule

    Required:
        Priority
        Name
        TargetName
    """

    if len(kwargs) is 0:
      raise ValueError("Missing required kwargs")

    if "Priority" not in kwargs:
      raise ValueError("Priority is required")

    if "Name" not in kwargs:
      raise ValueError("Name is required")

    if "TargetName" not in kwargs:
      raise ValueError("TargetName is required")

    try:
        response = self.__session.post(
            self.__address + "/api/provisioning/common/searchrule",
            json=kwargs,
            timeout=self.__timeout)

    except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as err:
        raise Exception(err)

    if response.status_code != 201:
      raise Exception("Post /api/provisioning/common/searchrule {}".format(response.status_code))
    return response.json()

  def get(self):
    """READ search rule
    """

    try:
        response = self.__session.get(
            self.__address + "/api/provisioning/common/searchrule",
            timeout=self.__timeout)

    except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as err:
        raise Exception(err)

    return response.json()
