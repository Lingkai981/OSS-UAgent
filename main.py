import json
import os
from typing import List

from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
import config
from pydantic import BaseModel, Field
import json
from flask import Flask, jsonify, request, Response
from flask_cors import CORS
from datetime import datetime
import time
import random
import requests
import base64
import re

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

VALID_PLATFORMS = {'Pregel', 'Grape', 'GraphX', 'Gthinker', 'Flash', 'PowerGraph', 'Ligra'}
VALID_ALGORITHMS = {'PageRank', 'SSSP', 'CD', 'BC', 'LPA', 'TriangleCounting', 'kClique', 'CC'}
TARGET_DIRECTORIES = ["example", "examples", "apps", "applications"]


my_config = config.Config()
class GeneratedCode(BaseModel):
    """Code generation output format"""
    code: str = Field(description="c++/java/python code")
    explanation: str = Field(description="design rationale")


class CodeEvaluation(BaseModel):
    """Evaluation metrics format"""
    strengths: str = Field(description="strengths")
    disadvantage: str = Field(description="disadvantage")
    compliance_score: float = Field(..., ge=0, le=100, alias="Compliance_score")
    correctness_score: float = Field(..., ge=0, le=100, alias="Correctness_score")
    readability_score: float = Field(..., ge=0, le=100, alias="Readability_score")

class EvaluationsResponse(BaseModel):
    """Container for multiple code evaluations"""
    evaluations: List[CodeEvaluation]
    analysis: str = Field(description="analysis")

class CodePath(BaseModel):
    """code path format"""
    algorithm: str = Field(description="algorithm")
    path: str = Field(description="path")

class CodePaths(BaseModel):
    algorithms: List[CodePath]

class APIPath(BaseModel):
    """code path format"""
    api: str = Field(description="api")
    path: str = Field(description="path")

class APIPaths(BaseModel):
    apis: List[APIPath]

class CodeItem(BaseModel):
    """Represents an item in the output list containing code or description."""
    code: str = Field(description="code")

class ReplacementOutput(BaseModel):
    """Defines the full JSON structure."""
    replacement_standards: str = Field(description="replacement_standards")
    output: List[CodeItem] = Field(description="output")

class Anonymization_rule(BaseModel):
    """Represents an item in the output list containing code or description."""
    original_function_name: str = Field(description="original function name")
    anonymized_function_name: str = Field(description="anonymized function name")

class Anonymization_rules(BaseModel):
    """Defines the full JSON structure."""
    language: str = Field(description="language")
    replacement_standards: List[Anonymization_rule]

class Get_substitute_code(BaseModel):
    """Defines the full JSON structure."""
    output: str = Field(description="output")

class Get_prompty_intermediate(BaseModel):
    """Defines the full JSON structure."""
    API_function_name: str = Field(description="API function name")
    parameters: str = Field(description="parameters")
    brief_explanation: str = Field(description="brief explanation")

class Get_prompty_intermediates(BaseModel):
    """Defines the full JSON structure."""
    function: List[Get_prompty_intermediate]

class Get_prompty_senior(BaseModel):
    """Defines the full JSON structure."""
    API_function_name: str = Field(description="API function name")
    parameters: str = Field(description="parameters")
    detailed_explanation: str = Field(description="detailed explanation")
    use_example: str = Field(description="use example")

class Get_prompty_seniors(BaseModel):
    """Defines the full JSON structure."""
    function: List[Get_prompty_senior]

class Get_prompty_expert(BaseModel):
    """Defines the full JSON structure."""
    pseudocode: str = Field(description="pseudocode")


llm = ChatOpenAI(
    openai_api_base="https://chatapi.littlewheat.com/v1",
    openai_api_key=my_config.get_api_key(),
    model = 'gpt-4o',
    temperature=0.7
)

embeddings = OpenAIEmbeddings(
    openai_api_base="https://chatapi.littlewheat.com/v1",
    openai_api_key=my_config.get_api_key()
)

