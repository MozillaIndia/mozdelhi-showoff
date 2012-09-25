=======
Showoff
=======

Summary
-------
Showoff is a web application meant for open communities to help them award their members for their contributions and to help the members display their achievements in their online profiles. Showoff is primarily a project for the Mozilla India Community to aggregate achievements of every contributor in the Mozilla ecosystem, is currently under development and makes use of Flask and Mozilla's Open Badges.


Description
-----------
Refer to this EtherPad doc for more details: https://etherpad.mozilla.org/Hozmas2AuK

This project is under development. Documentation will improve with time. If you are willing to get involved, fork this repository and send patches as pull requests.


Installation
------------
Do all this in a VirtualEnv if you like.

1. `pip insall -r requirements.txt`
2. Edit `website/settings.py` according to your wish.
3. Create a new MySQL database with the name as entered in `settings.py`.
4. Fire the Python interpreter and do the following:
   ```python
   >>> import website
   >>> from models import db
   >>> db.create_all()
   ```

   This will create all the required tables in the database.


Deployment
----------
We use Apache HTTPD with Gunicorn for deployment. You can use anything that you like. A sample Apache WSGI file is present in the repository for your use.

