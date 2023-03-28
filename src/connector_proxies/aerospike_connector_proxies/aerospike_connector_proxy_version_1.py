from .base_aerospike_connector_proxy import (
    BaseAerospikeConnectorProxy,
    BaseAerospikeConnectorProxyConfig
)
from typing import List, Dict, Tuple
from logger import SingletonLogger
import aerospike
import json


class AerospikeConnectorProxyVersion1(BaseAerospikeConnectorProxy):
    """
    Class for getting Aerospike Client version 1
    Check client status via is_connected() method
    """
    def __init__(
            self, hosts: List[str], policies: Dict
    ):
        """
        Init method
        :param hosts: list of Aerospike hosts (IP:port)
        :param policies: policies while connect to Aerospike
        """
        self.hosts = hosts
        self.policies = policies
        super().__init__()

    @property
    def hosts(self) -> List[str]:
        return self._hosts

    @hosts.setter
    def hosts(self, hosts: List[str]):
        assert isinstance(hosts, list)
        assert all(map(lambda x: isinstance(x, str), hosts))
        self._hosts: List[str] = hosts

    @property
    def policies(self) -> Dict:
        return self._policies

    @policies.setter
    def policies(self, policies: Dict):
        assert isinstance(policies, dict)
        self._policies: Dict = policies

    def _get_parsed_hosts(self) -> List[Tuple[str, int]]:
        """
        Convert hosts from a string (IP:port) to tuple(IP, port)
        :result: list of (IP, port) Tuple
        """
        parsed_hosts: List[Tuple[str, int]] = []
        for host in self.hosts:
            ip, port = host.split(":")
            parsed_hosts.append((ip, int(port)))
        return parsed_hosts

    def _create_client(self):
        """
        Set value to self._client
        :return: None
        """
        try:
            parsed_hosts: List[Tuple[str, int]] = self._get_parsed_hosts()
            self._client = aerospike.client({
                "hosts": parsed_hosts,
                "policies": self.policies
            }).connect()
        except:
            SingletonLogger.get_instance().exception(
                "Exception while create Aerospike client"
            )
            self._client = None

    def _check_client_status(self) -> bool:
        """
        Check status of Aerospike client
        :return: True if healthy, else False
        """
        if self._client is None:
            # No current client
            return False
        try:
            return self._client.is_connected()
        except:
            SingletonLogger.get_instance().exception(
                "Exception while checking Aerospike Client status"
            )
            return False


class AerospikeConnectorProxyVersion1Config(BaseAerospikeConnectorProxyConfig):
    """
    Config class for getting Aerospike Client version 1
    Check client status via is_connected() method
    """
    def __init__(
            self, hosts: List[str], policies: Dict
    ):
        """
        Init method
        :param hosts: list of Aerospike hosts (IP:port)
        :param policies: policies while connect to Aerospike
        """
        super().__init__()
        self.hosts = hosts
        self.policies = policies

    @property
    def hosts(self) -> List[str]:
        return self._hosts

    @hosts.setter
    def hosts(self, hosts: List[str]):
        assert isinstance(hosts, list)
        assert all(map(lambda x: isinstance(x, str), hosts))
        self._hosts: List[str] = hosts

    @property
    def policies(self) -> Dict:
        return self._policies

    @policies.setter
    def policies(self, policies: Dict):
        assert isinstance(policies, dict)
        self._policies: Dict = policies

    def __str__(self):
        return f"""AerospikeConnectorProxyVersion1Config
                   hosts: {';'.join(self.hosts)}
                   policies: {json.dumps(self.policies)}
                """
