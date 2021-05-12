import os
def find_path(board):
    base_path = "/home/ubuntu/actions-runner/cse145_testing/tock/tock/boards"
    list_result = os.popen("ls -la " + base_path).read()
    # print((list_result))
    list_result = list_result.split("\n")
    # print(list_result[3])

    # Remove ., .., Makefile, README
    list_result = list_result[5:]
    # print(list_result)

    final_result = []
    for result in list_result:
        final_result.append(result.split())
    
    # for i in final_result[0]:
    #     print(i)

    for row in final_result:
        temp = os.popen("ls -la " + base_path + "/" + row[8]).read()
        # print("===========", row[8], "=================")
        # print(temp)
        temp = temp.split("\n")

        temp_list = temp[1:]

        for i in temp:
            temp_list.append(i.split())

        
        valid_list = []
        # Check for directory
        for i in temp_list:
            print(i[0])
            if("d" in str(i[0])):
                valid_list.append(i[8])
            
        for i in valid_list:
            if("." in i):
                valid_list.remove(i)
            elif(".." in i):
                valid_list.remove(i)
            elif("bootloader" in i):
                valid_list.remove(i)
            elif("src" in i):
                valid_list.remove(i)
        print(valid_list)

        

    
def find_series(baord):
    pass

find_path("jwioejfwef")