from flask import jsonify, request, render_template, Flask, url_for
import threading
import queue

import service_dialogs as tua
import models, asyncio, os
import datetime


def visit_pref(endpoint):
	return f"visit http://127.0.0.1:5000/{endpoint}/index"

def get_date_now():
	return f"  {datetime.datetime.now().date()}"

class Service():
	def __init__(self):
		 pass 
	def bash(self, line):
		os.system('ls')
	def read_list_dialogs(self):
		bash("python service_dialogs.py > service_dialogs.txt")



class WebApp():
	def __init__(self,conf, logger, jsonfile):
		self.app = Flask(__name__)
		self.conf = conf
		self.ctrl = Service()
		self.logger = logger
		self.collection_page_blog = models.PageModelLastDialog(jsonfile)
		self.set_routes()

	def launch(self):
		self.app.run(debug=False)

	def set_routes(self):
		dtb = models.DataTemplateBlog()

		@self.app.route('/blog/prev')
		def blog_prev():
			self.logger.add(visit_pref("blog/prev"))
			self.collection_page_blog.now_page -= 1
			collect = self.collection_page_blog.get_page()
			return render_template(
				'blog.html', 
				collection_data_blog = collect, 
				collection_data_index_new_1 = self.collection_page_blog.get_random_collect(5),
				collection_data_index_new_2 = self.collection_page_blog.get_random_collect(5),
				data_template_blog=dtb,
				date_now = get_date_now())

		@self.app.route('/blog/next')
		def blog_nex():
			self.logger.add(visit_pref("blog/next"))
			self.collection_page_blog.now_page += 1
			collect = self.collection_page_blog.get_page()
			return render_template(
				'blog.html', 
				collection_data_blog = collect, 
				collection_data_index_new_1 = self.collection_page_blog.get_random_collect(5),
				data_template_blog=dtb,
				date_now = get_date_now())
				
		@self.app.route('/blog')
		async def blog():
			self.logger.add(visit_pref("blog/"))
			collect = self.collection_page_blog.get_page()
			return render_template(
				'blog.html', 
				collection_data_blog = collect, 
				collection_data_index_new_1 = self.collection_page_blog.get_random_collect(5),
				data_template_blog=dtb,
				date_now = get_date_now())

		@self.app.route('/single')
		def single():
			id = randint(0,5)
			self.logger.add(visit_pref("single/"+id))
			collect_single = self.collection_page_blog.get_obj_from_id(id)
			collect_trend = self.collection_page_blog.get_random_collect()
			return render_template('single.html', 
			collection_data_single = collect_single, 
			collection_data_single_trend=collect_trend,
			date_now = get_date_now())

		@self.app.route('/single/<id>')
		def single_name(id):
			self.logger.add(visit_pref("single/"+id))
			collect_single = self.collection_page_blog.get_obj_from_id(id)
			collect_trend = self.collection_page_blog.get_random_collect()
			return render_template('single.html', 
			collection_data_single = collect_single, 
			collection_data_single_trend=collect_trend,
			date_now = get_date_now())

		@self.app.route('/index')
		def index():
			self.logger.add(visit_pref("index"))
			di = self.collection_page_blog.get_random_collect(5)
			di1 = di[0]
			di2 = di[1]
			di3 = di[2]
			di4 = di[3]
			di5 = di[4]
			# print(di1)
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

			collection_data_index_new_1 = self.collection_page_blog.get_random_collect(10),
			collection_data_index_new_2 = self.collection_page_blog.get_random_collect(5),
			collection_data_index_new_3 = self.collection_page_blog.get_random_collect(5),
			)

		@self.app.route('/Contact_us')
		def Contact_us():
			self.logger.add(visit_pref("Contact_us"))
			return render_template('Contact_us.html',
			date_now = get_date_now())


		
conf = tua.Config()
logger = tua.Logger(conf.data["log_file"])
# ctrl = tua.ControlAPI(conf.data["api_hash"], conf.data["api_id"], logger)
webapp = WebApp(conf, logger, "test.json")

def main():
	webapp.launch()

main()