def post_to_instagram(payload):

    return {
        "platform": "Instagram",
        "status": "mock_success",
        "message": "Instagram API placeholder ready.",
        "payload": payload
    }


def post_to_facebook(payload):

    return {
        "platform": "Facebook",
        "status": "mock_success",
        "message": "Facebook API placeholder ready.",
        "payload": payload
    }


def post_to_linkedin(payload):

    return {
        "platform": "LinkedIn",
        "status": "mock_success",
        "message": "LinkedIn API placeholder ready.",
        "payload": payload
    }


def notify_team(payload):

    return {
        "status": "mock_success",
        "message": "Team notification placeholder ready.",
        "payload": payload
    }