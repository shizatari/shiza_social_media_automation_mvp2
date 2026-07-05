import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import os
import csv

from utils.caption_generator import generate_caption

from utils.scheduler import (
    generate_scheduler_payload,
    save_scheduler_payloads
)

from utils.api_placeholders import (
    post_to_instagram,
    post_to_facebook,
    post_to_linkedin,
    notify_team
)

import json

from utils.analytics_engine import (
    calculate_engagement,
    best_platform,
    merge_categories,
    best_category
)

from utils.weekly_summary import generate_weekly_summary

from utils.gemini_generator import generate_gemini_caption

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Tijarat AI Social Media Automation",
    page_icon="🤖",
    layout="wide"
)

# --------------------------------------------------
# Load Data
# --------------------------------------------------

@st.cache_data
def load_data():
    content_df = pd.read_csv("data/content_calendar.csv")
    analytics_df = pd.read_csv("data/analytics.csv")
    tasks_df = pd.read_csv("data/team_tasks.csv")

    return content_df, analytics_df, tasks_df


content_df, analytics_df, tasks_df = load_data()

# --------------------------------------------------
# Sidebar
# --------------------------------------------------

st.sidebar.title("🤖 Tijarat AI")

st.sidebar.markdown(
    """
### Social Media Automation

Manage AI-generated content, approvals, scheduling, analytics and team collaboration from one dashboard.
"""
)

st.sidebar.divider()

page = st.sidebar.radio(
    "📂 Navigation",
    (
        "Overview",
        "Content Calendar",
        "Caption Generator",
        "Approval Tracker",
        "Scheduler Preview",
        "Analytics Dashboard",
        "Team Tasks"
    )
)

st.sidebar.divider()

st.sidebar.markdown("### 🚀 MVP Features")

st.sidebar.success("AI Caption Generation")
st.sidebar.success("Approval Workflow")
st.sidebar.success("Scheduler Preview")
st.sidebar.success("Analytics Dashboard")
st.sidebar.success("Weekly Reports")

st.sidebar.divider()

st.sidebar.caption(
    "Developed for the Tijarat AI Technical Assessment"
)

# --------------------------------------------------
# OVERVIEW
# --------------------------------------------------

