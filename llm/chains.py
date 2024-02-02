from langchain_core.prompts import PromptTemplate
from llm.prompts import analyser_prompt_template
from operator import itemgetter
from llm.llm_config import initialize_google_llm



def build_analyser_chain(llm):
    prompt = PromptTemplate(
        template=analyser_prompt_template(),
        input_variables=["songs", "clustering_analysis"]
    )


    chain = (
        {
            "songs": itemgetter("songs"),
            "clustering_analysis": itemgetter("clustering_analysis")
        }
        | prompt
        | llm
    )

    return chain
