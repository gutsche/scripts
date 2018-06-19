#!/urs/bin/env python3
# -*- coding: utf-8 -*-
import sys, re, time, argparse, os, math
import sqlite3, shutil
from subprocess import Popen, PIPE
from datetime import datetime

current_date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def convertToInteger (s):
    return int.from_bytes(s.encode(), 'little')

def convertFromInteger (n):
    return n.to_bytes(math.ceil(n.bit_length() / 8), 'little').decode()

verbose =  False

def create_table(db_connection,table_name,column_name,column_type):
    """
    check if table with name table_name exists
    if not, create table with name table_name and column column_name and type column_type as primary key
    """
    c = db_connection.cursor()
    try:
        c.execute('create table {tn} ({cn} {ct} primary key)'\
        .format(tn=table_name,cn=column_name,ct=column_type))
        if verbose == True:
            print('Table \"%s\" not found, creating it with column \"%s\" as primary key'\
            % (table_name,column_name))
    except:
        if verbose == True:
            print('Table \"%s\" was found!'\
            % (table_name))
    c.close()
    return 0

def create_colum(db_connection,table_name,column_name,column_type,column_default):
    """
    check if column with name column_name in table table_name exists
    if not, create column with name column_name and type column_type and default column_default in table table_name
    """
    c = db_connection.cursor()
    try:
        c.execute('alter table {tn} add column "{cn}" {ct} default "{cd}"'\
        .format(tn=table_name,cn=column_name,ct=column_type,cd=column_default))
        if verbose == True:
            print('Column \"%s\" not found in table \"%s\", creating it with type \"%s\" and default \"%s\"'\
            % (column_name,table_name,column_type,column_default))
    except:
        if verbose == True:
            print('Column \"%s\" found in table \"%s\"!'\
            % (column_name,table_name))
    c.close()
    return 0



def open_db_file(db_file_name):
    """
    open db file name and ensure that it conforms to schema
    if not, update schema
    """
    if (verbose == True):
        print('Opening DB file: \"%s\"' % db_file_name)

    conn = sqlite3.connect(db_file_name)

    # table media
    # field id: hash of name, type TEXT
    # field name: name of media, type TEXT
    # field capacity: capacity of media[bytes], type INTEGER
    # field last_update: date/time of last update, type TEXT
    create_table(conn,'media','id','integer')
    create_colum(conn,'media','name','text','')
    create_colum(conn,'media','capacity','integer',0)
    create_colum(conn,'media','free','integer',0)
    create_colum(conn,'media','last_update','text','')

    # table files
    # field id: hash of name, type TEXT
    # field media_id: key from media table, type TEXT
    # field name: name of media file, type TEXT
    # field path: path relative to top level on media, type TEXT
    # field size: size[bytes], type INTEGER
    # field last_update: date/time of last update, type TEXT
    create_table(conn,'files','id','integer')
    create_colum(conn,'files','media_id','text','')
    create_colum(conn,'files','name','text','')
    create_colum(conn,'files','path','text','')
    create_colum(conn,'files','size','integer',0)
    create_colum(conn,'files','last_update','text','')

    return conn

def close_db(db_file_connection):
    c = db_file_connection.cursor()
    c.execute('pragma database_list')
    db_location_name = c.fetchall()[0][2]
    if (verbose == True):
        print('Committing and closing DB file: \"%s\"' % db_location_name)

    db_file_connection.commit()
    db_file_connection.close()
    return 0

def get_id_for_media(connection_list,media_name):
    """
    for a given media_name, check the id in the media table
    if the media does not have an entry, create it
    """

    generated_media_id = convertToInteger(media_name)
    queried_media_ids = []
    for connection in connection_list:
        c = connection.cursor()
        c.execute('select id from media where name="{name}"'\
        .format(name=media_name))
        rows = c.fetchall()
        if len(rows) > 1:
            print('ERROR: name \"%s\" cannot have more than one entry in media table!' % media_name)
            sys.exit(1)
        if len(rows) == 1:
            queried_media_ids.append(rows[0])
        c.close()
    # check if the name has entries in the media table
    if len(queried_media_ids)> 0:
        # check if the different connections have the same id
        id = 0
        for item in queried_media_ids:
            if id == 0:
                id = int(item)
            else:
                if id != int(item):
                    print('ERROR: List of queried media ids for name \"%s\" are not the same for all connections: %s' % (media_name,','.join(queried_media_ids)))
                    sys.exit(1)

        # check that queried id is equal to generated id
        if int(queried_media_ids[0]) != generated_media_id:
            print('ERROR: For name \"%s\", the queried id %i is not equal the generated id %i!' % (media_name,int(queried_media_ids[0]),generated_media_id) )
            sys.exit(1)
    else:
        # gather free space on media_name
        total, used, free = shutil.disk_usage(media_name)
        # for zfs volumes, total is not correct, use zpool status command to get total
        if total == used+free:
            # this is a zfs volume
            process = Popen(['zpool', 'list', '-pH', '-o', 'size', media_name.replace('/Volumes/','')], stdout=PIPE, stderr=PIPE)
            stdout, stderr = process.communicate()
            total = int(stdout.strip())
        # add row to table
        add_row_to_table(connection_list,'media',{'id': generated_media_id, 'name': media_name, 'capacity': total, 'free': free, 'last_update': current_date_time})

    return generated_media_id

