
def convert_dict(txtfile):
    """ convert this to dictonary, where key = CISC and val = ADIE"""
    with open(txtfile) as f:
        rename = {}
        for line in f:
            (key,val)=line.split()
            #Remove any non-digit i.e. 'CISC'
            rename[str(re.sub("[^0-9]","",key))] = str(val)
        return rename

def subpaths(sub):
    """ consolidate sub- dir as string - bit redundent for now but may come in handy"""
    return str(sub)

def idmatch(r):
    """ Extract CISC ID from directory, and match with ADIE ID"""
    # search for group of numbers after 'sub-'
    print(r)
    cid = re.search("sub-([0-9]*)",r).group(1)
    # match CISC ID with ADIE ID
    if cid in rename.keys():
        # return new ID with 'sub-' appended, as per BIDS convention, and CISCID
        return "sub-" + rename[cid], cid
    elif cid not in rename.keys():
        print("CISC ID ({}) not recognized!".format(cid))

def newdir(newid,root):
    """ Create new directory with same structure"""
    # Recreat directory structure, using the parent sub- directory as input
    for dirpath, dirnames, filenames in os.walk(r):
        structure = os.path.join(newid,os.path.relpath(dirpath,root))
        # Check to see if these new directories don't exist
        # if not, make the directory with the new ADIE names
        if not os.path.isdir(structure):
            # need to change directory to the same level as existing sub- dir
            # to ensure to that new directory is not made inside the existing one
            parentdir = os.path.split(os.path.normpath(root))[0]
            os.chdir(parentdir)
            # create directory
            os.makedirs(structure)
            print ("Creating {} inside {}".format(structure,os.getcwd()))
        else:
            print("Directory already exists!")

def movefiles(sub,newid,cid):
    """ Move files to new directories and rename"""
    # construct full CISC ID (with sub-)
    cid_full = 'sub-'+cid
    for root,dirs,files in os.walk(sub):
        for f in files:
            # Only continue with the file if it's NOT a stupid annoying mac file
            if 'DS_Store' not in f:
                # Construct full path
                fullf = os.path.join(root,f)
                # Create new path by replacing sub-CISCID with sub- ADIEID
                newf = fullf.replace(cid_full,newid)
                # Check that directories already exist - should've been created in F3
                if not os.path.isdir(os.path.split(newf)[0]):
                    print("WARNING: '{}' does NOT exists".format(os.path.split(newf)[0]))
                # If directory does exist, proceed with move and rename
                else:
                    print("Attempting to move",fullf,"to",newf,'\n')
                    shutil.move(fullf,newf)
            elif 'DS_Store' in f:
                continue

def numfiles(subdr):
    """ Count number of files in a sub- dir"""
    # initialize variable
    numf = 0
    for root, dirs, files in os.walk(subdr):
        numf += len(files)
        return numf
    print ("Number of files in {}: {}".format(subdr,numf))

def compare(numf_old,numf_new,dir_to_del):
    """ remove redundent dirs """
    if numf_old == numf_new:
        print ("Removing:",sub, '\n', 'Number of files equal - suggests successful conversion')
        shutil.rmtree(dir_to_del)
    else:
        print (" Not removing:",sub,'\n','Number of files not equal!')
