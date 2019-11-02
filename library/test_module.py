#!/usr/bin/python
# -*- coding: utf-8 -*-

DOCUMENTATION='''
module: count_page
author: Alexandre 
description: Module qui permet d'exécuter une requête SQL 
 
options: 
  db_name: 
    description: nom de la base de données
    required: yes 
  request: 
    description: requête à exécuter
    required: yes 
 
'''

EXAMPLES='''
- name: "SQL" 
  count_page: 
    db_name: "BDD" 
    request: "select * from user;" 
'''

RETURN = '''
results: 
    description: retourne le résultat de la requête 
'''

from ansible.module_utils.basic import AnsibleModule
import grp, pwd
import json

def user_repo_present(data):
	has_changed = False
	#meta = {"present": "not yet implemented"}
	#return (has_changed, meta)
	user = data['user']
	groups = [g.gr_name for g in grp.getgrall() if user in g.gr_mem]
	gid = pwd.getpwnam(user).pw_gid
	groups.append(grp.getgrgid(gid).gr_name)
	result = groups
	#meta = {"status": "SUCCESS", 'response': {"user":result[0]}}
	meta = {"status": "SUCCESS", 'response': json.dumps(result)}
	return False, meta

def user_repo_absent(data=None):
	has_changed = False
	meta = {"absent": "not yet implemented"}
	return (has_changed, meta)

def main():
	
	fields = {

	"user": {"required": True, "type": "str" },
	"state": {
        	"default": "present", 
        	"choices": ['present', 'absent'],  
        	"type": 'str' 
        },
	
	}	

	choice_map = {
	
		"present": user_repo_present,
		"absent": user_repo_absent, 
	}

	module = AnsibleModule(argument_spec=fields)
	has_changed, result = choice_map.get(module.params['state'])(module.params)
	module.exit_json(changed=has_changed, meta=result)


if __name__ == '__main__':
    main()
