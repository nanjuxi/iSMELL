import httpx
from openai import OpenAI
from javalang import parse
from javalang.tree import MethodDeclaration

client = OpenAI(
    base_url="https://api.xty.app/v1",
    api_key="xxxxx",
    http_client=httpx.Client(
        base_url="https://api.xty.app/v1",
        follow_redirects=True,
    ),
)

def refactor_code_smells_FeatureEnvy(example_java_code,java_code):
    try:
        response = client.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=[
                {"role": "system", "content": "I am an AI trained to refactor code smells in Java code."},
                {"role": "user", "content": f'''In computer programming, a code smell is any characteristic in the 
                source code of a program that possibly indicates a deeper problem. I will now tell you the definition 
                about Feature Envy. Please read the definition and refactor the code according to the target to 
                eliminate this smell. The definition of Feature Envy is: Feature Envy occurs when a method in one 
                class can't seem to keep its eyes off the data of another class. This sneaky behavior hints that 
                there might be a better home for the method, where it fits in more naturally and keeps the codebase 
                cleaner and easier to manage. Here is an example for refactoring code which has Feature Envy smell, 
                Please read it carefully and learn to show only the most modified critical code after refactoring. 
                You can replace functional code with comments. You do not need to keep the structure, improve the 
                code's readability and maintainability. {example_java_code}Now based on the example, refactor the 
                following code to eliminate the feature envy code smell. You can achieve it by dividing the method in 
                original code into as many methods or classes as possible. Also make sure every methods you give in 
                the refactored code should not have feature envy smell.
                \n{java_code}
                '''}
            ],
            max_tokens=1500
        )
        if response.choices:
            model_response = response.choices[0].message.content if response.choices[0].message else ""
        else:
            model_response = ""

    except Exception as e:
        print(f"Error while detecting code smells: {e}")
        model_response = "error"  # 在异常情况下确保 model_response 是一个空字符串

    return model_response

def refactor_code_smells_GodClass(example_java_code,java_code):
    try:
        response = client.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=[
                {"role": "system", "content": "I am an AI trained to refactor code smells in Java code."},
                {"role": "user", "content": f'''In computer programming, a code smell is any characteristic in the 
                source code of a program that possibly indicates a deeper problem. I will now tell you the definition 
                about God Class. Please read the definition and refactor the code according to the target to 
                eliminate this smell. The definition of God Class is: God Class is a large and unwieldy class that 
                takes on too many responsibilities within an application. It concentrates a multitude of functions, 
                oversees numerous objects, and effectively tries to do everything. Here is an example for refactoring 
                code which has God Class smell, Please read it carefully and learn to show only the most modified 
                critical code after refactoring. You can replace functional code with comments. You do not need to 
                keep the structure, improve the code's readability and maintainability {example_java_code}Now based 
                on the example, refactor the following code. You don't need to give the full code, just give the most 
                modified part of it. You should not output extra content.
                \n{java_code}
                '''}
            ],
            max_tokens=1500
        )
        if response.choices:
            model_response = response.choices[0].message.content if response.choices[0].message else ""
        else:
            model_response = ""

    except Exception as e:
        print(f"Error while detecting code smells: {e}")
        model_response = "error"  # 在异常情况下确保 model_response 是一个空字符串

    return model_response

def refactor_code_smells_RefusedBequest(example_java_code,java_code, parent_code):
    try:
        response = client.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=[
                {"role": "system", "content": "I am an AI trained to refactor code smells in Java code."},
                {"role": "user", "content": f'''In computer programming, a code smell is any characteristic in the 
                source code of a program that possibly indicates a deeper problem. I will now tell you the definition 
                about Refused Bequest. Please read the definition and refactor the code according to the target to 
                eliminate this smell. The definition of Refused Bequest is: Refused Bequest occurs if a subclass uses 
                only some of the methods and properties inherited from its parents. This is an indication that the 
                class should not be a subclass of that parent class, since child classes should be adding or 
                modifying functionality. Here is an example for refactoring code which has Refused Bequest smell, 
                Please read it carefully and learn to show only the most modified critical code after refactoring. 
                You can replace functional code with comments. You do not need to keep the structure, improve the 
                code's readability and maintainability {example_java_code}Now I will give you a piece of code that 
                needs refactoring and the superclass of that code. Please based on the example, refactor the 
                following code that needs refactoring. You don't need to give the full code, just give the most 
                modified part of it. You should not output extra content. This is the superclass of the code that 
                needs refactoring: {parent_code}
                This is the code that needs refactoring:
                {java_code}
                '''}
            ],
            max_tokens=1500
        )
        if response.choices:
            model_response = response.choices[0].message.content if response.choices[0].message else ""
        else:
            model_response = ""

    except Exception as e:
        print(f"Error while detecting code smells: {e}")
        model_response = "error"  # 在异常情况下确保 model_response 是一个空字符串

    return model_response


def extract_methods(java_code):
    methods = []
    try:
        tree = parse.parse(java_code)
        for _, node in tree.filter(MethodDeclaration):
            methods.append(node)
    except Exception as e:
        print(f"Error parsing Java code: {e}")
    return methods

def classify(model_response,methodname):
    try:
        response = client.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=[
                {"role": "system", "content": "I am an AI trained to refactor code smells in Java code."},
                {"role": "user", "content": f'''I will provide you with all the method names from the code before 
                refactoring. Please advise on which classes in the refactored code these methods should be assigned 
                to. {methodname}\n\n{model_response}'''}
            ],
            max_tokens=1500
        )
        if response.choices:
            model_response = response.choices[0].message.content if response.choices[0].message else ""
        else:
            model_response = ""

    except Exception as e:
        print(f"Error while detecting code smells: {e}")
        model_response = "error"  # 在异常情况下确保 model_response 是一个空字符串

    return model_response
if __name__ == "__main__":

    java_code_file = r"C:\Users\20560\Desktop\java_code.txt"
    parent_code_file = r"C:\Users\20560\Desktop\parent_code.txt"
    example_code_file = r"C:\Users\20560\Desktop\example.txt"

    with open(java_code_file, 'r', encoding='utf-8') as file:
         java_code = file.read()
         print(f"{java_code_file} read successfully!")

    with open(example_code_file, 'r', encoding='utf-8') as file:
         example_code = file.read()
         print(f"{example_code_file} read successfully!")

    with open(java_code_file, 'r', encoding='utf-8') as file:
         parent_code = file.read()
         print(f"{parent_code_file} read successfully!")

    methods = extract_methods(java_code)
    for method in methods:
        print(f"Method name: {method.name}")
    model_response = refactor_code_smells_GodClass(example_code,java_code)
    classified_methods = classify(model_response,methods)
    # model_response = refactor_code_smells_FeatureEnvy(example_code,java_code)
    # model_response = refactor_code_smells_RefusedBequest(example_code,java_code,parent_code)
    print(model_response)
    print(classified_methods)