platforms = ['Flash', 'Ligra', 'Grape', 'PowerGraph', 'Pregel', 'Graphx', 'Gthinker']
# platforms = ['Gthinker']

# algorithms = ['kClique']
algorithms = ['PageRank', 'SSSP', 'kCore', 'BC', 'LPA', 'TriangleCounting', 'kClique', 'CC']

levels = ['1', '2', '3', '4']

def GetCodePath(filtered_files):
    code_prompt_template = ChatPromptTemplate.from_template(my_config.get_CODE_PATH_TEMPLATE())
    parser = PydanticOutputParser(pydantic_object=CodePaths)

    chain = code_prompt_template | llm

    # print(evaluation_prompy)

    response = chain.invoke({
        "paths": str(filtered_files)
    })



    # print(response.content)

    parsed_result = parser.parse(response.content)
    # print(parsed_result)
    json_output = parsed_result.model_dump_json()
    data = json.loads(json_output)
    # print(data['algorithms'])
    return data['algorithms']

def GetAPIPath(code_files):
    code_prompt_template = ChatPromptTemplate.from_template(my_config.get_API_PATH_TEMPLATE())
    parser = PydanticOutputParser(pydantic_object=APIPaths)

    chain = code_prompt_template | llm

    response = chain.invoke({
        "paths": str(code_files)
    })



    # print(response.content)

    parsed_result = parser.parse(response.content)
    # print(parsed_result)
    json_output = parsed_result.model_dump_json()
    data = json.loads(json_output)
    # print(data['algorithms'])
    return data['apis']

def SetAnonymization(original_code):
    code_prompt_template = ChatPromptTemplate.from_template(my_config.get_SUBSTITUTE_TEMPLATE())
    parser = PydanticOutputParser(pydantic_object=ReplacementOutput)

    chain = code_prompt_template | llm

    # print(evaluation_prompy)

    response = chain.invoke({
        "codes": str(original_code)
    })

    # print(response.content)

    parsed_result = parser.parse(response.content)
    # print(parsed_result)
    json_output = parsed_result.model_dump_json()
    data = json.loads(json_output)
    # print(data['algorithms'])
    return data

def GetAnonymizationRules(original_code):
    code_prompt_template = ChatPromptTemplate.from_template(my_config.get_SUBSTITUTE_TEMPLATE())
    parser = PydanticOutputParser(pydantic_object=Anonymization_rules)

    chain = code_prompt_template | llm

    # print(code_prompt_template)

    response = chain.invoke({
        "codes": str(original_code)
    })

    print(response.content)

    parsed_result = parser.parse(response.content)
    # print(parsed_result)
    json_output = parsed_result.model_dump_json()
    data = json.loads(json_output)
    # print(data['algorithms'])
    return data

def GetSubstituteCode(rules, code):
    code_prompt_template = ChatPromptTemplate.from_template(my_config.get_CODE_SUBSTITUTE_TEMPLATE())
    parser = PydanticOutputParser(pydantic_object=Get_substitute_code)

    chain = code_prompt_template | llm

    # print(str(rules))
    # print(str(code))

    response = chain.invoke({
        "rules": str(rules),
        "code": str(code)
    })

    print(response.content)

    parsed_result = parser.parse(response.content)
    # print(parsed_result)
    json_output = parsed_result.model_dump_json()
    data = json.loads(json_output)
    # print(data['algorithms'])
    return data['output']

def GetPromptyIntermediate(data):
    code_prompt_template = ChatPromptTemplate.from_template(my_config.get_PROMPTY_2_TEMPLATE())
    parser = PydanticOutputParser(pydantic_object=Get_prompty_intermediates)

    chain = code_prompt_template | llm

    # print(evaluation_prompy)

    response = chain.invoke({
        "data": str(data)
    })

    # print(response.content)

    parsed_result = parser.parse(response.content)
    # print(parsed_result)
    json_output = parsed_result.model_dump_json()
    data = json.loads(json_output)
    # print(data['algorithms'])
    return data['function']

