def generate_weekly_summary(content_df, analytics_df, tasks_df):

    total_posts = len(content_df)

    posted_posts = len(content_df[content_df["status"] == "Posted"])

    pending_approvals = len(content_df[content_df["approval_status"] == "Pending"])

    completed_tasks = len(tasks_df[tasks_df["status"] == "Completed"])

    # FIXED: no Overdue column exists → use status logic
    overdue_tasks = len(tasks_df[tasks_df["status"] == "Overdue"])

    analytics = analytics_df.copy()

    analytics["engagement_rate"] = (
        (
            analytics["likes"]
            + analytics["comments"]
            + analytics["shares"]
            + analytics["saves"]
            + analytics["clicks"]
        )
        / analytics["reach"].replace(0, 1)
    ) * 100

    platform = (
        analytics.groupby("platform")["engagement_rate"]
        .mean()
        .idxmax()
    )

    merged = analytics.merge(
        content_df[["post_id", "post_category"]],
        on="post_id",
        how="left"
    )

    category = (
        merged.groupby("post_category")["reach"]
        .mean()
        .idxmax()
    )

    summary = f"""
WEEKLY SOCIAL MEDIA SUMMARY - TIJARAT AI SOCIAL MEDIA AUTOMATION

Total Posts Planned: {total_posts}

Posts Published: {posted_posts}

Best Performing Platform: {platform}

Best Performing Category: {category}

Pending Approvals: {pending_approvals}

Completed Tasks: {completed_tasks}

Overdue Tasks: {overdue_tasks}

Recommendation:

Focus on strengthening {category} content within Tijarat AI Social Media Automation.
Improve AI-driven workflows for {platform} to maximize engagement and automate content scaling.
"""

    return summary