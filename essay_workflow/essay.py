#!/usr/bin/env python
# coding: utf-8

# In[99]:


import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

# api_key = os.getenv("my_api_key")

# client = genai.Client(api_key=api_key)

# for model in client.models.list():
#     if "generateContent" in model.supported_actions:
#         print(model.name)


# In[100]:


from langgraph.graph import StateGraph ,START,END
from langgraph.graph import StateGraph
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from typing import TypedDict,Annotated
from pydantic import BaseModel,Field
import os
import operator


# In[101]:


load_dotenv()
api_key = os.getenv("my_api_key")


# In[136]:


model= ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite",google_api_key=api_key)


# In[137]:


class EvaluationSchema(BaseModel):

    feedback:str = Field(description="detaild feedback essay")
    score:int = Field(description="score out of 10",ge=0,le=10)


# In[138]:


structured_model=model.with_structured_output(EvaluationSchema)


# In[139]:


essay = """India in the Age of AI
As the world enters a transformative era defined by artificial intelligence (AI), India stands at a critical juncture — one where it can either emerge as a global leader in AI innovation or risk falling behind in the technology race. The age of AI brings with it immense promise as well as unprecedented challenges, and how India navigates this landscape will shape its socio-economic and geopolitical future.

India's strengths in the AI domain are rooted in its vast pool of skilled engineers, a thriving IT industry, and a growing startup ecosystem. With over 5 million STEM graduates annually and a burgeoning base of AI researchers, India possesses the intellectual capital required to build cutting-edge AI systems. Institutions like IITs, IIITs, and IISc have begun fostering AI research, while private players such as TCS, Infosys, and Wipro are integrating AI into their global services. In 2020, the government launched the National AI Strategy (AI for All) with a focus on inclusive growth, aiming to leverage AI in healthcare, agriculture, education, and smart mobility.

One of the most promising applications of AI in India lies in agriculture, where predictive analytics can guide farmers on optimal sowing times, weather forecasts, and pest control. In healthcare, AI-powered diagnostics can help address India’s doctor-patient ratio crisis, particularly in rural areas. Educational platforms are increasingly using AI to personalize learning paths, while smart governance tools are helping improve public service delivery and fraud detection.

However, the path to AI-led growth is riddled with challenges. Chief among them is the digital divide. While metropolitan cities may embrace AI-driven solutions, rural India continues to struggle with basic internet access and digital literacy. The risk of job displacement due to automation also looms large, especially for low-skilled workers. Without effective skilling and re-skilling programs, AI could exacerbate existing socio-economic inequalities.

Another pressing concern is data privacy and ethics. As AI systems rely heavily on vast datasets, ensuring that personal data is used transparently and responsibly becomes vital. India is still shaping its data protection laws, and in the absence of a strong regulatory framework, AI systems may risk misuse or bias.

To harness AI responsibly, India must adopt a multi-stakeholder approach involving the government, academia, industry, and civil society. Policies should promote open datasets, encourage responsible innovation, and ensure ethical AI practices. There is also a need for international collaboration, particularly with countries leading in AI research, to gain strategic advantage and ensure interoperability in global systems.

India’s demographic dividend, when paired with responsible AI adoption, can unlock massive economic growth, improve governance, and uplift marginalized communities. But this vision will only materialize if AI is seen not merely as a tool for automation, but as an enabler of human-centered development.

In conclusion, India in the age of AI is a story in the making — one of opportunity, responsibility, and transformation. The decisions we make today will not just determine India’s AI trajectory, but also its future as an inclusive, equitable, and innovation-driven society."""


# In[140]:


prompt = f'Evaluate the language quality of the fol lowing essay and provide a feedback and assign a score out of 10 \n {essay}'



# In[141]:


structured_model.invoke(prompt).feedback


# In[142]:


class UPSCState(TypedDict):


    essay:str
    language_feedback:str
    analysis_feedback:str
    clarity_feedback:str
    overall_feedback:str
    individual_feedback:Annotated[list[int],operator.add]
    avg_score:float






# In[143]:


def evaluate_language(state:UPSCState):
    prompt = f'Evaluate the language quality of the fol lowing essay and provide a feedback and assign a score out of 10 \n {state["essay"]}'

    output=structured_model.invoke(prompt)

    return {'language_feedback':output,"individual_feedback":[output.score]}



# In[144]:


def evaluate_analysis(state:UPSCState):
    prompt = f'Evaluate the depth of analysis of the following essay and provide a feedback and assign a score out of 10 \n {state["essay"]}'

    output=structured_model.invoke(prompt)

    return {'analysis_feedback':output,"individual_feedback":[output.score]}


# In[145]:


def evaluate_clarity(state:UPSCState):
    prompt = f'Evaluate the depth of the clarity of the following essay and provide a feedback and assign a score out of 10 \n {state["essay"]}'

    output=structured_model.invoke(prompt)

    return {'clarity_feedback':output,"individual_feedback":[output.score]}


# In[146]:


def final_evolution(state:UPSCState):
    prompt = f'Based on the following feedbacks create a summarized feedback \n language feedback - {state["language_feedback"]} \n depth of analysis feedback - {state["analysis_feedback"]} \n clarity of thought feedback - {state["clarity_feedback"]}'
    overall_feedback = model.invoke(prompt).content


    avg_score = sum(state['individual_feedback'])/len(state['individual_feedback'])

    return {'overall_feedback': overall_feedback, 'avg_score': avg_score}



# In[147]:


graph = StateGraph(UPSCState)

graph.add_node("evaluate_language", evaluate_language)
graph.add_node("evaluate_clarity", evaluate_clarity)
graph.add_node("evaluate_analysis", evaluate_analysis)
graph.add_node("final_evolution", final_evolution)

graph.add_edge(START, "evaluate_language")
graph.add_edge(START, "evaluate_clarity")
graph.add_edge(START, "evaluate_analysis")

graph.add_edge("evaluate_language", "final_evolution")
graph.add_edge("evaluate_clarity", "final_evolution")
graph.add_edge("evaluate_analysis", "final_evolution")

graph.add_edge("final_evolution", END)


# In[148]:


work=graph.compile()


# In[149]:


work


# In[150]:


essay2 = """India and AI Time

Now world change very fast because new tech call Artificial Intel… something (AI). India also want become big in this AI thing. If work hard, India can go top. But if no careful, India go back.

India have many good. We have smart student, many engine-ear, and good IT peoples. Big company like TCS, Infosys, Wipro already use AI. Government also do program “AI for All”. It want AI in farm, doctor place, school and transport.

In farm, AI help farmer know when to put seed, when rain come, how stop bug. In health, AI help doctor see sick early. In school, AI help student learn good. Government office use AI to find bad people and work fast.

But problem come also. First is many villager no have phone or internet. So AI not help them. Second, many people lose job because AI and machine do work. Poor people get more bad.

One more big problem is privacy. AI need big big data. Who take care? India still make data rule. If no strong rule, AI do bad.

India must all people together – govern, school, company and normal people. We teach AI and make sure AI not bad. Also talk to other country and learn from them.

If India use AI good way, we become strong, help poor and make better life. But if only rich use AI, and poor no get, then big bad thing happen.

So, in short, AI time in India have many hope and many danger. We must go right road. AI must help all people, not only some. Then India grow big and world say "good job India"."""


# In[151]:


intial_state = {
    'essay': essay2
}

op=work.invoke(intial_state)

print(op)