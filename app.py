from ReportBuilder import Project
import time

def main():

    project = Project("example_project")
    project.merge()
    project.save()

if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))