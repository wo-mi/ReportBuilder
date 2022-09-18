import os
files = os.listdir(os.path.dirname(__file__))

res = []
for file in files:
    if os.path.splitext(file)[1] == ".py" and file != "__init__.py":
        res.append(os.path.splitext(file)[0])

__all__ = res



# __all__ = ['test_auth', 'test_config_add']
# __all__ = ['test_auth', 
#             'test_config_add', 
#             'test_config_get', 
#             'test_file_add', 
#             'test_file_delete', 
#             'test_projects_get', 
#             'test_project_add', 
#             'test_project_delete', 
#             'test_project_get', 
#             'test_admin', 
#             'test_users_get', 
#             'test_user_add', 
#             'test_user_delete', 
#             'test_user_get']


# from os.path import dirname, basename, isfile, join
# import glob
# modules = glob.glob(join(dirname(__file__), "*.py"))
# __all__ = [ basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')]

