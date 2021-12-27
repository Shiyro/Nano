import toml
import logging
import os

EXAMPLE_CONFIG = """###BOTS###
\"token\"=\"\" # the bot's token
\"prefix\"=\"?\" # prefix used to denote commands

###DB###
\"host\"=\"\" #the db address
\"dbname\"=\"\" #the db name
\"user\"=\"\" #the db users
\"password\"=\"\" #the db user password

[hub]
#Options for the voice chat hub
\"hub_category_id\"=\"\" # The category where the vc are going to be created.
\"hub_vc_id\"=\"\" # The hub id.
"""


def load_config(path="./data/config/config.toml"):
    """Loads the config from `path`"""
    if os.path.exists(path) and os.path.isfile(path):
        config = toml.load(path)
        return config
    else:
        with open(path, "w") as config:
            config.write(EXAMPLE_CONFIG)
            logging.warn(
                f"No config file found. Creating a default config file at {path}"
            )
        return load_config(path=path)
