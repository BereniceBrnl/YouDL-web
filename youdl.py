from flask import Flask, render_template, request, flash, redirect
from flask_session import Session
from pytubefix import YouTube
from YoutubeUrl import YoutubeUrl
from pathlib import Path
from config import SECRET_KEY

app = Flask(__name__)

app.config.from_mapping(
    SECRET_KEY = SECRET_KEY
)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

youtube_url = YoutubeUrl()

@app.route("/", methods=["GET", "POST"])
def home():

    youtube_url.url = request.form.get("url")

    if request.method == "POST":
        try:
            yt = YouTube(youtube_url.url)
            return render_template("confirmation.html", video_title=yt.title, video_thumbnail=yt.thumbnail_url)
        except:
            return render_template("home.html", error_msg="URL invalide")


    return render_template("home.html")

@app.route("/confirmation", methods=["GET", "POST"])
def confirmation():  

    if request.method == "POST":
        try:
            downloads_path = str(Path.home() / "Downloads")
            yt = YouTube(youtube_url.url)
            audio = yt.streams.filter(only_audio=True).first()
            audio.download(output_path=downloads_path)
            flash("Le fichier a été téléchargé.")
            return redirect("/")
        except:
            flash("Le téléchargement a échoué.")
            return redirect("/")



    return render_template(
        "home.html",
        )

if __name__ == '__main__':
    app.run()