def GetPromptySenior(data, code):
    code_prompt_template = ChatPromptTemplate.from_template(my_config.get_PROMPTY_3_TEMPLATE())
    parser = PydanticOutputParser(pydantic_object=Get_prompty_seniors)

    chain = code_prompt_template | llm

    # print(evaluation_prompy)

    response = chain.invoke({
        "data": str(data),
        "code": str(code)
    })

    # print(response.content)

    parsed_result = parser.parse(response.content)
    # print(parsed_result)
    json_output = parsed_result.model_dump_json()
    data = json.loads(json_output)
    # print(data['algorithms'])
    
    return data['function']

def GetPromptyExpert(code):
    code_prompt_template = ChatPromptTemplate.from_template(my_config.get_PROMPTY_4_TEMPLATE())
    parser = PydanticOutputParser(pydantic_object=Get_prompty_expert)

    chain = code_prompt_template | llm

    # print(evaluation_prompy)

    response = chain.invoke({
        "code": str(code)
    })

    # print(response.content)

    parsed_result = parser.parse(response.content)
    # print(parsed_result)
    json_output = parsed_result.model_dump_json()
    data = json.loads(json_output)
    # print(data['algorithms'])
    
    return data['pseudocode']


@app.route('/api/analyze-github', methods=['POST'])
def analyze_github():
    data = request.json
    if not data or 'githubUrl' not in data:
        return jsonify({"error": "Missing GitHub URL"}), 400
    
    github_url = data['githubUrl']
    repo_name, branch_name = extract_repo_info(github_url)
    
    if not repo_name:
        return jsonify({"error": "Invalid GitHub URL"}), 400

    api_base_url = f"https://api.github.com/repos/{repo_name}"

    def stream_analysis():
        repo_info = fetch_github_repo(api_base_url)
        yield (json.dumps({"status": "Fetching repository information..."}) + "\n").encode("utf-8")

        

        yield (json.dumps({"status": "**Repository: " + repo_name}) + "\n").encode("utf-8")

        

        yield (json.dumps({"status": "**Platform: " + repo_info.get("name", "Unknown")}) + "\n").encode("utf-8")

        
    
        nonlocal branch_name
        if not branch_name:
            branch_name = get_default_branch(api_base_url)
            if not branch_name:
                yield (json.dumps({"error": "Unable to determine default branch"}) + "\n").encode("utf-8")
                return

        yield (json.dumps({"status": f"**Branch: {branch_name}"}) + "\n").encode("utf-8")

    
        yield (json.dumps({"status": "Fetching README..."}) + "\n").encode("utf-8")
        readme_content = fetch_readme(api_base_url, branch_name)

        

        platform_name = branch_name

        if platform_name == 'master':
            platform_name = repo_info.get("name", "Unknown")

        yield (json.dumps({"status": "Fetching core api files..."}) + "\n").encode("utf-8")
        code_files = fetch_code_files(api_base_url, branch_name)

        

        api_paths = GetAPIPath(code_files)

        print(api_paths)

        for api_path in api_paths:
            yield (json.dumps({"status": f"**{api_path['path']}"}) + "\n").encode("utf-8")

        original_code = []
        # original_code.append(readme_content)
        for api_path in api_paths[:1]:
            original_code.append(fetch_remote_file(api_base_url, api_path['path'], branch_name))

        yield (json.dumps({"status": "Fetching algorithm for evaluation..."}) + "\n").encode("utf-8")
        filtered_files = filter_target_directories(code_files)

        

        alg_paths = GetCodePath(filtered_files)

        for alg_path in alg_paths:
            yield (json.dumps({"status": f"**{alg_path['algorithm']}"}) + "\n").encode("utf-8")

        for alg_path in alg_paths[:1]:
            original_code.append(fetch_remote_file(api_base_url, alg_path['path'], branch_name))

        yield (json.dumps({"status": "Aonymizing..."}) + "\n").encode("utf-8")

        

        print(alg_paths)

        anonymization_rules = GetAnonymizationRules(original_code)

        print(anonymization_rules)

        for anonymization_rule in anonymization_rules['replacement_standards']:
            print(anonymization_rule)
            yield (json.dumps({
                "status": f"**{anonymization_rule['original_function_name']} --> {anonymization_rule['anonymized_function_name']}"
            }) + "\n").encode("utf-8")  

        yield (json.dumps({"status": "Build Knowledge Base..."}) + "\n").encode("utf-8")

        

        with open(f"knowledge_base/{platform_name}", "w", encoding="utf-8") as f:
            f.write(str(GetSubstituteCode(anonymization_rules['replacement_standards'], readme_content)) + '\n')
            # f.write(readme_content + '\n')
            for api_path in api_paths[:1]:
                substituted_code = GetSubstituteCode(
                    anonymization_rules['replacement_standards'],
                    fetch_remote_file(api_base_url, api_path['path'], branch_name)
                )

                f.write(str(substituted_code) + '\n')

        # yield (json.dumps({"status": "Knowledge base construction completed."}) + "\n").encode("utf-8")

        print(1)

        print("alg_paths:", alg_paths)

        for alg_path in alg_paths[:1]:
            
            anonymization_rule_ = anonymization_rules['replacement_standards']
            print(anonymization_rule_)
            code_ = fetch_remote_file(api_base_url, alg_path['path'], branch_name)
            print(code_)
            language_ = anonymization_rules['language']
            print(language_)
            algorithm_ = alg_path['algorithm']
            print(algorithm_)
            platform_ = platform_name

            yield (json.dumps({"status": f"Evaluating {algorithm_}..."}) + "\n").encode("utf-8")

            prompts = []
            prompty1 = 'Implement the algorithm'
            prompts.append(prompty1)

            data = ''
    
            with open(f"knowledge_base/{platform_}", 'r', encoding='utf-8') as file:
                data = file.read()

            

            yield (json.dumps({
                    "junior_ready": "Junior is ready!!!"
                }) + "\n").encode("utf-8")

            prompty2 = str(GetPromptyIntermediate(data))
            prompts.append(prompty2)

            yield (json.dumps({
                    "intermediate_ready": "Intermediate is ready!!!"
                }) + "\n").encode("utf-8")
    
            anonymization_code = GetSubstituteCode(anonymization_rule_, code_)
    
            prompty3 = str(GetPromptySenior(data, anonymization_code))
            prompts.append(prompty3)

            yield (json.dumps({
                    "senior_ready": "Senior is ready!!!"
                }) + "\n").encode("utf-8")
    
            prompty4 = prompty3 + '\n The following is the pseudo-code:\n' + str(GetPromptyExpert(anonymization_code))
            prompts.append(prompty4)

            yield (json.dumps({
                    "expert_ready": "Expert is ready!!!"
                }) + "\n").encode("utf-8")
            
            
    
            if not os.path.isdir('knowledge_base/' + platform_ + '_index'):
                my_config.build_faiss_index('knowledge_base/' + platform_, 'knowledge_base/' + platform_ + '_index')

            try:
                vectorstore = FAISS.load_local(
                    folder_path='knowledge_base/' + platform_ + '_index',
                    embeddings=embeddings,
                    allow_dangerous_deserialization=True 
                )
            except Exception as e:
                print(f"load error: {str(e)}")

            retriever = vectorstore.as_retriever()

            generate_code_prompt_template = ChatPromptTemplate.from_template(my_config.get_CODE_GEN_TEMPLATE())
            evaluation_prompy_template = ChatPromptTemplate.from_template(my_config.get_EVAL_TEMPLATE())
            code_parser = PydanticOutputParser(pydantic_object=GeneratedCode)
            ev_parser = PydanticOutputParser(pydantic_object=EvaluationsResponse)
            codes = []
            level_name = ['junior', 'intermediate', 'senior', 'expert']
            for level in levels:
                prompt = generate_code_prompt_template.format(
                    algorithm=algorithm_,
                    language=language_,
                    prompt_level=prompts[int(level)-1]
                )

                qa_chain = RetrievalQA.from_chain_type(
                    llm=llm,
                    chain_type="stuff",
                    retriever=retriever,
                    return_source_documents=True
                )

                # print(prompt)

                response = qa_chain.invoke({"query": prompt})
                # print(response['result'])

                parsed_result = code_parser.parse(response['result'])
                json_output = parsed_result.model_dump_json()

                data = json.loads(json_output)
                codes.append(data["code"])
                # print(data["code"])
                # print(parsed_result)

                

                yield (json.dumps({
                    level_name[int(level)-1] + "_code": data["code"]
                    }) + "\n").encode("utf-8")



            ev_chain = evaluation_prompy_template | llm

            # print(evaluation_prompy)

            response = ev_chain.invoke({
                "algorithm": algorithm_,
                "standard_code": anonymization_code,
                "evaluate_code": my_config.get_evaluate_code(codes)
            })



            # print(response.content)

            ev_parsed_result = ev_parser.parse(response.content)
            print(ev_parsed_result)
            json_output = ev_parsed_result.model_dump_json()
            data = json.loads(json_output)
            for i in range(len(codes)):
                print(data['evaluations'][i])
    
            print(data['analysis'])

            yield (json.dumps({
                "platform": platform_,
                "algorithm": algorithm_,
                "evaluations": data['evaluations'],
                "analysis": data['analysis'],
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }) + "\n").encode("utf-8")

    return Response(stream_analysis(), content_type='application/json; charset=utf-8', direct_passthrough=True)

