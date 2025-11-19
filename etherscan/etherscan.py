import json
from importlib import resources

import requests

import etherscan
from etherscan.enums.fields_enum import FieldsEnum as fields
from etherscan.enums.chainids_enum import ChainidsEnum as chainids
from etherscan.utils.parsing import ResponseParser as parser


class Etherscan:
    Chain = chainids

    def __new__(cls, api_key: str):
        with resources.path(etherscan, "config.json") as path:
            config_path = str(path)

        return cls.from_config(api_key=api_key, config_path=config_path)

    @staticmethod
    def __load_config(config_path: str) -> dict:
        with open(config_path, "r") as f:
            return json.load(f)

    @staticmethod
    def __run(func, api_key: str):
        def wrapper(*args, **kwargs):
            # Extract chain_id from kwargs, default to Ethereum Mainnet
            chain_id = kwargs.pop('chain_id', chainids.ETHEREUM_MAINNET)

            url = (
                f"{fields.PREFIX}"
                f"{func(*args, **kwargs)}"
                f"{fields.CHAIN_ID}"
                f"{chain_id}"
                f"{fields.API_KEY}"
                f"{api_key}"
            )
            r = requests.get(url, headers={"User-Agent": ""})
            return parser.parse(r)

        return wrapper

    @classmethod
    def from_config(cls, api_key: str, config_path: str):
        config = cls.__load_config(config_path)
        for func, v in config.items():
            if not func.startswith("_"):  # disabled if _
                attr = getattr(getattr(etherscan, v["module"]), func)
                setattr(cls, func, cls.__run(attr, api_key))
        return cls
