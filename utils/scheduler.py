import json


def generate_scheduler_payload(content_df):

    payloads = []

    for _, row in content_df.iterrows():

        payload = {
            "post_id": row["post_id"],
            "platform": row["platform"],
            "caption": row["caption"],
            "hashtags": row["hashtags"],
            "media_url": f"https://tijaratai.com/media/{row['post_id']}.jpg",
            "scheduled_time": row["scheduled_time"],
            "status": "Ready for API",
            "topic": row["topic"],
            "creative_type": row["creative_type"],
            "assigned_to": row["assigned_to"]
        }

        payloads.append(payload)

    return payloads


def save_scheduler_payloads(payloads):

    output_file = "outputs/scheduler_payloads.json"

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(payloads, file, indent=4)