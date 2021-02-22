import requests

from cartmigration.libs.utils import *
import optparse

from cartmigration.models.basecart import LeBasecart
class Command():
	def __init__(self, action):
		self._action = action

	def set_max_migration_id(self, migration_id):
		path = get_root_path() + '/cartmigration/etc/'
		file_name = path + 'max_id.ini'
		check_exist = False
		if os.path.isfile(file_name):
			check_exist = True
		with open(file_name, 'w') as log_file:
			log_file.write('[max_id]\n')
			log_file.write('max_id=' + to_str(migration_id))
		if not check_exist and os.path.isfile(file_name):
			os.chmod(file_name, 0o777)

	def get_max_migration_id(self):
		return get_config_ini('max_id', 'max_id', 0, file = 'max_id.ini')

	def map_customer_group(self, notice):
		if not notice['support']['customer_group_map']:
			return response_success(dict())
		src_customer_group = notice['src']['customer_group']
		if not src_customer_group:
			return response_error('Src Customer group is empty')
		target_customer_group = notice['target']['customer_group']
		if not target_customer_group:
			return response_error('target Customer group is empty')
		map_data = self.get_map_in_config('map-customer-group', src_customer_group, target_customer_group)

		group_default = next(iter(target_customer_group.keys()))
		for src_group_id, src_group_label in src_customer_group.items():
			if src_group_id in map_data:
				continue
			check = False
			for target_group_id, target_group_label in target_customer_group.items():
				if src_group_label.lower() == target_group_label.lower():
					map_data[str(src_group_id)] = to_str(target_group_id)
					check = True
					break
			if check is False:
				map_data[str(src_group_id)] = to_str(group_default)
		return response_success(map_data)

	def map_order_status(self, notice):
		if not notice['support']['order_status_map']:
			return response_success(dict())
		src_order_status = notice['src']['order_status']
		if not src_order_status:
			return response_success(dict())
		target_order_status = notice['target']['order_status']
		if not target_order_status:
			return response_error('target order status is empty')
		map_data = self.get_map_in_config('map-order-status', src_order_status, target_order_status)
		status_default = next(iter(target_order_status.keys()))
		for src_group_id, src_group_label in src_order_status.items():
			if src_group_id in map_data:
				continue
			check = False
			for target_group_id, target_group_label in target_order_status.items():
				if src_group_label.lower() == target_group_label.lower() \
						or src_group_label.lower() == target_group_id.lower() \
						or src_group_id.lower() == target_group_id.lower() \
						or src_group_id.lower() == target_group_label.lower():
					map_data[src_group_id] = target_group_id
					check = True
					break
			if check is False:
				map_data[src_group_id] = status_default
		return response_success(map_data)

	def map_language_data(self, notice):
		if not notice['support']['language_map']:
			return response_success()
		# if to_len(notice['src']['languages']) > to_len(notice['target']['languages']):
		# 	return response_error("Number languages src > Number languages target")
		src_languages = notice['src']['languages']
		if not src_languages:
			return response_error('Src language is empty')
		target_languages = notice['target']['languages']
		if not target_languages:
			return response_error('target language is empty')
		target_keys = list(target_languages.keys())
		key_default = 0
		len_target = to_len(target_languages)
		key_uses = list()
		map_data = self.get_map_in_config('map-language', src_languages, target_languages)
		for src_language_id, src_language_label in src_languages.items():
			if src_language_id in map_data:
				continue
			check = False
			check_break = False
			for target_language_id, target_language_label in target_languages.items():
				if src_language_label.lower() == target_language_label.lower():
					map_data[str(src_language_id)] = to_str(target_language_id)
					key_uses.append(target_language_id)
					check = True
					break
			if check is False:
				while key_default < to_len(target_keys) - 1:
					if key_default not in key_uses:
						break
					key_default += 1
				if key_default >= len_target:
					check_break = True
					break
				map_data[str(src_language_id)] = target_keys[key_default]
				key_uses.append(target_keys[key_default])
				key_default += 1
			if check_break:
				break
		return response_success(map_data)

	def get_map_in_config(self, key, src_data, target_data):
		map_data = dict()
		map_in_config = get_config_ini(key)
		if map_in_config:
			for src_group, target_group in map_in_config.items():
				map_key = None
				map_value = None
				for src_key, src_label in src_data.items():
					if src_group == src_key or src_group == src_label:
						map_key = src_key
						break
				if not map_key:
					continue
				for target_key, target_label in target_data.items():
					if target_group == target_key or target_group == target_label:
						map_value = target_key
						break
				if not map_value:
					continue
				map_data[map_key] = map_value
		return map_data
	def get_custom_headers(self):
		time_request = to_str(to_int(time.time()))
		private_key = get_config_ini('local', 'private_key')
		hmac = hash_hmac('sha256', time_request, private_key)
		custom_headers = dict()
		custom_headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64;en; rv:5.0) Gecko/20110619 Firefox/5.0'
		custom_headers['Authorization'] = time_request + ":" + hmac
		return custom_headers

	def call_server(self, path, data):
		custom_headers = self.get_custom_headers()
		if data and isinstance(data, dict):
			data['test'] = True
		try:
			ip_host = socket.gethostbyname(socket.gethostname())  # Default to any avialable network interface
		except Exception:
			ip_host = '127.0.0.1'
		url = 'http://' + ip_host + ':' + get_config_ini('local', 'port') + '/api/v1/' + path
		return self.call(url, data, custom_headers)

	def call(self, url, data, custom_headers = None):
		if isinstance(data, list) or isinstance(data, dict):
			data = json_encode(data)
		if not custom_headers:
			custom_headers = dict()
			custom_headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64;en; rv:5.0) Gecko/20110619 Firefox/5.0'
		elif isinstance(custom_headers, dict) and not custom_headers.get('User-Agent'):
			custom_headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64;en; rv:5.0) Gecko/20110619 Firefox/5.0'

		res = False
		try:
			r = requests.post(url, data, headers = custom_headers)

			res = r.text
			r.raise_for_status()
		except requests.exceptions.HTTPError as errh:
			log("Http Error:" + to_str(errh) + " : " + to_str(res), type_error = 'test_exp')
		except requests.exceptions.ConnectionError as errc:
			log("Error Connecting:" + to_str(errc) + " : " + to_str(res), type_error = 'test_exp')
		except requests.exceptions.Timeout as errt:
			log("Timeout Error:" + to_str(errt) + " : " + to_str(res), type_error = 'test_exp')
		except requests.exceptions.RequestException as err:
			log("OOps: Something Else" + to_str(err) + " : " + to_str(res), type_error = 'test_exp')
		return res

	def setup(self, migration_id = None, option_args = None):
		info = {
			'src': dict(get_config_ini('src', file = 'test.ini')),
			'target': dict(get_config_ini('target', file = 'test.ini')),
		}
		data = dict()
		if migration_id:
			data['migration_id'] = migration_id
		for _key, value in info.items():
			for data_key, data_value in value.items():
				if "[" not in data_key:
					data[_key + '_' + data_key] = data_value
				else:
					key_path = re.split(r"[\[\]]", data_key.strip(']'))
					if _key + '_' + key_path[0] not in data:
						data[_key + '_' + key_path[0]] = dict()
					data[_key + '_' + key_path[0]][key_path[1]] = data_value
		data['test'] = True
		setup_info = self.call_server('action/setup_cart', data)
		if isinstance(setup_info, str):
			setup_info = json_decode(setup_info)
		if setup_info['result'] != 'success':
			return setup_info
		notice = setup_info['data']
		migration_data = {
			'notice': json_encode(notice),
		}
		model = LeBasecart()
		migration_data['migration_id'] = migration_id
		if not migration_id:
			migration_id = to_int(self.get_max_migration_id()) + 1
			model.set_migration_id(migration_id)
			self.call_server('action/clear_previous_data', {'migration_id': migration_id, 'test': True})
			notice['migration_id'] = migration_id
			migration_data = {
				'notice': json_encode(notice),
			}
			migration_data['migration_id'] = migration_id
			model.get_db(test = True).set_migration_id(migration_id)
			migration = model.insert_obj(TABLE_MIGRATION, data = migration_data, insert_id = True)
			if migration['result'] != 'success':
				return response_error()
			self.set_max_migration_id(migration_id)
		else:
			migration = model.update_obj(TABLE_MIGRATION, migration_data, {'migration_id': migration_id})
			if migration['result'] != 'success':
				return response_error()
		return response_success(migration_id)

	def get_source_cart(self, notice):
		router = get_model('basecart')
		source_cart_type = notice['src']['cart_type']
		target_cart_type = notice['target']['cart_type']
		special_type = source_cart_type == target_cart_type
		cart_version = notice['src']['config']['version']
		cart_name = getattr(router, 'get_cart')(source_cart_type, cart_version, special_type)
		source_cart = get_model(cart_name)
		if not source_cart:
			return None
		getattr(source_cart, 'set_migration_id')(notice['migration_id'])
		getattr(source_cart, 'set_type')('src')
		getattr(source_cart, 'set_notice')(notice)
		getattr(source_cart, 'set_is_test')(True)

		return source_cart

	def display_upload(self, migration_id, notice):
		path_file = get_config_ini('src', 'file', file = 'test.ini')
		full_path_file = get_pub_path() + '/' + DIR_UPLOAD + '/' + path_file
		if not path_file or not os.path.isdir(full_path_file):
			return response_error("Don't file path")
		source_cart = self.get_source_cart(notice)
		getattr(source_cart, 'set_migration_id')(migration_id)
		source_cart.get_db(test = True).set_migration_id(migration_id)
		file_info = getattr(source_cart, 'get_file_info')()
		config_ini = dict(get_config_ini('config', file = 'test.ini'))
		config_data = dict()
		for config_key, config_value in config_ini.items():
			if notice['support'].get(config_key) and to_bool(config_value):
				config_data[config_key] = to_bool(config_value)
		upload_res = dict()
		for info_key, info_label in file_info.items():
			file_details = getattr(source_cart, 'get_default_file_details')()
			upload_name = getattr(source_cart, 'get_upload_file_name')(info_key)
			check = False
			parents = info_label['parents']
			for parent in parents:
				if notice['support'].get(parent) and to_bool(get_config_ini('config', parent, file = 'test.ini')):
					if os.path.isfile(full_path_file + '/' + upload_name):
						check = True
						break
					return response_error("Not found file " + upload_name)
			if check:
				try:
					file_details['upload'] = True
					file_details['name'] = upload_name
					file_details['storage'] = False
					notice['src']['config']['file'][info_key] = file_details
					if info_key not in upload_res:
						upload_res[info_key] = dict()
					upload_res[info_key]['result'] = 'success'
					upload_res[info_key]['name'] = upload_name
				except Exception as e:
					log_traceback(migration_id)
					file_details['upload'] = False
					upload_res[info_key]['result'] = 'error'
					notice['src']['config']['file'][info_key] = file_details
			else:
				file_details['upload'] = False
				notice['src']['config']['file'][info_key] = file_details
		getattr(source_cart, 'set_notice')(notice)
		prepare_display_upload = getattr(source_cart, 'prepare_display_upload')(config_data)
		display_upload = getattr(source_cart, 'display_upload')(upload_res)
		if display_upload['result'] != 'success':
			return display_upload
		upload_res = display_upload['msg']
		for type_file, res in upload_res.items():
			if res['result'] != 'success':
				return response_error('File ' + res['name'] + ': ' + res['msg'])
		notice = getattr(source_cart, 'get_notice')()
		source_cart.update_obj(TABLE_MIGRATION, {'notice': json_encode(notice)}, {'migration_id': migration_id})

		return response_success(notice)
	def config(self, migration_id = None, option_args = None):
		data_test = {
			'migration_id': migration_id
		}
		notice = self.call_server('action/get_migration_info', data_test)
		if not notice:
			return response_error()
		if isinstance(notice, str):
			notice = json_decode(notice)
		if notice['src']['setup_type'] == 'file':
			display_upload = self.display_upload(migration_id, notice)
			if display_upload['result'] != 'success':
				return display_upload
			notice = display_upload['data']
		config_ini = dict(get_config_ini('config', file = 'test.ini'))
		config_data = dict()
		for config_key, config_value in config_ini.items():
			if notice['support'].get(config_key) and to_bool(config_value):
				config_data[config_key] = to_bool(config_value)
		map_language = self.map_language_data(notice)
		if map_language['result'] != 'success':
			return map_language
		config_data['languages'] = map_language['data']
		config_data['languages_select'] = dict()
		for src_id, target_id in config_data['languages'].items():
			config_data['languages_select'][str(src_id)] = 'on'
		config_data['migration_id'] = migration_id
		customer_group_map = self.map_customer_group(notice)
		if customer_group_map['result'] != 'success':
			return customer_group_map
		config_data['customer_group'] = customer_group_map['data']
		order_status_map = self.map_order_status(notice)
		if order_status_map['result'] != 'success':
			return order_status_map
		config_data['order_status'] = order_status_map['data']
		config = self.call_server('action/config', config_data)
		if isinstance(config, str):
			config = json_decode(config)
		return config

	def full(self, migration_id = None, option_args = None):
		setup_info = self.setup(migration_id)
		if setup_info['result'] != 'success':
			setup_info['step'] = 'setup'
			return setup_info
		migration_id = setup_info['data']
		config_info = self.config(migration_id)
		if config_info['result'] == 'success':
			return self.start(migration_id, option_args)
		else:
			config_info['step'] = 'config'
			return config_info

	def start(self, migration_id, option_args = None):
		start = self.call_server('start/' + to_str(migration_id), {'migration_id': migration_id})
		start_decode = json_decode(start)
		if not start_decode or start_decode['result'] != 'success':
			return start
		return "Start migration id: {}. Run \033[94m\033[1m watch cat {}/log/{}/notice.log\033[0m to view process migration".format(migration_id, get_pub_path(), migration_id)

	def reset(self, migration_id, option_args = None):
		reset = self.call_server('action/reset_migration', {'migration_id': migration_id})
		reset_decode = json_decode(reset)
		if not reset_decode or reset_decode['result'] != 'success':
			return reset
		return "Start migration id: {}. Run \033[94m\033[1m watch cat {}/log/{}/notice.log\033[0m to view process migration".format(migration_id, get_pub_path(), migration_id)

	def stop_loop(self, migration_id, option_args = None):
		return self.call_server('action/kill_end_loop_migration', {'migration_id': migration_id})

	def stop(self, migration_id, option_args = None):
		return self.call_server('action/kill_migration', {'migration_id': migration_id})

	def recent(self, migration_id, option_args = None):
		recent = self.call_server('recent/' + to_str(migration_id), {'migration_id': migration_id})
		if recent['result'] != 'success':
			return recent
		return self.start(migration_id, option_args)

	def change_mode(self, migration_id, option_args):
		mode = option_args.mode
		model = LeBasecart()
		model.set_migration_id(migration_id)
		model.get_db(test = True).set_migration_id(migration_id)
		migration = model.select_row(TABLE_MIGRATION, {'migration_id': migration_id})
		if not migration:
			return
		update = dict()
		update['mode'] = MIGRATION_FULL if mode == 'full' else MIGRATION_DEMO
		notice = json_decode(migration['notice'])
		notice['mode'] = MIGRATION_FULL if mode == 'full' else MIGRATION_DEMO
		update['notice'] = json_encode(notice)
		model.update_obj(TABLE_MIGRATION, update, {'migration_id': migration_id})
		return

	def private_key(self, migration_id = None, option_args = None):
		config_file = get_root_path() + '/cartmigration/etc/config.ini'
		if not os.path.isfile(config_file):
			print("Not found config file")
			return
		config = configparser.ConfigParser()
		config.read(config_file)
		if not config.has_section('local'):
			print("Not found section local in config file")
			return
		private_key = md5(to_str(to_int(time.time())))
		config['local']['private_key'] = md5(to_str(to_int(time.time())))
		with open(config_file, 'w') as configfile:  # save
			config.write(configfile)
		return private_key

	def run(self, option_args = None):
		migration_id = option_args.migration_id
		if not hasattr(self, self._action):
			print('Action invalid')
			return
		mode = option_args.mode
		if mode and mode in ['full', 'demo']:
			self.change_mode(migration_id, option_args)
		action = getattr(self, self._action)(migration_id, option_args)
		print(action)
def get_list_action():
	return {
		'setup': 'Setup migration',
		'config': 'Config migration',
		'start': 'Start migration',
		'full': 'auto setup => config => start',
		'stop': 'stop migration',
		'stop_loop': 'stop end loop',
		'reset': 'reset migration',
		'change_mode': 'Change mode',
		'recent': 'recent Migration',
		'private_key': 'Generate private key',
	}
def get_help_action():
	action = get_list_action()
	desc = list()
	for action_key, action_desc in action.items():
		desc.append('[' + action_key + ':' + action_desc.capitalize() + ']')
	return "\n".join(desc)

parser = optparse.OptionParser()
parser.add_option('-m', '--migration_id', help="Migration Id", default="")
parser.add_option('-a', '--action', help=get_help_action(), default="")
parser.add_option('-o', '--mode', help="Mode: full or demo", default="")

options, args = parser.parse_args()
param_migration_id = options.migration_id
param_action = options.action
list_action = get_list_action()
if param_action not in list(list_action.keys()):
	print('Action ' + param_action + ' invalid')
	sys.exit()

if param_action not in ['setup', 'full', 'private_key'] and not param_migration_id:
	print('Action ' + param_action + ' required migration_id')
	sys.exit()
test = Command(param_action)
test.run(options)


