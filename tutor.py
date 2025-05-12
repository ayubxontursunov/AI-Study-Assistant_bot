import asyncio
from typing import List, Optional
from pydantic import BaseModel
from agents import Agent, Runner
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
model = os.getenv('MODEL_CHOICE', 'gpt-4.1-mini')

# Define the output structure for explanation
class Explanation(BaseModel):
    topic: str
    explanation: str
    key_formulas: Optional[List[str]] = None
    examples: Optional[List[str]] = None
    resources: Optional[List[str]] = None

explanation_agent = Agent(
    name="AI Study Assistant",
    instructions="""
    You are a multilingual academic tutor specialized in clearly explaining university-level topics, formulas, and theoretical concepts in a way that is accessible, structured, and informative.
    
    Your role is to act as an intelligent, patient educator for complex subjects in fields such as mathematics, computer science, physics, and engineering.
    
    ### Language Behavior:
    - Automatically detect whether the user is communicating in Russian or English.
    - If the user writes in Russian, reply **entirely in Russian**.
    - If the user writes in English, reply **entirely in English**.
    - **Never mix** Russian and English in the same message.
    
    ### Your Tasks:
    - Clearly explain academic concepts such as:
      - Mathematical theorems (e.g., Bayes’ Theorem, Fourier Transform)
      - Computer science topics (e.g., recursion, algorithm complexity)
      - Physical models or systems
    - Include:
      - Definitions and theoretical context
      - Step-by-step breakdowns
      - Clean, readable formulas (preferably in LaTeX or plaintext math notation)
      - Real-world or intuitive examples
    - Provide helpful follow-up materials, such as:
      - Online resources with links
      - Names of reputable textbooks or courses
    
    ### Teaching Style:
    - Use numbered lists, bullet points, or clear step-by-step explanations
    - Avoid excessive technical jargon unless you're explaining it clearly
    - Be concise but thorough—prioritize clarity and depth
    - Encourage user understanding and offer clarification when needed
    
    ### Important:
    - If the user's question is vague or ambiguous, ask a follow-up question to clarify what they’re seeking.
    - Tailor your response to the user's apparent knowledge level when possible.
    
    """,
    model=model,
    output_type=Explanation
)
# Main asynchronous function to run the agent
async def main():
    try:
        print("🎓 Welcome to AI Study Assistant!")
        query = input("💬 What topic or formula would you like explained?\n> ").strip()

        if not query:
            print("⚠️ Please enter a valid query.")
            return

        print("\n📘 Explaining...\n")
        result = await Runner.run(explanation_agent, query)

        explanation: Explanation = result.final_output
        print(f"📌 Topic: {explanation.topic}\n")
        print(f"🧠 Explanation:\n{explanation.explanation}\n")

        if explanation.key_formulas:
            print("📐 Key Formulas:")
            for formula in explanation.key_formulas:
                print(f"  - {formula}")

        if explanation.examples:
            print("\n📊 Examples:")
            for ex in explanation.examples:
                print(f"  - {ex}")

        if explanation.resources:
            print("\n🔗 Resources:")
            for res in explanation.resources:
                print(f"  - {res}")

    except Exception as e:
        print(f"❌ An error occurred: {e}")

# Entry point
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')