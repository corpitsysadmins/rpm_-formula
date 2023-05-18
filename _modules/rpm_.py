#! python
'''Extended rpm execution module.
This module implements extra execution actions related to the rpm module.

Version: 0.0.1

TODO:
- everything

Refs:
'''

import logging

import re

LOGGER = logging.getLogger(__name__)

def import_gpg_key(key_file):
	'''Import GPG key
	Import the supplied gpg file (as a path) to the RPM database.
	'''
	
	LOGGER.debug('Importing GPG key to RPM: %s', key_file)
	result = run('--import', key_file)
	return result
	
def list_gpg_keys():
	'''List GPG keys
	Return the list of GPG keys on the RPM database and their descriptions
	'''
	
	LOGGER.debug('Listing imported GPG keys')
	result = run('-q', 'gpg-pubkey', '--qf', "'%{NAME}-%{VERSION}-%{RELEASE}\t%{SUMMARY}\n'")
	return result
	
def remove_gpg_key(key_id):
	'''Remove GPG key
	Remove the supplied gpg file (as anid) from the RPM database.
	'''
	
	LOGGER.debug('Removing GPG key from RPM: %s', key_id)
	result = run('-e', key_id)
	return result

def run(*params, **kwargs):
	'''Run rpm command
	Run the rpm command and return the resulting lines.
	'''
	
	kwparams = ['--{}={}'.format(key, value) for key, value in kwargs.items() if key[0] != '_']
	
	LOGGER.debug('Running command: rpm %s', ' '.join((*params, *kwparams)))
	result = __salt__['cmd.run']('rpm {}'.format(' '.join((*params, *kwparams))))
	return result
