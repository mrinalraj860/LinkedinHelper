# import argparse
# from interface.cli import run_cli

# def main():
#     parser = argparse.ArgumentParser(description="LinkedIn Automation Tool")
#     parser.add_argument('--mode', choices=['cli'], default='cli', help="Choose interface mode")
#     args = parser.parse_args()

#     if args.mode == 'cli':
#         run_cli()
#     else:
#         print("Only CLI supported for now. GUI coming soon!")

# if __name__ == "__main__":
#     main()


import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import argparse
from scrapper import login, profile_scraper
from interface.cli import run_cli

def main():
    parser = argparse.ArgumentParser(description="LinkedIn Automation Tool")
    parser.add_argument('--mode', choices=['cli'], default='cli', help="Choose interface mode")
    parser.add_argument('--email', help='LinkedIn email')
    parser.add_argument('--password', help='LinkedIn password')
    parser.add_argument('--query_url', help='Search query URL')
    parser.add_argument('--send', action='store_true', help='Send messages too')
    parser.add_argument('--pages', type=int, default=3, help='Number of pages to scrape')
    args = parser.parse_args()

    if args.mode == 'cli':
        run_cli(args)
    else:
        print("Only CLI supported for now. GUI coming soon!")

if __name__ == "__main__":
    main()