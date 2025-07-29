# Library
from datetime import datetime

# Utils
from utils.constant import (
    STATUS_COMPLETE,
    STATUS_FAILED,
    STATUS_PENDING,
    STATUS_PROCESS,
    REPORT_LINE_WIDTH,
)
from utils.function import FuncDBLogRepo as LogRepo
from utils.function import FuncDBLogContributor as LogContributor
from utils.models import TGitHubContributorJoinLog, TGitHubRepoLog


def github_report(start: datetime, completed: bool = False) -> str:

    return github_report_repo(start, completed) + github_report_contributor(
        start, completed
    )


def github_report_repo(start: datetime, completed: bool = False) -> str:

    start_time = start
    current_time = datetime.now()
    total_duration = current_time - start_time

    pending = LogRepo.load([STATUS_PENDING])
    process = LogRepo.load([STATUS_PROCESS])
    complete = LogRepo.load([STATUS_COMPLETE])
    failed = LogRepo.load([STATUS_FAILED])

    records: list[TGitHubRepoLog] = []
    records.extend(pending)
    records.extend(process)
    records.extend(complete)
    records.extend(failed)

    total_records = len(records)
    completed_count = len(complete)
    failed_count = len(failed)
    pending_count = len(pending)
    processing_count = len(process)

    # Calculate percentage completed
    percentage_completed = (
        (completed_count / total_records * 100) if total_records > 0 else 0
    )

    # Calculate estimated time remaining
    elapsed_seconds = total_duration.total_seconds()
    if completed_count > 0 and elapsed_seconds > 0:
        records_per_second = completed_count / elapsed_seconds
        remaining_records = total_records - completed_count
        estimated_seconds_remaining = (
            remaining_records / records_per_second if records_per_second > 0 else 0
        )
        # Format to HH:MM:SS
        estimated_remaining = str(
            datetime.fromtimestamp(estimated_seconds_remaining).strftime("%H:%M:%S")
        )
    else:
        estimated_remaining = "N/A"

    # Generate report as single string
    report_lines = []
    report_lines.append("\n" + "=" * REPORT_LINE_WIDTH)
    report_lines.append("🚀 GitHub Scraping Repositories Report".center(20))
    report_lines.append("=" * REPORT_LINE_WIDTH)
    report_lines.append(
        f"⏱️  Report generated at: {current_time.strftime('%Y-%m-%d %I.%M %p')}"
    )
    report_lines.append(f"⏱️  Total duration: {str(total_duration).split('.')[0]}")
    report_lines.append("-" * REPORT_LINE_WIDTH)
    report_lines.append(f"📊 Total records: {total_records}")
    report_lines.append(
        f"✅ Completed: {completed_count} ({percentage_completed:.2f}%)"
    )
    report_lines.append(f"❌ Failed: {failed_count}")
    report_lines.append(f"🔄 Processing: {processing_count}")
    report_lines.append(f"⏳ Pending: {pending_count}")
    if not completed:
        report_lines.append("-" * REPORT_LINE_WIDTH)
        report_lines.append(f"⏱️  Estimated time remaining: {estimated_remaining}")
    report_lines.append("=" * REPORT_LINE_WIDTH + "\n")

    report_text = "\n".join(report_lines)

    # Print to console
    print(report_text)

    # Return the text for email or other uses
    return report_text


def github_report_contributor(start: datetime, completed: bool = False) -> str:

    start_time = start
    current_time = datetime.now()
    total_duration = current_time - start_time

    pending = LogContributor.load(status=[STATUS_PENDING])
    process = LogContributor.load(status=[STATUS_PROCESS])
    complete = LogContributor.load(status=[STATUS_COMPLETE])
    failed = LogContributor.load(status=[STATUS_FAILED])

    records: list[TGitHubContributorJoinLog] = []
    records.extend(pending)
    records.extend(process)
    records.extend(complete)
    records.extend(failed)

    total_records = len(records)
    completed_count = len(complete)
    failed_count = len(failed)
    pending_count = len(pending)
    processing_count = len(process)

    # Calculate percentage completed
    percentage_completed = (
        (completed_count / total_records * 100) if total_records > 0 else 0
    )

    # Calculate estimated time remaining
    elapsed_seconds = total_duration.total_seconds()
    if completed_count > 0 and elapsed_seconds > 0:
        records_per_second = completed_count / elapsed_seconds
        remaining_records = total_records - completed_count
        estimated_seconds_remaining = (
            remaining_records / records_per_second if records_per_second > 0 else 0
        )
        # Format to HH:MM:SS
        estimated_remaining = str(
            datetime.fromtimestamp(estimated_seconds_remaining).strftime("%H:%M:%S")
        )
    else:
        estimated_remaining = "N/A"

    # Generate report as single string
    report_lines = []
    report_lines.append("\n" + "=" * REPORT_LINE_WIDTH)
    report_lines.append("👷 GitHub Scraping Contributor Report".center(20))
    report_lines.append("=" * REPORT_LINE_WIDTH)
    report_lines.append(
        f"⏱️  Report generated at: {current_time.strftime('%Y-%m-%d %I.%M %p')}"
    )
    report_lines.append(f"⏱️  Total duration: {str(total_duration).split('.')[0]}")
    report_lines.append("-" * REPORT_LINE_WIDTH)
    report_lines.append(f"📊 Total records: {total_records}")
    report_lines.append(
        f"✅ Completed: {completed_count} ({percentage_completed:.2f}%)"
    )
    report_lines.append(f"❌ Failed: {failed_count}")
    report_lines.append(f"🔄 Processing: {processing_count}")
    report_lines.append(f"⏳ Pending: {pending_count}")
    if not completed:
        report_lines.append("-" * REPORT_LINE_WIDTH)
        report_lines.append(f"⏱️  Estimated time remaining: {estimated_remaining}")
    report_lines.append("=" * REPORT_LINE_WIDTH + "\n")

    report_text = "\n".join(report_lines)

    # Print to console
    print(report_text)

    # Return the text for email or other uses
    return report_text
