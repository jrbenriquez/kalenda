# Kalenda

TODO

* ~~Login with Google~~
* ~~Get Calender Events~~
* ~~Refresh Token Functionality for attach_google_token decorator~~
* Improve Events view
* Trigger day view if date is clicked on month view
* Properly plot calendar events in day view
* Make Calendar Events
* Create Event Model

      

Serve the project
====

Make sure you have Python 3

Change **PUBLIC_PATH** and **FRONTEND_URL** in tookie/settings.py if you wish to change URLS

#### Install Requirements

`pip install requirements.txt`

#### Run Django Backend on localhost:8000
`python manage.py runserver 0.0.0.0:8000`

#### Simulate a separate Frontend app running on localhost:8888
*(You can also create views from Django templates but make sure to follow authentication flow)*
```
cd frontend
python -m SimpleHTTPServer 8888
```



Authentication Flow
====
1. **Frontend** (or static html) Serves the login page
    *Visit it at localhost:8888*


      ![alt text](https://github.com/jrbenriquez/tookie-demo/raw/master/docs/signin.png "Sign In")

2. **Frontend** (or static html) sends the credentials securely through POST (usually *username* and *password*) along with a **redirect_url** so the backend knows where to redirect the user after authorization

    **POST Request**

```
   {
  "username": "test",
  "password": "testtest1234",
  "redirect_url": "http://localhost:8888/protected_data.html"
}
```
3. **Backend** responds with a link (containg a *token* and the *user ID*) to the frontend where the user is **required to be redirected**

    **Backend Response**
```
{
    "redirect": "http://localhost:8000/authorize?r=1&auth_token=DjOH-FOL8OlnF9KzmMU4hAd_WSJe07bLkaC0jEZO0NM%3D&redirect_url=http%3A%2F%2Flocalhost%3A8000%2Fprotected_data.html"
}
```

4. Redirection takes the user to a *backend served page* where it verifies the token and *sets the cookie* if successfully verified
5. Upon successful validation it *quickly redirects the user* back to the redirect url.
6. User can now access *protected API endpoints in the backend* as long as cookie is not deleted or expires (assuming frontend + backend are in the **same domain**)
    *Protected Page Link*
    `http://localhost:8888/protected_data.html
