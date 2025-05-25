import os
from langchain.agents import initialize_agent, Tool
from langchain.llms import OpenAI

from rekognition_tool import detect_labels
from s3_tool import list_photos, move_photo

def main():
    # 1) Ask for your bucket once
    bucket = input("Enter your S3 bucket name: ").strip().strip('"\'')
    
    # 2) Wrap the tools so they only need "key" (or "key,folder")
    def list_photos_tool(_):
        # ignore input, just list your bucket
        return list_photos(bucket)
    
    def detect_labels_tool(key: str):
        key = key.strip().strip('"\'')
        return detect_labels(bucket, key)
    
    def move_photo_tool(arg: str):
        # expect: "key,folder"
        parts = [p.strip().strip('"\'') for p in arg.split(",")]
        if len(parts) != 2:
            raise ValueError("move_photo expects exactly two parts: key,folder")
        key, folder = parts
        return move_photo(bucket, key, folder)
    
    tools = [
        Tool(
            name="list_photos",
            func=list_photos_tool,
            description="List all image keys in the given S3 bucket."
        ),
        Tool(
            name="detect_labels",
            func=detect_labels_tool,
            description="Given an image key (string), return the list of labels via Rekognition."
        ),
        Tool(
            name="move_photo",
            func=move_photo_tool,
            description="Given 'key,folder', move that image into the specified folder in the bucket."
        ),
    ]
    
    # 3) Initialize zero-shot agent
    llm = OpenAI(temperature=0)
    agent = initialize_agent(
        tools,
        llm,
        agent="zero-shot-react-description",
        verbose=True
    )
    
    # 4) Single prompt; agent will call each tool in turn
    prompt = (
        "List all photos, then for each photo key, "
        "call detect_labels <key>, "
        "then call move_photo <key>,<folder> where folder is the top label."
    )
    agent.run(prompt)

if __name__ == "__main__":
    main()
