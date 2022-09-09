import unittest
from ReportBuilder import Project

class UnitTests(unittest.TestCase):
    def test(self):
        project = Project()
        project.build_from_dir("Test project")
        project.merge()
        project.save()

if __name__ == '__main__':
    unittest.main()
