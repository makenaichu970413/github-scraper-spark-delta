# Utils
from utils.constant import DB_NAME_REPO, STATUS_PENDING
from utils.function import FuncDBLogRepo as Log
from utils.function.FuncFile import extract_urls_from_excel


dummy = [
    "https://github.com/openclimatefix",
    "https://github.com/huggingface/transformers",
    "https://github.com/stanford-crfm",
    "https://github.com/gizatechxyz",
    "https://github.com/tensorflow/tensorflow",
]


def read_input() -> list[str]:

    # Example usage
    URLs = extract_urls_from_excel("github_urls.xlsx")

    totalURLs = len(URLs)
    if not totalURLs:
        print("⚠️ No URLs found in Excel file")
        return []

    isInit = Log.init_table()

    if not isInit:
        return

    count = Log.insert_batch(URLs, STATUS_PENDING)
    if count != totalURLs:
        print(
            f'⚠️ Only inserted "{count}" from "{totalURLs}" xlsx records into "{DB_NAME_REPO}"'
        )

    inputs = Log.load([STATUS_PENDING])

    total = len(inputs)
    if not total:
        print("⚠️ No pending records found")
        return []

    print(f'\nIn "{DB_NAME_REPO}" found total "{total}" record')
    for i, item in enumerate(inputs, start=1):
        print(f"{i}. {item}")

    result = [item.url for item in inputs if item.url]

    # return dummy

    return result
