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
	if result['retcode']:
		raise RuntimeError(result['stderr'])
	key_details = __salt__['gpg_.key_details'](filename = key_file)
	key_list = list_gpg_keys(key_id = key_details['keyid'][-8:].lower())
	if not key_list:
		raise RuntimeError('Key import went sideways, somehow')
	elif len(key_list) > 1:
		raise RuntimeError('Imported key indistinguishable from another existing key')
	else:
		return key_list[0].keys()[0]
	
def list_gpg_keys(key_id = None):
	'''List GPG keys
	Return the list of GPG keys on the RPM database and their descriptions
	'''
	
	key_name = 'gpg-pubkey'
	if key_id is not None:
		key_name = '-'.join((key_name, key_id))
	LOGGER.debug('Listing imported GPG keys')
	result = run('-q', key_name, '--qf', "'%{NAME}-%{VERSION}-%{RELEASE}\t%{SUMMARY}\n'")
	return {key_line.split('\t')[0] : key_line.split('\t', maxsplit = 1)[1] for key_line in result['stdout'].splitlines()} if not result['retcode'] else {}
	
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
	result = __salt__['cmd.run_all']('rpm {}'.format(' '.join((*params, *kwparams))), ignore_retcode = True)
	return result
