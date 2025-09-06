from docxcompose.composer import Composer
from docx import Document

def merge_docs(output_path, *input_paths):
    """
    Merges multiple DOCX files into a single document.

    Args:
        output_path (str): The path to save the merged document.
        *input_paths (str): Variable number of paths to the input DOCX files.
    """
    if not input_paths:
        print("No input files provided.")
        return

    base_doc = Document(input_paths[0])
    composer = Composer(base_doc)

    for file_path in input_paths[1:]:
        doc = Document(file_path)
        composer.append(doc)

    composer.save(output_path)
    print(f"Documents merged successfully into {output_path}")

if __name__ == "__main__":
    output_file = "merged_document.docx"
    input_files = ["Acknowledgment.docx","Foreword.docx","A Thought Leader's Perspective Power and Responsibility.docx","Introduction.docx","What makes an AI system an 'agent'.docx","Chapter 1_ Prompt Chaining.docx","Chapter 2_ Routing.docx","Chapter 3_ Parallelization.docx","Chapter 4_ Reflection.docx","Chapter 5_ Tool Use.docx","Chapter 6_ Planning.docx","Chapter 7_ Multi-Agent.docx","Chapter 8_ Memory Management.docx","Chapter 9_ Learning and Adaptation.docx","Chapter 10_ Model Context Protocol (MCP).docx","Chapter 11_ Goal Setting and Monitoring.docx","Chapter 12_ Exception Handling and Recovery.docx","Chapter 13_ Human-in-the-Loop.docx","Chapter 14_ Knowledge Retrieval (RAG).docx","Chapter 15_ Inter-Agent Communication (A2A.docx","Chapter 16_ Resource-Aware Optimization.docx","Chapter 17_ Reasoning Techniques.docx","Chapter 18_ Guardrails Safety Patterns.docx","Chapter 19_ Evaluation and Monitoring.docx","Chapter 20_ Prioritization.docx","Chapter 21_ Exploration and Discovery.docx","Appendix A_ Advanced Prompting Techniques.docx","Appendix B - AI Agentic _ From GUI to Real world environment.docx","Appendix C - Quick overview of Agentic Frameworks.docx","Appendix D - Building an Agent with AgentSpace (on-line only).docx","Appendix E - AI Agents on the CLI (online) .docx","Appendix F - Under the Hood_ An Inside Look at the Agents Reasoning Engines.docx","Appendix G -  Coding agents.docx","Conclusion.docx","Glossary.docx","Index of Terms.docx","Online.docx","Contribution.docx","Frequently Asked Questions_ Agentic Design Patterns.docx"]
    merge_docs(output_file, *input_files)