# Copyright (c) 2012-2015, Mark Peek <mark@peek.org>
# All rights reserved.
#
# See LICENSE file for full license.

from . import AWSProperty, AWSObject, Tags
from .validators import boolean, integer, integer_range, positive_integer

VALID_VOLUME_TYPES = ('standard', 'gp2', 'io1')

try:
    from awacs.aws import Policy
    policytypes = (dict, Policy)
except ImportError:
    policytypes = dict,


def validate_volume_type(volume_type):
    """Validate VolumeType for ElasticsearchDomain"""
    if volume_type not in VALID_VOLUME_TYPES:
        raise ValueError("Elasticsearch Domain VolumeType must be one of: %s" %
                         ", ".join(VALID_VOLUME_TYPES))
    return volume_type


class EBSOptions(AWSProperty):
    props = {
        'EBSEnabled': (boolean, False),
        'Iops': (positive_integer, False),
        'VolumeSize': (integer, False),
        'VolumeType': (validate_volume_type, False)
    }

    def validate(self):
        volume_type = self.properties.get('VolumeType')
        iops = self.properties.get('Iops')
        if volume_type == 'io1' and not iops:
            raise ValueError("Must specify Iops if VolumeType is 'io1'.")


class ElasticsearchClusterConfig(AWSProperty):
    props = {
        'DedicatedMasterCount': (integer, False),
        'DedicatedMasterEnabled': (boolean, False),
        'DedicatedMasterType': (str, False),
        'InstanceCount': (integer, False),
        'InstanceType': (str, False),
        'ZoneAwarenessEnabled': (boolean, False)
    }


class EncryptionAtRestOptions(AWSProperty):
    props = {
        'Enabled': (boolean, False),
        'KmsKeyId': (str, False),
    }


class SnapshotOptions(AWSProperty):
    props = {
        'AutomatedSnapshotStartHour': (integer_range(0, 23), False)
    }


class VPCOptions(AWSProperty):
    props = {
        "SecurityGroupIds": ([str], False),
        "SubnetIds": ([str], False)
    }


class Domain(AWSObject):
    resource_type = "AWS::Elasticsearch::Domain"

    props = {
        'AccessPolicies': (policytypes, False),
        'AdvancedOptions': (dict, False),
        'DomainName': (str, False),
        'EBSOptions': (EBSOptions, False),
        'ElasticsearchClusterConfig': (ElasticsearchClusterConfig, False),
        'ElasticsearchVersion': (str, False),
        'EncryptionAtRestOptions': (EncryptionAtRestOptions, False),
        'SnapshotOptions': (SnapshotOptions, False),
        'Tags': ((Tags, list), False),
        'VPCOptions': (VPCOptions, False)
    }


# Backward compatibility
ElasticsearchDomain = Domain