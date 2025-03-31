from langchain.indexes import VectorstoreIndexCreator
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
from typing import List, Dict

from langchain.evaluation import criteria
from pydantic import BaseModel, Field
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI, OpenAIEmbeddings



class Config:
    def __init__(self):
        self.CODE_GEN_TEMPLATE = """Please implement the {algorithm} algorithm using {language}. 
        Prioritize using the knowledge base and the following provided API information. Do not consider the header files and the input/output of the graph data.
        **Platform Features**:
        The platform provides the following key APIs for graph processing:
        {prompt_level}

        Generate valid JSON output in the following format:
        {{
          "code": "complete {language} code for {algorithm}",
          "explanation": "detailed design rationale for the algorithm implementation"
        }}
        """

        self.EVAL_TEMPLATE = """Evaluate code quality of {algorithm} implementation 

        **This is the standard reference code**: {standard_code}

        **The evaluate code**: {evaluate_code}

        **Evaluation Criteria**:
        Code Evaluator systematically analyzes submitted code against a specific standard, focusing on three main areas: deviation from the standard code in the main body (excluding headers) with a focus on main function usage consistency compared to standard code (0-100), correctness of the implementation compared to standard code (0-100), and readability (0-100). The evaluation emphasizes identifying deviations from the reference code in the main body, with greater deviations resulting in lower scores. Correctness assesses how well the function calls and logic align with the expected outcomes. Readability considers the code's organization, naming conventions. Each code submission is evaluated individually with detailed analysis for each criterion, highlighting the differences between them. Do not consider the header files and the input/output of the graph data.
        Finally, based on the evaluation results, a final result analysis is provided. This analysis interprets the performance at different levels, identifying trends and patterns.

        Detailed Evaluation Criteria:
        -Compliance
        • Excellent (81-100 points) means the code fully follows the platform’s API best practices (as used in the standard code) with no unnecessary or incorrect calls.
        • Good (61-80 points) indicates that most APIs are used correctly, with only minor redundancy or unnecessary calls that do not affect core functionality.
        • Average (41-60 points) reflects partial adherence to best practices, with some errors or omissions in API usage, leading to incomplete utilization of the APIs.
        • Poor (0-40 points) describes code that either fails to use the platform’s APIs correctly or contains numerous incorrect calls.
 
        -Correctness
        • Excellent (81-100 points) indicates that all functionalities (as per the reference standard code) are implemented as expected, with no logical errors or potential issues.
        • Good (61-80 points) means that most functionalities are implemented correctly, with minor issues in logic that do not affect core functionality.
        • Average (41-60 points) reflects partial implementation of core functionalities, but with noticeable logical errors or omissions.
        • Poor (0-40 points) describes code with significant logical errors or non-standard implementations.
         
        -Readability
        • Excellent (81-100 points) indicates consistent coding style with clear, semantic variable names and a simple, well-organized structure that is easy to read and maintain.
        • Good (61-80 points) reflects overall clarity and good structure, though there may be minor complexities or repetitive logic.
        • Average (41-60 points) means the code is harder to read, with unclear structure and redundant or unnecessary complexity.
        • Poor (0-40 points) describes code with little to no clear structure, making it difficult to read and understand.

        **Only output JSON format (First analyze the reasons, then provide the score)**:
        {{
        "evaluations": [
            {{"strengths": advantage_1,
              "disadvantage": disadvantage_1,
              "Compliance_score": Compliance_score_1,
              "Correctness_score": Correctness_score_1,
              "Readability_score": Readability_score_1
            }},
            {{"strengths": advantage_2,
              "disadvantage": disadvantage_2,
              "Compliance_score": Compliance_score_2,
              "Correctness_score": Correctness_score_2,
              "Readability_score": Readability_score_2
            }},
            ...
          ],
          "analysis": analysis
        }}"""

        self.CODE_PATH_TEMPLATE = """Identify the possible graph algorithms implemented in the given file paths, prioritizing the following types: 'PageRank', 'SSSP', 'Core Decomposition', 'Betweenness Centrality', 'LPA', 'TriangleCounting', 'kClique', 'Connected Component'. Then, return up to five file paths along with their corresponding possible algorithm names.
        
        **The given file paths:
        {paths}

        **Only output JSON format:
        {{
        "algorithms": [
            {{"algorithm": algorithm1,
              "path": path1
            }},
            {{"algorithm": algorithm2,
              "path": path2
            }},
            ...
          ]
        }}

        """

        self.API_PATH_TEMPLATE = """From these file paths, find the core API file paths and output 1-3 of them.
        **The given file paths:
        {paths}
        
        **Only output JSON format:
        {{
        "apis": [
            {{"api": api1,
              "path": path1
            }},
            {{"api": api2,
              "path": path2
            }},
            ...
          ]
        }}
        """

        self.SUBSTITUTE_TEMPLATE = """Apply anonymization to the provided code. You need to output anonymization rules for the core functions (excluding generic functions), including the original functions and their anonymized versions. The anonymized functions should be different from the original ones but should still convey a similar meaning. Also determine the programming language.

        **The given codes:**
        {codes}

        **Only output JSON format:**
        {{
            "language": "language used in this platform"
            "replacement_standards": [
                {{"original_function_name": original_function_name1,
                  "anonymized_function_name": anonymized_function_name1
                }},
                {{"original_function_name": original_function_name2,
                  "anonymized_function_name": anonymized_function_name2
                }},
                ...
            ]
        }}
        """

        self.CODE_SUBSTITUTE_TEMPLATE = """Based on the anonymization rules provided below, apply anonymization to the given code or description. Replace platform names with 'Platform' and substitute relevant functions according to the rules. No other modifications are required.
        **The given anonymization rules:**
        {rules}

        **the given code or description:**
        {code}

        **Only output JSON format:**
        {{
            "output": "output code or description"
        }}
        """

        self.PROMPTY_2_TEMPLATE = """Extract the core API function names and parameters based on the provided data and provide a brief explanation.

        **The given data:**
        {data}

        **Only output JSON format:**
        {{
            "function": [
            {{"API_function_name": "API function name1",
              "parameters": "parameters1",
              "brief_explanation": "brief explanation1"
            }},
            {{"API_function_name": "API function name2",
              "parameters": "parameters2",
              "brief_explanation": "brief explanation2"
            }},
            ...
          ]
        }}
        """

        self.PROMPTY_3_TEMPLATE = """Extract the core API function names and parameters required by the provided code, and provide a detailed explanation along with simple examples (examples should not use data from the original code).

        **The given data:**
        {data}

        **The given code:**
        {code}

        **Only output JSON format:**
        {{
            "function": [
            {{"API_function_name": "API function name1",
              "parameters": "parameters1",
              "detailed_explanation": "detailed_explanation1",
              "use_example": "use_example1"
            }},
            {{"API_function_name": "API function name2",
              "parameters": "parameters2",
              "detailed_explanation": "detailed_explanation2",
              "use_example": "use_example2"
            }},
            ...
          ]
        }}
        """

        self.PROMPTY_4_TEMPLATE = """Generate pseudocode for the following code, ensuring it is concise.
        
        **The given code:**
        {code}

        **Only output JSON format:**
        {{
            "pseudocode": "pseudocode"
        }}
        """

    def get_api_key(self):
        return os.getenv('OPENAI_API_KEY')
    
    def get_algorithm_name(self):
        return {
            'PageRank': 'PageRank',
            'SSSP': 'Single-Source Shortest Path',
            'CD': 'Core Decomposition',
            'BC': 'Betweenness Centrality',
            'TriangleCounting': 'Triangle Counting',
            'kClique': 'k-Clique',
            'LPA': 'Label Propagation',
            'CC': 'Connected Component'
        }

    def get_prompt(self, platform, algorithm, level):
        with open('tips/' + platform + '/' + algorithm + '/' + level, 'r') as file:
            file_contents = file.read()
            return str(file_contents)

    def get_algoritm(self, platform, algorithm):
        return 'Refer to the above tips to help me generate the ' + self.get_algorithm_name()[algorithm] + ' algorithm completed code based on the platform’s API information.\n'
    def get_standard_code(self, platform, algorithm):
        with open('code/' + platform + '/' + algorithm, 'r') as file:
            file_contents = file.read()
            return str(file_contents)
    def get_evaluate_code(self, codes):
        str_ = ''
        code_i = 1
        for code in codes:
            str_+= 'The code ' + str(code_i) + ':\n' + code + '\n'
            code_i+=1

        return str_


    def getCode(self, s):
        start_index = s.find("```")
        if start_index != -1:
            
            end_index = s.find("```", start_index + 3)  
            if end_index != -1:
                
                code = s[start_index + 6:end_index]
                return code
            else:
                print("error \"```\"")
                return -1
        else:
            print("error \"```\"")
            return -1

    def build_faiss_index(self, input_dir, output_dir):
        embeddings = OpenAIEmbeddings(
            openai_api_key=self.get_api_key()
        )

        loader = TextLoader(input_dir, encoding='utf-8')
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        documents = loader.load_and_split(text_splitter)

        vectorstore = FAISS.from_documents(documents, embeddings)
        os.makedirs(output_dir, exist_ok=True)
        vectorstore.save_local(output_dir)

    def get_CODE_GEN_TEMPLATE(self):
        return self.CODE_GEN_TEMPLATE

    def get_EVAL_TEMPLATE(self):
        return self.EVAL_TEMPLATE
    
    def get_CODE_PATH_TEMPLATE(self):
        return self.CODE_PATH_TEMPLATE
    
    def get_API_PATH_TEMPLATE(self):
        return self.API_PATH_TEMPLATE
    
    def get_SUBSTITUTE_TEMPLATE(self):
        return self.SUBSTITUTE_TEMPLATE
        
    def get_CODE_SUBSTITUTE_TEMPLATE(self):
        return self.CODE_SUBSTITUTE_TEMPLATE
    
    def get_PROMPTY_2_TEMPLATE(self):
        return self.PROMPTY_2_TEMPLATE
    
    def get_PROMPTY_3_TEMPLATE(self):
        return self.PROMPTY_3_TEMPLATE
    
    def get_PROMPTY_4_TEMPLATE(self):
        return self.PROMPTY_4_TEMPLATE
    
    def get_language(self, platform):
        if platform == 'Graphx':
            return 'Java'
        else:
            return 'C++'





