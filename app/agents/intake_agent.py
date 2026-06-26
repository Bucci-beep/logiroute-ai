import json
from groq import Groq
from app.core.config import settings
from app.models.schemas import CargoIntakeSchema


class IntakeAgent:
    def __init__(self):
        self.client = Groq(api_key=settings.GROQ_API_KEY)
        # Using llama3-8b-8192 for fast, cost-effective structured text transformations
        self.model = "llama3-8b-8192"

    async def parse_unstructured_broker_text(self, raw_text: str) -> dict:
        """Parses messy, raw broker text strings into deterministic JSON schemas."""

        system_prompt = (
            "You are an elite operational broker tracking system. Your objective is to extract logistics details "
            "from unstructured communications and map them directly into structured configurations. "
            "You must output valid, pure JSON conforming explicitly to this layout structure:\n"
            "{\n"
            "  \"cargo_description\": \"string\",\n"
            "  \"weight_lbs\": float,\n"
            "  \"usdot_number\": \"string\",\n"
            "  \"pickup_date\": \"YYYY-MM-DD\",\n"
            "  \"origin_city\": \"string\",\n"
            "  \"destination_city\": \"string\"\n"
            "}\n"
            f"Note: For reference, today's system execution date context is: {CargoIntakeSchema.__fields__['pickup_date'].default or '2026-06-26'}. "
            "Ensure output is raw JSON only. Do not add markdown commentary outside the JSON blob."
        )

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Extract structural data elements from this raw message:\n\n{raw_text}"}
            ],
            temperature=0.0,
            response_format={"type": "json_object"}
        )

        extracted_json = json.loads(response.choices[0].message.content)
        return extracted_json