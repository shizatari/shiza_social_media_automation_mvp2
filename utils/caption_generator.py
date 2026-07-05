from datetime import datetime


def generate_caption(platform, topic, tone, audience, goal):

    platform = platform.lower()
    tone = tone.lower()
    audience = audience.lower()
    goal = goal.lower()

    openings = {
        "friendly": "🚀 Welcome to Tijarat AI Social Media Automation.",
        "professional": "Tijarat AI insight for modern businesses:",
        "informative": "💡 At Tijarat AI Social Media Automation, here's what you should know:",
        "promotional": "Scale your business with Tijarat AI Social Media Automation!",
        "inspiring": "Innovation at Tijarat AI starts with automation."
    }

    ctas = {
        "lead generation": "Book a demo to explore Tijarat AI automation workflows.",
        "sales": "Explore Tijarat AI Social Media Automation and upgrade your marketing.",
        "engagement": "Share your thoughts on AI automation in the comments.",
        "awareness": "Learn how Tijarat AI is transforming content workflows.",
        "website traffic": "Visit Tijarat AI to explore automation tools."
    }

    platform_hashtags = {
        "instagram": "#TijaratAI #AIAutomation #SocialMediaAutomation #Startups #Innovation",
        "facebook": "#TijaratAI #BusinessAutomation #AI #MarketingAutomation",
        "linkedin": "#TijaratAI #AIAutomation #BusinessGrowth #Startups #Innovation"
    }

    creative = {
        "instagram": "AI-powered reel showing automated content generation workflow.",
        "facebook": "Branded infographic on Tijarat AI automation benefits.",
        "linkedin": "Professional carousel explaining AI automation for startups and businesses."
    }

    opening = openings.get(tone, "Tijarat AI Social Media Automation helps businesses grow with AI.")

    cta = ctas.get(goal, "Learn more about Tijarat AI automation solutions.")

    hashtags = platform_hashtags.get(platform, "#TijaratAI #AIAutomation")

    creative_idea = creative.get(platform, "AI automation focused social media post.")

    long_caption = (
        f"{opening}\n\n"
        f"Topic: {topic}\n\n"
        f"Built for **{audience}**, this content focuses on **{goal}** using AI automation. "
        f"Tijarat AI Social Media Automation helps startups and businesses automate content creation, scheduling, and analytics.\n\n"
        f"{cta}"
    )

    short_caption = f"{opening} {topic}. {cta}"

    return {
        "date": datetime.today().strftime("%Y-%m-%d"),
        "caption": long_caption,
        "short_caption": short_caption,
        "hashtags": hashtags,
        "cta": cta,
        "creative_idea": creative_idea
    }