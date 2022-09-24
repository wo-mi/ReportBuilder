import pytest
from ReportBuilder import Project
from tests.web import *


class TestDesktop:
    def test(self):
        project = Project()
        project.build_from_dir("tests\\desktop\\Test project")
        project.merge()
        project.save("tests\\desktop\\")


class TestWeb:
    @pytest.fixture(scope='session')
    def token(self):
        return test_auth.run()

    def test_A(self, token):
        assert test_project_add.run(token) == True
    def test_B(self, token):
        assert test_projects_get.run(token) == True

    def test_C(self, token):
        assert test_config_add.run(token) == True
    def test_D(self, token):
        assert test_config_get.run(token) == True

    def test_E(self, token):
        assert test_file_add.run(token) == True

    def test_F(self, token):
        assert test_admin.run(token) == True

    def test_G(self, token):
        assert test_user_add.run(token) == True
    def test_H(self, token):
        assert test_users_get.run(token) == True
    def test_I(self, token):
        assert test_user_get.run(token) == True

    def test_J(self, token):
        test_project_get.run(token)

    def test_K(self, token):
        assert test_file_delete.run(token) == True
    def test_L(self, token):
        assert test_project_delete.run(token) == True
    def test_M(self, token):
        assert test_user_delete.run(token) == True

if __name__ == '__main__':
    pytest.main(['-q'])
    # pytest.main(['-q','-v','test_module.py::TestDesktop'])
    # pytest.main(['-q','-v','test_module.py::TestWeb'])