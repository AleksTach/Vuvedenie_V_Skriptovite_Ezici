import os
import json
from typing import Dict

def create_user_profile(file_path, **kwargs):
    user_profile = dict(kwargs)

    with open(file_path, "w") as f:
      json.dump(user_profile, f, indent=4)

def main():
    profile = create_user_profile(
    file_path = "user_profile.json",
    username = "NaklonenenataCherta",
    first_name = "Naklonen",
    last_name = "Slash",
    age = 62,
    email = "/naklonena_cherta/@gunz.ros",
  )


if __name__ ==  "__main__":
  main()