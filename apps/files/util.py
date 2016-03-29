from dyw.apps.files.models import FileAttach, ATTACH_TYPE
from django.conf import settings

def get_attachments(atype,aid):
    
    if type(aid) in [str,unicode]:
        return FileAttach.objects.filter(attach_type=ATTACH_TYPE.get(atype),attach_text=aid)
    else:
        return FileAttach.objects.filter(attach_type=ATTACH_TYPE.get(atype),attach_id=aid)

def attach_file(atype,aid,aby,_file, title='', description = ''):
    """ Zaczepianie pliku do obiektu """
    
    """
    
    @TODO: raise aid in INT albo string
    @TODO: raise atype not in ATTACH_TYPE
    @TODO: raise, filename, file
    @TODO: raise blad zapisu
    @TODO: raize aby not user
    @TODO: jezeli blad zapisu, - revert
    """
    
    attach = FileAttach(
        
        attach_type =  ATTACH_TYPE.get(atype),
        
        creator = aby,
        filename = _file.name,
        
        title = title,
        description = description
        
    )
    
    
    if type(aid) in [str,unicode]:
        attach.attach_id = 0
        attach.attach_text = aid
    else:
        attach.attach_id = aid

    
    attach.save()
    
    f = open('%s/%s' % (settings.ATTACH_FILES_DIR,attach.attach_filename()), 'wb')
    
    for chunk in _file.chunks():
        f.write(chunk)

    f.close()
    
    return attach
