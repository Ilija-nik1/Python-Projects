import pygetwindow as gw
import time
import logging

# Configurable delay and settings
DELAY = 1
DARK_THEME = "Dark"
SCREEN_RESOLUTION = "125%"
FONT_SIZE = "16"

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def activate_window(window_title):
    try:
        window = gw.getWindowsWithTitle(window_title)[0]
        if window.isMinimized:
            window.restore()
        window.activate()
        time.sleep(DELAY)
        return window
    except IndexError:
        logging.error(f"Window with title '{window_title}' not found.")
        return None

def change_theme(theme):
    logging.info("Changing theme...")
    settings_window = activate_window("Settings")
    if settings_window:
        settings_window.type('themes')
        time.sleep(DELAY)

        themes_window = activate_window("Themes and related settings")
        if themes_window:
            dark_theme_button = themes_window.child_window(title=theme, control_type="Button")
            dark_theme_button.click()
            time.sleep(DELAY)

        settings_window.close()

def change_screen_resolution(resolution):
    logging.info("Changing screen resolution...")
    settings_window = activate_window("Settings")
    if settings_window:
        system_tab = settings_window.child_window(title="System", control_type="TabItem")
        system_tab.click_input()
        time.sleep(DELAY)

        scale_layout_dropdown = settings_window.child_window(title="Scale and layout", control_type="ComboBox")
        scale_layout_dropdown.click_input()
        time.sleep(DELAY)

        dropdown_item = settings_window.child_window(title=resolution, control_type="ListItem")
        dropdown_item.click_input()

        settings_window.close()

def change_text_size_in_terminal(terminal_name, font_size):
    logging.info(f"Changing text size in {terminal_name}...")
    terminal_window = activate_window(terminal_name)
    if terminal_window:
        terminal_window.right_click_input(coords=(100, 10))
        time.sleep(DELAY)

        properties_menu_item = terminal_window.child_window(title="Properties", control_type="MenuItem")
        properties_menu_item.click_input()
        time.sleep(DELAY)

        font_tab = activate_window("Properties")
        if font_tab:
            font_size_button = font_tab.child_window(title="Font size:", control_type="Button")
            font_size_button.click_input()
            time.sleep(DELAY)

            # Enter the desired font size if necessary

        properties_window = activate_window("Properties")
        if properties_window:
            properties_window.press('enter')

        terminal_window.close()

if __name__ == "__main__":
    change_theme(DARK_THEME)
    change_screen_resolution(SCREEN_RESOLUTION)
    change_text_size_in_terminal("Windows PowerShell", FONT_SIZE)
    change_text_size_in_terminal("Command Prompt", FONT_SIZE)