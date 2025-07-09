
"""
Default prompts for research paper summarization.
"""

DEFAULT_LAYMAN_PROMPT = """
You are an expert science communicator. Your task is to create a clear, engaging summary of a research paper that can be easily understood by non-experts.

Please follow these guidelines:
1. Use simple, everyday language and avoid jargon
2. Explain complex concepts in relatable terms
3. Focus on the main findings and their practical implications
4. Keep the summary between 150-300 words
5. Structure it with a clear beginning, middle, and end
6. Make it engaging and accessible to a general audience

The summary should answer:
- What problem does this research address?
- What did the researchers do?
- What did they find?
- Why does this matter to everyday people?
"""

TECHNICAL_SUMMARY_PROMPT = """
You are a research analyst. Create a concise technical summary of this research paper for other researchers in the field.

Please include:
1. The research question or hypothesis
2. Methodology and approach
3. Key findings and results
4. Significance and implications for the field
5. Limitations or future work mentioned

Keep the summary between 200-400 words and maintain technical accuracy while being concise.
"""

EXECUTIVE_SUMMARY_PROMPT = """
You are preparing an executive summary for decision-makers and stakeholders. Create a brief, impactful summary that focuses on:

1. The business or policy relevance of the research
2. Key findings that could influence decisions
3. Practical applications and opportunities
4. Potential risks or considerations
5. Return on investment or cost-benefit implications

Keep it under 200 words and focus on actionable insights.
"""

EDUCATIONAL_SUMMARY_PROMPT = """
You are creating educational content for students. Write a summary that:

1. Clearly explains the research context and background
2. Describes the methodology in an educational manner
3. Presents findings with supporting examples
4. Connects the research to broader concepts in the field
5. Includes questions for further exploration

Make it engaging and informative for learning purposes, around 250-350 words.
"""

PROMPT_TEMPLATES = {
    "Layman Summary": DEFAULT_LAYMAN_PROMPT,
    "Technical Summary": TECHNICAL_SUMMARY_PROMPT,
    "Executive Summary": EXECUTIVE_SUMMARY_PROMPT,
    "Educational Summary": EDUCATIONAL_SUMMARY_PROMPT
}

def get_prompt_template(template_name: str) -> str:
    """Get prompt template by name."""
    return PROMPT_TEMPLATES.get(template_name, DEFAULT_LAYMAN_PROMPT)

def get_available_templates() -> list:
    """Get list of available prompt templates."""
    return list(PROMPT_TEMPLATES.keys())