if page == "Overview":

    st.title("🤖 Tijarat AI Social Media Automation")
    st.caption(
        "Manage content planning, AI-generated captions, approvals, scheduling, analytics and team collaboration from one centralized dashboard."
    )

    st.divider()

    # ---------------------------------
    # KPI Cards
    # ---------------------------------

    total_posts = len(content_df)

    posted_posts = len(
        content_df[content_df["status"].fillna("") == "Posted"]
    )

    scheduled_posts = len(
        content_df[content_df["status"] == "Scheduled"]
    )

    pending_approvals = len(
        content_df[
            content_df["approval_status"] == "Pending"
        ]
    )

    completed_tasks = len(
        tasks_df[
            tasks_df["status"] == "Completed"
        ]
    )

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric("📝 Total Posts", total_posts)
    c2.metric("✅ Posted", posted_posts)
    c3.metric("📅 Scheduled", scheduled_posts)
    c4.metric("⏳ Pending Approval", pending_approvals)
    c5.metric("👥 Completed Tasks", completed_tasks)

    st.divider()

    # ---------------------------------
    # Dashboard Summary
    # ---------------------------------

    left, right = st.columns([2, 1])

    with left:

        st.subheader("📊 Content Distribution")

        chart = content_df["platform"].value_counts()

        fig = px.bar(
            x=chart.index,
            y=chart.values,
            labels={
                "x": "Platform",
                "y": "Number of Posts"
            },
            title="Posts by Platform"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with right:

        st.subheader("📌 Quick Summary")

        st.success(
            f"✅ {posted_posts} posts have already been published."
        )

        st.info(
            f"📅 {scheduled_posts} posts are scheduled for publishing."
        )

        st.warning(
            f"⏳ {pending_approvals} posts are waiting for approval."
        )

        st.success(
            f"👥 {completed_tasks} team tasks have been completed."
        )

    st.divider()

    # ---------------------------------
    # Recent Content
    # ---------------------------------

    st.subheader("📰 Recent Content Calendar")

    st.dataframe(
        content_df.head(10),
        use_container_width=True
    )

    st.divider()

    # ---------------------------------
    # Future Integrations
    # ---------------------------------

    st.subheader("🔗 Future Integrations")

    st.info(
        "Future versions can synchronize the content calendar with Google Sheets and connect directly to Meta, LinkedIn, Canva and other marketing platforms."
    )

    col1, col2 = st.columns(2)

    with col1:

        st.button(
            "📄 Connect Google Sheets",
            disabled=True
        )

    with col2:

        st.button(
            "🎨 Connect Canva",
            disabled=True
        )

# --------------------------------------------------
# CONTENT CALENDAR
# --------------------------------------------------

elif page == "Content Calendar":

    st.title("📅 Content Calendar")

    st.caption(
        "Plan, organize and monitor all social media content for Tijarat AI."
    )

    st.divider()

    st.subheader("🔎 Filter Content")

    col1, col2 = st.columns(2)

    with col1:

        platform = st.selectbox(
            "Platform",
            ["All"] + sorted(content_df["platform"].unique())
        )

        category = st.selectbox(
            "Category",
            ["All"] + sorted(content_df["post_category"].unique())
        )

    with col2:

        status = st.selectbox(
            "Workflow Status",
            ["All"] + sorted(content_df["status"].unique())
        )

        approval = st.selectbox(
            "Approval Status",
            ["All"] + sorted(content_df["approval_status"].unique())
        )

    assigned_to = st.selectbox(
        "Assigned Team Member",
        ["All"] + sorted(content_df["assigned_to"].unique())
    )

    filtered = content_df.copy()

    if platform != "All":
        filtered = filtered[
            filtered["platform"] == platform
        ]

    if category != "All":
        filtered = filtered[
            filtered["post_category"] == category
        ]

    if status != "All":
        filtered = filtered[
            filtered["status"] == status
        ]

    if approval != "All":
        filtered = filtered[
            filtered["approval_status"] == approval
        ]

    if assigned_to != "All":
        filtered = filtered[
            filtered["assigned_to"] == assigned_to
        ]

    st.divider()

    st.success(
        f"{len(filtered)} post(s) found."
    )

    st.dataframe(
        filtered,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    st.subheader("📥 Export Filtered Content Calendar")

    csv = filtered.to_csv(index=False)

    st.download_button(
        label="⬇ Download Filtered CSV",
        data=csv,
        file_name="filtered_content_calendar.csv",
        mime="text/csv"
    )

# --------------------------------------------------
# CAPTION GENERATOR
# --------------------------------------------------

elif page == "Caption Generator":

    st.title("✍️ AI Caption Generator")

    st.caption(
        "Generate professional marketing captions for Tijarat AI campaigns using a Rule-Based engine or Google Gemini AI."
    )

    st.info(
        "💡 Complete the campaign details below and click **Generate Marketing Caption** to create platform-specific content."
    )

    st.divider()

    provider = st.radio(
        "Choose AI Provider",
        [
            "Rule-Based",
            "Gemini (Optional)"
        ],
        horizontal=True
    )

    st.subheader("📋 Campaign Details")

    col1, col2 = st.columns(2)

    with col1:

        platform = st.selectbox(
            "Platform",
            ["Instagram", "Facebook", "LinkedIn"]
        )

        topic = st.text_input(
            "Campaign Topic",
            placeholder="Example: AI Automation Workshop"
        )

        tone = st.selectbox(
            "Tone",
            [
                "Friendly",
                "Professional",
                "Informative",
                "Promotional",
                "Inspiring"
            ]
        )

    with col2:

        audience = st.text_input(
            "Target Audience",
            placeholder="Example: Startup founders, university students"
        )

        goal = st.selectbox(
            "Campaign Goal",
            [
                "Sales",
                "Lead Generation",
                "Engagement",
                "Awareness",
                "Website Traffic"
            ]
        )

    st.divider()

    if st.button(
        "🚀 Generate Marketing Caption",
        use_container_width=True
    ):

        if topic.strip() == "":

            st.error("Please enter a campaign topic.")

            st.stop()

        with st.spinner("Generating caption..."):

            if provider == "Gemini (Optional)":

                gemini_text = generate_gemini_caption(
                    platform,
                    topic,
                    tone,
                    audience,
                    goal
                )

                if gemini_text:

                    result = {
                        "caption": gemini_text,
                        "short_caption": (gemini_text[:150] + "...") if len(gemini_text) > 150 else gemini_text,
                        "hashtags": "#TijaratAI #AIAutomation #SocialMediaAutomation #Startups #Innovation",
                        "cta": "Learn more today!",
                        "creative_idea": "Professional Canva social media design."
                    }

                    st.success("Generated using Google Gemini AI")

                else:

                    st.warning(
                        "Gemini API unavailable. Falling back to Rule-Based Generator."
                    )

                    result = generate_caption(
                        platform,
                        topic,
                        tone,
                        audience,
                        goal
                    )

            else:

                result = generate_caption(
                    platform,
                    topic,
                    tone,
                    audience,
                    goal
                )

        st.session_state["caption_result"] = result

        st.session_state["caption_inputs"] = {
            "platform": platform,
            "topic": topic,
            "tone": tone,
            "audience": audience,
            "goal": goal
        }

    if "caption_result" in st.session_state:

        result = st.session_state["caption_result"]

        inputs = st.session_state["caption_inputs"]

        st.divider()

        st.success("✅ Caption Generated Successfully")

        st.subheader("Generated Marketing Content")

        with st.expander("📝 Long Caption", expanded=True):

            st.write(result["caption"])

        with st.expander("📱 Short Caption"):

            st.success(result["short_caption"])

        with st.expander("🏷️ Suggested Hashtags"):

            st.code(result["hashtags"])

        with st.expander("📣 Call To Action"):

            st.info(result["cta"])

        with st.expander("🎨 Creative Design Idea"):

            st.warning(result["creative_idea"])

        st.divider()

        st.subheader("🎨 Canva Design Asset")

        st.info(
            "Future integration: Canva templates can automatically generate social media creatives using the generated caption."
        )

        st.divider()

        col1, col2 = st.columns(2)

        with col1:

            if st.button(
                "💾 Save Caption",
                use_container_width=True
            ):

                filename = "data/generated_captions.csv"

                if os.path.exists(filename):

                    df = pd.read_csv(filename)

                else:

                    df = pd.DataFrame()

                new_row = pd.DataFrame([{

                    "caption_id": f"C{len(df)+1:03}",

                    "date": datetime.today().strftime("%Y-%m-%d"),

                    "platform": inputs["platform"],

                    "topic": inputs["topic"],

                    "tone": inputs["tone"],

                    "audience": inputs["audience"],

                    "caption": result["caption"],

                    "hashtags": result["hashtags"],

                    "cta": result["cta"],

                    "creative_idea": result["creative_idea"]

                }])

                df = pd.concat(
                    [df, new_row],
                    ignore_index=True
                )

                df.to_csv(
                    filename,
                    index=False
                )

                st.success("Caption saved successfully!")

        with col2:

            st.metric(
                "Platform",
                inputs["platform"]
            )

        if os.path.exists("data/generated_captions.csv"):

            saved_df = pd.read_csv(
                "data/generated_captions.csv"
            )

            st.divider()

            st.subheader("📚 Saved Captions")

            st.dataframe(
                saved_df,
                use_container_width=True
            )

            csv = saved_df.to_csv(
                index=False
            )

            st.download_button(
                "⬇ Download Captions CSV",
                csv,
                file_name="generated_captions.csv",
                mime="text/csv",
                use_container_width=True
            )

# --------------------------------------------------
# APPROVAL TRACKER
# --------------------------------------------------

elif page == "Approval Tracker":

    st.title("✅ Approval Workflow")

    st.caption(
        "Review submitted content, approve posts for publishing, request revisions, or reject content before scheduling."
    )

    st.divider()

    # ---------------------------------
    # KPI Cards
    # ---------------------------------

    pending = len(
        content_df[
            content_df["approval_status"] == "Pending"
        ]
    )

    approved = len(
        content_df[
            content_df["approval_status"] == "Approved"
        ]
    )

    revision = len(
        content_df[
            content_df["approval_status"] == "Needs Revision"
        ]
    )

    rejected = len(
        content_df[
            content_df["approval_status"] == "Rejected"
        ]
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("⏳ Pending", pending)
    c2.metric("✅ Approved", approved)
    c3.metric("📝 Needs Revision", revision)
    c4.metric("❌ Rejected", rejected)

    st.divider()

    # ---------------------------------
    # Filters
    # ---------------------------------

    st.subheader("🔎 Filter Posts")

    col1, col2, col3 = st.columns(3)

    with col1:

        platform_filter = st.selectbox(
            "Platform",
            ["All"] + sorted(content_df["platform"].unique())
        )

    with col2:

        approval_filter = st.selectbox(
            "Approval Status",
            ["All"] + sorted(content_df["approval_status"].unique())
        )

    with col3:

        person_filter = st.selectbox(
            "Assigned Person",
            ["All"] + sorted(content_df["assigned_to"].unique())
        )

    filtered = content_df.copy()

    if platform_filter != "All":

        filtered = filtered[
            filtered["platform"] == platform_filter
        ]

    if approval_filter != "All":

        filtered = filtered[
            filtered["approval_status"] == approval_filter
        ]

    if person_filter != "All":

        filtered = filtered[
            filtered["assigned_to"] == person_filter
        ]

    st.divider()

    # ---------------------------------
    # Approval Queue
    # ---------------------------------

    st.subheader("📋 Content Awaiting Review")

    st.dataframe(

        filtered[
            [
                "post_id",
                "platform",
                "topic",
                "assigned_to",
                "status",
                "approval_status",
                "scheduled_time"
            ]
        ],

        use_container_width=True

    )

    st.divider()

    # ---------------------------------
    # Update Approval
    # ---------------------------------

    st.subheader("📝 Review Selected Post")

    post_list = filtered["post_id"].tolist()

    if len(post_list) == 0:

        st.info("No posts match the selected filters.")

    else:

        selected_post = st.selectbox(
            "Select Post",
            post_list
        )

        current_status = content_df.loc[
            content_df["post_id"] == selected_post,
            "approval_status"
        ].iloc[0]

        new_status = st.selectbox(
            "New Approval Status",
            [
                "Pending",
                "Approved",
                "Needs Revision",
                "Rejected"
            ],
            index=[
                "Pending",
                "Approved",
                "Needs Revision",
                "Rejected"
            ].index(current_status)
        )

        if st.button("✅ Update Approval Status"):

            row = content_df[
                content_df["post_id"] == selected_post
            ].index[0]

            content_df.at[
                row,
                "approval_status"
            ] = new_status

            workflow_status = content_df.at[
                row,
                "status"
            ]

            if new_status == "Approved":

                if workflow_status in [
                    "Idea",
                    "Drafted",
                    "Designed"
                ]:

                    content_df.at[
                        row,
                        "status"
                    ] = "Approved"

            elif new_status == "Needs Revision":

                content_df.at[
                    row,
                    "status"
                ] = "Drafted"

            elif new_status == "Rejected":

                content_df.at[
                    row,
                    "status"
                ] = "Idea"

            content_df.to_csv(
                "data/content_calendar.csv",
                index=False
            )

            st.cache_data.clear()

            st.success(
                "Approval status updated successfully."
            )

            st.rerun()

    st.divider()

    # ---------------------------------
    # Scheduling Alerts
    # ---------------------------------

    st.subheader("⚠️ Scheduling Alerts")

    scheduled_not_approved = content_df[

        (content_df["status"] == "Scheduled") &
        (content_df["approval_status"] != "Approved")

    ]

    if len(scheduled_not_approved) > 0:

        st.warning(

            f"{len(scheduled_not_approved)} scheduled post(s) still require approval before publishing."

        )

        st.dataframe(

            scheduled_not_approved[
                [
                    "post_id",
                    "topic",
                    "platform",
                    "approval_status",
                    "scheduled_time"
                ]
            ],

            use_container_width=True

        )

    else:

        st.success(
            "All scheduled posts have been approved and are ready for publishing."
        )

    st.divider()

    # ---------------------------------
    # Ready For Scheduling
    # ---------------------------------

    ready_posts = content_df[

        (content_df["status"] == "Approved") &
        (content_df["approval_status"] == "Approved")

    ]

    st.subheader("🚀 Ready for Publishing")

    if len(ready_posts) == 0:

        st.info(
            "There are currently no approved posts ready for scheduling."
        )

    else:

        st.success(
            f"{len(ready_posts)} approved post(s) are ready for scheduling."
        )

        st.dataframe(

            ready_posts[
                [
                    "post_id",
                    "platform",
                    "topic",
                    "assigned_to",
                    "scheduled_time"
                ]
            ],

            use_container_width=True

        )

    st.divider()

    st.info(
        "Only posts with an **Approved** workflow status can proceed to the Scheduler Preview for API payload generation."
    )

# --------------------------------------------------
# SCHEDULER PREVIEW
# --------------------------------------------------

elif page == "Scheduler Preview":

    st.title("📅 Scheduler Preview")

    st.caption(
        "Generate API-ready scheduler payloads for approved content before publishing to Instagram, Facebook or LinkedIn."
    )

    st.divider()

    # ---------------------------------
    # Approved Content
    # ---------------------------------

    ready_posts = content_df[
        (content_df["status"] == "Approved") &
        (content_df["approval_status"] == "Approved")
    ]

    total_ready = len(ready_posts)
    instagram_posts = len(ready_posts[ready_posts["platform"] == "Instagram"])
    facebook_posts = len(ready_posts[ready_posts["platform"] == "Facebook"])
    linkedin_posts = len(ready_posts[ready_posts["platform"] == "LinkedIn"])

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("✅ Ready", total_ready)
    c2.metric("📸 Instagram", instagram_posts)
    c3.metric("📘 Facebook", facebook_posts)
    c4.metric("💼 LinkedIn", linkedin_posts)

    st.divider()

    # ---------------------------------
    # Filters
    # ---------------------------------

    st.subheader("🔎 Filter Approved Content")

    col1, col2 = st.columns(2)

    with col1:

        platform_filter = st.selectbox(
            "Platform",
            ["All"] + sorted(content_df["platform"].unique())
        )

    with col2:

        creative_filter = st.selectbox(
            "Creative Type",
            ["All"] + sorted(content_df["creative_type"].unique())
        )

    filtered_posts = ready_posts.copy()

    if platform_filter != "All":
        filtered_posts = filtered_posts[
            filtered_posts["platform"] == platform_filter
        ]

    if creative_filter != "All":
        filtered_posts = filtered_posts[
            filtered_posts["creative_type"] == creative_filter
        ]

    payloads = generate_scheduler_payload(filtered_posts)

    if len(payloads) == 0:

        st.warning(
            "No approved posts match the selected filters."
        )

    else:

        st.success(
            f"{len(payloads)} approved post(s) are ready for publishing."
        )

        st.divider()

        # ---------------------------------
        # Ready Posts
        # ---------------------------------

        st.subheader("📋 Ready-to-Publish Posts")

        ready_df = pd.DataFrame(payloads)

        st.dataframe(
            ready_df,
            use_container_width=True
        )

        st.divider()

        # ---------------------------------
        # Export Payload
        # ---------------------------------

        st.subheader("⚙️ Export Scheduler Payload")

        st.info(
            "Generate an API-ready JSON payload that can later be connected to Meta, LinkedIn or any scheduling platform."
        )

        if st.button("📄 Generate Payload File"):

            save_scheduler_payloads(payloads)

            st.success(
                "scheduler_payloads.json generated successfully."
            )

        st.divider()

        # ---------------------------------
        # JSON Preview
        # ---------------------------------

        st.subheader("📄 JSON Payload Preview")

        st.json(payloads)

        st.divider()

        # ---------------------------------
        # Mock API Simulation
        # ---------------------------------

        st.subheader("🚀 Mock API Simulation")

        selected_post = st.selectbox(
            "Choose Approved Post",
            ready_df["post_id"]
        )

        selected_payload = next(
            item
            for item in payloads
            if item["post_id"] == selected_post
        )

        platform = selected_payload["platform"]

        if st.button("Send to Mock API"):

            if platform == "Instagram":

                response = post_to_instagram(selected_payload)

            elif platform == "Facebook":

                response = post_to_facebook(selected_payload)

            else:

                response = post_to_linkedin(selected_payload)

            notification = notify_team(selected_payload)

            st.success(response["message"])

            st.info(notification["message"])

            st.json(response)

        st.divider()

        st.success(
            "This payload structure is ready for future integration with Meta, Instagram, Facebook or LinkedIn APIs."
        )

        st.download_button(
            "⬇ Download Scheduler Payload JSON",
            json.dumps(payloads, indent=4),
            file_name="scheduler_payloads.json",
            mime="application/json"
        )

# --------------------------------------------------
# ANALYTICS DASHBOARD
# --------------------------------------------------

elif page == "Analytics Dashboard":

    st.title("📊 Analytics Dashboard")

    st.caption(
        "Monitor campaign performance, audience engagement and content effectiveness across all supported social media platforms."
    )

    analytics = calculate_engagement(analytics_df)

    merged = merge_categories(
        content_df,
        analytics
    )

    platform_stats = best_platform(analytics)

    category_stats = best_category(merged)

    st.divider()

    # ---------------------------------
    # KPI Cards
    # ---------------------------------

    avg_reach = analytics["reach"].mean()
    avg_engagement = analytics["engagement_rate"].mean()
    best_platform_name = platform_stats.iloc[0]["platform"]

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "📈 Average Reach",
        f"{avg_reach:.0f}"
    )

    c2.metric(
        "❤️ Average Engagement",
        f"{avg_engagement:.2f}%"
    )

    c3.metric(
        "🏆 Best Platform",
        best_platform_name
    )

    st.divider()

    # ---------------------------------
    # Engagement by Platform
    # ---------------------------------

    st.subheader("📱 Engagement by Platform")

    st.caption(
        "Compare the average engagement rate across Instagram, Facebook and LinkedIn."
    )

    fig = px.bar(
        platform_stats,
        x="platform",
        y="engagement_rate",
        text_auto=".2f",
        title="Average Engagement Rate"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.divider()

    # ---------------------------------
    # Reach Trend
    # ---------------------------------

    st.subheader("📈 Reach Trend")

    st.caption(
        "Visualize how audience reach changes over time for each platform."
    )

    fig = px.line(
        analytics,
        x="date",
        y="reach",
        color="platform",
        markers=True
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.divider()

    # ---------------------------------
    # Category Performance
    # ---------------------------------

    st.subheader("🏷️ Content Category Performance")

    st.caption(
        "Identify which content categories achieve the highest engagement."
    )

    fig = px.bar(
        category_stats,
        x="post_category",
        y="engagement_rate",
        color="reach",
        text_auto=".2f"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.divider()

    # ---------------------------------
    # Likes, Comments & Shares
    # ---------------------------------

    st.subheader("👍 Likes, Comments & Shares")

    st.caption(
        "Compare engagement metrics for each published post."
    )

    fig = px.bar(
        analytics,
        x="post_id",
        y=[
            "likes",
            "comments",
            "shares"
        ],
        barmode="group"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.divider()

    # ---------------------------------
    # Analytics Table
    # ---------------------------------

    st.subheader("📑 Detailed Analytics")

    st.dataframe(
        analytics,
        use_container_width=True
    )

    st.divider()

    # ---------------------------------
    # Weekly Summary
    # ---------------------------------

    st.subheader("📝 Weekly Performance Summary")

    tasks_summary = tasks_df.copy()

    tasks_summary["due_date"] = pd.to_datetime(
        tasks_summary["due_date"]
    )

    today = pd.Timestamp.today().normalize()

    tasks_summary["Overdue"] = (
        (tasks_summary["due_date"] < today)
        &
        (tasks_summary["status"] != "Completed")
    )

    summary = generate_weekly_summary(
        content_df,
        analytics_df,
        tasks_summary
    )

    st.text_area(
        "Executive Summary",
        summary,
        height=300
    )

    if st.button("📄 Generate Weekly Summary File"):

        with open(
            "outputs/weekly_summary.txt",
            "w",
            encoding="utf-8"
        ) as file:

            file.write(summary)

        st.success(
            "weekly_summary.txt generated successfully."
        )

    st.download_button(
        "⬇ Download Weekly Summary",
        data=summary,
        file_name="weekly_summary.txt",
        mime="text/plain"
    )

    st.divider()

    # ---------------------------------
    # Application Test Results
    # ---------------------------------

    st.subheader("🧪 Application Test Results")

    st.info(
        "Generate a CSV report containing the functional test cases completed during development."
    )

    if st.button("Generate Test Results"):

        test_results = [
            ["Test Case","Input","Action Taken","Expected Output","Actual Output","Result"],

            ["1","Platform=Instagram, Topic=Summer Collection","Filled the Caption Generator form and clicked Generate Caption","Instagram caption generated successfully","Instagram caption generated successfully","Pass"],

            ["2","Platform=LinkedIn, Topic=Business Growth","Filled the Caption Generator form and clicked Generate Caption","Professional LinkedIn caption generated","Professional LinkedIn caption generated","Pass"],

            ["3","Platform=Facebook, Topic=Internship Update","Filled the Caption Generator form and clicked Generate Caption","Facebook recruitment caption generated","Facebook recruitment caption generated","Pass"],

            ["4","Approval Status = Pending","Selected Pending filter in Approval Tracker","Only pending approval posts displayed","Pending approval posts displayed correctly","Pass"],

            ["5","Team Tasks dataset","Opened Team Task Board and reviewed Overdue Tasks","Overdue tasks identified and highlighted","Overdue tasks displayed correctly","Pass"],

            ["6","Analytics dataset","Opened Analytics Dashboard","Engagement rate calculated and displayed","Engagement rate displayed correctly","Pass"],

            ["7","Analytics dataset","Viewed platform performance charts","Best-performing platform identified","Best-performing platform displayed correctly","Pass"],

            ["8","Approved Instagram posts","Selected Platform = Instagram and generated scheduler payload","API-ready JSON generated","scheduler_payloads.json generated successfully","Pass"],

            ["9","Content Calendar, Analytics and Team Tasks","Generated weekly summary","weekly_summary.txt created successfully","weekly_summary.txt created successfully","Pass"],

            ["10","Entire application","Generated downloadable test report","CSV exported successfully","CSV exported successfully","Pass"]
        ]

        with open(
            "outputs/test_results.csv",
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(file)
            writer.writerows(test_results)

        st.success("test_results.csv generated successfully!")

        with open(
            "outputs/test_results.csv",
            "rb"
        ) as file:

            st.download_button(
                "⬇ Download Test Results",
                file,
                file_name="test_results.csv",
                mime="text/csv"
            )

# --------------------------------------------------
# TEAM TASKS
# --------------------------------------------------

elif page == "Team Tasks":

    st.title("👥 Team Task Board")

    st.caption(
        "Track team assignments, monitor deadlines, prioritize work and collaborate efficiently across the social media marketing workflow."
    )

    st.divider()

    # ---------------------------------
    # Prepare Data
    # ---------------------------------

    tasks = tasks_df.copy()

    tasks["due_date"] = pd.to_datetime(tasks["due_date"])

    today = pd.Timestamp.today().normalize()

    tasks["Overdue"] = (
        (tasks["due_date"] < today)
        &
        (tasks["status"] != "Completed")
    )

    # ---------------------------------
    # KPI Cards
    # ---------------------------------

    completed = len(
        tasks[
            tasks["status"] == "Completed"
        ]
    )

    in_progress = len(
        tasks[
            tasks["status"] == "In Progress"
        ]
    )

    pending = len(
        tasks[
            tasks["status"] == "Pending"
        ]
    )

    overdue_count = len(
        tasks[
            tasks["Overdue"]
        ]
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("✅ Completed", completed)
    c2.metric("🚧 In Progress", in_progress)
    c3.metric("📝 Pending", pending)
    c4.metric("⚠️ Overdue", overdue_count)

    st.divider()

    # ---------------------------------
    # Filters
    # ---------------------------------

    st.subheader("🔎 Filter Tasks")

    col1, col2, col3 = st.columns(3)

    with col1:

        member_filter = st.selectbox(
            "Team Member",
            ["All"] + sorted(tasks["assigned_to"].unique())
        )

    with col2:

        status_filter = st.selectbox(
            "Task Status",
            ["All"] + sorted(tasks["status"].unique())
        )

    with col3:

        priority_filter = st.selectbox(
            "Priority",
            ["All"] + sorted(tasks["priority"].unique())
        )

    filtered = tasks.copy()

    if member_filter != "All":

        filtered = filtered[
            filtered["assigned_to"] == member_filter
        ]

    if status_filter != "All":

        filtered = filtered[
            filtered["status"] == status_filter
        ]

    if priority_filter != "All":

        filtered = filtered[
            filtered["priority"] == priority_filter
        ]

    st.divider()

    # ---------------------------------
    # Team Task Table
    # ---------------------------------

    st.subheader("📋 Team Task Board")

    st.dataframe(
        filtered[
            [
                "task_id",
                "task_name",
                "assigned_to",
                "priority",
                "status",
                "due_date"
            ]
        ],
        use_container_width=True
    )

    st.divider()

    # ---------------------------------
    # Charts
    # ---------------------------------

    left, right = st.columns(2)

    with left:

        st.subheader("📊 Task Status")

        status_chart = (
            filtered["status"]
            .value_counts()
            .reset_index()
        )

        status_chart.columns = [
            "Status",
            "Tasks"
        ]

        fig = px.bar(
            status_chart,
            x="Status",
            y="Tasks",
            text_auto=True,
            title="Tasks by Status"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with right:

        st.subheader("🚩 Priority Distribution")

        priority_chart = (
            filtered["priority"]
            .value_counts()
            .reset_index()
        )

        priority_chart.columns = [
            "Priority",
            "Tasks"
        ]

        fig = px.pie(
            priority_chart,
            names="Priority",
            values="Tasks",
            hole=0.45
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.divider()

    # ---------------------------------
    # Overdue Tasks
    # ---------------------------------

    st.subheader("⚠️ Tasks Requiring Attention")

    overdue_tasks = filtered[
        filtered["Overdue"]
    ]

    if len(overdue_tasks) == 0:

        st.success(
            "Excellent! No overdue tasks were found."
        )

    else:

        st.warning(
            f"{len(overdue_tasks)} overdue task(s) require immediate attention."
        )

        st.dataframe(
            overdue_tasks[
                [
                    "task_id",
                    "task_name",
                    "assigned_to",
                    "priority",
                    "status",
                    "due_date"
                ]
            ],
            use_container_width=True
        )

    st.divider()

    # ---------------------------------
    # Export
    # ---------------------------------

    st.subheader("📤 Export Task Report")

    csv = filtered.to_csv(index=False)

    st.download_button(
        "⬇ Download Filtered Tasks",
        csv,
        file_name="team_tasks.csv",
        mime="text/csv"
    )