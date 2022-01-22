import pafy

url = "https://www.youtube.com/watch?v=CRK2PmpyWbg"

video = pafy.new(url)

bestaudio = video.getbestaudio()
bestaudio.download()
