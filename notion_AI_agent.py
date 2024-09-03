import requests
from datetime import datetime

from dotenv import load_dotenv
from llama_index.core.llms import ChatMessage
from llama_index.llms.openai import OpenAI

import json

from datetime import datetime
from dotenv import load_dotenv



def query(textFromUser: str, size: int):
    load_dotenv()
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

    messages = [
        ChatMessage(
            role="system",
            content=(
                "You are a productivity bot whose sole goal is to read text, optimize it, and provide detailed information "
                "depending on whether it is for studying or for deploying new ideas or projects. You must choose from and "
                "produce the following types of content as needed, based on the input: "
                "'to-do list', 'paragraph', 'planner', 'bookmark', 'bulleted list item', 'callout', 'code', 'heading', "
                "'numbered list item', 'quote'. Each item should be separated by a blank line. "
                "When providing a 'paragraph', include only factual information directly related to the core topic. "
                "For 'to-do list' and 'numbered list item' blocks, provide specific dates and times when possible. "
                "Break down tasks by month, and/or day, and/or hour as needed. For 'bookmark' and 'callout' blocks, provide "
                "helpful details and suggestions to balance being concise, detailed, and precise. "
                "Include headings with different levels and ensure proper formatting for code blocks. "
                f"The datetime is: {dt_string}. Do not use any special strings such as ####. "
                "Simply state the type, followed by a colon, "
                "then provide info. Example is 'paragraph: \nInsert content here'. Additionally, "
                "you can indicate what goes on which page, "
                "by splitting pages using this: \\n\\n\\n. For anything that has a list, please do not use ** "
                "to bolden the numbers, and do not use numbering such as 1., 2., etc. to indicate lists, "
                f"simply use \\n to split to the next line. Create as many pages as needed, you have only {size} pages available. Use all of them as much as possible. You must provide content for more than one page as long as you more than one page available. "
            )
        ),
        ChatMessage(role="user", content=textFromUser),
    ]

    resp = str(OpenAI("gpt-4o").chat(messages))
    resp = resp.replace("assistant: ", "", 1)

    # Convert the response to a dictionary
    return {"response": resp}


import requests
import json


def SendToNotion(textFromOpenAI: str, notionAPIkey: str, parentPageIds: list):
    # Split the text into pages based on triple newline
    print (textFromOpenAI)

    pages = textFromOpenAI.split("\n\n\n")

    print (pages)
    for i, page in enumerate(pages):
        blocks = []
        splitText = page.split("\n\n")

        for block in splitText:
            block = block.strip()

            if block.lower().startswith("heading"):
                heading_text = block.replace("heading: ", "").strip()
                blocks.append({
                    "object": "block",
                    "type": "heading_2",  # Adjust as needed based on heading level
                    "heading_2": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {
                                    "content": heading_text
                                }
                            }
                        ]
                    }
                })

            elif block.lower().startswith("paragraph"):
                paragraph_text = block.replace("paragraph: ", "").strip()
                blocks.append({
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {
                                    "content": paragraph_text
                                }
                            }
                        ]
                    }
                })

            elif block.lower().startswith("numbered list item"):
                list_items = block.replace("numbered list item: ", "").strip().split("\n")
                for item in list_items:
                    blocks.append({
                        "object": "block",
                        "type": "numbered_list_item",
                        "numbered_list_item": {
                            "rich_text": [
                                {
                                    "type": "text",
                                    "text": {
                                        "content": item.strip()
                                    }
                                }
                            ]
                        }
                    })

            elif block.lower().startswith("bulleted list item"):
                bulleted_items = block.replace("bulleted list item: ", "").strip().split("\n")
                for item in bulleted_items:
                    blocks.append({
                        "object": "block",
                        "type": "bulleted_list_item",
                        "bulleted_list_item": {
                            "rich_text": [
                                {
                                    "type": "text",
                                    "text": {
                                        "content": item.strip()
                                    }
                                }
                            ]
                        }
                    })

            elif block.lower().startswith("bookmark"):
                bookmark_url = block.replace("bookmark: ", "").strip()
                bookmark_url_text =  block.split(": ", 1)
                blocks.append({
                    "object": "block",
                    "type": "bookmark",
                    "bookmark": {
                        "url": bookmark_url_text[1]
                    }
                })

            elif block.lower().startswith("callout"):
                callout_text = block.replace("callout: ", "").strip()
                callout_text = callout_text.replace("description: ", "", 1)
                blocks.append({
                    "object": "block",
                    "type": "callout",
                    "callout": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {
                                    "content": callout_text
                                }
                            }
                        ],
                        "icon": {
                            "emoji": "💡"  # You can change the emoji as needed
                        }
                    }
                })

        final_json = {
            "children": blocks
        }

        # Convert the dictionary to a JSON string
        final_json_str = json.dumps(final_json)

        # API endpoint for adding children to the parent page
        url = f"https://api.notion.com/v1/blocks/{parentPageIds[i]}/children"
        headers = {
            "Authorization": f"Bearer {notionAPIkey}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }

        # Send the request
        response = requests.patch(url, headers=headers, data=final_json_str)

        if response.status_code != 200:
            print(f"Failed to add block: {response.status_code}")
            print(response.json())
        else:
            print (response)