def extract_repo_info(url):
    match = re.search(r"github\.com/([^/]+/[^/]+)(?:/tree/([^/]+))?", url)
    if match:
        return match.group(1), match.group(2)  # (repo_name, branch_name)
    return None, None


def get_default_branch(api_base_url):
    response = requests.get(api_base_url)
    if response.status_code == 200:
        return response.json().get("default_branch", "main")
    return None


def fetch_github_repo(api_base_url):
    response = requests.get(api_base_url)
    return response.json() if response.status_code == 200 else {}


def fetch_readme(api_base_url, branch_name):
    url = f"{api_base_url}/contents/README.md?ref={branch_name}"
    response = requests.get(url)
    if response.status_code == 200:
        content = response.json().get("content", "")
        return base64.b64decode(content).decode("utf-8")
    return "README not found."


def fetch_code_files(api_base_url, branch_name):
    url = f"{api_base_url}/git/trees/{branch_name}?recursive=1"
    response = requests.get(url)
    if response.status_code == 200:
        tree = response.json().get("tree", [])
        code_extensions = (".py", ".cpp", ".c", ".java", ".h", ".hpp", ".C", ".cc", ".cxx", ".js", ".ts")
        return [file["path"] for file in tree if file["path"].endswith(code_extensions)]
    return []


