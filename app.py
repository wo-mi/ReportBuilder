from ReportBuilder import Project
import time

def main():
    
    project = Project("example_project")

    html = project.table_of_content.get_html()

    with open("toc.html","w") as f:
        f.write(html)

    # project.merge()



if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))