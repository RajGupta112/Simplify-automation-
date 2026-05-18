"""
AI Service - Production Grade
"""

import json
import logging
from google import genai
from django.conf import settings

logger = logging.getLogger(__name__)


class AIService:

    def __init__(self):
        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY
        )
        self.model_name = "gemini-2.5-flash"

    def analyze_company(self, lead, enrichment_data: dict) -> dict:

        try:
            content = enrichment_data.get("content", "")
            description = enrichment_data.get("description", "")
            technologies = enrichment_data.get("technologies", [])

            prompt = f"""
You are a senior B2B AI consultant.

Generate a HIGHLY DETAILED business audit.

CRITICAL RULES:
- NEVER return empty arrays
- ALWAYS return at least 4 items per list
- Be SPECIFIC to company context
- Avoid generic statements
- If data is missing, infer logically

-----------------------------------
COMPANY
-----------------------------------
Name: {lead.company_name}
Industry: {lead.industry}
Goal: {lead.business_goal}

Description:
{description}

Content:
{content[:3500]}

Tech Stack:
{technologies}

-----------------------------------
OUTPUT JSON ONLY
-----------------------------------

{{
  "company_summary": "detailed 6-8 line analysis",

  "pain_points": [
    "minimum 4 realistic pain points"
  ],

  "ai_opportunities": [
    "minimum 4 AI opportunities"
  ],

  "automation_recommendations": [
    "minimum 4 automation strategies"
  ],

  "website_insights": {{
    "title": "",
    "description": "",
    "technologies": []
  }},

  "personalized_email": "highly converting B2B email"
}}

STRICT:
- valid JSON only
- no markdown
"""

            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )

            raw = response.text

            cleaned = raw.replace("```json", "").replace("```", "").strip()

            parsed = json.loads(cleaned)

            # ---------------- SAFE FALLBACKS ----------------
            parsed.setdefault("pain_points", ["No pain points detected - inferred"])
            parsed.setdefault("ai_opportunities", ["AI opportunity not detected - inferred"])
            parsed.setdefault("automation_recommendations", ["Automation not detected - inferred"])

            return {
                "success": True,
                "data": parsed
            }

        except Exception as error:
            logger.error(f"AI analysis failed: {error}")

            return {
                "success": False,
                "error": str(error)
            }


ai_service = AIService()