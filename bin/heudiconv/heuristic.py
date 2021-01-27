import os


def create_key(template, outtype=('nii.gz',), annotation_classes=None):
    if template is None or not template:
        raise ValueError('Template must be a valid format string')
    return template, outtype, annotation_classes


def infotodict(seqinfo):
    """Heuristic evaluator for determining which runs belong where

    allowed template fields - follow python string module:

    item: index within category
    subject: participant id
    seqitem: run number during scanning
    subindex: sub index within group
    """

    t1w = create_key('sub-{subject}/{session}/anat/sub-{subject}_run-00{item:01d}_T1w')
    task_interoception = create_key('sub-{subject}/{session}/func/sub-{subject}_task-interoception_run-00{item:01d}_bold')
    task_mw = create_key('sub-{subject}/{session}/func/sub-{subject}_task-mw_run-00{item:01d}_bold')
    task_faces = create_key('sub-{subject}/{session}/func/sub-{subject}_task-faces_run-00{item:01d}_bold')
 
    info = {t1w: [], task_interoception: [], task_mw: [], task_faces: []}
    
    for s in seqinfo:

        if (s.dim1 == 320) and (s.dim2 == 300) and ('T1w_MPR' in s.protocol_name):
            info[t1w].append(s.series_id)
        elif (s.dim1 == 94) and (s.dim2 == 94) and ('INTEROCEPTION' in s.protocol_name):
            info[task_interoception].append(s.series_id) 
        elif (s.dim1 == 94) and (s.dim2 == 94) and ('MIND_WANDERING' in s.protocol_name):
            info[task_mw].append(s.series_id) 
        elif (s.dim1 == 94) and (s.dim2 == 94) and ('FEAR_FACES' in s.protocol_name):
            info[task_faces].append(s.series_id) 

    return info


