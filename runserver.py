#!/usr/bin/python3

from flask_failsafe import failsafe
from shikimori import app

@failsafe
def main():
	return app

if __name__ == "__main__":
	main().run(debug=True, host="0.0.0.0", port=5081)
