####################################################################
######################## MILITIAS DB README ########################
####################################################################

o   = Order
-   = File
--  = mehrere Files, keine nähere Aufteilung
... = noch mehr im Ordner, keine nähere Erklärung
|   = Strukturell unterhalb

########################## ORDNER-STRUKTUR #########################
- db.sqlite3
- requirements.txt
- manage.py
o mildb
| - admin.py (which content is manageable through the admin-page)
| - apps.py
| - models.py (which fields in database)
| - tests.py
| - urls.py (which url leads to which view)
| - views.py (which view uses which template with what data)
| o migrations (stages of migrations)
| o static
| | -- pictures
| | o css 
| | | - styling.css (main css file, change colors, widths etc here)
| | o img (no idea if this is even needed anymore)
| | | ...
| | o js (javascript files)
| | | ...
| o templates
	- 404.html
	- 500.html
| | o mildb
| | | -- html files (for each page of militias-db)
		    (changes in content here)
| | | - newbase.html (base page, reference for all other html-files)
		    (changes in navigation, header, footer... in newbase)
o dataentry
| - settings.py (base_dir, allowed hosts, debug mode, change database,
	  language, time zone, static root and url, ...)
| - urls.py (admin, data urls, general url specification)
| - wsgi.py (for apache to run properly?)