def filter_target_directories(code_files):
    target_files = [file for file in code_files if any(dir_name in file.split('/') for dir_name in TARGET_DIRECTORIES)]
    return target_files if target_files else code_files 

def fetch_remote_file(api_base_url, file_path, branch_name="main"):
    url = f"{api_base_url}/contents/{file_path}?ref={branch_name}"
    response = requests.get(url)

    if response.status_code == 200:
        content = response.json().get("content", "")
        return base64.b64decode(content).decode("utf-8")
    
    return f"Error: Unable to fetch file ({response.status_code})"

def EvaluationCode(anonymization_rules, algorithm, code, language, platform):

    print("EvaluationCode:" + algorithm + " "+language+" "+platform)

    prompts = []
    prompty1 = 'Implement the algorithm'
    prompts.append(prompty1)

    data = ''
    
    with open(f"knowledge_base/{platform}", 'r', encoding='utf-8') as file:
        data = file.read()

    yield (json.dumps({
            "junior_ready": "Junior is ready!!!"
        }) + "\n").encode("utf-8")

    prompty2 = str(GetPromptyIntermediate(data))
    prompts.append(prompty2)

    yield (json.dumps({
            "intermediate_ready": "Intermediate is ready!!!"
        }) + "\n").encode("utf-8")
    
    anonymization_code = GetSubstituteCode(anonymization_rules, code)
    
    prompty3 = str(GetPromptySenior(data, anonymization_code))
    prompts.append(prompty3)

    yield (json.dumps({
            "senior_ready": "Senior is ready!!!"
        }) + "\n").encode("utf-8")
    
    prompty4 = prompty3 + '\n The following is the pseudo-code:\n' + str(GetPromptyExpert(anonymization_code))
    prompts.append(prompty4)

    yield (json.dumps({
            "expert_ready": "Expert is ready!!!"
        }) + "\n").encode("utf-8")
    
    if not os.path.isdir('knowledge_base/' + platform + '_index'):
        my_config.build_faiss_index('knowledge_base/' + platform, 'knowledge_base/' + platform + '_index')

    try:
        vectorstore = FAISS.load_local(
            folder_path='knowledge_base/' + platform + '_index',
            embeddings=embeddings,
            allow_dangerous_deserialization=True 
        )
    except Exception as e:
        print(f"load error: {str(e)}")

    retriever = vectorstore.as_retriever()

    generate_code_prompt_template = ChatPromptTemplate.from_template(my_config.get_CODE_GEN_TEMPLATE())
    evaluation_prompy_template = ChatPromptTemplate.from_template(my_config.get_EVAL_TEMPLATE())
    code_parser = PydanticOutputParser(pydantic_object=GeneratedCode)
    ev_parser = PydanticOutputParser(pydantic_object=EvaluationsResponse)
    codes = []
    level_name = ['junior', 'intermediate', 'senior', 'expert']
    for level in levels:
        prompt = generate_code_prompt_template.format(
            algorithm=algorithm,
            language=language,
            prompt_level=prompts[int(level)-1]
        )

        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True
        )

        # print(prompt)

        response = qa_chain.invoke({"query": prompt})
        # print(response['result'])

        parsed_result = code_parser.parse(response['result'])
        json_output = parsed_result.model_dump_json()

        data = json.loads(json_output)
        codes.append(data["code"])
        # print(data["code"])
        # print(parsed_result)

        yield (json.dumps({
            level_name[int(level)-1] + "_code": data["code"]
            }) + "\n").encode("utf-8")



    ev_chain = evaluation_prompy_template | llm

    # print(evaluation_prompy)

    response = ev_chain.invoke({
        "algorithm": algorithm,
        "standard_code": my_config.get_standard_code(platform, algorithm),
        "evaluate_code": my_config.get_evaluate_code(codes)
    })



    # print(response.content)

    ev_parsed_result = ev_parser.parse(response.content)
    print(ev_parsed_result)
    json_output = ev_parsed_result.model_dump_json()
    data = json.loads(json_output)
    for i in range(len(codes)):
        print(data['evaluations'][i])
    
    print(data['analysis'])

    yield (json.dumps({
        "platform": platform,
        "algorithm": algorithm,
        "evaluations": data['evaluations'],
        "analysis": data['analysis'],
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }) + "\n").encode("utf-8")

    # return results




if __name__ == '__main__':
    # Evaluation('Flash', 'PageRank')
    app.run(host='127.0.0.1', port=5555, debug=True)
