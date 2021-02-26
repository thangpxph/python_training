import html
import math
from datetime import  datetime

from cartmigration.models.basecart import LeBasecart
from cartmigration.libs.utils import *


class LeCartCustom(LeBasecart):
	def display_config_source(self):
		parent = super().display_config_source()
		if parent['result'] != 'success':
			return parent
		response = response_success()
		order_status_data = {
			'completed': 'Completed'
		}
		language_data = {
			1: "Default Language"
		}
		self._notice['src']['category_root'] = 1
		self._notice['src']['site'] = {
			1: 'Default Shop'
		}
		self._notice['src']['category_data'] = {
			1: 'Default Category',
		}
		self._notice['src']['support']['language_map'] = True
		self._notice['src']['support']['country_map'] = False
		self._notice['src']['support']['customer_group_map'] = False
		self._notice['src']['support']['taxes'] = True
		self._notice['src']['support']['manufacturers'] = False
		self._notice['src']['support']['reviews'] = False
		self._notice['src']['support']['add_new'] = True
		self._notice['src']['support']['skip_demo'] = False
		self._notice['src']['support']['customer_group_map'] = False
		self._notice['src']['languages'] = language_data
		self._notice['src']['order_status'] = order_status_data
		response['result'] = 'success'
		return response

	def display_config_target(self):
		return response_success()

	def display_import_source(self):
		if self._notice['config']['add_new']:
			recent = self.get_recent(self._migration_id)
			if recent:
				types = ['taxes', 'manufacturers', 'categories', 'attributes', 'products', 'customers', 'orders', 'reviews', 'pages', 'blogs', 'coupons', 'cartrules']
				for _type in types:
					self._notice['process'][_type]['id_src'] = recent['process'][_type]['id_src']
					self._notice['process'][_type]['total'] = 0
					self._notice['process'][_type]['imported'] = 0
					self._notice['process'][_type]['error'] = 0
		queries = {
			# 'taxes': {
			# 	'type': 'select',
			# 	'query': "SELECT COUNT(1) AS count FROM  _DBPRF_StateTaxStates WHERE id > " + to_str(self._notice['process']['taxes']['id_src']),
			# },
			# 'manufacturers': {
			# 	'type': 'select',
			# 	'query': "SELECT COUNT(1) AS count  FROM _DBPRF_manufacturers WHERE manufacturers_id > " + to_str(self._notice['process']['manufacturers']['id_src']),
			# },
			'categories': {
				'type': 'select',
				'query': "SELECT COUNT(1) AS count FROM  categories WHERE categories_id > " + to_str(self._notice['process']['categories']['id_src']),
			},
			'products': {
				'type': 'select',
				'query': "SELECT COUNT(1) AS count FROM  products WHERE products_id > " + to_str(self._notice['process']['products']['id_src']),
			},
			'customers': {
				'type': 'select',
				'query': "SELECT COUNT(1) AS count FROM  customers WHERE customers_id > " + to_str(self._notice['process']['customers']['id_src']),
			},
			'orders': {
				'type': 'select',
				'query': "SELECT COUNT(1) AS count FROM  orders WHERE  orders_id > " + to_str(self._notice['process']['orders']['id_src']),
			},
			# 'reviews': {
			# 	'type': 'select',
			# 	'query': "SELECT COUNT(1) AS count FROM _DBPRF_reviews WHERE reviews_id > " + to_str(self._notice['process']['reviews']['id_src']),
			# },
		}
		count = self.select_multiple_data_connector(queries)
		if (not count) or (count['result'] != 'success'):
			return response_error()
		real_totals = dict()
		for key, row in count['data'].items():
			total = self.list_to_count_import(row, 'count')
			real_totals[key] = total
		for key, total in real_totals.items():
			self._notice['process'][key]['total'] = total
		return response_success()

	def display_import_target(self):
		return response_success()

	def display_confirm_source(self):
		return response_success()

	def display_confirm_target(self):
		self._notice['target']['clear']['function'] = 'clear_target_taxes'
		return response_success()

	# TODO: CLEAR
	def clear_target_address_book(self):
		next_clear = {
			'result': 'process',
			'function': 'clear_target_categories',
		}
		self._notice['target']['clear'] = next_clear
		return next_clear

	def clear_target_categories(self):
		next_clear = {
			'result': 'process',
			'function': 'clear_target_categories_description',
		}
		self._notice['target']['clear'] = next_clear
		return next_clear

	def clear_target_categories_description(self):
		next_clear = {
			'result': 'process',
			'function': 'clear_target_countries',
		}

		self._notice['target']['clear'] = next_clear
		return self._notice['target']['clear']

	def clear_target_countries(self):
		next_clear = {
			'result': 'process',
			'function': 'clear_target_currencies',
		}

		self._notice['target']['clear'] = next_clear
		return self._notice['target']['clear']

	def clear_target_currencies(self):
		next_clear = {
			'result': 'process',
			'function': 'clear_target_customers',
		}

		self._notice['target']['clear'] = next_clear
		return self._notice['target']['clear']

	def clear_target_customers(self):
		next_clear = {
			'result': 'process',
			'function': 'clear_target_customers_info',
		}

		self._notice['target']['clear'] = next_clear
		return self._notice['target']['clear']

	def clear_target_customers_info(self):
		next_clear = {
			'result': 'process',
			'function': 'clear_target_languages',
		}

		self._notice['target']['clear'] = next_clear
		return self._notice['target']['clear']

	def clear_target_languages(self):
		next_clear = {
			'result': 'process',
			'function': 'clear_target_orders',
		}

		self._notice['target']['clear'] = next_clear
		return self._notice['target']['clear']

	def clear_target_orders(self):
		next_clear = {
			'result': 'process',
			'function': 'clear_target_orders_products',
		}

		self._notice['target']['clear'] = next_clear
		return self._notice['target']['clear']

	def clear_target_orders_products(self):
		next_clear = {
			'result': 'process',
			'function': 'clear_target_orders_total',
		}

		self._notice['target']['clear'] = next_clear
		return self._notice['target']['clear']

	def clear_target_orders_total(self):
		next_clear = {
			'result': 'process',
			'function': 'clear_target_products',
		}

		self._notice['target']['clear'] = next_clear
		return self._notice['target']['clear']

	def clear_target_products(self):
		next_clear = {
			'result': 'process',
			'function': 'clear_target_products_description',
		}

		self._notice['target']['clear'] = next_clear
		return self._notice['target']['clear']

	def clear_target_products_description(self):
		next_clear = {
			'result': 'process',
			'function': 'clear_target_products_to_categories',
		}

		self._notice['target']['clear'] = next_clear
		return self._notice['target']['clear']

	def clear_target_products_to_categories(self):
		next_clear = {
			'result': 'process',
			'function': 'clear_target_zones',
		}

		self._notice['target']['clear'] = next_clear
		return self._notice['target']['clear']

	# TODO: TAX
	def prepare_taxes_import(self):
		return self

	def prepare_taxes_export(self):
		return self

	def get_taxes_main_export(self):
		id_src = self._notice['process']['taxes']['id_src']
		limit = self._notice['setting']['taxes']
		query = {
			'type': 'select',
			'query': "SELECT * FROM _DBPRF_StateTaxStates WHERE id > " + to_str(
				id_src) + " ORDER BY id ASC LIMIT " + to_str(limit)
		}
		taxes = self.get_connector_data(self.get_connector_url('query'), {'query': json.dumps(query)})
		if not taxes or taxes['result'] != 'success':
			return response_error('could not get taxes main to export')
		return taxes

	def get_taxes_ext_export(self, taxes):
		return response_success()

	def convert_tax_export(self, tax, taxes_ext):
		tax_product = list()
		tax_customer = list()
		tax_zone = list()
		tax_product_data = self.construct_tax_product()
		tax_product_data['id'] = 1
		tax_product_data['code'] = None
		tax_product_data['name'] = 'Product Tax Class Shopify'
		tax_product.append(tax_product_data)

		tax_zone_state = self.construct_tax_zone_state()

		tax_zone_country = self.construct_tax_zone_country()
		tax_zone_country['id'] = 'US'
		tax_zone_country['name'] = 'United States'
		tax_zone_country['country_code'] = 'US'

		tax_zone_rate = self.construct_tax_zone_rate()
		tax_zone_rate['id'] = None
		tax_zone_rate['name'] = tax['state']+' '+ tax['rate']
		tax_zone_rate['rate'] = tax['rate']

		tax_zone_data = self.construct_tax_zone()
		tax_zone_data['id'] = None
		tax_zone_data['name'] = 'United States'
		tax_zone_data['country'] = tax_zone_country
		tax_zone_state = self.construct_tax_zone_state()
		tax_zone_state['id'] = 'TX'
		tax_zone_state['name'] = 'Texas'
		tax_zone_state['state_code'] = 'TX'


		tax_zone_data['state'] = tax_zone_state
		tax_zone_data['rate'] = tax_zone_rate
		tax_zone.append(tax_zone_data)

		tax_data = self.construct_tax()
		tax_data['id'] = tax['id']
		tax_data['name'] = tax['state']+' '+tax['rate']
		tax_data['tax_products'] = tax_product
		tax_data['tax_zones'] = tax_zone
		return response_success(tax_data)

	def get_tax_id_import(self, convert, tax, taxes_ext):
		return tax['id']

	def check_tax_import(self, convert, tax, taxes_ext):
		return True if self.get_map_field_by_src(self.TYPE_TAX, convert['id']) else False

	def router_tax_import(self, convert, tax, taxes_ext):
		return response_success('tax_import')

	def before_tax_import(self, convert, tax, taxes_ext):
		return response_success()

	def tax_import(self, convert, tax, taxes_ext):
		return response_success(0)

	def after_tax_import(self, tax_id, convert, tax, taxes_ext):
		return response_success()

	def addition_tax_import(self, convert, tax, taxes_ext):
		return response_success()

	# TODO: MANUFACTURER
	def prepare_manufacturers_import(self):
		return self

	def prepare_manufacturers_export(self):
		return self

	def get_manufacturers_main_export(self):
		id_src = self._notice['process']['manufacturers']['id_src']
		limit = self._notice['setting']['manufacturers']
		query = {
			'type': 'select',
			'query': "SELECT * FROM _DBPRF_manufacturers WHERE manufacturers_id > " + to_str(
				id_src) + " ORDER BY manufacturers_id ASC LIMIT " + to_str(limit)
		}
		manufacturers = self.get_connector_data(self.get_connector_url('query'), {'query': json.dumps(query)})
		if not manufacturers or manufacturers['result'] != 'success':
			return response_error('could not get manufacturers main to export')
		return manufacturers

	def get_manufacturers_ext_export(self, manufacturers):
		url_query = self.get_connector_url('query')
		manufacturer_ids = duplicate_field_value_from_list(manufacturers['data'], 'manufacturer_id')
		manufacturers_ext_queries = {
			'manufacturers_info': {
				'type': 'select',
				'query': "SELECT * FROM _DBPRF_manufacturers_info WHERE manufacturers_id IN " + self.list_to_in_condition(
					manufacturer_ids)
			}
		}
		manufacturers_ext = self.get_connector_data(url_query,
		                                            {'serialize': True, 'query': json.dumps(manufacturers_ext_queries)})
		if not manufacturers_ext or manufacturers_ext['result'] != 'success':
			return response_error()
		return manufacturers_ext

	def convert_manufacturer_export(self, manufacturer, manufacturers_ext):
		manufacturer_data = self.construct_manufacturer()
		manufacturer_data['id'] = manufacturer['manufacturers_id']
		manufacturer_data['name'] = manufacturer['manufacturers_name']
		manufacturer_data['thumb_image']['url'] = self.get_url_suffix(self._notice['src']['config']['image_manufacturer'])
		manufacturer_data['thumb_image']['path'] = manufacturer['manufacturers_image']

		for language_id, language_label in self._notice['src']['languages'].items():
			manufacturer_language_data = dict()
			manufacturer_language_data['name'] = manufacturer['manufacturers_name']
			manufacturer_data['languages'][language_id] = manufacturer_language_data
		return response_success(manufacturer_data)

	def get_manufacturer_id_import(self, convert, manufacturer, manufacturers_ext):
		return manufacturer['manufacturers_id']

	def check_manufacturer_import(self, convert, manufacturer, manufacturers_ext):
		return True if self.get_map_field_by_src(self.TYPE_MANUFACTURER, convert['id']) else False

	def router_manufacturer_import(self, convert, manufacturer, manufacturers_ext):
		return response_success('manufacturer_import')

	def before_manufacturer_import(self, convert, manufacturer, manufacturers_ext):
		return response_success()

	def manufacturer_import(self, convert, manufacturer, manufacturers_ext):
		return response_success(0)

	def after_manufacturer_import(self, manufacturer_id, convert, manufacturer, manufacturers_ext):
		return response_success()

	def addition_manufacturer_import(self, convert, manufacturer, manufacturers_ext):
		return response_success()

	# TODO: CATEGORY
	def prepare_categories_import(self):
		return self

	def prepare_categories_export(self):
		return self

	def get_categories_main_export(self):
		id_src = self._notice['process']['categories']['id_src']
		limit = self._notice['setting']['categories']
		query = {
			'type': 'select',
			'query': "SELECT * FROM  categories WHERE categories_id > " + to_str(
				id_src) + " ORDER BY categories_id ASC LIMIT " + to_str(limit)
		}
		categories = self.select_data_connector(query)
		if not categories or categories['result'] != 'success':
			return response_error('could not get manufacturers main to export')
		return categories

	def get_categories_ext_export(self, categories):
		url_query = self.get_connector_url('query')
		category_ids = duplicate_field_value_from_list(categories['data'], 'categories_id')
		categories_ext_queries = {
			'categories_metakeys': {
				'type': 'select',
				'query': "SELECT * FROM  categories_description WHERE categories_id IN " + self.list_to_in_condition(
					category_ids)
			},
			# 'URIs': {
			# 	'type': 'select',
			# 	'query': "SELECT * FROM URIs WHERE cat_id IN " + self.list_to_in_condition(category_ids)
			# },
			# 'cate_imgs': {
			# 	'type': 'select',
			# 	'query': "SELECT * FROM  _DBPRF_CSSUI_CatTree WHERE cat_id IN " + self.list_to_in_condition(category_ids)
			# },
		}
		categories_ext = self.select_multiple_data_connector(categories_ext_queries)

		if not categories_ext or categories_ext['result'] != 'success':
			return response_warning()
		return categories_ext

	def convert_category_export(self, category, categories_ext):
		category_data = self.construct_category()
		parent = self.construct_category_parent()
		parent['id'] = 0
		if category['parent_id']:
			parent_data = self.get_category_parent(category['parent_id'])
			if parent_data['result'] == 'success':
				parent = parent_data['data']
		category_data['id'] = category['categories_id']
		category_data['parent'] = parent
		category_data['active'] = True
		# img = get_row_from_list_by_field(categories_ext['data']['cate_imgs'],'cat_id', category['categories_id'])
		# if img and img['image'] !='' :
		# 	category_data['thumb_image']['url'] = 'http://www.iemotorsport.com/mm5/'
		# 	category_data['thumb_image']['path'] = img['image']
		category_data['sort_order'] = category['sort_order']
		category_data['created_at'] = category['date_added']
		category_data['updated_at'] = category['last_modified']
		url_product_image = self.get_url_suffix(self._notice['src']['config']['image_manufacturer']) + 'images/'
		category_data['thumb_image']['url'] = url_product_image
		category_data['thumb_image']['path'] = category['categories_image']
		category_description = get_row_from_list_by_field(categories_ext['data']['categories_metakeys'],'categories_id', category['categories_id'])
		# category_data['meta_description'] = self.strip_html_tag(category['page_title'])
		if category_description:
			category_data['description'] = category_description['categories_name']
		else:
			category_data['description'] = ''
		category_data['name'] = category_description['categories_name']
		category_data['meta_title'] = category_description['categories_name']
		# category_data['meta_keyword'] = category['code']
		# meta_description

		# category_data['category'] = category
		# category_data['categories_ext'] = categories_ext
		# if self._notice['config']['seo_301']:
		# 	detect_seo = self.detect_seo()
		# 	category_data['seo'] = getattr(self, 'categories_' + detect_seo)(category, categories_ext)
		return response_success(category_data)

	def get_category_id_import(self, convert, category, categories_ext):
		return category['categories_id']

	def check_category_import(self, convert, category, categories_ext):
		id_imported = self.get_map_field_by_src(self.TYPE_CATEGORY, convert['id'], convert['code'])
		return id_imported

	def router_category_import(self, convert, category, categories_ext):
		return response_success('category_import')

	def before_category_import(self, convert, category, categories_ext):
		return response_success()

	def category_import(self, convert, category, categories_ext):
		return response_success(0)

	def after_category_import(self, category_id, convert, category, categories_ext):
		return response_success()

	def addition_category_import(self, convert, category, categories_ext):
		return response_success()

	# TODO: PRODUCT
	def prepare_products_import(self):
		return self

	def prepare_products_export(self):
		return self

	def get_products_main_export(self):
		id_src = self._notice['process']['products']['id_src']
		limit = 4
		query = {
			'type': 'select',
			'query': "SELECT * FROM  products WHERE products_id > " + to_str(id_src) + " ORDER BY products_id ASC LIMIT " + to_str(limit)
		}

		products = self.get_connector_data(self.get_connector_url('query'), {'query': json.dumps(query)})
		if not products or products['result'] != 'success':
			return response_error()
		return products

	def get_products_ext_export(self, products):
		url_query = self.get_connector_url('query')
		product_ids = duplicate_field_value_from_list(products['data'], 'products_id')
		product_id_con = self.list_to_in_condition(product_ids)
		product_id_query = self.product_to_in_condition_seourl(product_ids)
		manufacturer_id = duplicate_field_value_from_list(products['data'], 'manufacturers_id')
		manufacturer_id_con = self.list_to_in_condition(manufacturer_id)
		product_ext_queries = {
			'product_description': {
				'type': "select",
				'query': "SELECT * FROM  products_description WHERE products_id IN " + product_id_con ,
			},
			'product_attribute': {
				'type': "select",
				'query': "SELECT * FROM  product_attribute WHERE product_id IN  " + product_id_con ,
			},
			'attribute': {
				'type': "select",
				'query': "SELECT * FROM  attribute WHERE attribute_id IN  " +
				"(SELECT attribute_id FROM product_attribute WHERE product_id IN " + product_id_con + ")" ,
			},
			# 'URIs': {
			# 	'type': "select",
			# 	'query': "SELECT * FROM URIs WHERE product_id IN " + product_id_con,
			# },
			# 'specials': {
			# 	'type': "select",
			# 	'query': "SELECT * FROM _DBPRF_specials WHERE products_id IN  " + product_id_con,
			# },
			#
			'products_to_categories': {
				'type': 'select',
				'query': "SELECT * FROM products_to_categories WHERE products_id IN " + product_id_con,
			},
			# 'manufacturers': {
			# 	'type': 'select',
			# 	'query': "SELECT manufacturers_id, manufacturers_name FROM _DBPRF_manufacturers WHERE manufacturers_id IN " + manufacturer_id_con,
			# },

		}



		product_ext = self.get_connector_data(url_query, {
			'serialize': True, 'query': json.dumps(product_ext_queries)
		})
		if (not product_ext) or product_ext['result'] != 'success':
			return response_error()
		# image_ids=duplicate_field_value_from_list(product_ext['data']['products_images'], 'image_id')
		# image_id_con  = self.list_to_in_condition(image_ids)
		# product_option_ids = duplicate_field_value_from_list(product_ext['data']['products_attributes'], 'options_id')
		# option_value_ids = duplicate_field_value_from_list(product_ext['data']['products_attributes'], 'options_values_id')
		# option_ids_con = self.list_to_in_condition(product_option_ids)
		# option_value_ids_con = self.list_to_in_condition(option_value_ids)

		# product_ext_rel_queries = {
		# 	'images': {
		# 		'type': 'select',
		# 		'query': "SELECT * FROM  _DBPRF_Images WHERE id IN " + image_id_con,
		# 	},
		# 	# 'products_options_values': {
		# 	# 	'type': 'select',
		# 	# 	'query': "SELECT * FROM `_DBPRF_products_options_values` WHERE products_options_values_id IN " + option_value_ids_con,
		# 	# },
		# }

		# product_ext_rel = self.get_connector_data(url_query, {
		# 	'serialize': True, 'query': json.dumps(product_ext_rel_queries),
		# })
		# if (not product_ext_rel) or (product_ext_rel['result'] != 'success'):
		# 	return response_error()
		# product_ext = self.sync_connector_object(product_ext, product_ext_rel)

		return product_ext

	def convert_product_export(self, product, products_ext):
		products_ext_data = products_ext['data']
		product_data = self.construct_product()
		product_data['id'] = product['products_id']
		product_data['sku'] = product['products_upc_code']
		product_data['price'] = product['products_price']
		product_data['weight'] = product['products_weight']
		if to_int(product['products_status']) > 0:
			status = True
		else:
			status = False
		product_data['status'] = status
		product_data['manage_stock'] = True
		product_data['qty'] = product['products_quantity']
		product_data['length'] = product['products_length']
		product_data['width'] = product['products_width']
		product_data['height'] = product['products_height']
		product_data['date_available'] = product['products_date_available']
		product_description = get_row_from_list_by_field(products_ext_data['product_description'], 'products_id', product['products_id'])
		product_data['created_at'] = datetime.fromtimestamp(to_int(product['products_date_added'])) if to_int(product['products_date_added']) else get_current_time()
		product_data['updated_at'] = datetime.fromtimestamp(to_int(product['products_last_modified'])) if to_int(product['products_last_modified']) else get_current_time()
		product_data['name'] = html.unescape(product_description['products_name'])
		product_data['description'] = html.unescape(product_description['products_description'])
		product_data['short_description'] = html.unescape(product_description['products_description'])

		# if product_description:
		# 	meta_keywords=get_row_from_list_by_field(product_description,'name_id',1)
		# 	meta_description = get_row_from_list_by_field(product_description, 'name_id', 2)
		# 	meta_title = get_row_from_list_by_field(product_description, 'name_id', 3)
		# 	if meta_keywords:
		# 		product_data['meta_keyword'] = meta_keywords['value']
		# 	else:
		# 		product_data['meta_keyword'] = ''
		# 	if meta_description:
		# 		product_data['meta_keyword'] = meta_description['value']
		# 	else:
		# 		product_data['meta_keyword'] = ''
		# 	if meta_title:
		# 		product_data['meta_keyword'] = meta_title['value']
		# 	else:
		# 		product_data['meta_keyword'] = ''

			# product_data['meta_title'] = self.strip_html_tag(html.unescape(product_description_def['meta_title']))
			# product_data['meta_description'] = product_description_def['meta_description']
			# product_data['tags'] = product_description_def['tag']
		# product_data['short_description'] = html.unescape(product_description_def['short_description'])
		# product_data['meta_title'] = html.unescape(product_description_def['meta_title'])
		# product_data['meta_description'] = product_description_def['meta_description']
		# product_data['meta_keyword'] = product_description_def['meta_keyword']
		# product_data['tags'] = product_description_def['tag']
		url_product_image = self.get_url_suffix(self._notice['src']['config']['image_manufacturer']) + 'images/'
		product_data['thumb_image']['url'] = url_product_image
		product_data['thumb_image']['path'] = product['products_image']
		product_image_data = self.construct_product_image()
		product_image_data['url'] = url_product_image
		product_image_data['path'] = product['products_image']
		product_data['images'].append(product_image_data)



		# product_images = get_list_from_list_by_field(products_ext_data['products_images'], 'product_id',product['id'])
		# if product_images:
		# 	if check_thumbnail:
		# 		for product_image in product_images:
		# 			image_data = get_row_from_list_by_field(products_ext_data['images'], 'id',product_image['image_id'])
		# 			product_image_data = self.construct_product_image()
		# 			if image_data :
		# 				product_image_data['url'] = url_product_image
		# 				product_image_data['path'] = image_data['image']
		# 				product_data['images'].append(product_image_data)
		#
		# 	else:
		# 		i = 0
		# 		for product_image in product_images:
		# 			if i == 0 :
		# 				image_data = get_row_from_list_by_field(products_ext_data['images'], 'id', product_image['image_id'])
		# 				product_data['thumb_image']['url'] = url_product_image
		# 				product_data['thumb_image']['path'] = image_data['image']
		# 				i = 1
		# 			else:
		# 				image_data = get_row_from_list_by_field(products_ext_data['images'], 'id',product_image['image_id'])
		# 				product_image_data = self.construct_product_image()
		# 				if image_data :
		# 					product_image_data['url'] = url_product_image
		# 					product_image_data['path'] = image_data['image']
		# 					product_data['images'].append(product_image_data)
		# special = get_row_from_list_by_field(products_ext_data['specials'], 'products_id', product['products_id'])
		# if special:
		# 	product_data['special_price']['price'] = special['specials_new_products_price']
		# 	product_data['special_price']['start_date'] = special['specials_date_added']
		# 	product_data['special_price']['end_date'] = special['expires_date']

		#
		# product_data['tax']['id'] = product['products_tax_class_id']
		# if product['manufacturers_id']:
		# 	product_data['manufacturer']['id'] = product['manufacturers_id']
		# 	manufacturer = get_row_from_list_by_field(products_ext_data['manufacturers'], 'manufacturers_id',
		# 	                                          product['manufacturers_id'])
		# 	if manufacturer:
		# 		product_data['manufacturer']['name'] = manufacturer['manufacturers_name']

		products_to_categories = get_list_from_list_by_field(products_ext_data['products_to_categories'], 'products_id',
		                                                 product['products_id'])
		# if products_to_categories:
		# 	for products_to_categorie in products_to_categories:
		# 		products_to_categorie_data = self
		#
		# product_categories = get_list_from_list_by_field(products_ext_data['product_category'], 'product_id',
		#                                                  product['id'])
		if products_to_categories:
			for product_to_category in products_to_categories:
				product_category_data = self.construct_product_category()
				product_category_data['id'] = product_to_category['categories_id']
				product_data['categories'].append(product_category_data)

		# for language_id in self._notice['src']['languages_select']:
		# 	product_description_lang = get_row_from_list_by_field(product_description, 'language_id', language_id)
			product_language_data = self.construct_product_lang()
		# 	product_language_data['name'] = html.unescape(product_description_lang['products_name'])
		# 	product_language_data['description'] = html.unescape(product_description_lang['products_description'])
		# 	product_language_data['short_description'] = html.unescape(product_description_lang['products_description'])
			# product_language_data['meta_title'] = html.unescape(product_description_lang['meta_title'])
			# product_language_data['meta_description'] = product_description_lang['meta_description']
			# product_language_data['meta_keyword'] = product_description_lang['meta_keyword']
			# product_data['languages'][product_description_lang['language_id']] = product_language_data

		# product_options = get_list_from_list_by_field(products_ext_data['products_attributes'], 'products_id',
		#                                               product['products_id'])
		# if product_options:
		# 	childrent = list()
		# 	childs_data = list()
		# 	comb = self.construct_product_childrent()
		# 	comb['name'] = product_data['name']
		# 	comb['qty'] = product_data['qty']
		# 	comb['sku'] = product_data['sku']
		# 	comb['price'] = product_data['price']
		# 	comb['languages'] = product_data['languages']
		# 	childs_data.append(comb)
		# 	all_product_option_values = get_list_from_list_by_field(products_ext_data['products_attributes'],
		# 	                                                        'products_id', product['products_id'])
		# 	check_value_exist = list()
		# 	for option in product_options:
		# 		option_data = self.construct_product_option()
		# 		option_data['id'] = option['options_id']
		# 		product_option_desc = get_list_from_list_by_field(products_ext_data['products_options'], 'products_options_id',
		# 		                                                  option['options_id'])
		# 		if not product_option_desc:
		# 			continue
		# 		product_option_def = get_row_from_list_by_field(product_option_desc, 'language_id', language_default)
		#
		# 		if not product_option_def:
		# 			product_option_def = product_option_desc[0]
		# 		option_data['option_name'] = product_option_def['products_options_name']
		# 		option_data['option_type'] = 'select'
		# 		#option_data['required'] = option['required']
		#
		# 		for product_option in product_option_desc:
		# 			option_language_data = self.construct_product_option_lang()
		# 			option_language_data['option_name'] = product_option['products_options_name']
		# 			option_data['option_languages'][product_option['language_id']] = option_language_data
		#
		# 		product_option_values = get_list_from_list_by_field(all_product_option_values, 'options_id',
		# 		                                                    option['options_id'])
		# 		new_childs = list()
		#
		# 		for option_value in product_option_values:
		# 			if option_value['options_values_id'] in check_value_exist:
		# 				continue
		# 			check_value_exist.append(option_value['options_values_id'])
		# 			option_value_data = self.construct_product_option_value()
		# 			option_value_data['id'] = option_value['options_values_id']
		# 			product_option_value_description = get_list_from_list_by_field(
		# 				products_ext_data['products_options_values'], 'products_options_values_id',
		# 				option_value['options_values_id'])
		# 			if not product_option_value_description:
		# 				continue
		# 			product_option_value_def = get_row_from_list_by_field(product_option_value_description,
		# 			                                                      'language_id', language_default)
		# 			if not product_option_value_def:
		# 				product_option_value_def = product_option_value_description[0]
		# 			option_value_data['option_value_name'] = product_option_value_def['products_options_values_name']
		#
		# 			for product_option_value in product_option_value_description:
		# 				option_value_language_data = dict()
		# 				option_value_language_data['option_value_name'] = product_option_value['products_options_values_name']
		# 				language_id = product_option_value['language_id']
		# 				option_value_data['option_value_languages'][language_id] = option_value_language_data
		# 			product_attribute = get_row_from_list_by_field(product_option_values, 'options_values_id', option_value['options_values_id'])
		# 			option_value_data['option_value_price'] = product_attribute['options_values_price']
		# 			option_value_data['price_prefix'] = product_attribute['price_prefix']
		#
		# 			for child_data in childs_data:
		# 				child = self.construct_product_childrent()
		# 				child_attr = self.construct_product_child_attribute()
		# 				child_attr['option_id'] = option['options_id']
		# 				child_attr['option_type'] = 'select'
		# 				child_attr['option_name'] = html.unescape(product_option_def['products_options_name'])
		#
		# 				child_attr['option_languages'] = option_data['option_languages']
		#
		# 				child_attr['option_value_id'] = option_value['options_values_id']
		#
		# 				child_attr['option_value_name'] = product_option_value_def['products_options_values_name']
		# 				child_attr['option_value_languages'] = option_value_data['option_value_languages']
		# 				child_attr['option_value_price'] = product_attribute['options_values_price']
		# 				child_attr['price_prefix'] = product_attribute['price_prefix']
		# 				child['name'] = child_data['name'] + ' - ' + option_value_data['option_value_name']
		# 				child['sku'] = child_data['sku'] + '-' + self.join_text_to_key(
		# 					option_value_data['option_value_name'])
		# 				child['qty'] = child_data['qty']
		# 				if option_value_data['price_prefix'] == '-':
		# 					child['price'] = to_decimal(product_data['price']) - to_decimal(product_attribute['options_values_price'])
		# 				else:
		# 					child['price'] = to_decimal(product_data['price']) + to_decimal(product_attribute['options_values_price'])
		# 				for lang_id, lang_data in child_data['languages'].items():
		# 					child_language_data = dict()
		# 					child_language_data['name'] = html.unescape(lang_data['name'])
		# 					child_language_data['description'] = html.unescape(lang_data['description'])
		# 					child_language_data['short_description'] = html.unescape(lang_data['short_description'])
		# 					# child_language_data['meta_title'] = html.unescape(lang_data['meta_title'])
		# 					# child_data['meta_description'] = lang_data.get('meta_description', '')
		# 					# child_data['meta_keyword'] = lang_data.get('meta_keyword')
		# 					child['languages'][lang_id] = child_language_data
		# 				#child['attributes'] = child_data['attributes']
		# 				child['attributes'].append(child_attr)
		# 				del child_attr
		# 				new_childs.append(child)
		# 			option_data['values'].append(option_value_data)
		# 		childs_data = new_childs
		# 		del new_childs
		# 		if to_len(option_data['values']) >0:
		# 			product_data['options'].append(option_data)
		# 	#product_data['children'] = childs_data
		#
		# options_src = dict()
		# for option_each_data in product_data['options']:
		# 	values = list()
		# 	if option_each_data['values']:
		# 		for value in option_each_data['values']:
		# 			values.append(value['option_value_name'])
		#
		# 			opt_val = {
		# 				'option_name': option_each_data['option_name'],
		# 				'option_value_name': value['option_value_name'],
		# 				'price': value['option_value_price'],
		# 				'price_prefix': value['price_prefix'],
		# 				'value_id': value['id'],
		# 				'optionid': option_each_data['id'],
		# 				'option_id': option_each_data['id']
		# 			}
		# 			if option_each_data['id'] not in options_src:
		# 				options_src[option_each_data['id']] = list()
		# 			options_src[option_each_data['id']].append(opt_val)
		# combination = self.combination_from_multi_dict(options_src)
		# children_base_data = copy.deepcopy(product_data)
		# for children in combination:
		# 	children_data = copy.deepcopy(children_base_data)
		#
		# 	sku = product_data['name']
		# 	identifier_options = dict()
		# 	for attribute in children:
		# 		attribute_data = self.construct_product_child_attribute()
		# 		attribute_data['option_name'] = attribute['option_name']
		# 		attribute_data['option_code'] = attribute['option_name']
		# 		attribute_data['option_value_name'] = attribute['option_value_name']
		# 		attribute_data['option_value_code'] = attribute['option_value_name']
		#
		# 		attribute_data['price'] = attribute['price']
		# 		attribute_data['price_prefix'] = attribute['price_prefix']
		# 		if attribute_data['price_prefix'] == '-':
		# 			children_data['price'] = to_decimal(product_data['price']) - to_decimal(attribute_data['price'])
		# 		else:
		# 			children_data['price'] = to_decimal(product_data['price']) + to_decimal(attribute_data['price'])
		#
		#
		# 		children_data['attributes'].append(attribute_data)
		# 		children_data['sku']=sku + '-'+attribute['option_value_name']
		# 		children_data['sku']=children_data['sku'][:63]
		# 	product_data['children'].append(children_data)
		#
		# if product_data['children']:
		# 	product_data['type']='simple'


		attribute_data=[]
		product_attribute = get_list_from_list_by_field(products_ext_data['product_attribute'], 'product_id',
		                                                     product['products_id'])
		if product_attribute:
			for attr in product_attribute:
				product_attribute_ = get_list_from_list_by_field(products_ext_data['attribute'], 'attribute_id',
				                                                attr['attribute_id'])
				if product_attribute_:
					for attr_ in product_attribute_:
						attribute_data.append({
							'value_id': attr['value_id'],
							'attribute_id': attr['attribute_id'],
							'value': attr['value'],
							'attribute_name': attr_['attribute_name'],
							'attribute_code': attr_['attribute_code'],
							'attribute_type': attr_['attribute_type']
						})
		product_data['attributes']=attribute_data





		if self._notice['config']['seo_301']:
			detect_seo = self.detect_seo()
			product_data['seo'] = getattr(self, 'products_' + detect_seo)(product, products_ext)
		return response_success(product_data)

	def get_product_id_import(self, convert, product, products_ext):
		return product['products_id']

	def check_product_import(self, convert, product, products_ext):
		return True if self.get_map_field_by_src(self.TYPE_PRODUCT, convert['products_id'], convert['code']) else False

	def router_product_import(self, convert, product, products_ext):
		return response_success('product_import')

	def before_product_import(self, convert, product, products_ext):
		return response_success()

	def product_import(self, convert, product, products_ext):
		return response_success(0)

	def after_product_import(self, product_id, convert, product, products_ext):
		return response_success()

	def addition_product_import(self, convert, product, products_ext):
		return response_success()

	# TODO: CUSTOMER
	def prepare_customers_import(self):
		query = {
			'type': 'query',
			'query': "ALTER TABLE _DBPRF_customer MODIFY COLUMN password varchar(255)"
		}
		self.import_data_connector(query, 'customer')
		return self

	def prepare_customers_export(self):
		return self

	def get_customers_main_export(self):
		id_src = self._notice['process']['customers']['id_src']
		limit = self._notice['setting']['customers']
		query = {
			'type': 'select',
			'query': "SELECT * FROM  customers WHERE customers_id > " + to_str(id_src) + " ORDER BY customers_id ASC LIMIT " + to_str(limit)
		}

		customers = self.get_connector_data(self.get_connector_url('query'), {'query': json.dumps(query)})
		if not customers or customers['result'] != 'success':
			return response_error('could not get customers main to export')
		return customers

	def get_customers_ext_export(self, customers):
		url_query = self.get_connector_url('query')
		customers_ids = duplicate_field_value_from_list(customers['data'], 'customers_id')
		customer_ext_queries = {
			'address_book': {
				'type': 'select',
				'query': "SELECT * FROM  address_book WHERE customers_id IN " + self.list_to_in_condition(customers_ids),
			},
			'customers_info': {
				'type': 'select',
				'query': "SELECT * FROM  customers_info WHERE customers_info_id IN " + self.list_to_in_condition(customers_ids),
			}
		}
		customers_ext = self.get_connector_data(url_query,{'serialize': True, 'query': json.dumps(customer_ext_queries)})
		if not customers_ext or customers_ext['result'] != 'success':
			return response_error()
		country_ids = duplicate_field_value_from_list(customers_ext['data']['address_book'], 'entry_country_id')
		zone_ids = duplicate_field_value_from_list(customers_ext['data']['address_book'], 'entry_zone_id')
		customers_ext_rel_queries = {
			'countries': {
				'type': 'select',
				'query': "SELECT * FROM countries WHERE countries_id IN  " + self.list_to_in_condition(country_ids),
			},
			'zones': {
				'type': 'select',
				'query': "SELECT * FROM  zones WHERE zone_id IN " + self.list_to_in_condition(zone_ids),
			}
		}
		customers_ext_rel = self.get_connector_data(url_query,
		                                            {'serialize': True, 'query': json.dumps(customers_ext_rel_queries)})
		if not customers_ext_rel or customers_ext_rel['result'] != 'success':
			return response_error()
		customers_ext = self.sync_connector_object(customers_ext, customers_ext_rel)
		return customers_ext

	def convert_customer_export(self, customer, customers_ext):
		#customer_data = self.construct_customer()
		customer_data = {
			'phone': '',
			'id': None,
			'code': None,
			'site_id': '',
			'group_id': '',
			'language_id': '',
			'username': '',
			'email': '',
			'password': '',
			'first_name': '',
			'middle_name': '',
			'last_name': '',
			'gender': '',
			'dob': '',
			'is_subscribed': False,
			'active': True,
			'capabilities': list(),
			'created_at': None,
			'updated_at': get_current_time(),
			'address': list(),
			'customers_info_date_account_created': {},
			'customers_info_date_account_last_modified': {},
			'customers_info_date_of_last_logon': {},
			'groups': list(),
			'balance': 0.00,
			'user_url': ''
		}
		customer_data['id'] = customer['customers_id']
		customer_data['username'] = customer['customers_email_address']
		customer_data['email'] = customer['customers_email_address']
		customer_data['password'] = customer['customers_password']
		customer_data['first_name'] = customer['customers_firstname']
		customer_data['last_name'] = customer['customers_lastname']
		customer_data['gender'] = 'Male' if customer['customers_gender'].strip() == 'm' else 'Female'
		customer_data['dob'] = customer['customers_dob']
		customer_data['is_subscribed'] = customer['customers_newsletter']
		customer_data['telephone'] = customer['customers_telephone']
		customer_data['fax'] = customer['customers_fax']
		customer_data['active'] = True

		customer_metadata = get_list_from_list_by_field(customers_ext['data']['customers_info'], 'customers_info_id',
		                                                customer['customers_id'])
		address_books = get_list_from_list_by_field(customers_ext['data']['address_book'], 'customers_id',
		                                            customer['customers_id'])

		if (customer_metadata):

			for data in customer_metadata:
				customer_data['customers_info_date_account_created'] = data['customers_info_date_account_created']
				customer_data['customers_info_date_account_last_modified'] = data['customers_info_date_account_last_modified']
				customer_data['customers_info_date_of_last_logon'] = data['customers_info_date_of_last_logon']

		if address_books:
			for address_book in address_books:
				address_data = self.construct_customer_address()
				address_data['id'] = address_book['address_book_id']
				address_data['first_name'] = address_book['entry_firstname']
				address_data['last_name'] = address_book['entry_lastname']
				address_data['gender'] = 'Male' if address_book["entry_gender"].strip() == 'm' else "Female"
				address_data['address_1'] = address_book['entry_street_address']
				address_data['address_2'] = ''
				address_data['city'] = address_book['entry_city']
				address_data['postcode'] = address_book['entry_postcode']

				address_data['telephone'] = customer['customers_telephone']
				address_data['company'] = address_book['entry_company']
				address_data['fax'] = customer['customers_fax']
				country = get_row_from_list_by_field(customers_ext['data']['countries'], 'countries_id',
				                                     address_book['entry_country_id'])
				if country:
					address_data['country']['id'] = country['countries_id']
					address_data['country']['country_code'] = country['countries_iso_code_2']
					address_data['country']['name'] = country['countries_name']
				else:
					address_data['country']['id'] = address_book['entry_country_id']
				state_id = address_book['entry_state']
				if state_id:
					state = get_row_from_list_by_field(customers_ext['data']['zones'], 'zone_code', state_id)
					if state:
						address_data['state']['id'] = state['zone_id']
						address_data['state']['state_code'] = state['zone_code']
						address_data['state']['name'] = state['zone_name']
					else:
						address_data['state']['id'] = state_id
				else:
					address_data['state']['name'] = 'AL'
				if address_book['address_book_id'] == customer['customers_default_address_id']:
					address_data['default']['billing'] = True
					address_data['default']['shipping'] = True
				customer_data['address'].append(address_data)
		return response_success(customer_data)

	def get_customer_id_import(self, convert, customer, customers_ext):
		return customer['customers_id']

	def check_customer_import(self, convert, customer, customers_ext):
		return True if self.get_map_field_by_src(self.TYPE_CUSTOMER, convert['id'], convert['code']) else False

	def router_customer_import(self, convert, customer, customers_ext):
		return response_success('customer_import')

	def before_customer_import(self, convert, customer, customers_ext):
		return response_success()

	def customer_import(self, convert, customer, customers_ext):
		return response_success(0)

	def after_customer_import(self, customer_id, convert, customer, customers_ext):
		return response_success()

	def addition_customer_import(self, convert, customer, customers_ext):
		return response_success()

	# TODO: ORDER
	def prepare_orders_import(self):
		return self

	def prepare_orders_export(self):
		return self

	def get_orders_main_export(self):
		id_src = self._notice['process']['orders']['id_src']
		limit = 10
		query = {
			'type': 'select',
			'query': "SELECT * FROM  orders WHERE orders_id > " + to_str(
				id_src) + " ORDER BY orders_id ASC LIMIT " + to_str(limit)
		}
		orders = self.get_connector_data(self.get_connector_url('query'), {'query': json.dumps(query)})
		if not orders or orders['result'] != 'success':
			return response_error('could not get orders main to export')
		return orders

	def get_orders_ext_export(self, orders):
		url_query = self.get_connector_url('query')
		order_ids = duplicate_field_value_from_list(orders['data'], 'orders_id')
		bil_country = duplicate_field_value_from_list(orders['data'], 'billing_country')
		delivery_country = duplicate_field_value_from_list(orders['data'], 'delivery_country')
		country_ids = set(bil_country + delivery_country )

		# payment_zone = duplicate_field_value_from_list(orders['data'], 'bill_state')
		# shipping_zone = duplicate_field_value_from_list(orders['data'], 'ship_state')
		# # cus_zone = duplicate_field_value_from_list(orders['data'], 'customers_state')
		# state_ids = set(payment_zone + shipping_zone)
		cus_ids=duplicate_field_value_from_list(orders['data'], 'client_customers_id')
		orders_ext_queries = {
			'order_items': {
				'type': 'select',
				'query': "SELECT * FROM  orders_products WHERE orders_id IN " + self.list_to_in_condition(order_ids)
			},
			'orders_customer': {
				'type': 'select',
				'query': "SELECT * FROM customers WHERE customers_id IN " + self.list_to_in_condition(cus_ids)
			},
			'orders_total': {
				'type': 'select',
				'query': "SELECT * FROM  orders_total WHERE orders_id  IN " + self.list_to_in_condition(order_ids)
			},
			# 'orders_status_history': {
			# 	'type': 'select',
			# 	'query': "SELECT * FROM _DBPRF_orders_status_history"
			# },
			# 'orders_status_history': {
			# 	'type': 'select',
			# 	'query': "SELECT *  FROM _DBPRF_orders_status_history WHERE orders_id IN  " + self.list_to_in_condition(
			# 		order_ids) + " ORDER BY orders_status_history_id DESC"
			# },
			# 'countries': {
			# 	'type': 'select',
			# 	'query': "SELECT * FROM Countries WHERE alpha IN " + self.list_to_in_condition(country_ids)
			# },

			# 'zones': {
			# 	'type': 'select',
			# 	'query': "SELECT * FROM  _DBPRF_States WHERE code IN " + self.list_to_in_condition(state_ids)
			# }
		}
		orders_ext = self.get_connector_data(url_query, {'serialize': True, 'query': json.dumps(orders_ext_queries)})
		if not orders_ext or orders_ext['result'] != 'success':
			return response_error()
		return orders_ext

	def convert_order_export(self, order, orders_ext):
		order_data = self.construct_order()
		order_data['id'] = order['orders_id']
		order_data['status'] = order['orders_status']

		order_total = get_list_from_list_by_field(orders_ext['data']['orders_total'], 'orders_id', order[
			'orders_id'])
		tax_total = 0.0
		total_ship = 0.0
		subtotal_amount = 0.0
		total_amount = 0.0
		for cv_order in order_total:
			if cv_order['class'] == 'ot_tax':
				tax_total += to_decimal(float(cv_order['value']))
			if cv_order['class'] == 'ot_shipping':
				total_ship += to_decimal(float(cv_order['value']))
			if cv_order['class'] == 'ot_subtotal':
				subtotal_amount += to_decimal(float(cv_order['value']))
			if cv_order['class'] == 'ot_total':
				total_amount += to_decimal(float(cv_order['value']))
		# 	order_data['tax']['title'] = ot_tax['title']
		# 	order_data['tax']['amount'] = ot_tax['value']
		# 	if ot_subtotal:
		# 		order_data['tax']['percent'] = to_decimal(ot_tax['value']) / to_decimal(ot_subtotal['value'])
		order_data['client_customers_id'] = order['client_customers_id']
		order_data['id'] = order['orders_id']
		order_data['order_number'] = order['order_number']
		order_data['status'] = order['orders_status']
		order_data['tax']['title'] = 'Tax'
		order_data['tax']['amount'] = tax_total
		order_data['shipping']['title'] = 'Shipping'
		order_data['shipping']['amount'] = total_ship
		order_data['discount']['title'] = 'Discount'
		order_data['discount']['amount'] = 0.0000
		order_data['total']['title'] = 'Total'
		order_data['total']['amount'] = total_amount
		order_data['subtotal']['title'] = 'Total products'
		order_data['subtotal']['amount'] = subtotal_amount
		order_data['currency'] = order['currency']
		order_data['created_at'] = order['date_purchased'] or datetime.fromtimestamp(
			to_int(get_value_by_key_in_dict(order, 'date_purchased', 0))).strftime('%Y-%m-%d %H:%M:%S')


		#currency = get_row_value_from_list_by_field(orders_ext['data']['currencies'], 'code', order['currency'], 'currencies_id')
		# order_data['currency'] = order['currency']
		# order_data['currency_value'] = order['currency_value']
		# order_data['created_at'] = order['date_purchased']
		# order_data['updated_at'] = order['last_modified']
		customers = get_list_from_list_by_field(orders_ext['data']['orders_customer'], 'customers_id', order['client_customers_id'])
		order_customer = self.construct_order_customer()
		#order_customer = self.add_c(order_customer)
		if customers:
			order_customer['id'] = order['client_customers_id']
			order_customer['email'] = order['customers_email']
			order_customer['username'] = order['delivery_name']
			order_customer['first_name'] = customers['customers_firstname']
			order_customer['last_name'] = customers['customers_lastname']
		else:
			order_customer = self.construct_order_customer()
			order_customer['id'] = order['client_orders_id']
			order_customer['email'] = order['customers_email']
			order_customer['first_name'] = order['delivery_name'].strip().split()[0]
			order_customer['last_name'] = order['delivery_name'].strip().split()[-1]
		order_data['customer'] = order_customer

		customer_address = self.construct_order_address()
		#customer_address = self.addConstructDefault(customer_address)
		if customers:
			customer_address['first_name'] = customers['customers_firstname']
			customer_address['last_name'] = customers['customers_lastname']
			customer_address['address_1'] = order['delivery_address1']
			customer_address['address_2'] = order['delivery_address2']
			customer_address['city'] = customers['delivery_city']
			customer_address['postcode'] = order['delivery_postcode']
			customer_address['telephone'] = customers['customers_telephone']
			customer_address['company'] = order['delivery_company']
		else:
			customer_address = self.construct_order_address()
			customer_address['address_1'] = order['delivery_address1']
			customer_address['address_2'] = order['delivery_address2']
			customer_address['city'] = order['delivery_city']
			customer_address['postcode'] = order['delivery_postcode']
			customer_address['telephone'] = order['customers_telephone']
			customer_address['company'] = order['delivery_company']
			customer_address['state']['name'] = order['delivery_state']
			customer_address['country']['name'] = order['delivery_country']

		order_data['customer_address'] = customer_address



		order_billing = self.construct_order_address()
		#order_billing = this->addConstructDefault(order_billing)
		# billing_name = self.get_name_from_string(order['bill_fname'] + ' '+ order['bill_lname'])
		order_billing['first_name'] = order['delivery_name']
		# order_billing['last_name'] = order['customers_lastname']
		order_billing['address_1'] = order['billing_address1']
		order_billing['address_2'] = order['billing_address2']
		order_billing['city'] = order['billing_city']
		order_billing['postcode'] = order['billing_postcode']
		order_billing['telephone'] = order['customers_telephone']
		order_billing['company'] = order['billing_company']

		order_data['billing_address'] = order_billing



		order_delivery = self.construct_order_address()
		#order_delivery = self.addConstructDefault(order_delivery)
		# delivery_name = self.get_name_from_string(order['ship_fname'] + ' ' + order['ship_lname'])
		order_delivery['first_name'] = order['delivery_name']
		# order_delivery['last_name'] = customers['customers_lastname']
		order_delivery['address_1'] = order['delivery_name']
		order_delivery['address_2'] = order['delivery_address2']
		order_delivery['city'] = order['delivery_city']
		order_delivery['postcode'] = order['delivery_postcode']
		order_delivery['telephone'] = order['customers_telephone']
		order_delivery['company'] = order['delivery_company']
		order_delivery['country']['name'] = order['delivery_country']
		order_delivery['state']['state'] = order['delivery_state']

		order_delivery = self._cook_shipping_address_by_billing(order_delivery, order_billing)
		order_data['shipping_address'] = order_delivery


		payments = get_row_from_list_by_field(orders_ext['data']['orders_total'], 'orders_id', order['orders_id'])
		order_payment = self.construct_order_payment()
		order_payment['title'] = payments['title']
		order_data['payment'] = order_payment

		order_products = get_list_from_list_by_field(orders_ext['data']['order_items'], 'orders_id', order['orders_id'])
		# order_product_attributes = get_list_from_list_by_field(orders_ext['data']['orders_products_attributes'], 'orders_id', order['orders_id'])
		order_items = list()
		for order_product in order_products:
			order_item_subtotal = to_decimal(order_product['products_price']) * to_decimal(order_product['products_quantity'])
			order_item_tax = to_decimal(order_item_subtotal) * to_decimal(8.250) / 100
			order_item_total = to_decimal(order_item_subtotal) + to_decimal(order_item_tax)
			order_item = self.construct_order_item()
			#order_item = self.addConstructDefault(order_item)
			order_item['id'] = order_product['orders_id']
			order_item['product']['id'] = order_product['orders_products_id']
			order_item['product']['name'] = order_product['products_name']
			order_item['product']['sku'] = order_product['products_upc_code']
			order_item['qty'] = order_product['products_quantity']
			order_item['price'] = order_product['products_price']
			order_item['original_price'] = order_product['final_price']
			order_item['discount_amount'] = '0.0000'
			order_item['discount_percent'] = '0.0000'
			order_item['subtotal'] = order_item_subtotal
			order_item['total'] = order_item_subtotal

			order_items.append(order_item)
		order_data['items'] = order_items

		return response_success(order_data)

	def get_order_id_import(self, convert, order, orders_ext):
		return order['orders_id']

	def check_order_import(self, convert, order, orders_ext):
		return True if self.get_map_field_by_src(self.TYPE_ORDER, convert['id'], convert['code']) else False

	def router_order_import(self, convert, order, orders_ext):
		return response_success('order_import')

	def before_order_import(self, convert, order, orders_ext):
		return response_success()

	def order_import(self, convert, order, orders_ext):
		return response_success(0)

	def after_order_import(self, order_id, convert, order, orders_ext):
		return response_success()

	def addition_order_import(self, convert, order, orders_ext):
		return response_success()

	# TODO: REVIEW
	def prepare_reviews_import(self):
		return self

	def prepare_reviews_export(self):
		return self

	def get_reviews_main_export(self):
		id_src = self._notice['process']['reviews']['id_src']
		limit = self._notice['setting']['reviews']
		query = {
			'type': 'select',
			'query': "SELECT * FROM _DBPRF_reviews WHERE reviews_id > " + to_str(
				id_src) + " ORDER BY reviews_id ASC LIMIT " + to_str(limit)
		}
		reviews = self.get_connector_data(self.get_connector_url('query'), {'query': json.dumps(query)})
		if not reviews or reviews['result'] != 'success':
			return response_error('could not get manufacturers main to export')
		return reviews

	def get_reviews_ext_export(self, reviews):
		url_query = self.get_connector_url('query')
		reviews_id = duplicate_field_value_from_list(reviews['data'], 'reviews_id')
		product_ids = duplicate_field_value_from_list(reviews['data'], 'products_id')
		reviews_ext_queries = {
			'products_description': {
				'type': 'select',
				'query': "SELECT products_id, language_id, products_name FROM _DBPRF_products_description WHERE products_id IN " + self.list_to_in_condition(
					product_ids)
			},
			'reviews_description': {
				'type': 'select',
				'query': "SELECT * FROM _DBPRF_reviews_description WHERE reviews_id IN " + self.list_to_in_condition(
					reviews_id)
			},
		}
		reviews_ext = self.get_connector_data(url_query, {
			'serialize': True,
			'query': json.dumps(reviews_ext_queries)
		})

		if not reviews_ext or reviews_ext['result'] != 'success':
			return response_warning()
		return reviews_ext

	def convert_review_export(self, review, reviews_ext):
		review_data = self.construct_review()
		default_language = self._notice['src']['language_default']
		review_data['id'] = review['reviews_id']
		review_data['language_id'] = default_language
		review_description = get_row_from_list_by_field(reviews_ext['data']['reviews_description'], 'reviews_id', review['reviews_id'])
		if not review_description:
			return response_warning(self.warning_import_entity('Review', review['reviews_id'], None, 'Review data not exists.'))
		language_id = review_description['languages_id'] if review_description['languages_id'] else default_language
		product_descriptions = get_list_from_list_by_field(reviews_ext['data']['products_description'], 'products_id', review['products_id'])
		product_description = get_row_from_list_by_field(product_descriptions, 'language_id', language_id)
		if not product_description:
			product_description = get_row_from_list_by_field(product_descriptions, 'language_id', default_language)
		rv_status = {
			0: 2,  # pedding
			1: 1,  # approved
			3: 2  # not approved
		}
		review_data['language_id'] = language_id
		review_data['product']['id'] = review['products_id']
		review_data['product']['name'] = product_description['products_name'] if product_description else ' '
		review_data['customer']['id'] = review['customers_id']
		review_data['customer']['name'] = review['customers_name']
		review_data['title'] = ' '
		review_data['content'] = review_description['reviews_text']
		review_data['status'] = get_value_by_key_in_dict(rv_status, to_int(review['reviews_status']), 1) if 'reviews_status' in review else 1
		review_data['created_at'] = review['date_added']
		review_data['updated_at'] = review['last_modified']

		rating = self.construct_review_rating()
		rating['rate_code'] = 'default'
		rating['rate'] = review['reviews_rating']
		review_data['rating'].append(rating)
		return response_success(review_data)

	def get_review_id_import(self, convert, review, reviews_ext):
		return review['reviews_id']

	def check_review_import(self, convert, review, reviews_ext):
		return True if self.get_map_field_by_src(self.TYPE_REVIEW, convert['id'], convert['code']) else False

	def router_review_import(self, convert, review, reviews_ext):
		return response_success('review_import')

	def before_review_import(self, convert, review, reviews_ext):
		return response_success()

	def review_import(self, convert, review, reviews_ext):
		product_id = False
		if convert['product']['id'] or convert['product']['code']:
			product_id = self.get_map_field_by_src(self.TYPE_PRODUCT, convert['product']['id'],
			                                       convert['product']['code'])
		if not product_id:
			response_warning('Review ' + to_str(convert['id']) + ' import false. Product does not exist!')
		customer_id = 0
		if convert['customer']['id'] or convert['customer']['code']:
			customer_id = self.get_map_field_by_src(self.TYPE_CUSTOMER, convert['customer']['id'],
			                                        convert['customer']['code'])
			if not customer_id:
				customer_id = 0
		review_data = {
			'product_id': product_id,
			'customer_id': customer_id,
			'author': convert['customer']['name'] if convert['customer']['name'] else '',
			'rating': self.calculate_average_rating(convert['rating']),
			'date_added': convert['created_at'],
			'date_modified': convert['updated_at'],
			'status': 1 if convert['status'] else 0,
			'text': convert['content']
		}
		review_id = self.import_review_data_connector(self.create_insert_query_connector('review', review_data), True, convert['id'])
		if not review_id:
			response_warning('review id ' + to_str(convert['id']) + ' import false.')
			self.insert_map(self.TYPE_REVIEW, convert['id'], review_id, convert['code'])
		return response_success(review_id)

	def after_review_import(self, review_id, convert, review, reviews_ext):
		return response_success()

	def addition_review_import(self, convert, review, reviews_ext):
		return response_success()

	# TODO: PAGE
	def prepare_pages_import(self):
		return self

	def prepare_pages_export(self):
		return self

	def get_pages_main_export(self):
		return response_success()

	def get_pages_ext_export(self, pages):
		return response_success()

	def convert_page_export(self, page, pages_ext):
		return response_success()

	def get_page_id_import(self, convert, page, pages_ext):
		return False

	def check_page_import(self, convert, page, pages_ext):
		return False

	def router_page_import(self, convert, page, pages_ext):
		return response_success('page_import')

	def before_page_import(self, convert, page, pages_ext):
		return response_success()

	def page_import(self, convert, page, pages_ext):
		return response_success(0)

	def after_page_import(self, page_id, convert, page, pages_ext):
		return response_success()

	def addition_page_import(self, convert, page, pages_ext):
		return response_success()

	# TODO: BLOCK
	def prepare_blogs_import(self):
		return response_success()

	def prepare_blogs_export(self):
		return self

	def get_blogs_main_export(self):
		return self

	def get_blogs_ext_export(self, blocks):
		return response_success()

	def convert_blog_export(self, block, blocks_ext):
		return response_success()

	def get_blog_id_import(self, convert, block, blocks_ext):
		return False

	def check_blog_import(self, convert, block, blocks_ext):
		return False

	def router_blog_import(self, convert, block, blocks_ext):
		return response_success('block_import')

	def before_blog_import(self, convert, block, blocks_ext):
		return response_success()

	def blog_import(self, convert, block, blocks_ext):
		return response_success(0)

	def after_blog_import(self, block_id, convert, block, blocks_ext):
		return response_success()

	def addition_blog_import(self, convert, block, blocks_ext):
		return response_success()

	# todo: code opencart
	def _list_to_in_condition_product(self, products):
		if not products:
			return "('null')"
		products = list(map(self.escape, products))
		products = list(map(lambda x: to_str(x), products))
		res = "','product_id=".join(products)
		res = "('product_id=" + res + "')"
		return res

	def product_to_in_condition_seourl(self, ids):
		if not ids:
			return "('null')"
		result = "('product_id=" + "','product_id=".join([str(id) for id in ids]) + "')"
		return result

	def category_to_in_condition_seourl(self, ids):
		if not ids:
			return "('null')"
		result = "('category_id=" + "','category_id=".join([str(id) for id in ids]) + "')"
		return result

	def get_category_parent(self, category_id):
		query = {
			'type': 'select',
			'query': "SELECT * FROM  categories WHERE categories_id = " + to_str(category_id)
		}
		categories = self.get_connector_data(self.get_connector_url('query'), {'query': json.dumps(query)})
		if not categories or categories['result'] != 'success':
			return response_error('could not get category parent to export')
		if categories and categories['data']:
			category = categories['data'][0]
			categories_ext = self.get_categories_ext_export(categories)
			category_convert = self.convert_category_export(category, categories_ext)
			return category_convert
		return response_error('could not get category parent to export')

	def import_category_parent(self, convert_parent):
		parent_exists = self.get_map_field_by_src(self.TYPE_CATEGORY, convert_parent['id'], convert_parent['code'])
		if parent_exists:
			return response_success(parent_exists)
		category = convert_parent['category']
		categories_ext = convert_parent['categories_ext']
		category_parent_import = self.category_import(convert_parent, category, categories_ext)
		self.after_category_import(category_parent_import['data'], convert_parent, category, categories_ext)
		return category_parent_import

	def nl2br(self, string, is_xhtml=True):
		if is_xhtml:
			return string.replace('\n', '<br />\n')
		else:
			return string.replace('\n', '<br>\n')

	def get_country_id(self, code, name):
		query = 'SELECT country_id FROM `_DBPRF_country` '
		if code:
			query = query + ' WHERE iso_code_2 = "' + to_str(code) + '"'
		elif name:
			query = query + ' WHERE name = "' + to_str(name) + '"'
		countries_query = {
			'type': 'select',
			'query': query
		}
		countries = self.get_connector_data(self.get_connector_url('query'), {'query': json.dumps(countries_query)})
		if not countries or countries['result'] != 'success' or not countries['data']:
			return 0
		return countries['data'][0]['country_id']

	def get_state_id(self, code, name):
		query = 'SELECT zone_id FROM `_DBPRF_zone` '
		if code:
			query = query + ' WHERE code = "' + to_str(code) + '"'
		elif name:
			query = query + ' WHERE name = "' + to_str(name) + '"'
		zones_query = {
			'type': 'select',
			'query': query
		}
		zones = self.get_connector_data(self.get_connector_url('query'), {'query': json.dumps(zones_query)})
		if not zones or zones['result'] != 'success' or not zones['data']:
			return 0
		return zones['data'][0]['zone_id']

	def calculate_average_rating(self, rates, default='default'):
		rate = get_row_from_list_by_field(rates, 'rate_code', default)
		if rate and 'rate' in rate:
			return rate['rate']
		rate_total = 0
		count = to_len(rates)
		for _rate in rates:
			rate_total = rate_total + to_decimal(_rate['rate'])
		average = to_decimal(rate_total / count)
		if average > 5:
			return 5
		else:
			return math.ceil(average)

	def get_name_from_string(self, value):
		result = dict()
		parts = value.split(' ')
		result['lastname'] = parts.pop()
		result['firstname'] = " ".join(parts)
		return result

	def _cook_shipping_address_by_billing(self, shipping_address, billing_address):
		for key, value in shipping_address.items():
			if key in {'country', 'state'}:
				for child_key, child_value in shipping_address[key].items():
					if not shipping_address[key][child_key]:
						shipping_address[key][child_key] = billing_address[key][child_key]
			else:
				if not shipping_address[key]:
					shipping_address[key] = billing_address[key]

		return shipping_address

	def convert_float_to_percent(self, value):
		return value * 100

	def get_con_store_select(self):
		select_store = self._notice['src']['languages_select'].copy()
		src_store = self._notice['src']['languages'].copy()
		if self._notice['src']['language_default'] not in select_store:
			select_store.append(self._notice['src']['language_default'])
		src_store_ids = list(src_store.keys())
		unselect_store = [item for item in src_store_ids if item not in select_store]
		select_store.append(0)
		if to_len(select_store) >= to_len(unselect_store):
			where = ' IN ' + self.list_to_in_condition(select_store) + ' '
		else:
			where = ' NOT IN ' + self.list_to_in_condition(unselect_store) + ' '

		return where

	def detect_seo(self):
		return 'default_seo'
	def categories_default_seo(self, category, categories_ext):
		result = list()
		type_seo = self.SEO_301
		category_url = get_list_from_list_by_field(categories_ext['data']['URIs'],'cat_id', category['id'])
		seo_cate = self.construct_seo_category()
		if category_url:
			for cate_url in category_url:
				seo_cate['request_path'] = cate_url['uri']
				seo_cate['default'] = True
				seo_cate['type'] = type_seo
				result.append(seo_cate)


		return result

	def products_default_seo(self, product, products_ext):
		result = list()
		type_seo = self.SEO_301
		category_url = get_list_from_list_by_field(products_ext['data']['URIs'], 'cat_id', product['id'])
		seo_cate = self.construct_seo_product()
		if category_url:
			for cate_url in category_url:
				seo_cate['request_path'] = cate_url['uri']
				seo_cate['default'] = True
				seo_cate['type'] = type_seo
				result.append(seo_cate)

		return result

	def to_url(self, name):
		new_name = re.sub(r"[^a-zA-Z0-9-. ]", '', name)
		new_name = new_name.replace(' ', '-')
		url = new_name.lower()
		return url
