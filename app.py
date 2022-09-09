from ReportBuilder import Project
import time

def main():
    project = Project()
    project.build_from_dir("Test project")
    project.merge()
    project.save()

if __name__ == "__main__":
    start_time = time.time()
    main()
    print(f"--- {time.time() - start_time} seconds ---")
