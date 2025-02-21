from datetime import datetime

import aiofiles


async def save_log_file(file_name, content, title: str = "") -> None:
    async with aiofiles.open(file_name, "a") as file:
        start_msg = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {title}\n\n"
        traceback_msg = content
        end_msg = f"{'=' * 50}\n\n"
        await file.writelines(start_msg + traceback_msg + end_msg)
