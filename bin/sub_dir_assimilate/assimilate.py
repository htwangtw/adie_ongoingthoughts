from assimilate_funcs import *
import glob

subs = glob.glob('/research/cisc2/projects/critchley_adie/wills_data/bids/sub-*')
subs = [os.path.basename(i) for i in subs]

for sub in subs:
    #F1 - Get paths
    src,dst = paths()
    # F2 - Match sub dirs
    try:
        src,dst = submatch(src,dst,sub)
        print('error in F3')
    # F3 - Match session dirs 
    src, dst = sesmatch(src,dst)
    # F4 - Create sessions dictionary

    sescreate(src,dst)

    print ('---------------------------------------------------------------------')


