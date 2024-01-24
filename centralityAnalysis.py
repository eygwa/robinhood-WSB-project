import json
from collections import defaultdict

# Read the JSON file
with open("d:/CIS400/final/wallstreetbets_GME_posts_2022.json") as json_file:
    posts_data = json.load(json_file)
    posts = posts_data.values()

# Create a dictionary to store the authors and their comment scores
author_comment_scores = defaultdict(int)

# Calculate the comment scores for each author
for post in posts:
    author = post["author"]
    num_comments = post.get("num_comments", 0)
    author_comment_scores[author] += num_comments

# Remove the [deleted] entry from the author_comment_scores dictionary
if "[deleted]" in author_comment_scores:
    del author_comment_scores["[deleted]"]

# Sort the authors by their comment scores
sorted_authors = sorted(author_comment_scores.items(), key=lambda x: x[1], reverse=True)

# Print the top 10 authors and their comment scores
print("Top 10 authors by total comments on their posts:")
for i, (author, score) in enumerate(sorted_authors[:10]):
    print(f"{i + 1}. {author}: {score}")

