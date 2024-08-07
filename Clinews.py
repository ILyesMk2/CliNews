import requests
import json
import argparse
import os

BASE_URL = 'https://hacker-news.firebaseio.com/v0/'
HEADERS = {'User-Agent': 'CliNews/1.0'}

def fetch_data(endpoint):
    url = f"{BASE_URL}{endpoint}.json?print=pretty"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()

def fetch_story(story_id):
    story = fetch_data(f'item/{story_id}')
    return story

def fetch_user(username):
    user = fetch_data(f'user/{username}')
    return user

def fetch_stories(type):
    story_ids = fetch_data(f'{type}stories')
    return [fetch_story(story_id) for story_id in story_ids[:5]]

def print_story(story):
    print(f"Title: {story.get('title')}")
    print(f"URL: {story.get('url')}")
    print(f"Score: {story.get('score')}")
    print(f"By: {story.get('by')}")
    print(f"Comments: {story.get('descendants')}")
    print("-" * 40)

def fetch_comments(story_id):
    story = fetch_story(story_id)
    if 'kids' in story:
        for comment_id in story['kids'][:5]:
            comment = fetch_story(comment_id)
            print(f"Comment by {comment.get('by')}:")
            print(comment.get('text'))
            print("-" * 40)

def fetch_user_activity(username):
    user = fetch_user(username)
    if user:
        print(f"User: {user.get('id')}")
        print(f"Submitted Stories: {len(user.get('submitted', []))}")
        print("-" * 40)
        for item_id in user.get('submitted', [])[:5]:
            story = fetch_story(item_id)
            print_story(story)
    else:
        print("User not found.")

def save_story(story_id):
    saved_stories_file = 'saved_stories.json'
    if os.path.exists(saved_stories_file):
        with open(saved_stories_file, 'r') as f:
            saved_stories = json.load(f)
    else:
        saved_stories = []

    if story_id not in saved_stories:
        saved_stories.append(story_id)
        with open(saved_stories_file, 'w') as f:
            json.dump(saved_stories, f)
        print(f"Story {story_id} saved.")
    else:
        print(f"Story {story_id} is already saved.")

def list_saved_stories():
    saved_stories_file = 'saved_stories.json'
    if os.path.exists(saved_stories_file):
        with open(saved_stories_file, 'r') as f:
            saved_stories = json.load(f)
        for story_id in saved_stories:
            story = fetch_story(story_id)
            print_story(story)
    else:
        print("No saved stories found.")

def delete_saved_story(story_id):
    saved_stories_file = 'saved_stories.json'
    if os.path.exists(saved_stories_file):
        with open(saved_stories_file, 'r') as f:
            saved_stories = json.load(f)
        if story_id in saved_stories:
            saved_stories.remove(story_id)
            with open(saved_stories_file, 'w') as f:
                json.dump(saved_stories, f)
            print(f"Story {story_id} deleted.")
        else:
            print(f"Story {story_id} not found in saved stories.")
    else:
        print("No saved stories found.")

def main():
    parser = argparse.ArgumentParser(description='CLI News Aggregator for Hacker News.')
    parser.add_argument('command', choices=['latest', 'top', 'new', 'best', 'ask', 'show', 'jobs', 'details', 'user', 'comments', 'user-comments', 'user-submissions', 'user-activity', 'save', 'saved', 'delete', 'subscribe', 'unsubscribe', 'help'], help='Command to execute.')
    parser.add_argument('arg', nargs='?', help='Argument for the command.')

    args = parser.parse_args()

    if args.command == 'latest':
        stories = fetch_stories('top')
        for story in stories:
            print_story(story)
    elif args.command == 'top':
        stories = fetch_stories('top')
        for story in stories:
            print_story(story)
    elif args.command == 'new':
        stories = fetch_stories('new')
        for story in stories:
            print_story(story)
    elif args.command == 'best':
        stories = fetch_stories('best')
        for story in stories:
            print_story(story)
    elif args.command == 'ask':
        stories = fetch_stories('ask')
        for story in stories:
            print_story(story)
    elif args.command == 'show':
        stories = fetch_stories('show')
        for story in stories:
            print_story(story)
    elif args.command == 'jobs':
        stories = fetch_stories('job')
        for story in stories:
            print_story(story)
    elif args.command == 'details':
        if args.arg:
            story = fetch_story(args.arg)
            print_story(story)
        else:
            print("Story ID is required.")
    elif args.command == 'user':
        if args.arg:
            user = fetch_user(args.arg)
            if user:
                print(f"User: {user.get('id')}")
                print(f"Created: {user.get('created')}")
                print(f"Karma: {user.get('karma')}")
                print("-" * 40)
            else:
                print("User not found.")
        else:
            print("Username is required.")
    elif args.command == 'comments':
        if args.arg:
            fetch_comments(args.arg)
        else:
            print("Story ID is required.")
    elif args.command == 'user-comments':
        if args.arg:
            user = fetch_user(args.arg)
            if user:
                for item_id in user.get('submitted', [])[:5]:
                    story = fetch_story(item_id)
                    if 'kids' in story:
                        for comment_id in story['kids'][:5]:
                            comment = fetch_story(comment_id)
                            print(f"Comment by {comment.get('by')}:")
                            print(comment.get('text'))
                            print("-" * 40)
            else:
                print("User not found.")
        else:
            print("Username is required.")
    elif args.command == 'user-submissions':
        if args.arg:
            fetch_user_activity(args.arg)
        else:
            print("Username is required.")
    elif args.command == 'user-activity':
        if args.arg:
            fetch_user_activity(args.arg)
        else:
            print("Username is required.")
    elif args.command == 'save':
        if args.arg:
            save_story(args.arg)
        else:
            print("Story ID is required.")
    elif args.command == 'saved':
        list_saved_stories()
    elif args.command == 'delete':
        if args.arg:
            delete_saved_story(args.arg)
        else:
            print("Story ID is required.")
    elif args.command == 'subscribe':
        if args.arg:
            print(f"Subscribed to stories related to: {args.arg}")
        else:
            print("Topic is required.")
    elif args.command == 'unsubscribe':
        if args.arg:
            print(f"Unsubscribed from stories related to: {args.arg}")
        else:
            print("Topic is required.")
    elif args.command == 'help':
        parser.print_help()

if __name__ == '__main__':
    main()
