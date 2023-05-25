#! python
'''Extended rpm state module.
This module implements extra states related to the rpm module.

Version: 0.0.1

TODO:
- everything

Refs:
'''

import logging

LOGGER = logging.getLogger(__name__)

def _preload_keys(key_path = None, key_content = None):
	
	key_details = __salt__['gpg_.key_details'](text = key_content, filename = key_path)
	if key_content is not None:
		key_path = __salt__['temp.file']()
		__salt__['file.write'](key_path, *key_content.splitlines())
	rpm_key_name = __salt__['rpm_.list_gpg_keys'](key_id = key_details['keyid'][-8:].lower())
	
	return key_details, key_path, rpm_key_name

def imported_gpg_key(name, key_path = None, key_content = None):
	'''Import GPG key
	Make sure that the provided GPG key is imported into the RPM database.
	'''
	
	ret	=	{
		'name'		: name,
		'result'	: False,
		'changes'	: {},
		'comment'	: '',
	}
	
	key_details, key_path, rpm_key_name = _preload_keys(key_path = key_path, key_content = key_content))

	if rpm_key_name:
		ret['result'] = True
		ret['comment'] = 'The key is already in the RPM database: {}'.format(rpm_key_name)
	else:
		if __opts__['test']:
			ret['result'] = None
			ret['comment'] = 'The key would be added to the RPM database: {} -> {}'.format(key_details['keyid'], key_details['uids'])
			ret['changes'].update({'rpm' : {'old' : '', 'new' : 'gpg-pubkey-{}-...'.format(key_details['keyid'][-8:].lower())}})
		else:
			try:
				result = __salt__['rpm_.import_gpg_key'](key_file = key_path)
			except Exception as error:
				ret['comment'] = str(error)
				return ret
			else:
				ret['result'] = True
				ret['comment'] = 'Key added to the RPM database'
				ret['changes'].update({'rpm' : {'old' : '', 'new' : result}})
				