import json
import chainlit as cl
from agents import Runner, function_tool
from src.research_agents import  source_checker_agent, contradiction_detector_agent, final_answer_agent
from src.research_agents import planning_agent
from src.tools.search import parallel_search




@function_tool
async def comprehensive_research(original_question: str) -> str:
    """
    Use this tool for any complex question that requires in-depth research from multiple angles.
    This tool performs a multi-step research process: planning, parallel data gathering, source checking, contradiction detection, and final synthesis.
    """
    async with cl.Step(name="Comprehensive Researcher") as main:
        main.input = original_question

        # Step 1: Plan Research
        async with cl.Step(name="Planner") as plan_step:
            plan_step.input = original_question

            print("--- 📝 Phase 1: Planning Research ---")
            output = await Runner.run(planning_agent, original_question)
            sub_questions = output.final_output

            plan_step.output = sub_questions


        
        # Step 2: Gather data in Parallel
        async with cl.Step(name="Parallel Web Searcher") as search_step:
            search_step.input = sub_questions

            print("--- 🚀 Phase 2: Gathering Data in Parallel ---")
            (source_urls, content_for_analysis) = await parallel_search(sub_questions)

            search_step.output = json.dumps({"source_urls":source_urls, "contents_for_analyis": content_for_analysis})

        

        # Step 3: Check Source Quality
        async with cl.Step(name="Source Quality Checker") as quality_step:
            quality_step.input = search_step.output

            print("--- 🧐 Phase 3: Checking Source Quality ---")
            source_quality_report = await Runner.run(source_checker_agent, f"Please analyze these sources: {source_urls}")
            print(f"✅ Source quality report generated.\n")

            quality_step.output = source_quality_report.final_output

        
        # Step 4: Detect Contradictions
        async with cl.Step(name="Contradictions Detector") as contradict_step:
            contradict_step.input = search_step.output

            print("--- ⚔️ Phase 4: Detecting Contradictions ---")
            contradiction_report = await Runner.run(contradiction_detector_agent, content_for_analysis)
            print(f"✅ Contradiction analysis complete.\n")

            contradict_step.output = contradiction_report.final_output

        
        # Step 5: Synthesize Final Report
        async with cl.Step(name="Report Writer") as report_step:
            report_step.input = f"Original Question: {original_question}\n\n"
            f"Combined Raw Research Data:\n{content_for_analysis}\n\n"
            f"Source Quality Report:\n{source_quality_report.final_output}\n\n"
            f"Contradiction Report:\n{contradiction_report.final_output}\n\n"
            f"Source URLs:\n{source_urls}"

            final_result = await Runner.run(final_answer_agent, report_step.input)
            print(final_result)
            print(f"✅ Contradiction analysis complete.\n")

            report_step.output = final_result.final_output

        main.output = final_result.final_output
    
    return final_result.final_output
