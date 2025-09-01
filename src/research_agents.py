from agents import Agent
from src.config import llm_model

# 1. Planning Agent
planning_agent = Agent(
    name="ResearchPlanner",
    instructions=(
        "You are a research planner. Your task is to break down a complex research question into 4-6 focused sub-questions. "
    ),
    model=llm_model,
    output_type=list[str]
)

# 3. Source Checker Agent
source_checker_agent = Agent(
    name="SourceCheckerAgent",
    instructions=(
        "You are a source quality analyst. Review a list of source URLs and rate them as 'High', 'Medium', or 'Low'. "
        "Provide a brief report summarizing the quality of the sources."
    ),
    model=llm_model,
)

# 4. Contradiction Detector Agent
contradiction_detector_agent = Agent(
    name="ContradictionDetectorAgent",
    instructions=(
        "You are a contradiction detector. Your task is to analyze a body of text compiled from multiple sources. "
        "Identify any conflicting or contradictory statements. If you find conflicts, describe them clearly (e.g., 'Source A says X, but Source B says Y'). "
        "If you find no significant contradictions, state that."
    ),
    model=llm_model,
)

# 5. Final Answer Agent
final_answer_agent = Agent(
    name="FinalAnswerAgent",
    instructions=(
        "You are a professional report writer. Your task is to write a high-quality, analytical report based on the provided research findings.\n\n"
        "**CRITICAL INSTRUCTIONS:**\n"
        "1.  **Thematic Structure**: Do NOT just list facts. Analyze the research data to identify key themes, trends, and insights. Organize your report into clear sections based on these themes.\n"
        "2.  **Inline Citations**: Use IEEE citation guidelines For EVERY piece of information or claim you include in your report, you MUST add a numbered citation marker, like `[1]`, `[2]`, etc., immediately after the sentence or claim.\n"
        "3.  **Numbered Reference List**: At the end of your report, create a 'References' section. This section must be a numbered list where each number corresponds to the citation marker in your text. The research data is provided as a JSON array, where each object has a 'url'. Use the 'url' for the reference list. You will need to assign a number to each unique URL.\n"
        "4.  **Synthesize, Don't Copy**: Do not copy-paste from the sources. Synthesize the information in your own words to create a coherent narrative.\n"
        "5.  **Incorporate Analysis**: You will also receive a 'Source Quality Report' and a 'Contradiction Report'. Weave insights from these reports into your analysis. For example, add a 'Confidence Score' section and a 'Conflicting Information' section if applicable.\n\n"
        "**Final Report Structure:**\n"
        "- **Introduction**: Briefly introduce the topic.\n"
        "- **Thematic Sections**: Multiple sections, each dedicated to a key theme you identified (e.g., 'Cost Analysis', 'Environmental Impact').\n"
        "- **Confidence Score**: Based on the source quality report.\n"
        "- **Conflicting Information**: (If any) Detail the disagreements found in the contradiction report.\n"
        "- **Conclusion**: Summarize the key insights.\n"
        "- **References**: A numbered list of all source URLs in IEEE format."
    ),
    model=llm_model,
)
