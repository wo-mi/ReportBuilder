import unittest
from ReportBuilder import Project
from tests.web import *


class TestDesktop(unittest.TestCase):
    def test(self):
        project = Project()
        project.build_from_dir("tests\\desktop\\Test project")
        project.merge()
        project.save("tests\\desktop\\")

class TestWeb(unittest.TestCase):
    def setUp(self):
        self.token = test_auth.run()
        self.assertTrue(self.token)

    def test_A(self):
        self.assertTrue(test_project_add.run(self.token))
    def test_B(self):
        self.assertTrue(test_projects_get.run(self.token))

    def test_C(self):
        self.assertTrue(test_config_add.run(self.token))
    def test_D(self):
        self.assertTrue(test_config_get.run(self.token))

    def test_E(self):
        self.assertTrue(test_file_add.run(self.token))

    def test_F(self):
        self.assertTrue(test_admin.run(self.token))

    def test_G(self):
        self.assertTrue(test_user_add.run(self.token))
    def test_H(self):
        self.assertTrue(test_users_get.run(self.token))
    def test_I(self):
        self.assertTrue(test_user_get.run(self.token))

    def test_J(self):
        test_project_get.run(self.token)

    def test_K(self):
        self.assertTrue(test_file_delete.run(self.token))
    def test_L(self):
        self.assertTrue(test_project_delete.run(self.token))
    def test_M(self):
        self.assertTrue(test_user_delete.run(self.token))

if __name__ == '__main__':
    # unittest.main()
    # suite = unittest.TestLoader().loadTestsFromTestCase(TestDesktop)
    suite = unittest.TestLoader().loadTestsFromTestCase(TestWeb)
    unittest.TextTestRunner().run(suite)
