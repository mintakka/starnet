# This file is a part of StarNet code.
# https://github.com/nekitmm/starnet
# 
# StarNet is a neural network that can remove stars from images leaving only background.
# 
# Throughout the code all input and output images are 8 bits per channel tif images.
# This code in original form will not read any images other than these (like jpeg, etc), but you can change that if you like.
# 
# Copyright (c) 2018 Nikita Misiura
# http://www.astrobin.com/users/nekitmm/
# 
# This code is distributed on an "AS IS" BASIS WITHOUT WARRANTIES OF ANY KIND, express or implied.
# Please review LICENSE file before use.

import sys
import time
import os

# this line hides lots of additional bulky output from TF. Comment out if you debug your script.
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


epochs = 10000                         # Number of training epochs to do before exiting. You can safely interrupt the script only 
                                       # IN THE MIDDLE OF EPOCH. Do not interrupt the script in between epochs because you might interrupt
                                       # saving of the trained weights into checkpoint files, which will destroy everything.
                                       # I recommend creating an additional backups of weights.
batch = 1                              # Batch size, i.e. number of training examples fed to net simultaneously. The larger value the better
                                       # in terms of performance, but will consume increasing amounts of memory. 1 is default for current
                                       # structure of the net, which will require 2 Gb of video memory in case you use GPU and about 3 Gb of RAM.
steps = 1000                           # Training steps per epoch. 1000 is default. Do not change if you continue training of you model.
output_freq = 100                      # Console output frequency.
verbose = True                         # If True will print into console all loss components, if False - only main three. False is recommended.
images = True                          # If True will save images of transformations generated by net to monitor quality of the net. True is default.
log_freq = 50                          # Losses output frequency into text files. 50 is default
gen_plots = True                       # Plot losses after each epoch. This also can be done running starnet.py -u plot
#                    G        D        #
#learning_rates = [0.0002, 0.00005] - give good balance it seems for stage 1
#learning_rates = [0.00002, 0.000005]  # stage 2
#learning_rates = [0.000002, 0.0000005] # stage 3
#learning_rates = [0.0000002, 0.00000005] # finally 
learning_rates = [0.000002, 0.0000005] # Learning rates: the first is for generator, the second is for discriminator. Usually they are the same,
                                       # but who knows. In the beginning of training suitable values are about 0.0002 and then can be made smaller
                                       # as the model gets better.
stride = 64                            # Stride value for image transformation. The smaller it gets, the less artefacts you get in the final image,
                                       # but the more time it takes to transform an image. 100 looks about optimal for now.

if len(sys.argv) > 1:
    if sys.argv[1] == 'train':
        if len(sys.argv) > 2 and sys.argv[2] == 'new':
            resume = False
            print("")
            print("                        -------! WARNING !-------")
            print("                          Starting a new model!")
            print("                Make sure you backed up all necessary files!")
            print("          Previous state of the model and all output will be lost!")
            print("         Interrupt the script immediately if you changed your mind!")
            print("                        -------! WARNING !-------")
            print("")
            sys.stdout.flush()
        else:
            resume = True
        
        start = time.time()
        print("Starting training run: %d epochs with %d steps in each. Batch size is %d" % (epochs, steps, batch))
        sys.stdout.flush()
        
        import train
        train.train(epochs = epochs,
                    batch = batch,
                    steps = steps,
                    output_freq = output_freq,
                    verbose = verbose,
                    images = images,
                    log_freq = log_freq,
                    resume = resume,
                    gen_plots = gen_plots,
                    learning_rates = learning_rates)
                    
        stop = time.time()
        t = float((stop - start) / 60)
        if t > 60.0:
            print("Total time taken: %.1f hours" % t / 60)
        else:
            print("Total time taken: %.1f minutes" % t)
        
        print("Done!")
    elif sys.argv[1] == 'plot':
        import plot
        plot.plot()
    elif sys.argv[1] == 'test':
        if len(sys.argv) < 3:
            print("")
            print("Usage: python starnet.py test <image>")
            print("Exiting...")
        else:
            import test
            test.test(input = sys.argv[2], numtests = 20)
    elif sys.argv[1] == 'transform':
        if len(sys.argv) < 3:
            print("")
            print("Usage: python starnet.py transform <image>")
            print("Exiting...")
        else:
            start = time.time()
            import transform
            transform.transform(imageName = sys.argv[2],
                                stride    = stride)
            stop = time.time()
            t = float((stop - start) / 60)
            if t > 60.0:
                print("Total time taken: %.1f hours" % t / 60)
            else:
                print("Total time taken: %.1f minutes" % t)
    elif sys.argv[1] == 'export':
        print("Exporting graph")
        import export
        export.export()
    else:
        print("Wrong argument(s)!")
else:
    print("LOL! Give me some argument (train, test, plot or transform)!")