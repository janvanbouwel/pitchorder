import Project
import Input

if __name__ == "__main__":
    response = ""
    queue = {}
    while True:
        print(f"queue length is {len(queue)}")
        response = input("please give project name or type start: ")
        if response == "start":
            break
        url = input("Please give youtube url: ")
        queue[response] = url

    for response in queue:
        Project.make_all(response, queue[response])



