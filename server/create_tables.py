import sqlite3

#this file is only for testing

connection = sqlite3.connect('data.db')
cursor = connection.cursor()


create_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(create_table)

create_table = "CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, name text, price real)"
cursor.execute(create_table)


#create_table = "CREATE TABLE IF NOT EXISTS surveys (surveyid TEXT, serviceprovider TEXT, name text, status text, kommentar text)"
#cursor.execute(create_table)

# surveys neu
create_table = "CREATE TABLE IF NOT EXISTS surveys (id INTEGER PRIMARY KEY, surveyid TEXT, serviceprovider TEXT, surveyname TEXT, status TEXT, comment TEXT, questions TEXT)"
cursor.execute(create_table)

# tabelle fuer einen report
create_table = "CREATE TABLE IF NOT EXISTS reports (id INTEGER PRIMARY KEY, surveyid text, prr BOOLEAN, irr BOOLEAN,f real, p real, q real, answers text)"
cursor.execute(create_table)

#cursor.execute("INSERT INTO items VALUES (1,'test', 1333)")
# test surveys
cursor.execute("INSERT INTO surveys VALUES (1,'surveycreated', 'radio ulla', 'toergelen', 'created', 'wir testen hier nur, gehen sie weiter','test')")
cursor.execute("INSERT INTO surveys VALUES (2,'surveyactive', 'radio helga', 'umfrage', 'active', 'wir testen hier nur, gehen sie weiter','test')")
cursor.execute("INSERT INTO surveys VALUES (3,'surveyended', 'radio horst', 'charts', 'ended', 'wir testen hier nur, gehen sie weiter','test')")

cursor.execute("INSERT INTO surveys VALUES (11,'surveycreated2', 'radio ulla', 'toergelen', 'created', 'wir testen hier nur, gehen sie weiter','test')")
cursor.execute("INSERT INTO surveys VALUES (22,'surveyactive2', 'radio helga', 'umfrage', 'active', 'wir testen hier nur, gehen sie weiter','test')")
cursor.execute("INSERT INTO surveys VALUES (33,'surveyended2', 'radio horst', 'charts', 'ended', 'wir testen hier nur, gehen sie weiter','test')")
# test reports
#cursor.execute("INSERT INTO reports VALUES (1, 'surveyactive', 1, 0, 0.898, 0.733, 0.566,'wir testen hier nur, gehen sie weiter')")

connection.commit()
connection.close()
