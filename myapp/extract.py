import numpy as np
from flask import url_for
import os, sys, math
from skimage import io,transform
caffe_root = '/home/deepcare/Documents/caffe/'
sys.path.insert(0, caffe_root + 'python')
import caffe

class extractor:
    def __init__(self, scale):
        '''
        if scale == '400':
            caffe_model = '/home/deepcare/Documents/caffe/models/retrival_tumor/finetune/voc_48_iter_20000.caffemodel'
            mean_npy_file = caffe_root + 'models/retrival_tumor/mean_train.npy'
            net_file = caffe_root +'models/retrival_tumor/deploy.prototxt'
            self.net = caffe.Net(net_file, caffe_model, caffe.TEST)
            self.transformer = caffe.io.Transformer({'data': self.net.blobs['data'].data.shape})
            self.transformer.set_transpose('data', (2,0,1))
            self.transformer.set_mean('data', np.load(mean_npy_file).mean(1).mean(1))
            self.transformer.set_raw_scale('data', 255)
            self.transformer.set_channel_swap('data', (2,1,0))
        elif scale == '100':
            caffe_model = '/home/deepcare/Documents/caffe/models/retrival_tumor_m/finetune/voc_48_iter_20000.caffemodel'
            mean_npy_file = caffe_root + 'models/retrival_tumor_m/mean_train.npy'
            net_file = caffe_root +'models/retrival_tumor_m/deploy.prototxt'
            self.net = caffe.Net(net_file, caffe_model, caffe.TEST)
            self.transformer = caffe.io.Transformer({'data': self.net.blobs['data'].data.shape})
            self.transformer.set_transpose('data', (2,0,1))
            self.transformer.set_mean('data', np.load(mean_npy_file).mean(1).mean(1))
            self.transformer.set_raw_scale('data', 255)
            self.transformer.set_channel_swap('data', (2,1,0))
        else:
            caffe_model = '/home/deepcare/Documents/caffe/models/retrival_tumor_m/finetune/voc_48_iter_20000.caffemodel'
            mean_npy_file = caffe_root + 'models/retrival_tumor_m/mean_train.npy'
            net_file = caffe_root +'models/retrival_tumor_m/deploy.prototxt'
            self.net = caffe.Net(net_file, caffe_model, caffe.TEST)
            self.transformer = caffe.io.Transformer({'data': self.net.blobs['data'].data.shape})
            self.transformer.set_transpose('data', (2,0,1))
            self.transformer.set_mean('data', np.load(mean_npy_file).mean(1).mean(1))
            self.transformer.set_raw_scale('data', 255)
            self.transformer.set_channel_swap('data', (2,1,0))
        '''
        caffe_model = '/home/deepcare/Documents/caffe/models/retrival_tumor/finetune/voc_48_iter_20000.caffemodel'
        mean_npy_file = caffe_root + 'models/retrival_tumor/mean_train.npy'
        net_file = caffe_root +'models/retrival_tumor/deploy.prototxt'
        self.net = caffe.Net(net_file, caffe_model, caffe.TEST)
        self.transformer = caffe.io.Transformer({'data': self.net.blobs['data'].data.shape})
        self.transformer.set_transpose('data', (2,0,1))
        self.transformer.set_mean('data', np.load(mean_npy_file).mean(1).mean(1))
        self.transformer.set_raw_scale('data', 255)
        self.transformer.set_channel_swap('data', (2,1,0))

        caffe.set_mode_cpu()

    def extract_features(self, image):
        img_large = transform.resize(image, (256, 256))
        img = img_large[15 : 15 + 227, 15 : 15 + 227, :]
        self.net.blobs['data'].data[...] = self.transformer.preprocess('data', img)
        self.net.forward()
        fine = self.net.blobs['fc7'].data[0]
        fine_list = [repr(x) for x in fine]
        self.fine_str = ';'.join(fine_list)
        coarse = self.net.blobs['fc8_encode'].data[0]
        self.coarse_str = self.list2str(coarse)
        res_list = self.net.blobs['fc8_new'].data[0]
        exp_list = [math.exp(x) for x in res_list]
        exp_sum = sum(exp_list)
        res_list = ['%.1f'%(x/exp_sum*100,) for x in exp_list ]
        res_dict = dict()
        idx = 0
        for res in res_list:
            res_dict[idx] = []
            res_dict[idx].append(res)
            idx += 1
        return self.fine_str, self.coarse_str,res_dict

    def list2str(self, list1):
        len_list = len(list1)
        binary_code = [ '1' for x in xrange(len_list)]
        for i in xrange(len_list):
            if list1[i] >= 0.5:
                binary_code[i] = '1'
            else:
                binary_code[i] = '0'
        res_str = ''.join(binary_code)
        return res_str

    def sortDict(self, adict):
        keys = adict.keys()
        keys.sort()
        return map(adict.get, keys)

