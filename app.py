from flask import jsonify, request, render_template, Flask, url_for

import config, logger, models, service, bd

import datetime
import sys

def build_visit_href(endpoint:str) -> str:
	return f"visit http://127.0.0.1:5000/{endpoint}/index"

def get_date_now() -> str:
	return f"   {datetime.datetime.now().date()}"

class WebApp():
	def __init__(self, conf:config.Config, log:logger.Logger, ctrlbd:bd.ControlBD) -> None:
		self.app = Flask(__name__)
		self.conf = conf
		self.log = log
		self.ctrlbd = ctrlbd
		self.collection_page_blog = models.PageModelDialog(self.conf.get("bd_file"), 5)
		self.set_routes()

	def launch(self) -> None:
		self.app.run(debug=False)

	def set_routes(self) -> str:
		data_temp_blog = models.DataTemplateBlog()

		@self.app.route('/blog/prev')
		def blog_prev():
			self.log.add(build_visit_href("blog/prev"))
			self.collection_page_blog.now_page -= 1
			collect = self.collection_page_blog.get_list_items_dialog()
			return render_template(
				'blog.html', 
				collection_data_blog = collect, 
				collection_data_index_new_1 = self.collection_page_blog.get_list_items_dialog_random(5),
				collection_data_index_new_2 = self.collection_page_blog.get_list_items_dialog_random(5),
				data_template_blog=data_temp_blog,
				date_now = get_date_now())

		@self.app.route('/blog/next')
		def blog_nex():
			self.log.add(build_visit_href("blog/next"))
			self.collection_page_blog.now_page += 1
			collect = self.collection_page_blog.get_list_items_dialog()
			return render_template(
				'blog.html', 
				collection_data_blog = collect, 
				collection_data_index_new_1 = self.collection_page_blog.get_list_items_dialog_random(5),
				data_template_blog=data_temp_blog,
				date_now = get_date_now())
				
		@self.app.route('/blog')
		async def blog():
			self.log.add(build_visit_href("blog/"))
			collect = self.collection_page_blog.get_list_items_dialog()
			return render_template(
				'blog.html', 
				collection_data_blog = collect, 
				collection_data_index_new_1 = self.collection_page_blog.get_list_items_dialog_random(5),
				data_template_blog=data_temp_blog,
				date_now = get_date_now())

		@self.app.route('/single')
		def single():
			collect = self.collection_page_blog.get_list_items_dialog()
			return render_template(
				'blog.html', 
				collection_data_blog = collect, 
				collection_data_index_new_1 = self.collection_page_blog.get_list_items_dialog_random(5),
				data_template_blog=data_temp_blog,
				date_now = get_date_now())

		@self.app.route('/single/<id>')
		def single_name(id):
			self.log.add(build_visit_href("single/"+id))
			collect_single = self.collection_page_blog.get_item_dialog(id)
			collect_trend = self.collection_page_blog.get_list_items_dialog_random(5)
			return render_template('single.html', 
			collection_data_single = collect_single, 
			collection_data_single_trend=collect_trend,
			date_now = get_date_now())

		@self.app.route('/index')
		def index():
			self.log.add(build_visit_href("index"))
			di = self.collection_page_blog.get_list_items_dialog_random(5)
			di1 = di[0]
			di2 = di[1]
			di3 = di[2]
			di4 = di[3]
			di5 = di[4]
			return render_template('index.html',
			date_now = get_date_now(),

			di1_image = di1['image'],
			di1_date = di1['date_create'],
			di1_id = di1['id'],
			di1_name = di1['name'],

			di2_image = di2['image'],
			di2_date = di2['date_create'],
			di2_id = di2['id'],
			di2_name = di2['name'],

			di3_image = di3['image'],
			di3_date = di3['date_create'],
			di3_id = di3['id'],
			di3_name = di3['name'],

			di4_image = di4['image'],
			di4_date = di4['date_create'],
			di4_id = di4['id'],
			di4_name = di4['name'],

			di5_image = di5['image'],
			di5_date = di5['date_create'],
			di5_id = di5['id'],
			di5_name = di5['name'],

			collection_data_index_new_1 = self.collection_page_blog.get_list_items_dialog_random(10),
			collection_data_index_new_2 = self.collection_page_blog.get_list_items_dialog_random(5),
			collection_data_index_new_3 = self.collection_page_blog.get_list_items_dialog_random(5),
			)

		@self.app.route('/Contact_us')
		def Contact_us():
			self.log.add(build_visit_href("Contact_us"))
			return render_template('Contact_us.html',
			date_now = get_date_now())

def main():
	if len(sys.argv)>1:
		arg_namefile_config = sys.argv[1]
		conf = config.Config(sys.argv[1])
		log = logger.Logger(conf)
		ctrlbd = bd.ControlBD(conf)
		webapp = WebApp(conf, log, ctrlbd)
		webapp.launch()
	else:
		print("enter setup-params for file")
		return

main()