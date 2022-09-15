import os
from .model import db, File

basedir = os.path.dirname(os.path.abspath(__file__))

def save_file(project, file):

    if file is None:
        return False

    filename = file.filename
    extension = os.path.splitext(filename)[1]
    if extension != ".pdf":
        return False

    new_file = File(name=filename, project=project)
    db.session.add(new_file)
    db.session.commit()

    if not os.path.isdir(os.path.dirname(new_file.relative_path)):
        os.makedirs(os.path.dirname(new_file.relative_path))

    file.save(new_file.relative_path)

    return True
