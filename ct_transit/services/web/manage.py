from flask.cli import FlaskGroup
from video_pull import app

cli = FlaskGroup(app)

if __name__ == "__main__":
    cli()

