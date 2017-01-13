import os
from myapp import app, caffe_net_500_vae
from flask import render_template
from flask import request,Response,send_file,url_for,redirect
from skimage import io
from werkzeug import secure_filename
from database import database
from details import Details

@app.route('/')
def search_image():
    return render_template('upload.html')

@app.route('/upload',methods=['GET','POST'])
def upload():
	file = request.files['image']
	scale = request.form.get('scale')
	scale = str(scale)
	if file:
		filename = secure_filename(file.filename)
		file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
		img = io.imread(file)
		pre_folder = 'camelyon16/'
		database_name = 'camelyon16'
        '''
		if scale == '400':
			fine_str, coarse_str, res_dict = caffe_net_500_vae.extract_features(img)
			pre_folder = 'train_l/'
			database_name = 'lung_l'
		else :
			pre_folder = 'train_m/'
			database_name = 'lung_m'
			fine_str, coarse_str, res_dict = caffe_net_m.extract_features(img)
        '''
        fine_str, coarse_str = caffe_net_500_vae.extract_features(img)

        data_dealer = database()
		#types_tumor = data_dealer.get_types_tumor()
		files = data_dealer.search_top(coarse_str, fine_str, 5, scale)
		res_files = []
		for file in files:
			res_file = []
			res_file.append(url_for('static',filename='%s'%pre_folder + file[0]))
			res_file.append(file[1])
			res_file.append(database_name)
			res_files.append(res_file)
		return render_template('result.html',ori_file=url_for('static',filename='upload_images/' + filename), res_files=res_files)
	return redirect(url_for('search_image'))
@app.route('/results/<database_name>/<image_name>', methods=['GET'])
def show_details(database_name,image_name):
	details = Details()
	res_list = details.get_details(database_name,image_name)
	return render_template('details.html',res_list=res_list)
