#! python
'''Extended rpm execution module.
This module implements extra execution actions related to the rpm module.

Version: 0.0.1

TODO:
- everything

Refs:
'''

import logging

LOGGER = logging.getLogger(__name__)

def import_gpg_key(key_file):
	'''Import GPG key
	Import the supplied gpg file (as a path) to the RPM database.
	'''
	
	LOGGER.debug('Importing GPG key to RPM: %s', key_file)
	result = run('--import', key_file)
	return result
	
def list_gpg_keys(key_id = None):
	'''List GPG keys
	Return the list of GPG keys on the RPM database and their descriptions
	'''
	
	key_name = 'gpg-pubkey'
	if key_id is not None:
		key_name = '-'.join((key_name, key_id))
	LOGGER.debug('Listing imported GPG keys')
	result = run('-q', key_name, '--qf', "'%{NAME}-%{VERSION}-%{RELEASE}\t%{SUMMARY}\n'")
	return {key_line.split('\t')[0] : key_line.split('\t', maxsplit = 1)[1] for key_line in result.splitlines()} if result else {}
	
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
