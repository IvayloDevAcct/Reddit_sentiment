from reddit.analyser import TextAnalyser
import praw
import os, time, datetime
import pandas as pd

from dashboard.gsheet import *

import json

# Path to my creds file. IT WON'T work on another machine. Please set the path to your Reddit credentials.
with open("C:\\Users\\ivayl\\Documents\\Nexo Work\\creds.json", "r", encoding="utf8") as f:
    creds = json.load(f)

# Set a Subreddit and keywords for the search (could be done via frontend/web interface)
SUBREDDIT = "cryptocurrency"
assets_for_analysis = [("btc", "bitcoin"), ("eth", "ether"), ("ada", "cardano")]
TODAY = datetime.datetime.utcnow().date()


def main():

    # Initiate reddit reader object using the PRAW module
    reader = praw.Reddit(
        client_id=creds['user_id'],
        client_secret=creds['secret'],
        username="ivailo_opalchenski",
        password=creds['pass'],
        user_agent="ivailo_opalchenski"
    )

    # Set the search parameters
    topic = reader.subreddit(SUBREDDIT)
    new_posts = topic.new(limit=1000)

    # Create a data frame to store new results
    new_data = pd.DataFrame()

    # Create a list to results for posts we already have but might have gotten new comments
    existing_data = []

    # Create a google sheet object
    sheet = GoogleSheet(service_file_path, workbook_id, sheet_name)

    # Get the IDs of all posts in the "database" (currently using google sheet for this purpose, ideally SLQ)
    existing_post_ids = sheet.get_existing_post_ids()

    # Create a parser object
    parser = TextAnalyser("english")

    for post in new_posts:

        # Assign not analysed status for the post until it's recognized as relevant for one of the assets in the list
        analysed = False

        # Loop through the list of targets and look for mention within the posts/comments.
        for asset in assets_for_analysis:

            # Get day and hour of the post
            time_of_creation = post.created_utc
            day_of_creation = datetime.datetime.utcfromtimestamp(time_of_creation).date()
            hour_of_creation = datetime.datetime.utcfromtimestamp(time_of_creation).hour

            # Filter for relevant, non-stickied posts:
            if day_of_creation == TODAY and not post.stickied:

                processed_title = parser.process_text(post.title)
                processed_body = parser.process_text(post.selftext)

                if (asset[0] in processed_title or asset[1] in processed_title) \
                        or (asset[0] in processed_body or asset[1] in processed_body):

                    # Create a variable to store the vader scores all comments
                    vader_score = []

                    # Score the post entire text using Vader
                    vader_post_score = parser.score_post_vader(post.selftext)
                    vader_score.append(vader_post_score)

                    # Get all comments
                    comments = post.comments.list()

                    processed_comments = []
                    for comment in comments:
                        try:
                            if comment.author != "AutoModerator":
                                # Score the comments using Vader
                                vader_comment_score = parser.score_post_vader(comment.body)
                                vader_score.append(vader_comment_score)

                                # Clean up and break down the text and add to the pool of words for the post
                                processed_comment = parser.process_text(comment.body)
                                processed_comments.extend(processed_comment)

                        except AttributeError:
                            pass

                    # Score the post using proprietary keywords
                    content_score = parser.score_post(processed_body + processed_comments)

                    # Calculate the average of the vader sores of all comments
                    vader_content_score = sum(vader_score) / len(vader_score)

                    if content_score:

                        if not analysed and content_score["words_count"] > 100:

                            # Create a post data row for the DB
                            post_info = {
                                "id": post.id,
                                "day_created": day_of_creation,
                                "hour_created": hour_of_creation,
                                "relevant asset": asset[0].upper(),
                                "up_votes": post.ups,
                                "number_of_comments": len(comments),
                                "title": post.title,
                                'positive_points': content_score['positive'],
                                "negative points": content_score['negative'],
                                "total_relevant_words": content_score["words_count"],
                                "vader_score": vader_content_score,
                                "prop_score": content_score['overall']
                            }

                            # Calculate an average of the two scores
                            post_info["score"] = (post_info['vader_score'] + post_info['prop_score']) / 2

                            if post.id not in existing_post_ids:

                                # Add row to the Data frame
                                new_data = new_data.append(post_info, ignore_index=True)

                            else:
                                existing_data.append(post_info)

                            # Assign analysed status in order to avoid adding the same post again for another asset
                            analysed = True

    if not new_data.empty:

        # Store the results locally (ideally in a Database)
        new_data.to_csv(os.path.dirname(os.getcwd()) +
                    f'\\Reddit_sentiment\\files\\posts_{datetime.datetime.now().strftime("%d_%m_%y_%H_%M")}.csv')

        # Write to google sheet for the purposes of the dashboard
        sheet.add_data(new_data)

    else:
        print("No new data matching the query.")

    if existing_data:
        # Update the existing entries for the latest posts
        sheet.update_data(existing_data)

    else:
        print("No existing records for update.")

    time.sleep(60 * 60 * 24)
    main()


if __name__ == '__main__':
    main()
