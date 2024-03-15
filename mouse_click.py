import pyautogui
import time
import datetime
from typing import Tuple
from colorama import init as colorama_init
from colorama import Fore
from colorama import Style


def is_time_in_range(start: datetime.time, end: datetime.time, current_time: datetime.time) -> bool:
    """Check if the current time is within the specified range."""
    return start <= current_time <= end


def is_click_time_enabled(start_time: datetime.time, end_time: datetime.time) -> bool:
    """Determine if the current time is within the allowed click time range, based on provided start and end times."""
    now = datetime.datetime.now().time()
    return is_time_in_range(start_time, end_time, now)


def get_time_from_user(prompt: str, default_time: datetime.time = None) -> datetime.time:
    """Prompt the user for a time in HH:MM format or use the default time if 'd' is entered."""
    while True:
        user_input = input(prompt).strip()
        if user_input.lower() == 'd' and default_time:
            return default_time
        try:
            hours, minutes = map(int, user_input.split(':'))
            return datetime.time(hours, minutes)
        except ValueError:
            print("Invalid format. Please enter the time in HH:MM format or press 'd' for default.")


def get_validated_time_range(prompt_start: str, prompt_end: str, default_start_time: datetime.time,
                             default_end_time: datetime.time) -> Tuple[datetime.time, datetime.time]:
    """Prompt the user for start and end times, ensuring the end time is after the start time, or use default times."""
    while True:
        start_time = get_time_from_user(prompt_start, default_start_time)
        end_time = get_time_from_user(prompt_end, default_end_time)

        if start_time < end_time:
            return start_time, end_time
        else:
            print("The end time must be later than the start time. "
                  "Please enter the times again or press 'd' for default.")


def get_delay_time(prompt: str, default_delay: int = 180) -> int:
    """Prompt the user for a delay time in seconds."""
    while True:
        user_input = input(prompt).strip()
        if user_input.lower() == 'd':
            return default_delay
        try:
            delay = int(user_input)
            if delay > 0:
                return delay
            else:
                print("Please enter a positive integer.")
        except ValueError:
            print("Invalid input. Please enter an integer or press 'd' for default.")


def mouse_left_click():
    colorama_init()

    # Define default start and end times
    default_start_time = datetime.time(9, 0)
    default_end_time = datetime.time(18, 0)
    default_delay_time = 180  # unit is seconds

    # Get start and end times from the user or use defaults
    work_start, work_end = get_validated_time_range(
        ("Enter the start time (HH:MM)(24-hour clock) or 'd' for default (%s): " % default_start_time.strftime("%H:%M")),
        ("Enter the end time (HH:MM)(24-hour clock) or 'd' for default (%s): " % default_end_time.strftime("%H:%M")),
        default_start_time, default_end_time)

    # Get delay time from the user or use default
    delay_time = get_delay_time(("Enter the delay time in seconds (or 'd' for %s minutes default): "
                                 % str(default_delay_time/60)), default_delay_time)

    while input('Move the mouse to the desired position, '
                'press \'p\' and then press \'enter\' to capture the position:') != 'p':
        pass  # Wait for the user to press 'p'

    target_x, target_y = pyautogui.position()
    print(f"Mouse position set to: {target_x}, {target_y}")

    try:
        while True:
            if is_click_time_enabled(work_start, work_end):
                # Record the mouse cursor to the original position
                current_x, current_y = pyautogui.position()
                # Click the mouse at the desired position
                pyautogui.click(target_x, target_y, button='left')
                # Move the mouse cursor to the original position
                pyautogui.moveTo(current_x , current_y)
                print(f'Mouse left clicked at: {target_x}, {target_y}')
            else:
                print("Outside allowed click time. Skipping click.")
            time.sleep(delay_time)
            print("Current time:", time.ctime())
    except KeyError:
        pass
    except Exception as e:
        print(f"{Fore.RED}An error occurred:{Style.RESET_ALL} {e}")