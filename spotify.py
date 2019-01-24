import json, requests
from bottle import redirect

client_id="XXXX"
client_secret="XXXX"

def spapp_do(q):
    outp=""
    try:
        code=q['code']
    except:
        code=""
    try:
        token=q['token']
    except:
        token=""

    # We got neither a token nor a code to retrieve one. Ask the user to sign in and authorize
    if code == "" and token == "":
        redirect("https://accounts.spotify.com/authorize?client_id=2525ce57a88a450aa2df4153b542e099&redirect_uri=https:%2F%2Fwww2.sotong.io%2Fspapp&scope=user-read-private%20user-read-email%20user-top-read%20user-read-recently-played%20user-read-playback-state%20user-read-playback-state%20user-read-recently-played%20user-read-playback-state%20user-read-currently-playing%20user-modify-playback-state%20playlist-read-private&response_type=code&state=123")
    
    # We received a code. Quick, let's trade it in for a user token!
    elif code != "":
        url = 'https://accounts.spotify.com/api/token'
        headers = {'Content-Type': "application/x-www-form-urlencoded"}
        payload = {'grant_type': 'authorization_code', 'code': code, 'redirect_uri': 'https://www2.sotong.io/spapp'}
        res = requests.post(url, data=payload, headers=headers, auth=(client_id, client_secret))
        j=json.loads(res.text)
        access=j["access_token"]
        redirect("/spapp?token=" + access)

    # Yay! We have a token. Let's find out what the user is listening to!
    elif token != "":
        try:
            headers = {'Authorization': 'Bearer ' + token}
            url = "https://api.spotify.com/v1/me/player/currently-playing"
            res = requests.get(url, headers=headers)
            user_response=res.text
            j=json.loads(res.text)
            song = j["item"]["name"]
            image = str(j["item"]["album"]["images"][0]["url"])

            outp="<h1>" + song + "</h1>" + "<img src='" + image + "'><p>"
        except:
            if res.status_code == 401:
                redirect("/spapp")
            else:
                return "Please play a song on Spotify and reload this page!"
    return outp
