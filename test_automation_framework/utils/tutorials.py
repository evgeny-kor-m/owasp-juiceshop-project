import sys
import requests
from jsonpath_ng.ext import parse
from helper import *

if __name__ == '__main__':
    hours = 12
    run_shuffle = False
    clean_seq = False
    print("Hello, World!")
    print(sys.version)

    help = util()
    print(help.GUID())

    path=r"E:\Git_Projects\Amdocs\Python_tutorials\output\example_test.txt"
    contentStr="Hello file"
    file.writeToFile(path,contentStr)

    contentStr = file.readFile(path)
    print(f"My string is: {contentStr}")

    path=r"E:\Git_Projects\Amdocs\Python_tutorials\output\ProductOrder_416885050005696512.json"
    jsonFile = file.readJsonFile(path)

    path=r"E:\Git_Projects\Amdocs\Python_tutorials\output\ProductOrder_416885050005696512_2.json"
    file.writeJsonFile(path,jsonFile)

    # Access a specific value
    company = jsonFile.get("id")
    print("Company:", company)  # Output: TechCorp

    # search by jsonpath
    try:
        jsonpath_expr = parse('$..productOrderItem[?(@.productOffering.productOfferingType=="Mobile_Offer")].id')
        print("For search jsonpath_expr:", jsonpath_expr)
        matches = [match.value for match in jsonpath_expr.find(jsonFile)]
        if isinstance(matches,list):
            for item in matches:
                print("Find item:", item )
        # print("City of Bob:", matches[0] if matches else "Not found")
    except Exception as e:
        print("Error parsing JSONPath:", e)

    # update by jsonpath
    try:
        jsonpath_expr = parse('$..productOrderItem[?(@.productOffering.productOfferingType=="Mobile_Offer")].id')
        print("For update jsonpath_expr:", jsonpath_expr)
        for match in jsonpath_expr.find(jsonFile):
            print(f"Old Value: {match.value}")
            # Update the value
            match.context.value[match.path.fields[0]] = 999
            print(f"New Value: {match.context.value[match.path.fields[0]]}")
            path=r"E:\Git_Projects\Amdocs\Python_tutorials\output\ProductOrder_416885050005696512_4.json"
            file.writeJsonFile(path,jsonFile)
    except Exception as e:
        print("Error parsing JSONPath:", e)

    # search in recursive
    result = Jason_util.find_value(jsonFile, "18fb30cd-cac7-4af6-bc1c-29a007ad6453")
    if result:
        print("Found Value:", result)
        # Output: ('city', 'Los Angeles')
    else:
        print("Value not found.")

    # update in recursive
    Jason_util.update_value(jsonFile,"name","Suite Advance B2C - Starter Offer","Updated Suite Advance B2C Offer")
    path=r"E:\Git_Projects\Amdocs\Python_tutorials\output\ProductOrder_416885050005696512_3.json"
    file.writeJsonFile(path,jsonFile)

    # replace
    source="hnfpoabzkjdabcisqabcew"
    target ="abc"
    new ="xyz"
    result= util.replaceStr(source,target,new)
    print("replaceStr result:", result)

    # Sort
    result= util.sortStr(source)
    print("replaceStr result:", result)

    # Calculate num items in String
    # sourceList=["Now" "we" "have" "a" "List" "without" "any" "duplicates" "and" "it" "has" "the" "same" "order" "as" "the" "original" "List" "Print" "the" "List" "to" "demonstrate" "the" "result"]
    sourceList="Now we have a List without any duplicates and it has the same order as the original List Print the List to demonstrate the result"
    print(sourceList)
    result= util.calcListItems(sourceList)
    for k,v in result.items():
        print(f"Find '{k}':{v} times\n"  )

    # HTTP requests
    url = "https://www.linkedin.com/jobs/"
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        print("Response JSON:", response)
    else:
        print("Failed to retrieve data. Status code:", response.status_code)

    #-DB-------------------------------------------------
    # dbPg = connection("localhost","mypostgresdb","postgres","postgresdb",5432,"")
    # dbPg.pg_connect()
    # dbPg.insertRow()
    #
    # dbPg.pg_disconect()






def fib(n):    # write Fibonacci series less than n
    """Print a Fibonacci series less than n."""
    a, b = 0, 1
    while a < n:
        print(a, end=' ')
        a, b = b, a+b
    print()