def add_row_to_table(connection_list,table_name,values):
    """

    add row to table

    """

    for connection in connection_list:
        c = connection.cursor()
        try:
            column_list_string = ','.join(list(values.keys()))
            value_list_string = ''
            for key in values.keys():
                if isinstance(values[key], str):
                    value_list_string = value_list_string + '\'' + values[key] + '\','
                else:
                    value_list_string = value_list_string + str(values[key]) + ','
            value_list_string = value_list_string[:-1]
            c.execute("INSERT INTO {tn} ({cls}) VALUES ({vls})".\
            format(tn=table_name, cls=column_list_string, vls=value_list_string))
            if verbose == True:
                print('SUCCESS: inserted into \"%s\" the values \"%s\"' % (column_list_string,value_list_string))
        except sqlite3.IntegrityError:
            if verbose == True:
                print('ERROR: ID %i already exists in PRIMARY KEY column %s' % (values['id'],'id'))
                print('ERROR: something went wrong inserting into \"%s\" the values \"%s\"' % (column_list_string,value_list_string))
        except:
            if verbose == True:
                print('ERROR: something went wrong inserting into \"%s\" the values \"%s\"' % (column_list_string,value_list_string))

        c.close()

    return 0



def update_from_directory(connection_list,top_directory,project_list):
    """
    update the databases in the connection list with all media files in the project_list in the top_directory
    """

    # loop over files in directory and gather all needed information
    filelist = {}
    for project_dir in project_list:
        counter = 0
        for (root, dirs, files) in os.walk(top_directory + '/' + project_dir):
            dir = root.replace(top_directory + '/' + project_dir + '/','')
            if dir[0] != '.':
                for file in files:
                    name = project_dir + '/' + file
                    id = convertToInteger(name)
                    size = os.path.getsize(root + '/' + file)
                    filelist[str(id)] = {'name' : name, 'size' : size}
                    counter += 1
        if verbose == True:
            print('Gathered information for %i files in project dir \"%s\"' % (counter,project_dir))

    media_id = get_id_for_media(connection_list,top_directory)
    if verbose == True:
        print('ID of external media with top directory \"%s\": %i' % (top_directory,media_id))

def main(args):
    """

    backup media to a collection of external disks
    all interaction with media is POSIX

    """

    parser = argparse.ArgumentParser()
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    parser.add_argument("--central_db_file_location", action="store", default = "/Volumes/Home/gutsche/Documents/Private/Projects/Backup", help="Location of centrally stored db file")
    parser.add_argument("--server_media_top_directory", action="store", default = "/Volumes/Media", help="Location of central server media top directory")
    parser.add_argument("--external_media_top_directory", action="store", default = None, help="Top media directory on external media", required=True)
    parser.add_argument("--db_file_name", action="store", default = "media_backup.sqlite", help="Name of media backup db file")
    parser.add_argument("--project", action="append", default = [], help="Name of a directory in the media top directory", required=True)
    args = parser.parse_args()
    global verbose
    verbose = args.verbose
    projects = args.project
    print (projects)

    # open db files on external media and from central location
    central_db_file_connection = open_db_file(args.central_db_file_location + '/' + args.db_file_name)
    external_media_db_file_connection = open_db_file(args.external_media_top_directory + '/' + args.db_file_name)

    # update from information from media folder on central server
    update_from_directory([central_db_file_connection,external_media_db_file_connection],args.server_media_top_directory,projects)

    # close external media and central db central db files
    close_db(central_db_file_connection)
    close_db(external_media_db_file_connection)

if __name__ == '__main__':
    main(sys.argv)
