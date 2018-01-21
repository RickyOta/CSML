from train import train_step
from infer import infer_step

import configparser
import sys


# start segmentation based on .ini
def Cell_Segmentation():
	
	if len(sys.argv) != 2:
		raise SyntaxError("Expect: 2 args Actual: {0} args.".format(len(sys.argv)))

	config = configparser.ConfigParser()
	config.read(sys.argv[1])
	
	if sys.argv[1] == 'train_infer.ini':
		fname_train = "data/" + config['paths']['filename train']
		fname_label = "data/" + config['paths']['filename label']
		fname_model = "data/" + config['paths']['filename model']
		fname_infer = "data/" + config['paths']['filename infer']
		fname_save = "data/" + config['paths']['filename save']
		
		N_train = int(config['training parameters']['number train'])
		N_test = int(config['training parameters']['number test'])
		N_epoch = int(config['default']['number epoch'])
		batchsize = int(config['default']['number batch'])
		hgh = int(config['training parameters']['height'])
		wid = int(config['training parameters']['width'])
		
		thre_discard = int(config['inference parameters']['threshold discard'])
		wid_dilate = int(config['inference parameters']['width dilate'])
		thre_fill = int(config['inference parameters']['threshold fill'])
		
		train_step(fname_train=fname_train, fname_label=fname_label, fname_model=fname_model, N_test=N_test, N_train=N_train, N_epoch=N_epoch, batchsize=batchsize, hgh=hgh, wid=wid)
		infer_step(fname_infer=fname_infer, fname_save=fname_save, fname_model=fname_model, thre_discard=thre_discard, wid_dilate=wid_dilate, thre_fill=thre_fill)
		print("all done.")
		
	elif sys.argv[1] == 'infer.ini':
		fname_model = "data/" + config['paths']['filename model']
		fname_infer = "data/" + config['paths']['filename infer']
		fname_save = "data/" + config['paths']['filename save']
		
		thre_discard = int(config['inference parameters']['threshold discard'])
		wid_dilate = int(config['inference parameters']['width dilate'])
		thre_fill = int(config['inference parameters']['threshold fill'])
		
		infer_step(fname_infer=fname_infer, fname_save=fname_save, fname_model=fname_model, thre_discard=thre_discard, wid_dilate=wid_dilate, thre_fill=thre_fill)
		print("all done.")

		
if __name__ == '__main__':
	Cell_Segmentation()
