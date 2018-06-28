import boto3
import glob
import logging
import os
import yaml
import boto3


client = boto3.client('ssm')


def configuration(filename='config.yaml'):
    """Load configuration from config file."""
    logger = logging.getLogger(__name__)

    config = {}
    with open(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', filename)), 'r') as f:
        config = yaml.load(f)
        logger.info('Loaded raw config: {0}'.format(config))

    new_config = {}
    logger.info('Inspecting configuration to see if any ParameterStore lookups are required')
    for (k,v) in config.items():
        key = k
        if isinstance(v, str):
            value = os.path.expandvars(v)
            if k.startswith('parameterstore_'):
                key = k.split('parameterstore_')[-1]
                value = client.get_parameter(Name=value, WithDecryption=True)['Parameter']['Value']
        else:
            value = v
        new_config[key] = value

    return new_config


