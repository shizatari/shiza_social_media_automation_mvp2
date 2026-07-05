import os
import google.generativeai as genai


def generate_gemini_caption(platform, topic, tone, audience, goal):

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return None

    try:
        genai.configure(api_key=api_key)

        model = genai.GenerativeModel("gemini-1.5-flash")

        prompt = f"""
You are generating content for "Tijarat AI Social Media Automation".

Platform: {platform}
Topic: {topic}
Tone: {tone}
Audience: {audience}
Goal: {goal}

This is a SaaS platform focused on:
- AI automation
- startup workflows
- marketing automation
- business productivity

Return strictly in this structure:
1. Caption
2. Short Caption
3. Hashtags
4. Call To Action
5. Creative Idea
"""

        response = model.generate_content(prompt)

        return response.text

    except Exception:
        return None