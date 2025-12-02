# rag/generator.py
import google.generativeai as genai

class Generator:
    def __init__(self):
        self.model = genai.GenerativeModel("gemini-2.5-flash")

    def apply_safety(self, user_msg: str):
        unsafe_keywords = ["raw chicken", "undercooked pork", "expired"]
        for k in unsafe_keywords:
            if k in user_msg.lower():
                return (
                    True,
                    "⚠️ For your safety, avoid unsafe food practices. "
                    "I can help you cook it properly if you want!"
                )
        return False, None

    def generate(self, user_msg, docs, memory):
        # Safety layer check
        unsafe, msg = self.apply_safety(user_msg)
        if unsafe:
            return msg

        context = "\n\n".join(docs)

        prompt = f"""
You are ChefBot, an intelligent RAG-based cooking assistant.

USER MESSAGE:
{user_msg}

CONVERSATION MEMORY:
{memory}

RAG DOCUMENTS:
{context}

YOUR TASK:
- Detect intent (recipe_query, cooking_help, substitution, smalltalk)
- Use RAG when relevant
- Summarize recipes clearly
- Provide clean bullet points + steps
- Keep friendly tone
"""

        res = self.model.generate_content(prompt)
        return res.text

    # Bonus feature — generate recipe from ingredients
    def generate_recipe_from_ingredients(self, ingredients):
        prompt = f"""
Create an original recipe using only these ingredients:

{ingredients}

Return:
- Recipe name
- Ingredients list
- Step-by-step cooking method
"""

        return self.model.generate_content(prompt).text
