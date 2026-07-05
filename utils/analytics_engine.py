import pandas as pd


def calculate_engagement(df):
    analytics = df.copy()

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

    return analytics


def best_platform(df):
    df = calculate_engagement(df)

    result = (
        df.groupby("platform")["engagement_rate"]
        .mean()
        .reset_index()
        .sort_values(by="engagement_rate", ascending=False)
    )

    return result


def merge_categories(content_df, analytics_df):
    merged = analytics_df.merge(
        content_df[["post_id", "post_category"]],
        on="post_id",
        how="left"
    )

    return merged


def best_category(merged_df):
    result = (
        merged_df.groupby("post_category")
        .agg({
            "reach": "mean",
            "engagement_rate": "mean"
        })
        .reset_index()
        .sort_values(by="engagement_rate", ascending=False)
    )

    return result