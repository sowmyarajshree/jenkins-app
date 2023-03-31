from werkzeug.wrappers import Response
import frappe
import requests
from requests.structures import CaseInsensitiveDict
import hashlib
import hmac
from datetime import datetime
from frappe.utils import now ,getdate
from datetime import timedelta
from frappe import _
from frappe.utils.password import get_decrypted_password

@frappe.whitelist()
def fetch_youtube_video():
	api_key = "AIzaSyBEnFnKovQic12pLNpBhx4fLxbyfjVm98k"
	playlist_id = "PLz6u70FanBhkxDaZIGKlg4BtGWMujsoUm"
	url = f"https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=30&playlistId=PLz6u70FanBhkxDaZIGKlg4BtGWMujsoUm&key=AIzaSyBEnFnKovQic12pLNpBhx4fLxbyfjVm98k"
	response = requests.get(url)
	data = response.json()
	video_description_list = []
	for item in data['items']:
		video_description_list.append({"video_id":item['snippet']['resourceId']['videoId'],"video_description":item['snippet']['description']})
	return video_description_list