import pickle
import os
import warnings
from chainer.optimizers import Adam

from .imclass import ImClass
from .FCN_Classifier import FCN
from . import epoch


# training step
def train_step(fname_train, fname_label, fname_model,
               N_train, N_test, N_epoch, batchsize, hgh, wid,
               mode):

    print("Start training.")
    print("train:", fname_train, "label", fname_label)
    print("N_train:", N_train, "N_test:", N_test, "hgh:", hgh, "wid:", wid)

    cim = ImClass('train', fname_train=fname_train, fname_label=fname_label,
                  N_train=N_train, N_test=N_test, hgh=hgh, wid=wid,
                  mode=mode)

    model = FCN()
    optimizer = Adam()
    optimizer.setup(model)

    # Learning loop
    for epoch_i in range(1, N_epoch + 1):
        print("epoch:", epoch_i, "/", N_epoch)

        # training
        sum_loss_training, sum_acc_training = 0.0, 0.0
        for i in range(0, N_train, batchsize):
            train_loss_tmp, train_acc_tmp = epoch.training_epoch(
                i, cim, model, optimizer, batchsize)

            sum_loss_training += train_loss_tmp * batchsize
            sum_acc_training += train_acc_tmp * batchsize

            if i == 0 or (i + batchsize) % 5000 == 0:
                print("training:", i + batchsize, "/", N_train,
                      "loss:", "{:.3f}".format(train_loss_tmp),
                      "acc:", "{:.3f}".format(train_acc_tmp))

        train_loss, train_acc = sum_loss_training / N_train, sum_acc_training / N_train

    # testing
    if N_test != 0:
        sum_acc_testing = 0.0
        for i in range(0, N_test, batchsize):
            test_acc_tmp = epoch.testing_epoch(i, cim, model, batchsize)
            sum_acc_testing += test_acc_tmp * batchsize

            if (i + batchsize) % 1000 == 0:
                print("testing:", i + batchsize, "/", N_test,
                      "acc:", "{:.3f}".format(test_acc_tmp))

        test_acc = sum_acc_testing / N_test

        print("Result", "\n",
              "train_loss:", "{:.3f}".format(train_loss), "\n",
              "train_acc:", "{:.3f}".format(train_acc), "\n",
              "test_acc:", "{:.3f}".format(test_acc))
    else:
        test_acc = 0.0

    data_model = {}
    data_model['model'] = model
    data_model['shape'] = (hgh, wid)
    data_model['testacc'] = test_acc
    if os.path.isfile(fname_model):
        warnings.warn("File is being overwritten: {}.".format(fname_model))
    with open(fname_model, 'wb') as p:
        pickle.dump(data_model, p, -1)

    print("Done training.")
