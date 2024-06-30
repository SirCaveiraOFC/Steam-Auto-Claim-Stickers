#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Name: Steam Auto Claim Stickers
Description: Script to automatically claim Steam Stickers (running in the background).
Coded BY: Sr.Caveira
GitHub: https://github.com/SirCaveiraOFC/
Steam: https://steamcommunity.com/id/srcaveira/
"""

import os
import sys
import ctypes
import time
import requests
from win10toast import ToastNotifier

toast_running_in_background_fired = False
program_version = "1.0.0"

# Main function to claim Steam Stickers.
def main():
	global toast_running_in_background_fired

	if toast_running_in_background_fired is False:
		toast(f"Steam Auto Claim Stickers (v{program_version}) is running in background", 3)

		toast_running_in_background_fired = True

	while True:
		try:
			webapi_token = getWebAPIToken() # Try to get the API token

			# toast(f"Token successfully obtained: {webapi_token}", 3)

			if checkWebAPIToken(webapi_token) is not False:
				checkCanClaim(webapi_token) # Checks if can claim the sticker.
				break
			else:
				toast("Invalid Token! Update your token at \"steam_webapi_token.txt\" file. Trying again in 10 seconds...", 10)
				time.sleep(10)
		except ValueError as e:
			# toast("Trying to get the Token again in 10 seconds.", 10)
			time.sleep(10)

# Display a toast notification.
def toast(text, duration):
	# Create a ToastNotifier object.
	toaster = ToastNotifier()

	# Send a notification.
	toaster.show_toast("Steam Auto Claim Stickers", text, duration=duration)

# Gets the WebAPIToken.
def getWebAPIToken():
    token_file = "./steam_webapi_token.txt"
    steam_webapi_token = None

    # Checks if the file exists
    if os.path.exists(token_file):
    	while True:
	        # Open the file for reading
	        with open(token_file, 'r') as file:
	            webapi_token = file.read().strip()

	            # Check if the file is empty
	            if len(webapi_token) == 0:
	            	toast("Place your Steam Web Api Token in the \"steam_webapi_token.txt\" file.", 10)
	            	time.sleep(10)
	            else:
	            	steam_webapi_token = webapi_token
	            	break
    else:
        with open(token_file, 'w') as file:
        	toast("Place your Steam Web Api Token in the \"steam_webapi_token.txt\" file.", 10)
        	time.sleep(10)

    return steam_webapi_token

# Checks the WebAPIToken
def checkWebAPIToken(webapi_token):
    url = f"https://api.steampowered.com/ISaleItemRewardsService/CanClaimItem/v1/?access_token={webapi_token}"
    authorized = None

    while authorized is None:
        try:
            response = requests.get(url)
            response.raise_for_status()  # Throw an exception if the response status is not 2xx
            authorized = True
        except requests.exceptions.RequestException as e:
            authorized = False

    return authorized

# Checks if can claim the sticker.
def checkCanClaim(webapi_token):
	url = f"https://api.steampowered.com/ISaleItemRewardsService/CanClaimItem/v1/?access_token={webapi_token}"

	while True:
		try:
			response = requests.get(url)
			response.raise_for_status() # Throw an exception if the response status is not 2xx
			json_response = response.json()

			if 'response' in json_response and json_response['response'] is not None and 'can_claim' in json_response['response']:
				if json_response['response']['can_claim']:
					claimSticker(webapi_token) # Claim the sticker if the request is successful
					break
				else:
					# toast("There's no stickers to claim.", 3)
					time.sleep(300) # Wait 300 seconds (5 minutes) before trying again
					break
		except requests.exceptions.RequestException as e:
			time.sleep(10) # Wait 10 seconds before trying again

# Claim the sticker
def claimSticker(webapi_token):
	url = f"https://api.steampowered.com/ISaleItemRewardsService/ClaimItem/v1/?access_token={webapi_token}"

	while True:
		try:
			response = requests.post(url)
			response.raise_for_status() # Throw an exception if the response status is not 2xx

			toast("Sticker(s) claimed to your Steam Account!", 10)
			break
		except requests.exceptions.RequestException as e:
			time.sleep(10) # Wait 10 seconds before trying again

# Closes the console window
def close_console_window():
    # Get the handle (identifier) of the console window associated with the current process
    hwnd = ctypes.windll.kernel32.GetConsoleWindow()

    # Check if a valid handle to the console window was obtained
    if hwnd != 0:
        ctypes.windll.user32.ShowWindow(hwnd, 0) # 0 means SW_HIDE (hide the console window)

if __name__ == "__main__":
	# Redirect standard output and error streams to 'nul' (discard) to suppress console output
	sys.stdout = open('nul', 'w')
	sys.stderr = open('nul', 'w')

	# Close the console window to prevent it from staying open
	close_console_window()

	# Main loop to run the program continuously
	while True:
	    main() # Call the main function