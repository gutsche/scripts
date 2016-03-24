#!/usr/bin/python

# Grant Assistive Access to Terminal and “osascript”.
import sqlite3
conn = sqlite3.connect('/Library/Application Support/com.apple.TCC/TCC.db')

conn.cursor().execute("INSERT or REPLACE INTO access VALUES('kTCCServiceAccessibility','com.apple.Terminal',0,1,1,NULL,NULL)")
conn.cursor().execute("INSERT or REPLACE INTO access VALUES('kTCCServiceAccessibility','$(which osascript)',1,1,1,NULL,NULL)")

conn.commit()
conn.close()