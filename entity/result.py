import re
import json
from model.pipeline import get_answer
from model.compare import Comparer
from model.pipeline import get_pipeline
import os

class Result:
    def __init__(self, score, content):
        self.score = score
        self.content = content

class best_answer_qa:

    def __init__(self,ans):

        self.question = ans["query"]
        self.answer = ans["answers"][0]["answer"]
        self.score = ans["answers"][0]["score"]
        self.probability = ans["answers"][0]["probability"]
        self.context = ans["answers"][0]["context"]


pipe = get_pipeline()
comparer = Comparer()

def solve_question(question):
    query = re.sub(r"[._]{5,}", " what ", question.content)
    query = re.sub(r"\s+", " ", query.strip())
    prediction = get_answer(query, pipe=pipe)
    
    best_qa = best_answer_qa(prediction)

    best_comparer_answer = None
    

    '''Scores from Dense Passage Retrieval'''
    best_qa_answer = best_qa.score + best_qa.probability

    '''Comparing options with best context'''
    for option in question.options:
        score = comparer.compare(option.content, best_qa.context)
        # print("Comparer: {}, score: {:.3f}".format(option.content, score))
        if best_comparer_answer is None or best_comparer_answer.score < score + best_qa.score:
            best_comparer_answer = Result(score + best_qa.score, option.key)
    
    best_answer = None
    if best_qa_answer >= best_comparer_answer.score:
        '''QA method has higher score, comparing QA answer with options'''
        for option in question.options:
            score = comparer.compare(option.content, best_qa.answer)
            # print("Comparer: {}, score: {:.3f}".format(option.content, score))
            if best_answer is None or best_answer.score < score:
                best_answer = Result(score, option.key)
    else:
        # print("> Comparing method has higher score.")
        best_answer = best_comparer_answer

    question.answer = best_answer.content
    os.system('clear')
    
    return best_answer