# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the License);
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an AS IS BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Shared classes for use in objects describing ontology components.

Classes representing ontology components parsed from files should use these.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import re
import enum
import typing

# Holds the root path to the ontology and relative path to a file from the root
PathParts = typing.NamedTuple('PathParts', [('root', str),
                                            ('relative_path', str)])

GOOGLE3_REGEX = re.compile(r'^.*google3/(.*$)')
# Isolates the first segment of a typename, typically the equipment class
EQUIPMENT_CLASS_REGEX = re.compile(r'^(.*/)?([a-zA-Z]+)(_.*)*$')
GLOBAL_NAMESPACE = ''

AUTOGENERATED_TYPES = frozenset([
    'AUTOGENERATED_NETWORK_DEVICE', '/AUTOGENERATED_NETWORK_DEVICE',
    'HVAC/AUTOGENERATED_NETWORK_DEVICE'
])

DEPRECATED_TYPES = frozenset([
    'DEPRECATED', '/DEPRECATED', 'HVAC/DEPRECATED', 'INCOMPLETE', '/INCOMPLETE',
    'HVAC/INCOMPLETE'
])


class ComponentType(enum.Enum):
  """Possible component types for a folder to contain."""
  SUBFIELD = 1
  MULTI_STATE = 2
  FIELD = 3
  ENTITY_TYPE = 4
  UNIT = 5
  CONNECTION = 6


SUBFOLDER_NAMES = {
    ComponentType.SUBFIELD: 'subfields',
    ComponentType.MULTI_STATE: 'states',
    ComponentType.FIELD: 'fields',
    ComponentType.ENTITY_TYPE: 'entity_types',
    ComponentType.UNIT: 'units',
    ComponentType.CONNECTION: 'connections',
}


def HasAutogeneratedType(parent_names):
  """True if list contains an AUTOGNERATED_NETWORK_DEVICE type name.

  Args:
    parent_names: a list of parent names from an entity. qualified or not
  """
  return AUTOGENERATED_TYPES.intersection(parent_names)


def HasDeprecatedType(parent_names):
  """True if list contains a DEPRECATED or INCOMPLETE type name.

  Args:
    parent_names: a list of parent names from an entity. qualified or not
  """
  return DEPRECATED_TYPES.intersection(parent_names)


def GetEquipmentClass(typename):
  """Parses out the equipment class from a typename.

  Args:
    typename: a relative or fully qualified typename

  Returns:
    The equipment class string or None
  """
  p_match = EQUIPMENT_CLASS_REGEX.match(typename)
  if p_match:
    return p_match.group(2)
  return None


def GetGoogle3RelativePath(path):
  """Parses out google3 local path from an absolute path.

  Args:
    path: a path to a directory in google3

  Returns:
    the relative path to google3 with no leading / or None
  """

  m = GOOGLE3_REGEX.match(path)
  if m is not None:
    return m.group(1)
  return None